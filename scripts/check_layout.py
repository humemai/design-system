"""Headless layout smoke: measure the layout classes in a real browser.

    uv sync --locked
    uv run python scripts/check_layout.py                 # the good page: must pass
    uv run python scripts/check_layout.py --variant ID    # one bad variant: must fail on ID
    uv run python scripts/check_layout.py --self-test     # every bad variant fails on its own check

The page is scripts/fixtures/layout/page.html, which uses every class of css/layout.css
and css/components.css the documented way. Chrome is the installed one (the runner has
it) or Playwright's own. These are the headless-checkable requirements of the README
("Layout across screen sizes"), each with an id:

  no-sideways-scroll  the page never scrolls sideways, at 320, 360, 768, 1280 and 2560 CSS px
                      and at a 100% and a 200% root font size (WCAG 1.4.10, 1.4.4)
  scroller-named      an element that scrolls sideways is a .hm-table-scroll with role,
                      tabindex 0 and an aria-label
  table-wrapper       a wide table scrolls inside its wrapper at 320px (and the wrapper is there)
  scroll-cue          a table that scrolls shows a shadow on the right edge of its scroller while more is to
                      the right, and none at the far end or when it does not scroll, in light and in dark
                      (pixels of a screenshot, beside a body row)
  card-heights        cards in .hm-card-grid share one height and their last lines one baseline
  measure             prose is the measure (68ch) wide on a wide screen, and a split's content
                      column is never wider than it
  container-width     a container-type box is not 0 wide at 320px
  container-base      with every @container block removed, the page still does not scroll sideways
  size-classes        the size classes switch at 600 and 1000 CSS px exactly and nothing changes at 1600
                      (the rem range queries equal the px queries they replaced, at the default font size)
  page-container      the container is 1180px of content at 1440 and 2560, centred, and its wide
                      variant is the Tower's frame
  tabs                every .hm-tabs link is a control height tall (44px below 1000, 36 from 1000) and only
                      the open one (aria-current="page") has the brand rule under it and semibold text; a
                      count is muted
  key-values          every .hm-kv value stands in its own column to the right of its label, all values on one
                      left edge, the label column at most 40% of the list or 8.5rem, no label wider than it
  static-card         a .hm-card--static does not move or change its border under the pointer, its rows take
                      their own height in a stretched card, and a span in it is plain text

The bad variants are the same page with one defect each; --self-test runs them all.
"""
import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "scripts" / "fixtures" / "layout" / "page.html"

WIDTHS = (320, 360, 768, 1280, 2560)
# 200% is what WCAG 1.4.4 asks for. At 300% a single word of a card no longer fits
# 320px whatever the grid does, so it is not a check of this system.
ROOTS = (100, 200)
CHECKS = ("no-sideways-scroll", "scroller-named", "table-wrapper", "scroll-cue", "card-heights", "measure",
          "container-width", "container-base", "size-classes", "page-container", "tabs", "key-values", "static-card")

# One defect each: (old, new) text replacements on the good page, every anchor present once.
BAD = {
    "no-sideways-scroll": [('<p><button class="hm-hint"', '<div style="width: 600px; height: 4px; background: red"></div><p><button class="hm-hint"')],
    "scroller-named": [('<div class="hm-table-scroll" id="scroller" role="region" tabindex="0" aria-label="Wide results">', '<div class="hm-table-scroll" id="scroller">')],
    "table-wrapper": [('<div class="hm-table-scroll" id="scroller"', '<div class="hm-table-scroll" id="scroller" style="overflow: visible"')],
    "scroll-cue": [('<div class="hm-table-scroll" id="scroller" role="region"', '<div class="hm-table-scroll" id="scroller" style="background-image: none" role="region"')],
    "card-heights": [('<div class="hm-card-grid" id="cards">', '<div class="hm-card-grid" id="cards" style="grid-auto-rows: auto">')],
    "measure": [('<p class="hm-measure" id="prose">', '<p id="prose">')],
    "container-width": [('<div class="hm-fit" id="fit">', '<div style="display: flex"><div class="hm-fit" id="fit">'),
                        ('<div>The second part sits beside it when the box is 40rem wide.</div>\n      </div>\n    </div>', '<div>The second part sits beside it when the box is 40rem wide.</div>\n      </div>\n    </div></div>')],
    "container-base": [('</style>', '.base-wide { width: 700px; height: 4px; background: red } @container hm-fit (width < 40rem) { .base-wide { width: 100% } }\n  </style>'),
                       ('<div class="hm-fit__pair">', '<div class="base-wide"></div><div class="hm-fit__pair">')],
    "size-classes": [('</style>', '@media (width >= 62.5rem) { :root { --hm-control-h: 3rem } }\n  </style>')],
    "page-container": [('</style>', '.hm-container { max-inline-size: 90rem }\n  </style>')],
    "tabs": [('</style>', '.hm-tabs a[aria-current="page"] { border-block-end-color: transparent }\n  </style>')],
    "key-values": [('<dl class="hm-kv" id="kv">', '<dl class="hm-kv" id="kv" style="display: block">')],
    "static-card": [('<div class="hm-card hm-card--static" id="static">', '<div class="hm-card" id="static">')],
}


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def strip_container_blocks(css):
    """Remove every @container { ... } block (the base styles must stand without them)."""
    css = strip_comments(css)
    while True:
        start = css.find("@container")
        if start < 0:
            return css
        depth, i = 0, css.index("{", start)
        for j in range(i, len(css)):
            depth += (css[j] == "{") - (css[j] == "}")
            if depth == 0:
                css = css[:start] + css[j + 1:]
                break


def build(html, strip=False):
    """The page with its stylesheets inlined, so the browser reads nothing from disk."""
    def inline(m):
        css = (PAGE.parent / m.group(1)).resolve().read_text()
        return f"<style>{strip_container_blocks(css) if strip else css}</style>"
    html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', inline, html)
    if strip:  # the page's own <style> blocks too
        html = re.sub(r"<style>(.*?)</style>", lambda m: f"<style>{strip_container_blocks(m.group(1))}</style>", html, flags=re.S)
    return html


def variant_html(name):
    html = PAGE.read_text()
    for old, new in BAD.get(name, []):
        assert html.count(old) == 1, f"{name}: anchor {old[:40]!r} found {html.count(old)} times"
        html = html.replace(old, new)
    return html


class Run:
    def __init__(self, page, html):
        self.page, self.html, self.failures, self.ran = page, html, [], dict.fromkeys(CHECKS, 0)

    def load(self, strip=False):
        self.page.set_content(build(self.html, strip))

    def at(self, width, root=100):
        self.page.set_viewport_size({"width": width, "height": 900})
        self.page.evaluate("p => { document.documentElement.style.fontSize = p + '%' }", root)

    def js(self, script, arg=None):
        return self.page.evaluate(script, arg)

    def check(self, cid, ok, message):
        self.ran[cid] += 1
        if not ok:
            self.failures.append((cid, message))


SCROLLERS = """() => [...document.querySelectorAll('body *')].filter(e => {
  const s = getComputedStyle(e);
  return (s.overflowX === 'auto' || s.overflowX === 'scroll') && e.scrollWidth > e.clientWidth + 1;
}).map(e => ({id: e.id, cls: e.className, role: e.getAttribute('role'), tab: e.getAttribute('tabindex'), label: e.getAttribute('aria-label')}))"""

PAGE_SCROLL = "() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]"


# The pixel at the right edge of the scroller, beside a body row (the row's top padding, where no text is), against the scroller's own fill.
CUE_PROBE = """() => { const w = document.querySelector('#scroller'); w.scrollIntoView({block: 'center'}); const r = w.getBoundingClientRect(); const td = w.querySelector('tbody td').getBoundingClientRect();
  return {x: r.right - 4, y: td.top + 1, fill: getComputedStyle(w).backgroundColor, over: w.scrollWidth > w.clientWidth + 1, left: w.scrollLeft, max: w.scrollWidth - w.clientWidth}; }"""


def cue_strength(run):
    """How far the right edge differs from the scroller's fill (the largest channel difference, 0 to 255), and the facts it was measured with."""
    probe = run.js(CUE_PROBE)
    png = run.page.screenshot(clip={"x": probe["x"], "y": probe["y"], "width": 1, "height": 1})
    pixel = Image.open(io.BytesIO(png)).convert("RGB").getpixel((0, 0))
    fill = [int(v) for v in re.findall(r"\d+", probe["fill"])[:3]]
    return max(abs(a - b) for a, b in zip(pixel, fill)), probe


def scroll_cue(run):
    for theme in ("light", "dark"):
        run.js("t => document.documentElement.setAttribute('data-theme', t)", theme)
        for width in (320, 360, 2560):
            run.at(width)
            run.js("() => { document.querySelector('#scroller').scrollLeft = 0 }")
            start, facts = cue_strength(run)
            if facts["over"]:
                run.check("scroll-cue", start >= 12, f"{theme}, {width}px: the table scrolls but its right edge is {start} from the fill at scrollLeft 0 (a cue is at least 12)")
                run.js("() => { const w = document.querySelector('#scroller'); w.scrollLeft = w.scrollWidth }")
                end, _ = cue_strength(run)
                run.check("scroll-cue", end <= 3, f"{theme}, {width}px: scrolled to the far end the right edge is {end} from the fill (no cue there)")
            else:
                run.check("scroll-cue", start <= 3, f"{theme}, {width}px: the table does not scroll but its right edge is {start} from the fill (no cue without overflow)")
    run.js("() => { document.documentElement.removeAttribute('data-theme'); window.scrollTo(0, 0) }")


def run_checks(run):
    run.load()
    for root in ROOTS:
        for width in WIDTHS:
            run.at(width, root)
            sw, cw = run.js(PAGE_SCROLL)
            run.check("no-sideways-scroll", sw <= cw, f"{width}px at {root}% root: scrollWidth {sw} > clientWidth {cw}")
            if width <= 360:
                for s in run.js(SCROLLERS):
                    named = "hm-table-scroll" in s["cls"].split() and s["role"] == "region" and s["tab"] == "0" and (s["label"] or "").strip()
                    run.check("scroller-named", named, f"{width}px at {root}% root: #{s['id']} scrolls sideways but is not a named .hm-table-scroll (role={s['role']}, tabindex={s['tab']}, aria-label={s['label']!r})")
                run.check("scroller-named", True, "")

    # A wide table scrolls inside its wrapper, and the wrapper is what scrolls.
    run.at(320)
    t = run.js("""() => { const w = document.querySelector('#scroller'); const s = getComputedStyle(w);
      return {inWrapper: !!document.querySelector('#table').closest('.hm-table-scroll'), overflowX: s.overflowX, sw: w.scrollWidth, cw: w.clientWidth}; }""")
    run.check("table-wrapper", t["inWrapper"] and t["overflowX"] in ("auto", "scroll") and t["sw"] > t["cw"],
              f"320px: table in wrapper={t['inWrapper']}, wrapper overflow-x={t['overflowX']}, scrollWidth {t['sw']} vs clientWidth {t['cw']} (the table must be wider than the screen and scroll inside its wrapper)")

    # The scroll cue: a shadow on the right edge of the scroller while more is to the right.
    scroll_cue(run)

    # Cards share one height; their last lines sit on one baseline.
    for width in (360, 768, 1280, 2560):
        run.at(width)
        c = run.js("""() => [...document.querySelectorAll('#cards .hm-card')].map(c => { const r = c.getBoundingClientRect(); const s = c.querySelector(':scope > span').getBoundingClientRect(); return [r.height, r.bottom - s.bottom]; })""")
        heights = {round(h, 1) for h, _ in c}
        offsets = {round(o, 1) for _, o in c}
        run.check("card-heights", len(c) == 5 and len(heights) == 1 and len(offsets) == 1, f"{width}px: {len(c)} cards, heights {sorted(heights)}, footer offsets {sorted(offsets)}")

    # The measure: prose is 68ch on a wide screen; a split's content column never exceeds it.
    probe = """() => { const p = document.querySelector('#prose'); const b = document.querySelector('.hm-split__body'); const d = document.createElement('div');
      d.style.cssText = 'position:absolute;visibility:hidden;inline-size:68ch'; d.style.font = getComputedStyle(p).font; p.parentNode.appendChild(d);
      const w = d.getBoundingClientRect().width; d.remove(); return [p.getBoundingClientRect().width, b.getBoundingClientRect().width, w]; }"""
    for width in (1280, 2560):
        run.at(width)
        prose, body, measure = run.js(probe)
        run.check("measure", abs(prose - measure) <= 1 and body <= measure + 1, f"{width}px: prose {prose:.0f}px, split body {body:.0f}px, 68ch is {measure:.0f}px")

    # A container-type box is not 0 wide at 320px.
    for root in ROOTS:
        run.at(320, root)
        boxes = run.js("() => [...document.querySelectorAll('body *')].filter(e => getComputedStyle(e).containerType !== 'normal').map(e => [e.id || e.className, e.getBoundingClientRect().width])")
        run.check("container-width", len(boxes) > 0 and all(w > 0 for _, w in boxes), f"320px at {root}% root: container boxes {boxes}")

    # The size classes switch exactly where the px queries did.
    for width in (599, 600, 999, 1000, 1599, 1600):
        run.at(width)
        got = run.js("""() => { const p = getComputedStyle(document.querySelector('#probe')); const h = getComputedStyle(document.querySelector('#hint'), '::after');
          return {base: parseFloat(p.fontSize), control: parseFloat(p.minHeight), gutter: parseFloat(p.paddingLeft), hitArea: h.content !== 'none' && h.content !== 'normal',
                  cols: getComputedStyle(document.querySelector('#split')).gridTemplateColumns.split(' ').length}; }""")
        want = {"base": 17 if width >= 1000 else 16, "control": 36 if width >= 1000 else 44, "gutter": 24 if width >= 600 else 16,
                "hitArea": width < 1000, "cols": 2 if width >= 1000 else 1}
        run.check("size-classes", got == want, f"{width}px: got {got}, want {want}")

    # The page container: 1180px of content, centred; the wide variant is the Tower's frame.
    for width in (390, 768, 1280, 1440, 2560):
        run.at(width)
        g = 24 if width >= 600 else 16
        r = run.js("""() => { const out = {}; for (const id of ['frame', 'wide']) { const e = document.querySelector('#' + id); const b = e.getBoundingClientRect(); const s = getComputedStyle(e);
          out[id] = {content: b.width - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight), left: b.left, right: document.documentElement.clientWidth - b.right}; } return out; }""")
        want_content = min(73.75 * 16, width - 2 * g)
        frame = min(width, max(97 * 16 + 2 * g, 0.9 * width))
        want_wide = frame - 2 * g
        ok = (abs(r["frame"]["content"] - want_content) <= 0.5 and abs(r["frame"]["left"] - r["frame"]["right"]) <= 1
              and abs(r["wide"]["content"] - want_wide) <= 0.5 and abs(r["wide"]["left"] - r["wide"]["right"]) <= 1)
        run.check("page-container", ok, f"{width}px: content {r['frame']['content']:.0f} (want {want_content:.0f}), wide {r['wide']['content']:.0f} (want {want_wide:.0f}), margins {r['frame']['left']:.0f}/{r['frame']['right']:.0f}")

    # Tabs: control height, one marked link, a muted count.
    for width in (320, 999, 1000, 2560):
        run.at(width)
        t = run.js("""() => { const probe = document.createElement('i'); probe.style.cssText = 'color: var(--hm-brand); background: var(--hm-text-muted)'; document.body.appendChild(probe);
          const brand = getComputedStyle(probe).color, muted = getComputedStyle(probe).backgroundColor; probe.remove();
          return {brand, muted, links: [...document.querySelectorAll('#tabs a')].map(a => { const s = getComputedStyle(a); const c = a.querySelector('.hm-tabs__count');
            return {current: a.getAttribute('aria-current') === 'page', height: a.getBoundingClientRect().height, rule: s.borderBottomColor, ruleWidth: s.borderBottomWidth, weight: s.fontWeight,
                    count: getComputedStyle(c).color}; })}; }""")
        want = 36 if width >= 1000 else 44
        links = t["links"]
        short = [round(a["height"], 1) for a in links if a["height"] < want - 0.5]
        marked = [a for a in links if a["rule"] == t["brand"] and a["ruleWidth"] == "2px" and a["weight"] == "600"]
        clear = [a for a in links if not a["current"] and a["rule"] == "rgba(0, 0, 0, 0)" and a["weight"] == "400"]
        ok = (len(links) == 3 and not short and len(marked) == 1 and marked[0]["current"] and len(clear) == 2
              and all(a["count"] == t["muted"] for a in links) and (width < 1000 or abs(links[0]["height"] - want) <= 0.5))
        run.check("tabs", ok, f"{width}px: want links {want}px tall, one marked; got {[(round(a['height'], 1), a['current'], a['rule'], a['weight']) for a in links]}, short {short}")

    # Label and value rows: two columns at every width, the label column bounded.
    for root in ROOTS:
        for width in (320, 360, 768, 1280):
            run.at(width, root)
            k = run.js("""() => { const d = document.querySelector('#kv'); const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
              const dts = [...d.querySelectorAll('dt')], dds = [...d.querySelectorAll('dd')];
              return {rem, width: d.getBoundingClientRect().width, rows: dts.map((t, i) => { const a = t.getBoundingClientRect(), b = dds[i].getBoundingClientRect();
                return {dtRight: a.right, ddLeft: b.left, dtWidth: a.width, over: t.scrollWidth - t.clientWidth, overlap: Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top), ddOver: dds[i].scrollWidth - dds[i].clientWidth}; })}; }""")
            cap = min(8.5 * k["rem"], 0.4 * k["width"])
            rows = k["rows"]
            ok = (len(rows) == 3 and all(r["ddLeft"] >= r["dtRight"] and r["overlap"] > 0 and r["dtWidth"] <= cap + 0.5 and r["over"] <= 0 and r["ddOver"] <= 0 for r in rows)
                  and len({round(r["ddLeft"], 1) for r in rows}) == 1)
            run.check("key-values", ok, f"{width}px at {root}% root: label cap {cap:.0f}px, rows {[{k2: round(v) for k2, v in r.items()} for r in rows]}")

    # A static card: no hover lift, rows sized to content, a span is plain text.
    for width in (360, 1280):
        run.at(width)
        run.js("() => { document.querySelector('#static').scrollIntoView({block: 'center'}) }")
        run.page.mouse.move(0, 0)
        run.page.wait_for_timeout(300)
        style = "() => { const s = getComputedStyle(document.querySelector('#static')); return [s.transform, s.borderTopColor] }"
        before = run.js(style)
        run.page.hover("#static")
        run.page.wait_for_timeout(300)  # longer than the card's 160ms transition
        after = run.js(style)
        c = run.js("""() => { const kv = document.querySelector('#kv').getBoundingClientRect(), n = document.querySelector('#note'), card = document.querySelector('#static');
          return {gap: n.getBoundingClientRect().top - kv.bottom, noteColor: getComputedStyle(n).color, text: getComputedStyle(card).color, want: parseFloat(getComputedStyle(card).rowGap)}; }""")
        ok = before == after and after[0] == "none" and abs(c["gap"] - c["want"]) <= 0.5 and c["noteColor"] == c["text"]
        run.check("static-card", ok, f"{width}px: hover {before} to {after}; the note is {c['gap']:.0f}px under the list (row gap {c['want']:.0f}), span {c['noteColor']} against text {c['text']}")
    run.page.mouse.move(0, 0)

    # With every @container block removed the single-column base still fits.
    run.load(strip=True)
    for root in ROOTS:
        run.at(320, root)
        sw, cw = run.js(PAGE_SCROLL)
        run.check("container-base", sw <= cw, f"320px at {root}% root, no @container rules: scrollWidth {sw} > clientWidth {cw}")


def launch(p):
    last = None
    for kwargs in ({"channel": "chrome"}, {}):
        try:
            return p.chromium.launch(**kwargs)
        except Exception as error:  # noqa: BLE001 - report the last one
            last = error
    sys.exit(f"no headless Chrome to run the layout smoke in: {last}")


def run_page(browser, html):
    page = browser.new_page()
    run = Run(page, html)
    run_checks(run)
    page.close()
    empty = [cid for cid, n in run.ran.items() if n == 0]
    if empty:
        run.failures.append(("(none)", f"checks that never ran: {empty}"))
    return run


def report(run, label):
    for cid, message in run.failures:
        print(f"{label}: [{cid}] {message}")
    return len(run.failures)


def main():
    args = sys.argv[1:]
    with sync_playwright() as p:
        browser = launch(p)
        print(f"Chrome {browser.version}")
        if args == ["--self-test"]:
            failed = 0
            good = run_page(browser, variant_html("good"))
            failed += report(good, "page.html")
            for cid in CHECKS:
                run = run_page(browser, variant_html(cid))
                found = {c for c, _ in run.failures}
                if cid not in found:
                    print(f"✗ variant {cid}: expected [{cid}] to fail, got {sorted(found) or 'nothing'}")
                    failed += 1
            browser.close()
            if failed:
                sys.exit(f"{failed} problem(s)")
            print(f"✓ page.html passes; each of {len(CHECKS)} bad variants fails on its own check")
            return
        if len(args) == 2 and args[0] == "--variant":
            run = run_page(browser, variant_html(args[1]))
            browser.close()
            bad = report(run, f"variant {args[1]}")
            sys.exit(f"{bad} layout problem(s)" if bad else 0)
        if args:
            sys.exit(__doc__)
        run = run_page(browser, variant_html("good"))
        browser.close()
        bad = report(run, "page.html")
        if bad:
            sys.exit(f"{bad} layout problem(s)")
        print(f"✓ layout smoke: {sum(run.ran.values())} measurements in {len(CHECKS)} checks")


if __name__ == "__main__":
    main()
