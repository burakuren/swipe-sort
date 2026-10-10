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

## Phase 3: Group A (S01–S07)

- **A-46** Before sign-in the device holds 4 lists (Wedding guests + the 3 in `me.guest.deviceLists`); S05 says "4 lists moved to your account". Lists move one at a time, starting with the list being shared; a list counts as moved only after server confirmation; the local copy stays usable. Moving into an account with lists adds them (same name gets " (2)").
- **A-47** Splash: Android SplashScreen API (static mark, wordmark as branding image); iOS launch screen shows the mark only; web loader only after 300 ms. An invite link at cold start skips onboarding (S32-app).
- **A-48** Onboarding demo uses 4 neutral cards (p02, ph09, p05, ph05); gestures in any order with a checklist; recap opens 700 ms after the third different gesture; no undo/notes/counts in the demo (coach marks teach those); Skip goes to S08-first-run.
- **A-49** Email sign-in and create-account are separate forms. Password: ≥ 8 characters with a number or symbol; live rules, errors on submit; lock after 5 wrong attempts in 15 minutes; no blocking email verification.
- **A-50** Password reset: same "sent" screen whether or not an account exists; links last 1 hour, single use; 60 s resend cooldown; reset signs out other devices.
- **A-51** Official Google "G" and native Apple buttons are the only non-token colors allowed (brand requirements); mockups use stand-ins.
- **A-52** Settings: Haptics is an inline switch; Appearance sub-page (System default, per device); Notifications: master push switch + six per-event switches (per account); on web the switches control the in-app Activity badge. Sign out removes backed-up lists from the phone; unsynced changes trigger a separate "Sign out anyway" dialog. Backup states: Backed up, Backing up…, Backup paused, Not backed up.
- **A-53** Profile: email read-only in v1; connected accounts are labeled "Sign-in methods"; the last sign-in method cannot be disconnected; re-authentication after 5 minutes for sensitive actions.
- **A-54** Account deletion: per owned shared list, transfer ownership (default: the Decision Maker) or delete for everyone; the person's decisions and notes are removed from shared lists; confirmation word "delete"; Apple token revoked; web deletion route `swipesort.app/account/delete` (Google Play requirement). Store links use `https://swipesort.app/get`.

## Phase 3: Group C1 (S11–S15)

- **A-55** The source grid is data-driven: each Source definition has name, icon, description, availableOn, needsConnection, needsPermission, selectStep, hasFieldMapping, webReplacement. `S11-new-source` shows a future "Calendar" tile. S11 has no loading/error state (static, local).
- **A-56** On web the Contacts tile stays visible but unavailable (sheet: "Get the app" or "Import a CSV instead"); Photos becomes "Upload photos". Offline, only Google Sheets is unavailable. "Get the app" links to `https://swipesort.app/get` (store redirect, QR on desktop).
- **A-57** Permission explainers sit at stepper step 2. The notifications explainer is a standalone modal shown once after a list is first shared or joined (not during joining), then only from Activity or Settings. Android has denied-once and don't-ask-again recovery; iOS goes to Settings. Denials use muted icons and no error haptic; every recovery offers an alternative (CSV for contacts, system photo picker for photos). Limited access designed for photos and iOS 18 contacts.
- **A-58** Contacts start all selected (the select step removes junk such as service numbers); the sample address book has 96 contacts (c001–c088 + 8 service numbers) → 88 imported. Search ignores accents and matches name, phone digits and email; Turkish collation; fast-scroll index above 200 contacts; max 10,000 contacts per import.
- **A-59** File limits: 20 MB, 10,000 rows, 50 columns per file or sheet; .csv/.tsv/.xlsx supported. Too many columns → "Choose columns" or "Continue with the first 50"; too many rows → import the first 10,000. Partial imports are caught at preview ("84 of 88 rows can be imported"), finishing with "Imported 84 of 88 items". At ≥150% text the preview table becomes a record view.
- **A-60** Several Excel sheets or Google tabs combine into one list with an automatic Tab/Sheet field. Google Sheets import uses read-only scopes; the write scope is requested at export. Connecting Google Sheets does not sign in to SwipeSort (works without an account). Web OAuth: popup on desktop (popup-blocked state), redirect on mobile.
- **A-61** Import chrome (all import screens): modal app bar "Import" / "New list" / "Add items", ImportStepper under it, primary h-14 at the bottom with a ghost secondary below it; iOS: first step `x` only, later steps "Back" + `x`. Closing with progress asks "Discard import?".

## Phase 3: Group C2 (S16–S21)

- **A-62** Step counts: contacts / CSV / Google Sheets 5; plain text 4 (duplicate lines handled on S16); manual entry 4 (Choose source, Set up fields, Add items, Finish); photos 3; Add items 5 ending with "Add to list". One import is capped at 5,000 items for text and photos (photos warn at 1,000+). A list has at most 50 fields.
- **A-63** Field detection: a type is chosen when ≥ 90% of non-empty values fit; the title is the first text field present in ≥ 90% of items; constant or ≥ 90%-empty fields start in a collapsed "Hidden by SwipeSort" group. Hiding the title field unsets it. Several phone numbers default to "All numbers in one field" (card shows first + "+1"); options "First number only", "One field per label".
- **A-64** Duplicates are detected after mapping. Merge / Keep both / Skip is a per-group radiogroup; unreviewed groups import as separate items (nothing lost by default). Merge combines multi-value fields and keeps the first record's other values unless changed.
- **A-65** Add items (S21): new columns default to "New field" (empty for existing items, not added to the card template); Merge fills empty fields of existing items and never overwrites edits; decisions and notes stay; identical rows default to Skip. Sample: mert-family.csv has 15 rows → 12 added (c089–c100), 1 skipped, 2 merged; the list grows from 88 to 100. New items join the current round, members get an activity event; "Added 12 items" has Undo.
- **A-66** Manual entry: item form is a sheet ("Add another" saves and stays; "Add item" saves and closes); deletes are immediate with Undo. Plain text has Text / Preview tabs; duplicate lines are kept unless "Remove duplicates". Photos are grouped by day in a 4-column grid; web uploads accept JPG/PNG/HEIC/WebP up to 25 MB and resume after going offline.

## Phase 3: Group E (S24, S26, S27)

- **A-67** On shared lists the Maybe and Accepted piles in S24 count final decisions; Pending/Conflict items are reachable through Custom selection (List status filter). Filters: AND across fields, OR within one; "My decision" and "List status" are pseudo-fields; hand-picking replaces filters. Sorting by a field puts empty values last.
- **A-68** Starting a round on a shared list needs a connection; solo lists work offline. Collaborators and the Decision Maker can "Suggest a round" ("Ask Deniz") → new activity event `roundRequested` for the Owner. Starting while a round is open asks "End Round 1 for everyone?". Start round replaces the modal with S25 and shows "Round 2 started".
- **A-69** Item detail over S25 is a bottom sheet (85% → full) with a pinned decide bar; from Results/Conflicts it is a pushed screen with a segmented "My decision" control (changes apply at once, "Changed to Maybe" + Undo). While sorting a shared list, others' decisions in S26 stay hidden until I decide that item.
- **A-70** Editing: one edit mode (Edit or tap a field), Cancel / Save changes; edited fields show "Edited" / "Edited by Mert", the original value and "Revert to original" (confirm + Undo). Missing values show "Add {field}" (editable) or "—" (read-only). Notes come before fields when present; others' private notes are never shown. Concurrent edits: last save wins with an inline "Keep mine / Use Mert's" choice.
- **A-71** Round summary: one orchestrated count-up (500 ms) with the success haptic; duration counts active time only (gaps over 5 min excluded), hidden on shared lists. Shared: the Decision Maker's primary action is "Review 15 conflicts", the Owner's is "Review results". An ended round can be continued until a new round starts. S27 is not kept in the back stack.
- **A-72** Illustrative numbers not in sample data: Frontend hiring Q4 round 1 = 4 accepted, 8 rejected, 0 maybe; Mert's finished Round 1 in S27-shared = 58 / 27 / 15; the solo Wedding guests summary (S27-default) = 62 accepted, 24 rejected, 14 maybe.
- **A-73** Sample data fix: Mert's decision on c079 is Accept (matches his note "Obviously yes."); Mert's Round 1 counts are 50 accepted, 21 rejected, 14 maybe.

## Phase 3: Group G1 (S31–S34)

- **A-74** Flow 3: Deniz invites Mert as Collaborator (preselected); later makes him Decision Maker in S34 (matches the activity data).
- **A-75** Invite links are per member (so S32 can say who invited you; refines A-36). The Owner can switch their own link to Decision Maker: only the first person to join with it becomes Decision Maker, later joins are Collaborators. Anyone can reset their own link; the Owner can turn off anyone's. Pending invites = active links (people who open without joining are not tracked). Expired links show "Create new link".
- **A-76** Decision Maker assignment (DM-10): a "Decision Maker" group on the Owner's members screen with one switch per member (at most one on), repeated in the member options sheet. A confirmation appears only when the role moves away from someone or is turned off while the rule needs one.
- **A-77** Member rows show the role as text with an icon (crown, gavel) instead of badges. A member who leaves keeps their decisions (they still count). Removing defaults to "Keep their decisions"; "Removed Selin" has Undo for 6 s. The Owner must transfer ownership before leaving ("Make Mert Owner and leave" / "… and stay").
- **A-78** Web: a signed-in person opening an invite skips the preview and joins (S33 shows "Joining as {name}" + "Switch account"). Dead links (expired, reset) name the sender but never show list contents; unknown links show nothing. "Share…" appears only where Web Share exists; desktop "Get the app" opens a QR dialog; iOS Safari uses the native Smart App Banner.
