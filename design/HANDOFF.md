# Handoff to the coding agent

You will build SwipeSort with **Expo, React Native and TypeScript**, styled with **NativeWind** and built
from **React Native Reusables** (RNR) components, plus a web build of the same app. This folder is the
complete design. You should never have to invent a screen, a flow or a feature behavior; you may only
fill in platform defaults listed in the brief's `<out_of_scope>` (system dialogs, status bars, safe areas,
backend, analytics, payments, translations).

## 1. What is the source of truth

| Question | Source of truth |
| --- | --- |
| How does it look? | `03-screens/Sxx-*.html` frames (visual reference) + `01-foundations/` |
| How does it behave? | `03-screens/Sxx-*.md` specs, `02-architecture/navigation-map.md`, `02-architecture/domain-model.md` |
| What exact words? | §6 "Copy" of each spec (every string, including errors) |
| Which values? | `01-foundations/tokens.json` (generated `tokens.ts`, `tokens.css`, `tailwind.config.js`) |
| How does it move? | `01-foundations/motion.md` and the working reference `04-prototype/swipe-demo.html` |
| Why was it decided? | `00-brief/assumptions.md` (A-nn IDs are cited in specs) |
| What must it satisfy? | `00-brief/requirements.md` (IDs) mapped in `05-qa/traceability.md` |

**The HTML is a visual reference, not code to port.** Do not copy its structure literally: frames, system
bars, `mock-*` classes, `phone`/`desktop` wrappers and the `:target` prototype mode exist only for
presentation. Build real screens from RNR components with NativeWind classes; most utility classes in the
mockups map 1:1 to NativeWind (same token names), which is the point.

## 2. Setup

1. Tokens: copy `01-foundations/tokens.css` variables into the app's `global.css` (`:root` and `.dark`) and
   use `01-foundations/tailwind.config.js` as the theme (add `presets: [require('nativewind/preset')]`,
   `content`, and `darkMode: 'class'`). Colors are `hsl(var(--token) / <alpha-value>)`, so `bg-accept/25`
   works.
2. `tokens.ts` gives the same values to Reanimated, gesture thresholds, StatusBar and navigation themes.
3. Font: Inter (`@expo-google-fonts/inter` on native, `@fontsource-variable/inter` on web), with
   `fontFeatureSettings: "cv11"` on web; on native the single-storey a is optional.
4. Icons: `lucide-react-native` (same names as the mockups' `i-lucide-*` classes).
5. Theme: System / Light / Dark setting (S06) drives NativeWind's color scheme.

## 3. Where to find things

- Screens: `03-screens/` — one HTML + one spec per screen ID S01–S40. Frame IDs (`S25-drag-accept`) name
  states; the spec's §4 table says what triggers each state.
- Components: `01-foundations/components.html` (every variant and state) and `components.md` (anatomy,
  props, accessibility, RNR mapping, custom components to build).
- Design rules: `01-foundations/design-principles.md` (surfaces, colors, decision language, copy rules).
- Navigation: `02-architecture/navigation-map.md` — expo-router structure, every connection, deep links
  (`https://swipesort.app/join/<token>` and list links), cross-screen frame IDs, the four main flows.
- Data and states: `02-architecture/domain-model.md` — entities, list status rules (Pending / Agreed /
  Conflict), conflict rules, bulk resolve, permissions per role, offline behavior.
- Sample data: `02-data/sample-data.json` (use it for seed/demo data and the "Try a sample list" feature).
- Motion: `01-foundations/motion.md`; reference implementation `04-prototype/swipe-demo.html` (vanilla JS;
  port the logic to `Gesture.Pan()` + Reanimated shared values).
- Brand: `01-foundations/brand/` — app icon (1024), Android adaptive icon layers (foreground, background,
  monochrome, 108 dp), logo marks, wordmarks, favicon.
- Prototype: `04-prototype/index.html` walks the four main flows.
- QA evidence: `05-qa/` (screenshots of every frame in light and dark, accessibility report, coverage,
  traceability, review report).

## 4. Build order

1. **Tokens and theme** (global.css, tailwind config, tokens.ts, fonts, icons, dark mode).
2. **Components**: RNR primitives first (Button, Input, Switch, Checkbox, RadioGroup, ToggleGroup, Tabs,
   Select, AlertDialog, Dialog, DropdownMenu, Avatar, Badge, Progress, Skeleton, Alert), then the custom
   ones in `components.md` (AppBar, BottomNav, ListGroup/rows, BottomSheet, Snackbar, DecisionButton,
   DecisionBadge, StatusBadge, MemberDecisions, ImportStepper, SourceTile, TemplateTile, EmptyState,
   ErrorState, OfflineBanner, CoachMark, Kbd).
3. **Sorting screen (S25)** with SwipeCard, CardStack, DecisionStamp: gestures, thresholds, haptics,
   undo, notes, coach marks, keyboard on web, accessibility actions, reduced motion. Match swipe-demo.html.
4. **Main flows**, in this order:
   1. First launch → onboarding → import contacts without an account → map fields → review duplicates →
      sort → round summary (S01, S02, S08, S11, S12, S13, S19, S20, S22 pick mode, S25, S27).
   2. Re-sort the Maybe pile → results → export to Google Sheets (S09, S24, S27, S28, S29, S39).
   3. Invite a partner → sign-in prompt → partner opens the link on the web → both sort → conflicts →
      Decision Maker bulk resolves → export (S05, S03, S31–S37, S39).
   4. Create a list from CSV with a custom template (S14, S19, S22, S23).
5. **Everything else**: settings and profile (S06, S07), list management (S10), remaining sources (S15–S18,
   S21), round history (S30), activity and notifications (S38), global patterns (S40).

## 5. Rules that are easy to get wrong

- **Terminology**: List, Item, Field, Source, Card template, Round, Accept/Reject/Maybe, Decided, My
  decision, Final decision, Conflict, Owner, Decision Maker, Collaborator, Member. Never show domain words
  ("guest", "invitee", "wedding") in UI strings; they appear only in sample data.
- **Decisions** always show icon + label + color; order Reject, Maybe, Accept everywhere.
- **Every gesture has a button and an accessibility action** (`accessibilityActions` on the card).
- **Data safety**: the original source is never modified automatically. Edits are stored as working-copy
  overrides with the original value kept (revertible). Google Sheets write-back only after the explicit
  confirmation in S39.
- **Guest mode**: the app works fully without an account for solo lists; sign-in is requested only for
  sharing and backup (S05), and existing device lists move to the account.
- **Web**: contacts import, photo gallery, haptics and push are unavailable — show them disabled with the
  reason and "Get the app" exactly as designed; keyboard hints only on web desktop.
- **Local first**: every decision, note and edit saves locally first; sync is invisible except for the
  offline banner and sync notice (S40).
- **Touch targets** ≥ 48 dp; text scales to 200% (see large-text frames).

## 6. Platform specifics

Android is the reference (Material 3 behavior: predictive back, bottom sheets, snackbars). iOS variant
frames (`*-ios`) show where iOS differs: navigation bars, back swipe, page sheets, action sheets, Sign in
with Apple. Web uses the same phone layout; desktop browsers center it (`S40-desktop-frame`).
