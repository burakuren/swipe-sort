// npm run shots [-- <filter>...] [--scale=2] [--theme=light|dark]
// Screenshots every [data-frame] element in design/03-screens/*.html, in light and dark mode,
// into design/05-qa/screenshots/<frame>.<theme>.png.
// Filters (case-insensitive substrings) match the file name or the frame id, e.g. `npm run shots -- S03`.
import { chromium } from 'playwright';
import { basename, join } from 'node:path';
import { SCREENS, QA, THEMES, listHtml, parseArgs, setTheme, openFile, ensureDir, rel } from './lib.mjs';

const { filters, flags } = parseArgs();
const scale = Number(flags.scale ?? 2);
const themes = flags.theme ? [flags.theme] : THEMES;
const outDir = join(QA, 'screenshots');
const matches = (s) => filters.length === 0 || filters.some((f) => s.toLowerCase().includes(f));

const files = listHtml(SCREENS, { recursive: false });
if (files.length === 0) {
  console.log(`shots: no HTML files in ${rel(SCREENS)} — nothing to do`);
  process.exit(0);
}

ensureDir(outDir);
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: scale });
const page = await context.newPage();
const errors = [];
const seen = new Map();
let count = 0;

try {
  for (const file of files) {
    const fileMatch = matches(basename(file));
    try {
      await openFile(page, file);
      const ids = await page.$$eval('[data-frame]', (els) => els.map((el) => el.dataset.frame));
      const wanted = ids.filter((id) => fileMatch || matches(id));
      if (wanted.length === 0) continue;
      for (const theme of themes) {
        await setTheme(page, theme);
        for (const id of wanted) {
          if (theme === themes[0]) {
            if (seen.has(id)) errors.push(`duplicate frame id "${id}" in ${basename(file)} and ${seen.get(id)}`);
            seen.set(id, basename(file));
          }
          const path = join(outDir, `${id}.${theme}.png`);
          await page.locator(`[data-frame="${id}"]`).first().screenshot({ path, animations: 'disabled', caret: 'hide' });
          count++;
        }
      }
      console.log(`  ${basename(file)}: ${wanted.length} frame(s) × ${themes.length} theme(s)`);
    } catch (err) {
      errors.push(`${basename(file)}: ${err.message.split('\n')[0]}`);
    }
  }
} finally {
  await browser.close();
}

console.log(`shots: ${count} screenshot(s) → ${rel(outDir)}${filters.length ? ` (filter: ${filters.join(', ')})` : ''}`);
if (count === 0 && filters.length) console.log('shots: filter matched no frames');
for (const e of errors) console.error(`  error: ${e}`);
process.exit(errors.length ? 1 : 0);
