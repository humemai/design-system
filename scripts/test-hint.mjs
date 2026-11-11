// Check js/hint.js: it parses as an ES module, it keeps no Stateloop names, and
// termHint and termHintElement give the markup, unique ids, escaping, a thrown
// error for a missing key, and the "Learn more" line (humemai/design-system #12).
//   node scripts/test-hint.mjs
// js/hint.js has no package.json beside it, so older Node treats a .js file as
// CommonJS and `export` fails. The script runs a copy named .mjs, which every
// Node version reads as a module. Node has no DOM, so termHintElement runs
// against a tiny fake document whose serialisation must equal termHint's string.
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { copyFileSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const src = join(dirname(fileURLToPath(import.meta.url)), "..", "js", "hint.js");
const tmp = mkdtempSync(join(tmpdir(), "hm-hint-"));
const copy = join(tmp, "hint.mjs");
copyFileSync(src, copy);

let mod;
try {
  // 1. It parses as a module (a syntax error here is a CI failure with the line).
  execFileSync(process.execPath, ["--check", copy], { stdio: "inherit" });
  mod = await import(pathToFileURL(copy).href);
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
const { bindHints, termHint, termHintElement } = mod;
assert.equal(typeof bindHints, "function", "bindHints is exported");

// 2. The port keeps no Stateloop class or id prefix.
assert.ok(!/stl-/.test(readFileSync(src, "utf8")), "js/hint.js still names an stl- class");

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");

class Node {
  constructor(tag) { this.tag = tag; this.attrs = []; this.kids = []; }
  setAttribute(k, v) { this.attrs.push([k, String(v)]); }
  set type(v) { this.setAttribute("type", v); }
  set className(v) { this.setAttribute("class", v); }
  set id(v) { this.setAttribute("id", v); }
  set href(v) { this.setAttribute("href", v); }
  set target(v) { this.setAttribute("target", v); }
  set rel(v) { this.setAttribute("rel", v); }
  set textContent(v) { this.kids = [String(v)]; }
  append(...nodes) { this.kids.push(...nodes); }
  html() {
    const a = this.attrs.map(([k, v]) => (v === "" ? ` ${k}` : ` ${k}="${esc(v)}"`)).join("");
    if (this.tag === "br") return "<br>";
    return `<${this.tag}${a}>${this.kids.map((k) => (typeof k === "string" ? esc(k) : k.html())).join("")}</${this.tag}>`;
  }
}
const fakeDoc = { createElement: (t) => new Node(t), createDocumentFragment: () => new Node("#frag") };
const htmlOf = (frag) => frag.kids.map((k) => k.html()).join("");
const idsOf = (html) => [...html.matchAll(/ id="([^"]+)"/g)].map((m) => m[1]);

const G = {
  est: { term: "the estimate", text: "How long the lane expects the job to take, in hours." },
  tag: { term: "a tag", text: 'Use <b>"R&D"</b> & \'more\'' },
  more: { term: "a rule", text: "Short.", learnMore: "https://example.com/doc?a=1&b=2" },
  rel: { term: "a rule", text: "Short.", learnMore: "/docs/rule.md" },
  bad: { term: "x", text: "Short.", learnMore: "javascript:alert(1)" },
};

// 3. The markup, with the id of the first call (the counter is module state, so read the id back).
const first = termHint(G, "est", "the estimate");
const [id1] = idsOf(first);
assert.match(id1, /^hm-hint-\d+$/);
assert.equal(
  first,
  `<button type="button" class="hm-hint" popovertarget="${id1}" popovertargetaction="show" aria-label="What is the estimate?" aria-describedby="${id1}">?</button>` +
    `<span id="${id1}" class="hm-hint__bubble" popover role="tooltip">How long the lane expects the job to take, in hours.</span>`,
  "markup of one hint",
);

// 4. Unique ids on repeated calls, in one string and across strings and elements.
const second = termHint(G, "est", "the estimate");
const el = htmlOf(termHintElement(G, "est", "the estimate", fakeDoc));
const ids = [id1, ...idsOf(second), ...idsOf(el)];
assert.equal(new Set(ids).size, 3, `three hints, three ids: ${ids}`);
assert.ok(ids.every((i) => /^hm-hint-\d+$/.test(i)));
assert.equal(Number(ids[1].split("-")[2]), Number(id1.split("-")[2]) + 1, "the counter counts up by one");
assert.equal(el.replace(/hm-hint-\d+/g, "ID"), second.replace(/hm-hint-\d+/g, "ID"), "the element serialises like the string");

// 5. The term argument is the label; without it the entry's own term is.
assert.match(termHint(G, "est", "a figure"), /aria-label="What is a figure\?"/);
assert.match(termHint(G, "est"), /aria-label="What is the estimate\?"/);

// 6. The sentence and the term are escaped.
const tag = termHint(G, "tag", 'a "tag" <i>');
assert.ok(tag.includes("Use &lt;b&gt;&quot;R&amp;D&quot;&lt;/b&gt; &amp; &#39;more&#39;"), tag);
assert.ok(!tag.includes("<b>"), "no raw tag from the sentence");
assert.ok(tag.includes('aria-label="What is a &quot;tag&quot; &lt;i&gt;?"'), tag);

// 7. A missing key throws an Error that names it; so do an empty entry and a glossary that inherits the key.
assert.throws(() => termHint(G, "nope", "x"), (e) => e instanceof Error && e.message.includes('"nope"'));
assert.throws(() => termHintElement(G, "nope", "x", fakeDoc), (e) => e instanceof Error && e.message.includes('"nope"'));
assert.throws(() => termHint({ k: { term: "k", text: "" } }, "k", "k"), /"k"/);
assert.throws(() => termHint(G, "toString", "x"), /"toString"/);
assert.throws(() => termHint(undefined, "est", "x"), /"est"/);

// 8. learnMore adds the last line: a link after the sentence; an unsafe URL is refused.
const more = termHint(G, "more", "a rule");
assert.ok(more.endsWith('Short.<br><a href="https://example.com/doc?a=1&amp;b=2" target="_blank" rel="noopener">Learn more</a></span>'), more);
assert.ok(termHint(G, "rel", "a rule").includes('<a href="/docs/rule.md"'));
assert.ok(!termHint(G, "est", "x").includes("Learn more"), "no link without learnMore");
assert.throws(() => termHint(G, "bad", "x"), /"bad"/);
assert.throws(() => termHintElement(G, "bad", "x", fakeDoc), /"bad"/);

console.log("✓ js/hint.js parses as a module, keeps no stl- names, and its markup, ids, escaping, errors and learnMore are as documented");
