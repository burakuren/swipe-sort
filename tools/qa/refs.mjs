// node tools/qa/refs.mjs
// Checks that every frame ID referenced in specs, navigation-map.md, components.md, assumptions.md and
// HANDOFF/README exists as a [data-frame] in 03-screens, and that every prototype link in a frame points to an
// existing frame. Also checks navigation-map §5 required frame IDs and §6 data-action names per frame.
// Prints a report; exits 1 on missing references.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN, SCREENS } from '../lib.mjs';

const frames = new Map(); // id -> file
const elementIds = new Map(); // file -> Set(ids)
const actions = new Map(); // frame -> [{action, href}]
for (const f of readdirSync(SCREENS).filter((x) => x.endsWith('.html'))) {
  const html = readFileSync(join(SCREENS, f), 'utf8');
  elementIds.set(f, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  // split by frame start to attribute data-actions to frames
  const parts = html.split(/(?=<[a-z]+[^>]*\sdata-frame=")/);
  for (const part of parts) {
    const id = part.match(/^<[a-z]+[^>]*\sdata-frame="([^"]+)"/)?.[1];
    if (!id) continue;
    frames.set(id, f);
    const list = [];
    for (const m of part.matchAll(/<(a|button)\b([^>]*)>/g)) {
      const a = m[2].match(/data-action="([^"]+)"/)?.[1];
      const href = m[2].match(/href="([^"]+)"/)?.[1];
      if (a) list.push({ action: a, href });
    }
    actions.set(id, list);
  }
}
const isFrame = (id) => frames.has(id);
// Frame-like tokens that are not frame IDs (screen IDs with words used as prose, explorations, etc.)
const IGNORE = /^S\d\d-(name|direction-[abc]|[a-z]+\.(html|md))$/;

const missing = [];
const docs = [
  ...readdirSync(SCREENS).filter((x) => x.endsWith('.md')).map((x) => join(SCREENS, x)),
  join(DESIGN, '02-architecture/navigation-map.md'),
  join(DESIGN, '02-architecture/domain-model.md'),
  join(DESIGN, '01-foundations/components.md'),
  join(DESIGN, '00-brief/assumptions.md'),
  join(DESIGN, 'HANDOFF.md'),
  join(DESIGN, 'README.md'),
].filter(existsSync);
for (const d of docs) {
  const txt = readFileSync(d, 'utf8');
  const lines = txt.split('\n');
  lines.forEach((line, i) => {
    // strip file names like S25-sorting.html / .md
    const clean = line.replace(/S\d\d-[a-z0-9-]+\.(html|md|py|\*)/g, ' ');
    for (const m of clean.matchAll(/(?<!D-)\b(S\d\d-[a-z0-9]+(?:-[a-z0-9]+)*)\b/g)) {
      let id = m[1];
      if (IGNORE.test(id) || isFrame(id)) continue;
      // tolerate wildcard prose like "S28-shared-*" or trailing hyphen
      if (/\*$/.test(line.slice(m.index + id.length, m.index + id.length + 1))) continue;
      missing.push(`${d.replace(DESIGN + '/', '')}:${i + 1} references unknown frame ${id}`);
    }
  });
}

// in-frame prototype hrefs
const badHref = [];
for (const [fid, list] of actions) for (const { action, href } of list) {
  if (!href || /^(https?:|mailto:|tel:)/.test(href) || href === '#') continue;
  const [path, hash] = href.split('#');
  const file = path ? path.split('/').pop().split('?')[0] : frames.get(fid);
  if (path && path.includes('04-prototype')) continue;
  if (hash && !(elementIds.get(file) ?? new Set()).has(hash)) badHref.push(`${fid} [${action}] → ${href}`);
}

// navigation-map §5 required frames and §6 actions
const nav = readFileSync(join(DESIGN, '02-architecture/navigation-map.md'), 'utf8');
const sec5 = nav.match(/## 5\.[\s\S]*?(?=## 6\.)/)[0];
const required = [...new Set([...sec5.matchAll(/`(S\d\d-[a-z0-9-]+)`/g)].map((m) => m[1]))];
const reqMissing = required.filter((id) => !isFrame(id));
const sec6 = nav.match(/## 6\.[\s\S]*/)[0].replace(/\n/g, ' ');
const flowMissing = [];
for (const m of sec6.matchAll(/`(S\d\d-[a-z0-9-]+)`\s*\[`([a-z0-9-]+)`/g)) {
  const [, fid, act] = m;
  if (!isFrame(fid)) { flowMissing.push(`${fid}: frame missing`); continue; }
  if (!(actions.get(fid) ?? []).some((a) => a.action === act)) flowMissing.push(`${fid}: no data-action="${act}" (has: ${(actions.get(fid) ?? []).map((a) => a.action).join(', ') || 'none'})`);
}
// screens without a default frame
const noDefault = [...new Set([...frames.values()])].filter((f) => !isFrame(`${f.slice(0, 3)}-default`));

console.log(`frames: ${frames.size}`);
console.log(`\n## Unknown frame references in docs (${missing.length})`);
missing.forEach((x) => console.log('- ' + x));
console.log(`\n## Broken in-frame hrefs (${badHref.length})`);
badHref.forEach((x) => console.log('- ' + x));
console.log(`\n## navigation-map §5 required frames missing (${reqMissing.length})`);
reqMissing.forEach((x) => console.log('- ' + x));
console.log(`\n## navigation-map §6 flow steps missing frame/action (${flowMissing.length})`);
flowMissing.forEach((x) => console.log('- ' + x));
console.log(`\n## Screen files without Sxx-default (${noDefault.length})`);
noDefault.forEach((x) => console.log('- ' + x));
process.exit(missing.length + badHref.length + reqMissing.length + flowMissing.length ? 1 : 0);
