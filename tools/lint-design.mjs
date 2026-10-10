// npm run lint [-- <filter>...] [--no-targets]
// Static and rendered checks for the design files; writes design/05-qa/lint-report.md.
// Errors (exit 1): forbidden domain words in UI text, hard-coded values in screen HTML, duplicate or
// malformed frame IDs, frames without a visible label, icon-only controls without an accessible name.
// Warnings: touch targets smaller than 48×48 (rendered with Playwright), checked by QA by eye.
import { readFileSync, readdirSync, writeFileSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';
import { chromium } from 'playwright';
import { DESIGN, SCREENS, QA, listHtml, parseArgs, openFile, rel } from './lib.mjs';

const { filters, flags } = parseArgs();
const match = (f) => !filters.length || filters.some((x) => f.toLowerCase().includes(x));
const errors = [];
const warnings = [];

// Domain words may appear only in sample data and template names (brief <terminology>).
const FORBIDDEN = /\b(guests?|invitees?|wedding|rsvps?|attendees?|bride|groom)\b/gi;
const ALLOWED_PHRASES = [
  /Wedding guests/g, // sample list name
  /Guest with table side/g, // sample custom template name
  /Bride's|Groom's/g, // sample field values
  /mert-family\.csv/g,
  /guest (mode|user|lists?|session|state|variant)/gi, // account state wording in specs and frame labels
  /\bS0?5[^<\n]*/g, // S05 is "sign-in prompt from guest mode" by brief definition (labels only)
];
const visibleText = (html) =>
  html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<figcaption[\s\S]*?<\/figcaption>/gi, ' ')
    .replace(/<header class="mock-doc"[\s\S]*?<\/header>/gi, ' ')
    .replace(/<h2 class="mock-section"[\s\S]*?<\/h2>(\s*<p>[\s\S]*?<\/p>)?/gi, ' ')
    .replace(/<[^>]+>/g, ' ');
function checkTerms(file, text) {
  let t = text.replace(/\bS\d\d-[a-z0-9-]+/g, ' '); // frame IDs are identifiers, not copy
  for (const re of ALLOWED_PHRASES) t = t.replace(re, ' ');
  for (const m of t.matchAll(FORBIDDEN)) {
    const at = Math.max(0, m.index - 40);
    errors.push(`${rel(file)}: forbidden domain word "${m[0]}" in "…${t.slice(at, m.index + 40).replace(/\s+/g, ' ').trim()}…"`);
  }
}

// ---------- static checks on screen HTML ----------
const screenFiles = listHtml(SCREENS, { recursive: false }).filter((f) => match(basename(f)));
const frameOwner = new Map();
for (const file of screenFiles) {
  const html = readFileSync(file, 'utf8');
  const name = basename(file);
  const screenId = name.match(/^(S\d\d)/)?.[1];
  if (!screenId) errors.push(`${rel(file)}: file name must start with its screen ID (Sxx-)`);
  if (!/<html[^>]*lang="en"[^>]*data-theme="light"/.test(html)) errors.push(`${rel(file)}: root must be <html lang="en" data-theme="light">`);
  if (!/href="\.\.\/assets\/css\/app\.css"/.test(html)) errors.push(`${rel(file)}: missing ../assets/css/app.css`);
  if (/https?:\/\/[^"']*(cdn|unpkg|jsdelivr|googleapis)/i.test(html)) errors.push(`${rel(file)}: CDN link found (must work offline)`);
  if (/prefers-color-scheme/.test(html)) errors.push(`${rel(file)}: prefers-color-scheme is not allowed`);
  if (/\sstyle="/.test(html)) errors.push(`${rel(file)}: inline style attribute found`);
  for (const m of html.matchAll(/<style[\s\S]*?<\/style>/gi)) {
    if (/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\((?!var)|\d+px/i.test(m[0])) errors.push(`${rel(file)}: <style> block with hard-coded values`);
  }
  for (const m of html.matchAll(/class="([^"]*)"/g)) {
    for (const cls of m[1].split(/\s+/)) {
      const arb = cls.match(/\[([^\]]+)\]/);
      if (!arb) continue;
      const v = arb[1];
      if (/#|rgb|hsl\(|px|rem|em\b|vh|vw/.test(v) && !/^(w|h|min-w|min-h|max-w|max-h|size)-\[(412|393|1280|915|852|800)px\]$/.test(cls)) {
        errors.push(`${rel(file)}: hard-coded value in class "${cls}"`);
      }
    }
  }
  // frames
  const frames = [...html.matchAll(/<([a-z]+)([^>]*\sdata-frame="([^"]+)"[^>]*)>/g)];
  if (!frames.length) errors.push(`${rel(file)}: no [data-frame] elements`);
  for (const [, , attrs, id] of frames) {
    if (frameOwner.has(id)) errors.push(`duplicate frame id "${id}" in ${name} and ${frameOwner.get(id)}`);
    frameOwner.set(id, name);
    if (screenId && !id.startsWith(`${screenId}-`)) errors.push(`${name}: frame "${id}" must start with "${screenId}-"`);
    if (!/^S\d\d-[a-z0-9-]+$/.test(id)) errors.push(`${name}: frame id "${id}" must be lowercase, hyphenated`);
    if (!new RegExp(`\\sid="${id}"`).test(attrs)) errors.push(`${name}: frame "${id}" needs id="${id}" for prototype links`);
  }
  const labels = (html.match(/class="frame-label"/g) || []).length;
  if (labels < frames.length) errors.push(`${name}: ${frames.length - labels} frame(s) without a frame-label`);
  // icon-only controls
  for (const m of html.matchAll(/<(button|a)\b([^>]*)>([\s\S]*?)<\/\1>/g)) {
    const [, tag, attrs, inner] = m;
    const text = inner.replace(/<[^>]+>/g, '').trim();
    if (!text && !/aria-label=|aria-labelledby=|title=/.test(attrs)) errors.push(`${name}: icon-only <${tag}> without aria-label (${inner.match(/i-lucide-[a-z0-9-]+/)?.[0] ?? 'no icon'})`);
  }
  checkTerms(file, visibleText(html));
}

// ---------- link integrity: every file.html#frame and #frame link resolves ----------
{
  const allFrames = new Map(); // file name -> Set(frame ids + element ids)
  for (const f of listHtml(DESIGN)) {
    const html = readFileSync(f, 'utf8');
    allFrames.set(f, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  }
  const linkFiles = [...screenFiles, ...listHtml(join(DESIGN, '04-prototype')).filter((f) => match(basename(f)))];
  for (const file of linkFiles) {
    const html = readFileSync(file, 'utf8');
    for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
      if (/^(https?:|mailto:|tel:|data:)/.test(href) || href.endsWith('.md') || href.endsWith('.css') || href.endsWith('.svg') || href === '#') continue;
      const [path, hash] = href.split('#');
      const target = path ? join(file, '..', path.split('?')[0]) : file;
      if (!existsSync(target)) { errors.push(`${rel(file)}: broken link to ${href} (file missing)`); continue; }
      if (hash && target.endsWith('.html') && !(allFrames.get(target) ?? new Set()).has(hash)) errors.push(`${rel(file)}: broken link to ${href} (no element #${hash})`);
    }
  }
}

// ---------- terminology in specs and other UI files ----------
const mdFiles = existsSync(SCREENS) ? readdirSync(SCREENS).filter((f) => f.endsWith('.md') && match(f)).map((f) => join(SCREENS, f)) : [];
for (const file of mdFiles) {
  // Only quoted UI strings in specs are checked ("…" or `…`), prose may discuss the brief.
  const md = readFileSync(file, 'utf8');
  const quoted = [...md.matchAll(/"([^"\n]{1,200})"|“([^”\n]{1,200})”/g)].map((m) => m[1] ?? m[2]).join('\n');
  checkTerms(file, quoted);
}
for (const dir of ['04-prototype']) {
  for (const file of listHtml(join(DESIGN, dir))) if (match(basename(file))) checkTerms(file, visibleText(readFileSync(file, 'utf8')));
}

// ---------- rendered touch-target check ----------
if (!flags['no-targets'] && screenFiles.length) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  for (const file of screenFiles) {
    await openFile(page, file);
    const small = await page.$$eval('[data-frame] button, [data-frame] [role="button"], [data-frame] a[href], [data-frame] [role="tab"], [data-frame] [role="menuitem"]', (els) =>
      els
        .filter((el) => !el.closest('p, li > span, kbd, .frame-label, [aria-hidden="true"]') && getComputedStyle(el).visibility !== 'hidden')
        .map((el) => {
          const r = el.getBoundingClientRect();
          return { w: Math.round(r.width), h: Math.round(r.height), frame: el.closest('[data-frame]')?.dataset.frame, label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40) };
        })
        .filter((b) => b.w > 0 && b.h > 0 && (b.w < 48 || b.h < 48)),
    );
    for (const b of small) warnings.push(`${b.frame}: target ${b.w}×${b.h} "${b.label}"`);
  }
  await browser.close();
}

const lines = [
  '# Design lint report',
  '',
  `Generated ${new Date().toISOString()} by \`npm run lint\`${filters.length ? ` (filter: ${filters.join(', ')})` : ''}.`,
  '',
  `**${errors.length} error(s), ${warnings.length} touch-target warning(s)** across ${screenFiles.length} screen file(s) and ${mdFiles.length} spec(s).`,
  '',
  '## Errors',
  '',
  ...(errors.length ? errors.map((e) => `- ${e}`) : ['None.']),
  '',
  '## Touch targets under 48×48 (review: acceptable only when a larger parent row is the target)',
  '',
  ...(warnings.length ? warnings.map((w) => `- ${w}`) : ['None.']),
  '',
];
if (!filters.length) writeFileSync(join(QA, 'lint-report.md'), lines.join('\n'));
console.log(`lint: ${errors.length} error(s), ${warnings.length} warning(s)${filters.length ? '' : ' → design/05-qa/lint-report.md'}`);
for (const e of errors.slice(0, 50)) console.log(`  error: ${e}`);
if (errors.length > 50) console.log(`  …and ${errors.length - 50} more`);
if (filters.length) for (const w of warnings.slice(0, 40)) console.log(`  warn: ${w}`);
process.exit(errors.length ? 1 : 0);
