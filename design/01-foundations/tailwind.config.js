// SwipeSort Tailwind theme (Tailwind 3, CommonJS, theme only) — shared by the HTML mockups and the
// Expo app. In the app add `presets: [require('nativewind/preset')]`, `content`, and
// `darkMode: 'class'`; the mockup build adds its own content glob and data-theme dark selector.
// Values mirror tokens.json; colors resolve to the CSS variables in tokens.css.
const tokens = require('./tokens.json');

const color = (name) => `hsl(var(--${name}) / <alpha-value>)`;
const colorNames = Object.keys(tokens.color.light);
const colors = Object.fromEntries(colorNames.map((n) => [n, color(n)]));

// Group into shadcn-style nested objects: { primary: { DEFAULT, foreground, soft, 'soft-foreground' } }
const nested = {};
for (const n of colorNames) {
  const m = n.match(/^(primary|secondary|muted|accent|destructive|card|popover|accept|reject|maybe|conflict)(?:-(.+))?$/);
  if (!m) { nested[n] = colors[n]; continue; }
  const [, base, sub] = m;
  nested[base] = nested[base] || {};
  nested[base][sub || 'DEFAULT'] = colors[n];
}

const px = (n) => `${n}px`;
const r = tokens.radius;
const fontSize = Object.fromEntries(
  Object.entries(tokens.font.size)
    .filter(([k]) => !k.startsWith('$'))
    .map(([k, [size, lh, ls, weight]]) => [k, [px(size), { lineHeight: px(lh), letterSpacing: `${ls}em`, fontWeight: String(weight) }]]),
);

/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: nested,
      fontFamily: {
        sans: tokens.font.family.sans.map((f) => (f.includes(' ') ? `"${f}"` : f)),
      },
      fontSize,
      borderRadius: {
        // shadcn base scale (React Native Reusables components use these)
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
        // SwipeSort hierarchy
        xs: px(r.xs),
        control: px(r.control),
        tile: px(r.tile),
        group: px(r.group),
        sheet: px(r.sheet),
        dialog: px(r.dialog),
        hero: px(r.hero),
      },
      boxShadow: {
        raised: 'var(--shadow-raised)',
        overlay: 'var(--shadow-overlay)',
        sheet: 'var(--shadow-sheet)',
        hero: 'var(--shadow-hero)',
        'hero-drag': 'var(--shadow-hero-drag)',
        dialog: 'var(--shadow-dialog)',
      },
      spacing: {
        13: '52px', // M3 switch track width
        gutter: px(tokens.spacing.gutter),
        section: px(tokens.spacing.section),
        touch: px(tokens.spacing.touch),
        'app-bar': px(tokens.spacing.appBar),
        'bottom-nav': px(tokens.spacing.bottomNav),
      },
      minHeight: { touch: px(tokens.spacing.touch) },
      minWidth: { touch: px(tokens.spacing.touch) },
      maxWidth: { card: px(tokens.size.cardMaxWidth), prose: '64ch' },
      transitionDuration: Object.fromEntries(Object.entries(tokens.motion.duration).map(([k, v]) => [k, `${v}ms`])),
      transitionTimingFunction: Object.fromEntries(
        Object.entries(tokens.motion.easing).map(([k, v]) => [k, `cubic-bezier(${v.join(', ')})`]),
      ),
    },
  },
  plugins: [],
};
