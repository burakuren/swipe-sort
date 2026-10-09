# Assumptions and decisions

Every decision the brief did not make, with the reason. Newest sections at the bottom. Subagent decisions
are merged here by the lead designer after each phase. IDs (A-nn) are referenced from specs.

## Process and tooling

- **A-01** `00-brief/brief.md` did not exist; it was written as a verbatim copy of the prompt.
- **A-02** Frame size: the brief's 412×915 Android frame overrides the 390×844 example in CLAUDE.md. iOS
  variants use 393×852 (iPhone 15/16). Desktop web frames are 1280×800 with the 412-wide phone column
  centered.
- **A-03** Status bar, navigation bar and safe areas are out of scope; frames show neutral, non-designed
  placeholder bars (`sysbar-top`, `sysbar-nav`) so layouts are judged at true size. Web frames have none.
- **A-04** Mockup-only CSS (frames, bars, labels, canvas colors, prototype mode) lives in
  `tools/tailwind/mockup-plugin.js`, never in the app's Tailwind config.
- **A-05** Prototype navigation uses the CSS `:target` rule: opening `Sxx-name.html#frame-id` shows only
  that frame. No JavaScript is needed for screen-to-screen links.
- **A-06** `tokens.json` is the single source; `npm run build:tokens` (run by `build:css`) generates
  `tokens.css`, `tokens.ts` and `contrast.md`. `tailwind.config.js` reads `tokens.json` directly.
- **A-07** Tailwind colors use `hsl(var(--token) / <alpha-value>)` so opacity modifiers work (NativeWind v4
  supports this form).
- **A-08** `build:css` inlines local `@import`s and writes atomically (temp file + rename) so parallel
  builds never leave a truncated stylesheet.
- **A-09** `npm run shots -- --dir=01-foundations` (or `04-explorations`) screenshots non-screen folders.
  Foundation frames use `DS-` and `C-` IDs.
- **A-10** Sample images are generated SVG illustrations (`tools/gen-images.mjs`): portraits, product
  objects, small landscapes. No text, no hotlinks. `02-data/sample-data.js` mirrors the JSON for scripts
  (file:// cannot `fetch` local JSON).
- **A-11** Foundations documentation pages (`design-system.html`, `components.html`) may use fixed
  demonstration widths (`w-[1040px]` etc.). Screen files may not use arbitrary values except those the
  mockup plugin provides.

## Visual system

- **A-12** One accent: **ink indigo** (`primary` 234 54% 45% light, 232 88% 76% dark). It stays clear of
  the three decision hues (green, rose, amber), reads as calm and trustworthy, and avoids the generic
  black-primary shadcn look. Confirmed or revised in Phase 2 (see A-40+).
- **A-13** Reject uses a calm, desaturated rose (354 46% 45%), distinct from `destructive` (0 70% 42%). Deleting
  data must feel more serious than rejecting an item.
- **A-14** Maybe amber is a light fill: amber surfaces always carry dark `maybe-foreground` text; text on
  neutral surfaces uses `maybe-soft-foreground`. The amber fill's low contrast against the page is accepted
  because it is never the only identifier (icon + label + its own dark content).
- **A-15** The list status Conflict uses an inverted neutral chip (`conflict` token) instead of a fourth hue,
  keeping color meaning limited to decisions. Agreed = outline chip, Pending = muted chip.
- **A-16** Surface hierarchy (see design-principles §3): groups 16 flat, tiles 16 with border, controls 12,
  sheets/dialogs 24, sort card 28 with the only deep resting shadow.
- **A-17** Added token `primary-inverse` (M3 inversePrimary) for actions on the inverse snackbar.
- **A-18** Added spacing `13` (52 dp) for the M3 switch track.
- **A-19** Inter stays the typeface (decision made in Phase 2, A-40+). Feature `cv11` (single-storey a) is on
  for a softer texture.
- **A-20** Logo: two cards, one set aside and one tilted right with a check. Wordmark SVGs use live Inter text;
  the production build should outline it.

## Product and behavior

- **A-21** Bottom navigation has three tabs: **Lists**, **Activity**, **Settings**. Templates are reached from a
  list (Card template) and from Settings › Card templates; a fourth tab would dilute the list-first app.
- **A-22** Import finish combines brief steps 5 and 6 ("Choose a card template" and "Name the list and start
  sorting") in one screen (S22 in pick mode: list name field + template choice + Start sorting). Fewer
  steps keeps first-decision time under a minute (SUC-04).
- **A-23** The duplicate step is skipped automatically when no duplicates are found (a short "No duplicates
  found" confirmation appears inside the finish step instead). S20 still has a `S20-none` frame for the
  case where the user navigates back.
- **A-24** Plain text import (S16) goes through field mapping with a single field so users can rename it
  ("Text" → "Book") and set its type; photos (S18) and manual entry (S17) skip mapping because their fields
  are fixed or defined inline.
- **A-25** List status **Conflict** appears as soon as two members disagree, even if others have not decided:
  it can no longer become Agreed. Under Majority, such items show "Waiting for 1 member" until everyone has
  decided.
- **A-26** Default conflict rule when a list is first shared: **Decision Maker decides**, with the Owner as
  Decision Maker. The Owner can switch the rule and move the Decision Maker at any time.
- **A-27** Bulk resolve is available only to the Decision Maker and only under rules that need one
  (Decision Maker decides; Majority ties).
- **A-28** One note per member per item. Notes on solo lists have no private option.
- **A-29** Undo history is kept per member per round and survives leaving and resuming the round.
- **A-30** Down-swipes never decide (the card follows with resistance and snaps back) so an attempt to scroll
  is never a decision.
- **A-31** All decisions use the same commit haptic (medium impact): calm and equal; Reject is not
  punished with a harsher feel.
- **A-32** Decision buttons show the running count under each button ("Reject 17") so counts sit where the
  decisions are made (final layout confirmed in Phase 2).
- **A-33** Results show the latest decision per item across rounds; round history keeps each round's
  results.
- **A-34** Starting a new round while one is in progress asks to end the current round (S40 dialog).
- **A-35** Guest lists are labeled "On this phone only" with a `cloud-off` icon (the not-backed-up indicator).
- **A-36** Invite links are reusable for any number of people, expire after 14 days and can be reset by the
  Owner. Invite roles: Collaborator, or Decision Maker (Owner only; moves the role).
- **A-37** Permissions per role are defined in `02-architecture/domain-model.md`.

## Sample data

- **A-38** "Today" in all mockups is Saturday, Oct 10, 2026. The signed-in user is **Deniz Yılmaz** (Owner of
  "Wedding guests"); partner **Mert Aydın** is the Decision Maker; **Selin Yılmaz** (Deniz's sister) is a
  Collaborator. Round 1 progress: Deniz 76/100 (48 Accept, 17 Reject, 11 Maybe), Mert 85/100, Selin 43/100.
  List status: 32 Agreed, 53 Pending, 15 Conflict, of which 3 are on items Mert never decided.
- **A-39** Products are priced in EUR; apartments in TRY. Names mix Turkish and international contacts to
  exercise Turkish characters and long names.

## Phase 2: sorting screen direction

- **A-40** Three directions were explored (`04-explorations/S25-direction-a|b|c.html`, screenshots
  `05-qa/screenshots/Xa-*`, `Xb-*`, `Xc-*`):
  - **A, Quiet deck** (chosen): ink indigo accent; a tall card with the image on top and fields below; large
    round decision buttons with labels and running counts; progress under the app bar.
  - **B, Immersive photo**: plum accent; photo fills the card with an info panel; floating unlabeled buttons;
    counts as chips. Rejected: it hides fields (most lists are text, not photos), the unlabeled buttons break
    the icon + label rule, and the card style only works for image-heavy templates (GOAL-02).
  - **C, Index card**: monochrome primary; dense form-like card; stat tiles; wide labeled pill buttons.
    Rejected: the card reads like a settings form (no bold moment, VIS-03), the stat tiles are the
    big-number template tell, and the near-black primary looks like stock shadcn (VIS-04).
  - A keeps boldness in the card (largest radius, deep shadow, tilt, tint and a rotated stamp) and stays
    calm around it. It works for every template: image area collapses for text-only lists.
- **A-41** Kept from the others: B's idea of a large image area (A uses 46% of the card for images);
  C's explicit labels (A puts labels and counts under every decision button).
- **A-42** Inter is kept (STK-09): its large x-height and tabular figures suit counts and dense fields;
  Turkish coverage is complete; it ships for React Native via `@expo-google-fonts/inter` and on the web via
  `@fontsource-variable/inter`. No alternative was clearly better for the calm direction.
- **A-43** The next card peeks 12 dp below the top card and is 12 dp narrower on each side, so the stack
  reads as a deck without stealing attention.
- **A-44** Sorting is a full-screen modal with a close (`x`) button; progress saves continuously so closing
  never asks. The overflow menu holds: Show others' decisions (shared lists), Card template, Show the
  tutorial again, End round.
- **A-45** After a member decides on a shared list with others' decisions hidden, a snackbar reveals a new
  conflict ("Mert chose Maybe. This is now a conflict.") — transparency after the unbiased decision.
