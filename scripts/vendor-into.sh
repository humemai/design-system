#!/usr/bin/env bash
# Copy the design system into a consumer, with a VERSION.md that pins it.
#
#   scripts/vendor-into.sh <dest>
#
#   humem.ai            scripts/vendor-into.sh ../humem.ai/public/brand
#   an MkDocs project   scripts/vendor-into.sh ../<repo>/docs/brand
#
# Copies css/, logo/, assets/ and the icon files from export/ (not the social
# cards, which are uploaded to the platforms, not served). Run it from a clean
# checkout: the commit it records must be the one the files came from.
set -euo pipefail
cd "$(dirname "$0")/.."

dest=${1:?usage: vendor-into.sh <dest>}
if [ -n "$(git status --porcelain -- css logo assets export)" ]; then
  echo "✗ css/, logo/, assets/ or export/ has uncommitted changes; commit first" >&2
  exit 1
fi

rm -rf "$dest"
mkdir -p "$dest/export"
cp -R css logo assets "$dest/"
cp export/favicon.svg export/favicon.ico export/apple-touch-icon.png \
   export/icon-192.png export/icon-512.png export/lockup*.png "$dest/export/"
cp scripts/verify.sh "$dest/verify.sh"

hash=$(cd "$dest" && find css logo assets export -type f | LC_ALL=C sort | xargs sha256sum | sha256sum | awk '{print $1}')
cat > "$dest/VERSION.md" <<VERSION
# HumemAI design system (vendored copy)

Do not edit these files here. Change them in github.com/humemai/design-system,
then vendor again. \`./verify.sh\` checks this copy against the hash below.

Commit: $(git rev-parse HEAD)
Date: $(git log -1 --format=%cs)
Hash: $hash
VERSION
echo "✓ vendored $(git rev-parse --short HEAD) into $dest"
