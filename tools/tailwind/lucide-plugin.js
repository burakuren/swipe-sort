// Tailwind plugin: `i-lucide-<name>` renders a Lucide icon as a CSS mask filled with currentColor.
// Only icons actually used in /design are emitted (Tailwind JIT). HTML mockups only; the app
// will use lucide-react-native instead.
const { readdirSync, readFileSync } = require('node:fs');
const { join, dirname } = require('node:path');
const plugin = require('tailwindcss/plugin');

const iconsDir = join(dirname(require.resolve('lucide-static/package.json')), 'icons');

module.exports = plugin(({ addComponents }) => {
  const components = {};
  for (const file of readdirSync(iconsDir)) {
    if (!file.endsWith('.svg')) continue;
    const svg = readFileSync(join(iconsDir, file), 'utf8')
      .replace(/<!--[\s\S]*?-->/g, '')
      .replace(/\s+/g, ' ')
      .trim();
    const url = `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
    components[`.i-lucide-${file.slice(0, -4)}`] = {
      display: 'inline-block',
      flexShrink: '0',
      width: '1.5rem',
      height: '1.5rem',
      backgroundColor: 'currentColor',
      '-webkit-mask': `${url} no-repeat center / 100% 100%`,
      mask: `${url} no-repeat center / 100% 100%`,
    };
  }
  addComponents(components);
});
