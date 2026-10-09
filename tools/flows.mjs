// npm run flows [-- <filter>...] [--theme=light|dark] [--headed]
// Runs prototype click-through tests from tools/flows/*.flow.mjs against the HTML mockups
// over file:// URLs. Each flow runs in a fresh browser context. Exits 1 if any flow fails.
//
// Flow module shape:
//   export default {
//     name: 'Onboarding → Home',
//     async run({ page, open, assert, shot, theme }) {
//       await open('03-screens/S01-onboarding.html');      // path relative to /design
//       await page.click('[data-action="continue"]');
//       assert.match(page.url(), /S02-home\.html$/);
//       await shot('after-continue');                      // → design/05-qa/flows/<flow>/<name>.<theme>.png
//     },
//   };
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readdirSync } from 'node:fs';
import { join, basename } from 'node:path';
import { ROOT, DESIGN, QA, fileUrl, parseArgs, setTheme, ensureDir, rel } from './lib.mjs';

const FLOWS = join(ROOT, 'tools/flows');
const { filters, flags } = parseArgs();
const theme = flags.theme ?? 'light';
const files = readdirSync(FLOWS)
  .filter((f) => f.endsWith('.flow.mjs'))
  .sort()
  .filter((f) => !filters.length || filters.some((x) => f.toLowerCase().includes(x)));

if (files.length === 0) {
  console.log(`flows: no flows in ${rel(FLOWS)} (*.flow.mjs)${filters.length ? ' matching filter' : ''} — nothing to do`);
  process.exit(0);
}

const browser = await chromium.launch({ headless: !flags.headed });
const results = [];
try {
  for (const file of files) {
    const slug = basename(file, '.flow.mjs');
    const outDir = join(QA, 'flows', slug);
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
    const page = await context.newPage();
    const pageErrors = [];
    page.on('pageerror', (e) => pageErrors.push(e.message));
    const t0 = Date.now();
    let name = slug;
    try {
      const flow = (await import(fileUrl(join(FLOWS, file)))).default;
      name = flow.name ?? slug;
      const open = async (p) => {
        await page.goto(fileUrl(join(DESIGN, p)), { waitUntil: 'load' });
        await setTheme(page, theme);
      };
      const shot = async (label) => {
        ensureDir(outDir);
        await page.screenshot({ path: join(outDir, `${label}.${theme}.png`), animations: 'disabled' });
      };
      // Keep the theme applied across link navigations inside the prototype.
      page.on('load', () => page.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme).catch(() => {}));
      await flow.run({ page, open, assert, shot, theme });
      if (pageErrors.length) throw new Error(`page error: ${pageErrors[0]}`);
      results.push({ name, ok: true, ms: Date.now() - t0 });
    } catch (err) {
      ensureDir(outDir);
      await page.screenshot({ path: join(outDir, `FAILED.${theme}.png`) }).catch(() => {});
      results.push({ name, ok: false, ms: Date.now() - t0, error: err.message.split('\n')[0] });
    } finally {
      await context.close();
    }
  }
} finally {
  await browser.close();
}

for (const r of results) console.log(`  ${r.ok ? 'PASS' : 'FAIL'} ${r.name} (${r.ms}ms)${r.error ? ` — ${r.error}` : ''}`);
const failed = results.filter((r) => !r.ok).length;
console.log(`flows: ${results.length - failed} passed, ${failed} failed (theme: ${theme})`);
process.exit(failed ? 1 : 0);
