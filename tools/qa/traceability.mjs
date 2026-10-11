// node tools/qa/traceability.mjs
// Builds design/05-qa/traceability.md: every requirement ID in 00-brief/requirements.md mapped to the
// screens whose spec §1 ("Purpose and requirements") claims it, plus documents for foundation/process
// requirements. Also lists IDs mentioned elsewhere in specs (secondary evidence) and unknown IDs cited.
// Exits 1 when a requirement has no screen and no document mapping.
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN, SCREENS, QA } from '../lib.mjs';

const reqText = readFileSync(join(DESIGN, '00-brief/requirements.md'), 'utf8');
const reqs = [];
for (const m of reqText.matchAll(/\*\*([A-Z]+-\d{2})\*\*\s*(.*)/g)) {
  const text = m[2].trim().length > 3 ? m[2].trim() : 'Every screen is designed with all applicable states (default, empty, loading, error, offline, web-unavailable, screen-specific).';
  reqs.push({ id: m[1], text });
}
const reqIds = new Set(reqs.map((r) => r.id));

/** Expand "SRT-01–SRT-17", "PLT-14–19", "PLT-03/PLT-04" and plain IDs into a list of IDs. */
function extractIds(text) {
  const ids = new Set();
  const t = text.replace(/\s+/g, ' ');
  for (const m of t.matchAll(/\b([A-Z]{2,5})-(\d{2})\s*[–—-]\s*(?:([A-Z]{2,5})-)?(\d{2})\b/g)) {
    const [, p, a, p2, b] = m;
    if (p2 && p2 !== p) continue;
    for (let i = +a; i <= +b; i++) ids.add(`${p}-${String(i).padStart(2, '0')}`);
  }
  for (const m of t.matchAll(/\b([A-Z]{2,5}-\d{2})\b/g)) ids.add(m[1]);
  return [...ids].filter((id) => !/^(A|S)-/.test(id));
}

const specs = readdirSync(SCREENS).filter((f) => /^S\d\d-.*\.md$/.test(f)).sort();
// Retired screens (kept for reference only) never count as primary coverage: S18 Photos import (D-32).
const RETIRED = new Set(['S18']);
const primary = new Map(); // req -> Set(screen)
const secondary = new Map();
const unknown = [];
const add = (map, id, s) => { if (!map.has(id)) map.set(id, new Set()); map.get(id).add(s); };
for (const f of specs) {
  const sid = f.slice(0, 3);
  const md = readFileSync(join(SCREENS, f), 'utf8');
  const sec1 = md.match(/^## 1\.[\s\S]*?(?=^## 2\.)/m)?.[0] ?? '';
  if (!sec1) unknown.push(`${f}: no §1 section found`);
  for (const id of extractIds(sec1)) {
    if (reqIds.has(id)) add(RETIRED.has(sid) ? secondary : primary, id, sid);
    else unknown.push(`${f} §1 cites unknown ID ${id}`);
  }
  for (const id of extractIds(md.replace(sec1, ''))) if (reqIds.has(id)) add(secondary, id, sid);
}

// Documents that satisfy foundation / process requirements (verified to exist below).
const F = '01-foundations/';
const DOCS = {
  'GOAL-06': ['00-brief/assumptions.md'],
  'SCR-00': ['05-qa/coverage.md', '05-qa/review-report.md (coverage check)'],
  'PLT-01': ['00-brief/assumptions.md (A-02)'],
  'PLT-13': [`${F}contrast.md`, '05-qa/a11y-report.md'],
  'PLT-17': [`${F}motion.md`],
  'STK-01': [`${F}tokens.json`, `${F}design-system.html`],
  'STK-02': [`${F}components.md`, `${F}components.html`],
  'STK-03': [`${F}tailwind.config.js`],
  'STK-04': [`${F}tokens.css`],
  'STK-05': [`${F}tokens.json`, `${F}tokens.css`],
  'STK-06': [`${F}design-principles.md`, `${F}components.md`],
  'STK-07': [`${F}design-principles.md`],
  'STK-08': [`${F}design-system.html`],
  'STK-09': [`${F}design-system.html`, '00-brief/assumptions.md (A-42)'],
  'STK-10': [`${F}motion.md`],
  'STK-11': [`${F}motion.md`],
  'VIS-15': ['04-explorations/S25-direction-a.html', '04-explorations/S25-direction-b.html', '04-explorations/S25-direction-c.html', '00-brief/assumptions.md (A-40)'],
  'TPL-04': ['00-brief/assumptions.md'],
  'SRT-06': [`${F}motion.md`],
  'BRD-01': [`${F}brand/logo-mark.svg`],
  'BRD-02': [`${F}brand/wordmark-light.svg`, `${F}brand/wordmark-dark.svg`],
  'BRD-03': [`${F}brand/app-icon.svg`],
  'BRD-04': [`${F}brand/adaptive-foreground.svg`, `${F}brand/adaptive-background.svg`, `${F}brand/adaptive-monochrome.svg`],
  'BRD-05': [`${F}brand/logo-mark-dark.svg`, `${F}brand/logo-mark-mono.svg`, `${F}design-system.html`],
  'OUT-01': ['02-architecture/navigation-map.md'], 'OUT-02': ['00-brief/assumptions.md (A-03)'],
  'OUT-03': ['00-brief/assumptions.md (A-02)'], 'OUT-04': ['HANDOFF.md'], 'OUT-05': ['HANDOFF.md'],
  'OUT-06': ['HANDOFF.md'], 'OUT-07': ['HANDOFF.md'], 'OUT-08': ['HANDOFF.md'],
  'SMP-01': ['02-data/sample-data.json'], 'SMP-02': ['02-data/sample-data.json'], 'SMP-03': ['02-data/sample-data.json'],
  'SMP-04': ['02-data/sample-data.json'], 'SMP-05': ['02-data/sample-data.json'], 'SMP-06': ['02-data/sample-data.json'],
  'SMP-07': ['02-data/images/'],
  'DEL-01': ['README.md'], 'DEL-02': ['HANDOFF.md'],
  'DEL-03': ['00-brief/brief.md', '00-brief/requirements.md', '00-brief/assumptions.md'],
  'DEL-04': [`${F}design-principles.md`],
  'DEL-05': [`${F}tokens.json`, `${F}tokens.css`, `${F}tailwind.config.js`, `${F}tokens.ts`],
  'DEL-06': [`${F}design-system.html`], 'DEL-07': [`${F}components.html`], 'DEL-08': [`${F}components.md`],
  'DEL-09': [`${F}motion.md`], 'DEL-10': [`${F}brand/`], 'DEL-11': ['02-architecture/navigation-map.md'],
  'DEL-12': ['02-architecture/domain-model.md'], 'DEL-13': ['02-data/sample-data.json'],
  'DEL-14': ['03-screens/ (40 HTML + 40 specs)'], 'DEL-15': ['04-explorations/'],
  'DEL-16': ['04-prototype/index.html', '04-prototype/swipe-demo.html'],
  'DEL-17': ['05-qa/screenshots/', '05-qa/a11y-report.md', '05-qa/coverage.md', '05-qa/traceability.md', '05-qa/review-report.md'],
  'DEL-18': ['05-qa/lint-report.md'], 'DEL-19': ['05-qa/lint-report.md'], 'DEL-20': ['05-qa/lint-report.md'],
  'DEL-21': ['02-data/sample-data.json'],
  'DEL-22': ['tools/flows/01-first-launch.flow.mjs'], 'DEL-23': ['tools/flows/02-resort-maybe.flow.mjs'],
  'DEL-24': ['tools/flows/03-invite-web.flow.mjs'], 'DEL-25': ['tools/flows/04-csv-template.flow.mjs'],
  'PRC-01': ['git log'], 'PRC-02': ['tools/flows/*.flow.mjs'], 'PRC-03': ['05-qa/review-report.md'],
  'SUC-01': ['05-qa/coverage.md'], 'SUC-02': ['05-qa/traceability.md'], 'SUC-03': ['05-qa/review-report.md', '05-qa/a11y-report.md'],
  'SUC-04': ['tools/flows/01-first-launch.flow.mjs'], 'SUC-05': ['tools/flows/03-invite-web.flow.mjs'],
  'SUC-09': ['00-brief/assumptions.md (A-55)'], 'SUC-10': ['HANDOFF.md'],
};
// Requirements taken out of scope by a build decision are satisfied by the decision record.
for (const r of reqs) if (/Out of scope \(D-\d\d\)/.test(r.text)) DOCS[r.id] = [...(DOCS[r.id] ?? []), '00-brief/assumptions.md (A-129)'];
const ROOTFILES = new Set(['git log', 'tools/flows/*.flow.mjs']);
const docMissing = [];
const docOk = (p) => {
  const path = p.replace(/ \(.*\)$/, '');
  if (ROOTFILES.has(path)) return true;
  if (path.startsWith('tools/')) return existsSync(join(DESIGN, '..', path));
  if (path.startsWith('03-screens/')) return true;
  return existsSync(join(DESIGN, path));
};
for (const [id, docs] of Object.entries(DOCS)) {
  if (!reqIds.has(id)) docMissing.push(`doc map cites unknown ${id}`);
  for (const d of docs) if (!docOk(d)) docMissing.push(`${id}: ${d} does not exist`);
}

const rows = [];
const gaps = [];
const docOnly = [];
for (const r of reqs) {
  const scr = [...(primary.get(r.id) ?? [])].sort();
  const sec = [...(secondary.get(r.id) ?? [])].filter((s) => !scr.includes(s)).sort();
  const docs = (DOCS[r.id] ?? []).filter(docOk);
  let status = 'Mapped';
  const oos = r.text.match(/Out of scope \((D-\d\d)\)/);
  if (!scr.length && !docs.length) { status = sec.length ? 'Gap: mentioned only outside §1' : 'GAP'; gaps.push({ ...r, sec }); }
  else if (oos) status = `Out of scope (${oos[1]})`;
  else if (!scr.length) { status = 'Mapped (documents)'; docOnly.push(r.id); }
  rows.push(`| ${r.id} | ${r.text.replace(/\|/g, '\\|')} | ${scr.join(', ') || '—'} | ${docs.join('<br>') || '—'} | ${sec.join(', ') || ''} | ${status} |`);
}

const out = `# Traceability

Generated by \`node tools/qa/traceability.mjs\` (QA, Phase 4). Every requirement ID in
\`00-brief/requirements.md\` mapped to the screens whose spec §1 claims it ("Screens (spec §1)"), the
documents that satisfy it, and other screens whose spec mentions it outside §1 (secondary evidence). Retired
screens (S18, out of scope by D-32) count only as secondary evidence; out-of-scope requirements cite A-129.
Re-run the script after spec changes; do not edit the table by hand.

**${reqs.length} requirements · ${reqs.length - gaps.length} mapped · ${gaps.length} gap(s) · ${docOnly.length} mapped to documents only.**

${gaps.length ? `## Gaps (blocking)\n\n${gaps.map((g) => `- **${g.id}** ${g.text}${g.sec.length ? ` (mentioned outside §1 in ${g.sec.join(', ')})` : ''}`).join('\n')}\n` : '## Gaps\n\nNone.\n'}
${unknown.length || docMissing.length ? `## Spec citation problems\n\n${[...unknown, ...docMissing].map((u) => `- ${u}`).join('\n')}\n` : ''}
## Matrix

| ID | Requirement | Screens (spec §1) | Documents | Also in spec body | Status |
| --- | --- | --- | --- | --- | --- |
${rows.join('\n')}
`;
writeFileSync(join(QA, 'traceability.md'), out);
console.log(`traceability: ${reqs.length} requirements, ${gaps.length} gap(s), ${docOnly.length} document-only, ${unknown.length} unknown citation(s)`);
for (const g of gaps) console.log(`  GAP ${g.id} ${g.text.slice(0, 80)}${g.sec.length ? ` [body: ${g.sec.join(',')}]` : ''}`);
for (const u of [...unknown, ...docMissing]) console.log(`  ${u}`);
process.exit(gaps.length ? 1 : 0);
