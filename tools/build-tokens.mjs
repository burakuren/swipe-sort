// npm run build:tokens — design/01-foundations/tokens.json → tokens.css (shadcn CSS variables, light + dark)
// and tokens.ts (React Native). Also checks WCAG contrast for the pairs listed in tokens.json.
// --strict exits 1 when a pair is below its minimum.
import { readFileSync, writeFileSync, renameSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { DESIGN, parseArgs, rel } from './lib.mjs';

const { flags } = parseArgs();
const dir = join(DESIGN, '01-foundations');
const src = join(dir, 'tokens.json');
if (!existsSync(src)) {
  console.log(`build:tokens: ${rel(src)} not found — nothing to do`);
  process.exit(0);
}
const t = JSON.parse(readFileSync(src, 'utf8'));
const atomic = (path, text) => {
  const tmp = `${path}.${process.pid}.tmp`;
  writeFileSync(tmp, text);
  renameSync(tmp, path);
};

// ---------- contrast ----------
function hslToRgb(str) {
  const [h, s, l] = str.split(/\s+/).map((x) => parseFloat(x));
  const S = s / 100, L = l / 100;
  const k = (n) => (n + h / 30) % 12;
  const a = S * Math.min(L, 1 - L);
  const f = (n) => L - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return [f(0), f(8), f(4)];
}
const lum = (rgb) => {
  const [r, g, b] = rgb.map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => {
  const [x, y] = [lum(hslToRgb(a)), lum(hslToRgb(b))].sort((m, n) => n - m);
  return (x + 0.05) / (y + 0.05);
};
const hex = (str) => '#' + hslToRgb(str).map((c) => Math.round(c * 255).toString(16).padStart(2, '0')).join('');

const failures = [];
const contrastRows = [];
for (const theme of ['light', 'dark']) {
  const c = t.color[theme];
  for (const [fg, bg, min] of t.contrastPairs) {
    const r = ratio(c[fg], c[bg]);
    contrastRows.push({ theme, fg, bg, min, r });
    if (r < min) failures.push(`${theme}: ${fg} on ${bg} = ${r.toFixed(2)} (min ${min})`);
  }
}

// ---------- tokens.css ----------
const header = '/* Generated from tokens.json by `npm run build:tokens` — do not edit by hand. */\n';
const block = (sel, vars) => `${sel} {\n${vars.map(([k, v]) => `  --${k}: ${v};`).join('\n')}\n}\n`;
const lightVars = [
  ...Object.entries(t.color.light),
  ['radius', `${t.radius.base}px`],
  ...Object.entries(t.elevation.light).map(([k, v]) => [`shadow-${k}`, v]),
];
const darkVars = [
  ...Object.entries(t.color.dark),
  ...Object.entries(t.elevation.dark).map(([k, v]) => [`shadow-${k}`, v]),
];
const css =
  header +
  '/* Light is the default. Dark applies with data-theme="dark" (mockups) or the .dark class (NativeWind). */\n' +
  block(':root', lightVars) +
  '\n' +
  block('[data-theme="dark"],\n.dark', darkVars) +
  '\n[data-theme="dark"], .dark { color-scheme: dark; }\n';
atomic(join(dir, 'tokens.css'), css);

// ---------- tokens.ts ----------
// RN shadows: [offsetY, radius, opacity, androidElevation] per role, approximating the CSS shadows.
const rnShadow = {
  raised: [1, 2, 0.06, 1],
  overlay: [4, 12, 0.12, 4],
  sheet: [-6, 20, 0.14, 8],
  hero: [12, 28, 0.2, 10],
  'hero-drag': [24, 44, 0.3, 16],
  dialog: [16, 40, 0.3, 12],
};
const camel = (s) => s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
const colorsTs = (theme) =>
  Object.fromEntries(Object.entries(t.color[theme]).map(([k, v]) => [camel(k), `hsl(${v.split(' ').join(', ')})`]));
const fontSize = Object.fromEntries(
  Object.entries(t.font.size)
    .filter(([k]) => !k.startsWith('$'))
    .map(([k, [size, lineHeight, ls, weight]]) => [camel(k), { fontSize: size, lineHeight, letterSpacing: +(ls * size).toFixed(2), fontWeight: String(weight) }]),
);
const strip = (o) => JSON.parse(JSON.stringify(o, (k, v) => (k.startsWith('$') ? undefined : v)));
const ts = `// Generated from tokens.json by \`npm run build:tokens\` — do not edit by hand.
// React Native tokens. NativeWind classes cover most styling; use these for Reanimated, gesture
// thresholds, StatusBar/navigation theming and anything outside className.

export const colors = {
  light: ${JSON.stringify(colorsTs('light'), null, 2).replace(/\n/g, '\n  ')},
  dark: ${JSON.stringify(colorsTs('dark'), null, 2).replace(/\n/g, '\n  ')},
} as const;

export const radius = ${JSON.stringify(strip(t.radius), null, 2)} as const;

export const spacing = ${JSON.stringify(strip(t.spacing), null, 2)} as const;

export const fontFamily = { sans: '${t.font.family.native}' } as const;

export const typography = ${JSON.stringify(fontSize, null, 2)} as const;

/** iOS shadow props + Android elevation per role. */
export const shadows = ${JSON.stringify(
  Object.fromEntries(
    Object.entries(rnShadow).map(([k, [y, r, o, e]]) => [camel(k), { shadowColor: '#0F172A', shadowOffset: { width: 0, height: y }, shadowRadius: r, shadowOpacity: o, elevation: e }]),
  ),
  null,
  2,
)} as const;

export const motion = ${JSON.stringify(strip(t.motion), null, 2)} as const;

export const size = ${JSON.stringify(strip(t.size), null, 2)} as const;

export type ThemeName = keyof typeof colors;
export type ColorToken = keyof typeof colors.light;
`;
atomic(join(dir, 'tokens.ts'), ts);

// ---------- contrast report (design-system.html reads nothing; this is for humans) ----------
const md = [
  '# Token contrast',
  '',
  'Generated by `npm run build:tokens`. Ratios are WCAG 2.x contrast ratios.',
  '',
  '| Theme | Foreground | Background | Ratio | Minimum | Pass |',
  '| --- | --- | --- | --- | --- | --- |',
  ...contrastRows.map((r) => `| ${r.theme} | ${r.fg} | ${r.bg} | ${r.r.toFixed(2)} | ${r.min} | ${r.r >= r.min ? 'yes' : '**no**'} |`),
  '',
  '## Hex reference',
  '',
  '| Token | Light | Dark |',
  '| --- | --- | --- |',
  ...Object.keys(t.color.light).map((k) => `| ${k} | ${hex(t.color.light[k])} | ${hex(t.color.dark[k])} |`),
  '',
].join('\n');
atomic(join(dir, 'contrast.md'), md);

console.log(`build:tokens OK → tokens.css, tokens.ts, contrast.md (${contrastRows.length} pairs checked)`);
for (const f of failures) console.warn(`  contrast FAIL ${f}`);
if (failures.length && flags.strict) process.exit(1);
