// Shared helpers for the design tooling. Everything works on file:// URLs, no server.
import { readdirSync, statSync, mkdirSync } from 'node:fs';
import { join, relative, resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const DESIGN = join(ROOT, 'design');
export const SCREENS = join(DESIGN, '03-screens');
export const QA = join(DESIGN, '05-qa');
export const THEMES = ['light', 'dark'];

const SKIP_DIRS = new Set(['node_modules', 'assets', 'screenshots', '.git']);

/** Recursively list .html files under dir (skips assets and screenshot folders). */
export function listHtml(dir, { recursive = true } = {}) {
  let out = [];
  let entries;
  try { entries = readdirSync(dir); } catch { return out; }
  for (const name of entries.sort()) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) {
      if (recursive && !SKIP_DIRS.has(name)) out = out.concat(listHtml(full));
    } else if (name.endsWith('.html')) out.push(full);
  }
  return out;
}

export const fileUrl = (p) => pathToFileURL(p).href;
export const rel = (p) => relative(ROOT, p);
export const ensureDir = (d) => mkdirSync(d, { recursive: true });

/** Split argv into positional filters and --flags (--key or --key=value). */
export function parseArgs(argv = process.argv.slice(2)) {
  const filters = [];
  const flags = {};
  for (const a of argv) {
    if (a.startsWith('--')) {
      const [k, v] = a.slice(2).split('=');
      flags[k] = v ?? true;
    } else filters.push(a.toLowerCase());
  }
  return { filters, flags };
}

/** Theme switching convention: <html data-theme="light|dark">. */
export async function setTheme(page, theme) {
  await page.emulateMedia({ colorScheme: theme });
  await page.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme);
  await page.evaluate(() => document.fonts.ready);
}

export async function openFile(page, file) {
  await page.goto(fileUrl(file), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
}
