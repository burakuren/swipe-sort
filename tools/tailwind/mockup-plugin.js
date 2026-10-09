// Tailwind plugin for the HTML mockups only (injected by build-css.mjs, never part of the app config).
// Provides device frames, non-designed system bars, frame labels and the prototype `:target` mode.
//
//   <body class="mock-page">
//     <header class="mock-doc">…page title, links to spec…</header>
//     <main class="mock-canvas">
//       <figure class="frame" data-frame="S25-default" id="S25-default">
//         <figcaption class="frame-label">S25 · Default · <span class="theme-name"></span></figcaption>
//         <div class="phone">                       (.phone-ios for iOS, .desktop for desktop web)
//           <div class="sysbar-top" aria-hidden="true"><span>9:41</span><span class="sysbar-icons"></span></div>
//           <div class="screen">…the designed screen (flex column, fills the space between bars)…</div>
//           <div class="sysbar-nav" aria-hidden="true"></div>
//         </div>
//       </figure>
//     </main>
//   </body>
//
// Prototype mode: open any screen file with `#<frame-id>` and only that frame is shown, centered.
const plugin = require('tailwindcss/plugin');

const v = (name) => `hsl(var(--${name}))`;

module.exports = plugin(({ addComponents, addBase }) => {
  addBase({
    // Presentation-only colors (page canvas and device bezel); not app tokens.
    ':root': { '--mock-canvas': '220 12% 90%', '--mock-bezel': '220 10% 78%', '--mock-bezel-outer': '220 10% 84%' },
    '[data-theme="dark"]': { '--mock-canvas': '225 10% 4%', '--mock-bezel': '225 8% 24%', '--mock-bezel-outer': '225 8% 13%' },
    '.theme-name::after': { content: '"light"' },
    '[data-theme="dark"] .theme-name::after': { content: '"dark"' },
  });

  addComponents({
    '.mock-page': {
      minHeight: '100vh',
      backgroundColor: v('mock-canvas'),
      color: v('foreground'),
      fontFamily: '"Inter Variable", Inter, system-ui, sans-serif',
      padding: '40px',
    },
    '.mock-doc': {
      maxWidth: '72ch',
      marginBottom: '32px',
      lineHeight: '1.5',
      '& h1': { fontSize: '28px', lineHeight: '34px', fontWeight: '600', letterSpacing: '-0.01em', marginBottom: '8px' },
      '& p': { color: v('muted-foreground'), fontSize: '15px' },
      '& a': { color: v('primary'), textDecoration: 'underline', textUnderlineOffset: '3px' },
    },
    '.mock-section': {
      fontSize: '18px',
      lineHeight: '24px',
      fontWeight: '600',
      margin: '48px 0 16px',
      maxWidth: '72ch',
      '& + p': { color: v('muted-foreground'), fontSize: '15px', marginBottom: '16px', maxWidth: '72ch' },
    },
    '.mock-canvas': {
      display: 'flex',
      flexWrap: 'wrap',
      alignItems: 'flex-start',
      gap: '40px 32px',
    },
    '.frame': {
      display: 'flex',
      flexDirection: 'column',
      gap: '12px',
      padding: '12px',
      backgroundColor: v('mock-canvas'),
      color: v('foreground'),
      fontFamily: '"Inter Variable", Inter, system-ui, sans-serif',
    },
    '.frame-label': {
      fontSize: '13px',
      lineHeight: '18px',
      fontWeight: '500',
      color: v('muted-foreground'),
      maxWidth: '412px',
    },
    // Android reference frame: 412 × 915 dp
    '.phone, .phone-ios': {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      width: '412px',
      height: '915px',
      borderRadius: '28px',
      backgroundColor: v('background'),
      color: v('foreground'),
      outline: `1px solid ${v('mock-bezel')}`,
      boxShadow: `0 0 0 6px ${v('mock-bezel-outer')}`,
      isolation: 'isolate',
    },
    // iOS variant frame: 393 × 852 pt (iPhone 15/16)
    '.phone-ios': { width: '393px', height: '852px', borderRadius: '48px' },
    // Desktop browser viewport: phone layout centered, page background around it
    '.desktop': {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      width: '1280px',
      height: '800px',
      borderRadius: '12px',
      backgroundColor: v('muted'),
      color: v('foreground'),
      outline: `1px solid ${v('mock-bezel')}`,
      isolation: 'isolate',
    },
    '.desktop-chrome': {
      flex: 'none',
      height: '40px',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '0 16px',
      backgroundColor: v('secondary'),
      borderBottom: `1px solid ${v('border')}`,
      fontSize: '12px',
      color: v('muted-foreground'),
      '& .desktop-url': {
        flex: '1',
        maxWidth: '480px',
        margin: '0 auto',
        height: '26px',
        borderRadius: '13px',
        backgroundColor: v('background'),
        display: 'flex',
        alignItems: 'center',
        padding: '0 12px',
      },
    },
    // The phone layout column inside the desktop frame
    '.desktop-column': {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      width: '412px',
      flex: '1',
      minHeight: '0',
      margin: '0 auto',
      overflow: 'hidden',
      backgroundColor: v('background'),
      borderLeft: `1px solid ${v('border')}`,
      borderRight: `1px solid ${v('border')}`,
    },
    '.screen': {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      flex: '1',
      minHeight: '0',
      overflow: 'hidden',
    },
    // Not designed (out of scope): neutral placeholders for the OS bars
    '.sysbar-top': {
      flex: 'none',
      height: '28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      fontSize: '13px',
      fontWeight: '500',
      fontVariantNumeric: 'tabular-nums',
      color: v('foreground'),
      '& .sysbar-icons': {
        width: '44px',
        height: '10px',
        borderRadius: '3px',
        backgroundColor: 'currentColor',
        opacity: '0.7',
        WebkitMask: 'linear-gradient(90deg,#000 0 26%,transparent 26% 36%,#000 36% 62%,transparent 62% 72%,#000 72%)',
        mask: 'linear-gradient(90deg,#000 0 26%,transparent 26% 36%,#000 36% 62%,transparent 62% 72%,#000 72%)',
      },
    },
    '.phone-ios .sysbar-top': { height: '54px', padding: '8px 32px 0 40px', fontSize: '15px', fontWeight: '600' },
    '.sysbar-nav': {
      flex: 'none',
      height: '24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      '&::after': {
        content: '""',
        width: '108px',
        height: '4px',
        borderRadius: '2px',
        backgroundColor: v('foreground'),
        opacity: '0.45',
      },
    },
    '.phone-ios .sysbar-nav': { height: '34px', '&::after': { width: '134px', height: '5px', opacity: '0.85' } },

    // Prototype mode: `file.html#frame-id` shows that frame only, centered.
    'body:has([data-frame]:target) .mock-doc, body:has([data-frame]:target) .mock-section, body:has([data-frame]:target) .mock-section + p': {
      display: 'none',
    },
    'body:has([data-frame]:target) [data-frame]:not(:target)': { display: 'none' },
    'body:has([data-frame]:target) .mock-canvas': { justifyContent: 'center' },
    'body:has([data-frame]:target) .frame-label': { display: 'none' },
  });
});
