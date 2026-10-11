# SwipeSort design

SwipeSort turns any list into a deck of cards you sort with swipes: right to **Accept**, left to **Reject**,
up for **Maybe**, alone or with others. This folder is the complete, implementation-ready design: every
screen, every state, light and dark, Android first with iOS and web variants.

## Start here

1. **See it work**: open `04-prototype/index.html` in a browser. It walks the four main flows end to end;
   `04-prototype/swipe-demo.html` is the live sorting interaction (touch, mouse, keyboard).
2. **See the heart of the product**: `03-screens/S25-sorting.html` (the sorting screen, 38 frames) and its
   spec `S25-sorting.md`.
3. **See the visual system**: `01-foundations/design-system.html` and `components.html`.
4. **Building it?** Read `HANDOFF.md`.

Everything opens offline from the file system; no server or internet needed. After changing any HTML,
run `npm run build:css` (see `/CLAUDE.md` for all scripts).

## Folder map

| Path | What it is |
| --- | --- |
| `00-brief/brief.md` | The client brief, verbatim |
| `00-brief/requirements.md` | Every requirement with an ID (GOAL, PLT, SRT, DM, COL…) |
| `00-brief/assumptions.md` | Every decision the brief didn't make (A-01…), with reasons |
| `01-foundations/design-principles.md` | The rules every screen follows: surfaces, color, decision language, copy, accessibility, template tells to avoid |
| `01-foundations/tokens.json` | Single source of truth for tokens → generates `tokens.css`, `tokens.ts`, `contrast.md` |
| `01-foundations/tailwind.config.js` | Tailwind 3 theme mapped to the tokens, usable by NativeWind |
| `01-foundations/design-system.html` | Colors, type, spacing, radii, elevation, icons, text expansion, brand |
| `01-foundations/components.html` / `components.md` | Every component in every variant and state; specs mapped to React Native Reusables, plus components promoted from the screens |
| `01-foundations/motion.md` | Gesture thresholds, velocities, timings, easing, haptics, reduced motion |
| `01-foundations/brand/` | Logo mark, wordmark, app icon, Android adaptive icon layers |
| `02-architecture/navigation-map.md` | Every screen, how screens connect, tabs/stacks/modals, deep links, the four flows |
| `02-architecture/domain-model.md` | Lists, items, fields, sources, templates, rounds, decisions, notes, members, statuses, permissions |
| `02-data/sample-data.json` | Shared sample data (100 contacts, 20 products, 30 trip places, shared-list decisions) + generated images |
| `03-screens/Sxx-name.html` / `.md` | 40 screens: all frames side by side, and a 9-part spec each |
| `04-explorations/` | The three sorting-screen directions explored (A chosen; B and C kept) |
| `04-prototype/` | Clickable prototype and the live swipe demo |
| `05-qa/` | Screenshots of every frame (light + dark), accessibility report, lint report, coverage, traceability, QA review |

## Screens

| Group | Screens |
| --- | --- |
| A. Onboarding and account | S01 Splash, S02 Onboarding, S03 Sign in, S04 Forgot password, S05 Sign-in prompt, S06 Settings, S07 Profile |
| B. Lists | S08 Home, S09 List overview, S10 List management |
| C. Import | S11 Source picker, S12 Permissions, S13 Contacts, S14 File, S15 Google Sheets, S16 Plain text, S17 Manual entry, S18 Photos (out of scope, D-32), S19 Field mapping, S20 Duplicates, S21 Add items |
| D. Templates | S22 Template library, S23 Template editor |
| E. Sorting | S24 Start a round, S25 Sorting, S26 Item detail, S27 Round summary |
| F. Results | S28 Results, S29 Filter and sort, S30 Round history |
| G. Collaboration | S31 Invite, S32 Invite link, S33 Join, S34 Members, S35 Conflict rule, S36 Conflicts, S37 Bulk resolve, S38 Activity |
| H. Export | S39 Export |
| I. Global patterns | S40 Dialogs, snackbars, banners, errors, desktop frame |

## How to read a screen file

- Each phone is a **frame** labeled "S25 · State · light|dark". Frame IDs (`S25-drag-accept`) are stable
  names used in specs, links and screenshots (`05-qa/screenshots/S25-drag-accept.dark.png`).
- Android frames are 412 × 915; iOS variants (`-ios`) 393 × 852; web desktop frames show the phone layout
  centered in a browser window.
- Switch the whole page to dark mode by setting `data-theme="dark"` on `<html>`.
- Open a file with `#frame-id` (for example `S25-sorting.html#S25-default`) to see that frame alone — the
  prototype uses this.
- Status bars and system navigation are neutral placeholders (out of scope).

## Regenerating

Screen HTML is produced by small generators in `/tools/generators` (`npm run build:screens` runs them all,
in the right order). Tokens: `npm run build:tokens`. Sample data mirror for scripts: `npm run build:data`.
QA: `npm run qa` (CSS, screenshots, accessibility, flow tests, lint).
