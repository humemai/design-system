#!/usr/bin/env bash
# Vendor the design system into every HumemAI repository that carries a copy.
#
#   scripts/vendor-all.sh            re-vendor every copy that is behind
#   scripts/vendor-all.sh --check    report only; exit 1 if any copy is behind
#
# The consumers are sibling checkouts of this repo (../<repo>). One run
# replaces a vendor-into.sh call per repository, which is how copies went
# stale: on 2026-10-02 four of the five were a social card behind (#3).
# Commit the result in each consumer; this script never commits or pushes.
set -euo pipefail

# <repo>:<brand directory inside it>
CONSUMERS=(
  "humem.ai:public/brand"
  "humemdb:docs/brand"
  "audit-ready-memory:docs/brand"
  "humemai-docs:brand"
  "arcadedb-embedded-python:bindings/python/docs/brand"
)

mode=apply
case "${1:-}" in
  "") ;;
  --check) mode=check ;;
  *) echo "usage: scripts/vendor-all.sh [--check]" >&2; exit 2 ;;
esac

here=$(cd "$(dirname "$0")/.." && pwd)
root=$(dirname "$here")

# A copy records the commit it came from, so that commit must be one the
# consumers' readers can find, and it must be the whole source of the copy:
# scripts/ decides which files a copy holds, so an uncommitted edit there
# (vendor-into.sh's file list, say) makes a copy no commit can reproduce.
# That happened while this script was written. --check compares against the
# working tree as it is.
if [ "$mode" = apply ]; then
  if [ -n "$(git -C "$here" status --porcelain -- css logo assets export scripts)" ]; then
    echo "✗ design-system has uncommitted changes in css/, logo/, assets/, export/ or scripts/; commit and merge first" >&2
    exit 1
  fi
  git -C "$here" fetch -q origin main
  if ! git -C "$here" merge-base --is-ancestor HEAD origin/main; then
    echo "✗ design-system HEAD $(git -C "$here" rev-parse --short HEAD) is not on origin/main; merge it first" >&2
    exit 1
  fi
fi

# Stage the copy vendor-into.sh would write, and compare every consumer
# against it. Staging through vendor-into.sh keeps one definition of what a
# copy contains; it also refuses uncommitted changes in this repo.
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
"$here/scripts/vendor-into.sh" "$stage/brand" >/dev/null
want=$(sed -n 's/^Hash:[[:space:]]*//p' "$stage/brand/VERSION.md")

# Files that differ between a copy and the staged one, relative to the copy.
# diff exits 1 when it finds a difference, which is the point; under pipefail
# that would end the script at the first stale copy.
changed() {
  { diff <(cd "$1" 2>/dev/null && find css logo assets export -type f -exec sha256sum {} + 2>/dev/null | LC_ALL=C sort -k2) \
         <(cd "$2" && find css logo assets export -type f -exec sha256sum {} + | LC_ALL=C sort -k2) || true; } \
    | sed -n 's/^[<>] [0-9a-f]*  //p' | LC_ALL=C sort -u
}

behind=0
skipped=0
for entry in "${CONSUMERS[@]}"; do
  repo=${entry%%:*}
  rel=${entry#*:}
  dir="$root/$repo"
  dest="$dir/$rel"
  if ! git -C "$dir" rev-parse --git-dir >/dev/null 2>&1; then
    echo "✗ $repo: no checkout at $dir"
    skipped=1
    continue
  fi
  have=$(sed -n 's/^Hash:[[:space:]]*//p' "$dest/VERSION.md" 2>/dev/null || true)
  pinned=$(sed -n 's/^Commit:[[:space:]]*//p' "$dest/VERSION.md" 2>/dev/null | cut -c1-7 || true)
  if [ "$have" = "$want" ]; then
    echo "✓ $repo: up to date (${pinned})"
    continue
  fi
  behind=1
  echo "• $repo: behind (pinned ${pinned:-nothing}), differs in:"
  changed "$dest" "$stage/brand" | sed 's/^/    /'
  [ "$mode" = check ] && continue
  if [ -n "$(git -C "$dir" status --porcelain -- "$rel")" ]; then
    echo "  ✗ skipped: $rel has uncommitted changes"
    skipped=1
    continue
  fi
  "$here/scripts/vendor-into.sh" "$dest" >/dev/null
  "$dest/verify.sh" >/dev/null
  echo "  ✓ vendored into $rel on branch $(git -C "$dir" branch --show-current); commit it there"
done

# A missing checkout fails both modes: a copy nobody could look at is not
# known to be current.
if [ "$mode" = check ]; then
  exit $((behind || skipped))
fi
exit "$skipped"
