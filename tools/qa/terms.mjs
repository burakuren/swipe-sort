// node tools/qa/terms.mjs
// Terminology sweep over visible frame text (HTML) and quoted strings in specs. Reports every occurrence of
// domain words (guest, invitee, wedding, attendee, RSVP, bride, groom, candidate, product) with context, minus
// known sample-data values and template names, so QA can judge each one. Also flags non-glossary synonyms.
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { SCREENS, DESIGN } from '../lib.mjs';

const WORDS = /\b(guests?|invitees?|weddings?|attendees?|rsvps?|brides?|grooms?|candidates?|products?)\b/gi;
const SYNONYMS = /\b(entries|entry|records?|cards? deck|vote[sd]?|voting|approve[sd]?|declined?|undecided|tags? as|categor(y|ies)|admin|editor role|viewer|participants?|collaborators? role|columns?)\b/gi;
// Sample-data values and template names (allowed).
const ALLOW = [
  /Wedding guests( \(copy\))?/g, /Guest with table side/g, /Bride's|Groom's/g, /candidates-q4(\.csv)?/gi,
  /\bProduct\b(?= template| card template)/g, /\bCandidate\b(?= template)/g, /template: (Product|Candidate)/g,
  /mert-family\.csv/g, /Frontend hiring/g, /\bwedding-guests[a-z0-9.-]*/gi, /\bguest-list[a-z0-9.-]*/gi,
];
const visible = (html) => html
  .replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<figcaption[\s\S]*?<\/figcaption>/gi, ' ').replace(/<header class="mock-doc"[\s\S]*?<\/header>/gi, ' ')
  .replace(/<h2 class="mock-section"[\s\S]*?<\/h2>(\s*<p[^>]*>[\s\S]*?<\/p>)?/gi, ' ')
  .replace(/aria-label="([^"]*)"/g, ' [aria:$1] ').replace(/<[^>]+>/g, ' ').replace(/&#39;|&rsquo;/g, "'").replace(/&amp;/g, '&').replace(/\s+/g, ' ');

const hits = new Map();
const note = (key, ctx) => { if (!hits.has(key)) hits.set(key, new Set()); hits.get(key).add(ctx); };
for (const f of readdirSync(SCREENS).filter((x) => x.endsWith('.html')).sort()) {
  const html = readFileSync(join(SCREENS, f), 'utf8');
  for (const part of html.split(/(?=<[a-z]+[^>]*\sdata-frame=")/)) {
    const id = part.match(/^<[a-z]+[^>]*\sdata-frame="([^"]+)"/)?.[1];
    if (!id) continue;
    let t = visible(part);
    for (const re of ALLOW) t = t.replace(re, ' ');
    for (const m of t.matchAll(WORDS)) note(`HTML ${m[0].toLowerCase()}`, `${id}: …${t.slice(Math.max(0, m.index - 50), m.index + 40).trim()}…`);
  }
}
for (const f of readdirSync(SCREENS).filter((x) => x.endsWith('.md')).sort()) {
  const md = readFileSync(join(SCREENS, f), 'utf8');
  for (const m of md.matchAll(/"([^"\n]{1,240})"|“([^”\n]{1,240})”/g)) {
    let q = m[1] ?? m[2];
    for (const re of ALLOW) q = q.replace(re, ' ');
    for (const w of q.matchAll(WORDS)) note(`SPEC ${w[0].toLowerCase()}`, `${f}: "${q.slice(0, 160)}"`);
  }
}
for (const [k, v] of [...hits].sort()) {
  console.log(`\n## ${k} (${v.size})`);
  [...v].slice(0, 60).forEach((x) => console.log('- ' + x));
}
