// npm run a11y [-- <filter>...] [--strict]
// Runs axe-core (WCAG 2.x A/AA) on every HTML file under /design in light and dark mode and writes
// design/05-qa/a11y-report.md. Exits 0 with a summary; --strict exits 1 when violations exist.
import { chromium } from 'playwright';
import { AxeBuilder } from '@axe-core/playwright';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN, QA, THEMES, listHtml, parseArgs, setTheme, openFile, ensureDir, rel } from './lib.mjs';

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const { filters, flags } = parseArgs();
const files = listHtml(DESIGN).filter((f) => !filters.length || filters.some((x) => rel(f).toLowerCase().includes(x)));
const reportPath = join(QA, 'a11y-report.md');

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();
const results = []; // { file, theme, violations, error }

try {
  for (const file of files) {
    for (const theme of THEMES) {
      try {
        await openFile(page, file);
        await setTheme(page, theme);
        const { violations } = await new AxeBuilder({ page }).withTags(TAGS).analyze();
        results.push({ file: rel(file), theme, violations });
      } catch (err) {
        results.push({ file: rel(file), theme, violations: [], error: err.message.split('\n')[0] });
      }
    }
  }
} finally {
  await browser.close();
}

const total = results.reduce((n, r) => n + r.violations.reduce((m, v) => m + v.nodes.length, 0), 0);
const failed = results.filter((r) => r.violations.length || r.error);
const lines = [
  '# Accessibility report',
  '',
  `Generated ${new Date().toISOString()} by \`npm run a11y\` (axe-core, tags: ${TAGS.join(', ')}).`,
  '',
  `**${files.length} file(s) × ${THEMES.length} themes — ${total} violating node(s) in ${failed.length} run(s).**`,
  '',
  '| File | Theme | Violations | Nodes |',
  '| --- | --- | --- | --- |',
  ...results.map((r) => `| ${r.file} | ${r.theme} | ${r.error ? 'ERROR' : r.violations.length} | ${r.violations.reduce((m, v) => m + v.nodes.length, 0)} |`),
  '',
];
for (const r of failed) {
  lines.push(`## ${r.file} (${r.theme})`, '');
  if (r.error) lines.push(`Error: ${r.error}`, '');
  for (const v of r.violations) {
    lines.push(`- **${v.id}** (${v.impact}): ${v.help} — ${v.helpUrl}`);
    for (const n of v.nodes.slice(0, 10)) lines.push(`  - \`${n.target.join(' ')}\` ${n.failureSummary?.split('\n').slice(1).join(' ').trim() ?? ''}`);
    if (v.nodes.length > 10) lines.push(`  - …and ${v.nodes.length - 10} more`);
  }
  lines.push('');
}
ensureDir(QA);
writeFileSync(reportPath, lines.join('\n'));

console.log(`a11y: ${files.length} file(s) × ${THEMES.length} themes, ${total} violating node(s) → ${rel(reportPath)}`);
for (const r of failed) console.log(`  ${r.file} [${r.theme}]: ${r.error ?? r.violations.map((v) => v.id).join(', ')}`);
process.exit(flags.strict && failed.length ? 1 : 0);
