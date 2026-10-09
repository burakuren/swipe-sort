# Requirements

Every requirement in `brief.md`, with an ID. IDs are stable: never renumber; add new ones at the end of
a section. `05-qa/traceability.md` maps each ID to the screens and documents that satisfy it.

ID prefixes: GOAL design goals · PLT platforms · STK design stack · VIS visual direction · TERM terminology ·
DM decision model · ACC accounts · SRC data sources and import · TPL card templates · RND rounds ·
SRT sorting screen · SAFE data safety · RES results · COL collaboration · EXP export · SET settings ·
BRD branding · SCR screens · OUT out of scope · SMP sample data · DEL deliverables · PRC process ·
SUC success criteria.

## Design goals

- **GOAL-01** Sorting feels effortless and satisfying; the sorting screen gets the most craft.
- **GOAL-02** The app works for any kind of list, not only guests.
- **GOAL-03** Users never fear losing or damaging their data.
- **GOAL-04** Group decisions are fair and transparent; disagreements are easy to resolve.
- **GOAL-05** The design scales: new data sources and features fit without redesign.
- **GOAL-06** When goals conflict, the higher-priority goal wins (order GOAL-01 → GOAL-05).

## Platforms

- **PLT-01** Android phones first: every screen is designed in an Android phone frame of 412×915.
- **PLT-02** iPhone support: where iOS differs meaningfully (navigation, back gesture, sheets, sign-in options) an iOS variant frame exists and the spec describes the difference.
- **PLT-03** Web app on mobile browsers uses the same phone layout.
- **PLT-04** Desktop browsers show the phone layout centered on the page; no wide layouts.
- **PLT-05** On desktop web, arrow keys sort: Right = Accept, Left = Reject, Up = Maybe, Z = Undo.
- **PLT-06** Keyboard hints are shown only on web.
- **PLT-07** Phone contacts import is unavailable on web: disabled state, short explanation, link to get the Android or iOS app.
- **PLT-08** The photo gallery picker is unavailable on web; web uses photo file upload instead.
- **PLT-09** Haptics are unavailable on web (design states how the haptics setting appears on web).
- **PLT-10** Push notifications are unavailable on web; web uses in-app notifications.
- **PLT-11** Every web-unavailable feature appears as a disabled state with a short explanation and a link to get the Android or iOS app.
- **PLT-12** Phones only: no tablet or desktop layouts.
- **PLT-13** WCAG 2.1 AA contrast everywhere.
- **PLT-14** Minimum touch target 48×48 dp.
- **PLT-15** Screen reader labels for all controls.
- **PLT-16** Support for large text sizes (layouts reflow; demonstrated in mockups).
- **PLT-17** A reduced-motion alternative for every animation.
- **PLT-18** Every swipe has a visible button equivalent.
- **PLT-19** Every swipe has a screen-reader action.
- **PLT-20** Copy is English only.
- **PLT-21** Layouts tolerate text 30–40% longer (Turkish first).
- **PLT-22** No text inside images.
- **PLT-23** Light and dark mode for every screen.

## Design stack

- **STK-01** shadcn/ui visual language: neutral, clean, token-driven, one accent color.
- **STK-02** Components named and structured like React Native Reusables; missing ones designed in the same style.
- **STK-03** Mockups use Tailwind utility classes mirroring NativeWind.
- **STK-04** CSS-variable tokens in shadcn convention (background, foreground, primary, muted, accent, destructive, border, ring…).
- **STK-05** SwipeSort tokens for Accept, Reject and Maybe extend the shadcn set.
- **STK-06** Material 3 guides Android behavior (navigation, back, bottom sheets, snackbars, system bars).
- **STK-07** Apple HIG guides iOS differences.
- **STK-08** Icons are Lucide.
- **STK-09** Typography: Inter by default; an alternative open-licensed sans-serif only if clearly better, supporting ğ, ş, ı, İ, available for React Native and web; the choice is documented.
- **STK-10** Motion follows Material 3 durations and easing.
- **STK-11** Gesture and motion values are specified in terms usable by react-native-gesture-handler and Reanimated.

## Visual direction

- **VIS-01** Calm and clean: generous whitespace, restrained color, clear hierarchy, quiet surfaces, one accent color.
- **VIS-02** Cards and user content are the stars; the interface steps back.
- **VIS-03** Boldness is spent in one place: the card and the moment of swiping it.
- **VIS-04** Avoid the stock component-kit look.
- **VIS-05** Corner radius and elevation vary with hierarchy; the sorting card is not styled like a settings row.
- **VIS-06** Surfaces are not all identical rounded cards with the same soft shadow.
- **VIS-07** No decorative gradients.
- **VIS-08** Decision colors: green Accept, red Reject, amber Maybe.
- **VIS-09** Decision colors always paired with an icon (check, cross, question mark) and a label; color is never the only signal.
- **VIS-10** Reject red is calm, not alarming.
- **VIS-11** Copy uses plain verbs, sentence case, no filler.
- **VIS-12** An action keeps the same name through its whole flow (Export → Exported).
- **VIS-13** Errors say what happened and how to fix it, without apologizing.
- **VIS-14** Empty screens invite the next action.
- **VIS-15** Explore two or three sorting-screen variations (accent, card style, density, type), pick one, keep the others, document the reasoning in assumptions.md.

## Terminology

- **TERM-01** The UI and specs use exactly: List, Item, Field, Source, Card template, Round, Decisions (Accept, Reject, Maybe), Decided, My decision, Final decision, Conflict, Owner, Decision Maker, Collaborator, Member.
- **TERM-02** Never use domain-specific words such as "guest" or "invitee" for items in the UI.
- **TERM-03** Domain language appears only in sample data and template names.

## Decision model

- **DM-01** Solo list: my decision is the final decision.
- **DM-02** Shared list: every member decides every item independently.
- **DM-03** List status Pending: not every member has decided the item yet.
- **DM-04** List status Agreed: every member chose the same decision; it becomes the final decision.
- **DM-05** List status Conflict: members chose differently (Maybe vs. Accept counts as a difference).
- **DM-06** The Owner chooses the conflict rule.
- **DM-07** Rule "Everyone must agree": conflicts stay open until members change decisions to match; members can review conflicts and see others' decisions.
- **DM-08** Rule "Majority decides": majority becomes final; ties go to the Decision Maker, or stay as conflicts if there is none.
- **DM-09** Rule "Decision Maker decides": every conflict is resolved by the Decision Maker, whose resolution is final.
- **DM-10** The Owner assigns the Decision Maker role to any member (including themselves) with a single switch on the members screen.
- **DM-11** Bulk resolve: the Decision Maker applies their own earlier decisions to all open conflicts in the current round in one action.
- **DM-12** Bulk resolve leaves conflicts on items the Decision Maker never decided open; the confirmation summary shows how many.
- **DM-13** While sorting, show the user's own progress ("76 / 100 decided") and counts per decision.
- **DM-14** On shared lists, the list overview shows list progress: Agreed, Pending and Conflict counts.
- **DM-15** Rounds on shared lists are started by the Owner and apply to every member.
- **DM-16** A member who joins mid-round sorts all items of the current round.
- **DM-17** When a member is removed, the Owner chooses in the confirmation dialog whether to keep or discard that member's decisions.
- **DM-18** Notes are visible to all members by default.
- **DM-19** A note can be marked private; private notes are visibly distinguished.
- **DM-20** The decision model is visible and consistent across all screens.

## Accounts

- **ACC-01** No account is needed to use the app alone.
- **ACC-02** Guest lists are stored on the device; a subtle indicator shows they are not backed up.
- **ACC-03** Signing in is required to share a list or back up lists.
- **ACC-04** When a guest tries to share or back up, a sign-in prompt explains why.
- **ACC-05** After sign-in, the guest's existing lists move to the account.
- **ACC-06** Sign in with Google on all platforms.
- **ACC-07** Sign in with email on all platforms (sign up and sign in).
- **ACC-08** Sign in with Apple on iOS.
- **ACC-09** Forgot password flow.

## Data sources and import

- **SRC-01** Sources at launch: phone contacts, CSV, Excel (.xlsx), plain text (paste or .txt, one item per line), manual entry, Google Sheets, photos (each photo becomes a card).
- **SRC-02** Web availability follows PLT-07/PLT-08 for contacts and photos.
- **SRC-03** The source picker is a modular pattern (grid of source tiles) where a new source is one more tile reusing the same import steps.
- **SRC-04** Import step 1: choose a source.
- **SRC-05** A pre-permission screen explains why access is needed and how data is used before any system permission prompt (contacts, photos).
- **SRC-06** Permission-denied recovery state.
- **SRC-07** Import step 2: select items — search and multi-select contacts, pick a file or a sheet tab, select photos.
- **SRC-08** Import step 3: map fields — detected fields with sample values.
- **SRC-09** Field mapping: rename fields.
- **SRC-10** Field mapping: hide fields.
- **SRC-11** Field mapping: set field type (text, number, phone, email, date, link, image).
- **SRC-12** Field mapping: choose the title field.
- **SRC-13** Field mapping: handle multi-value fields (e.g. several phone numbers).
- **SRC-14** Import step 4: review duplicates (common when combining sources).
- **SRC-15** Duplicate actions: merge, keep both or skip.
- **SRC-16** Import step 5: choose a card template.
- **SRC-17** Import step 6: name the list and start sorting.
- **SRC-18** A list can combine several sources.
- **SRC-19** Items can be added to an existing list later.
- **SRC-20** Import error: unreadable file.
- **SRC-21** Import error: empty file.
- **SRC-22** Import error: too many columns.
- **SRC-23** Import error: Google connection failure.
- **SRC-24** Import error: partial import.

## Card templates

- **TPL-01** Library of ready-made templates: Person, Product, Photo, Task, Candidate, Generic.
- **TPL-02** Template editor: choose which fields appear.
- **TPL-03** Template editor: arrange the layout (title, subtitle, image area, field rows, tags).
- **TPL-04** Fonts and colors are not customizable in this version.
- **TPL-05** Live preview uses real items from the current list.
- **TPL-06** Preview shows how the card handles missing values.
- **TPL-07** Preview shows how the card handles very long text.
- **TPL-08** Custom templates can be saved.
- **TPL-09** Custom templates can be renamed.
- **TPL-10** Custom templates can be duplicated.
- **TPL-11** Custom templates can be deleted.
- **TPL-12** Custom templates can be reused across lists.
- **TPL-13** A list's template can be changed at any time.

## Rounds

- **RND-01** Starting a round: choose items — all, the Maybe pile, accepted items to narrow down, or a custom selection (e.g. filtered by a field).
- **RND-02** Starting a round: choose card order — original, shuffled, or sorted by a field.
- **RND-03** Round history per list with each round's results.

## Sorting screen

- **SRT-01** Card stack: current card on top, next card visible behind it.
- **SRT-02** Gestures: swipe right = Accept, left = Reject, up = Maybe.
- **SRT-03** While dragging, show the pending decision with card tilt, color tint, icon and label.
- **SRT-04** The decision commits only past a threshold; releasing earlier snaps the card back.
- **SRT-05** Commit with haptic feedback.
- **SRT-06** Thresholds, velocities and animation timings are specified in the motion spec.
- **SRT-07** Visible Reject, Maybe, Accept and Undo buttons.
- **SRT-08** Undo the last decision at any time; multiple undos step back in order.
- **SRT-09** Always-visible progress ("76 / 100 decided") plus a compact count per decision.
- **SRT-10** Add or edit a note on the current card without leaving the screen.
- **SRT-11** Tap a card to open item details and edit fields on the spot.
- **SRT-12** Shared lists: a member can choose to see others' decisions on the card before deciding; off by default.
- **SRT-13** Progress saves automatically; leaving and resuming returns exactly to where the user stopped.
- **SRT-14** Sorting works offline and syncs later.
- **SRT-15** First-time coach marks teach the gestures.
- **SRT-16** End-of-round summary with next actions: review results, re-sort Maybe, start a new round, export.
- **SRT-17** Web version with keyboard hints (see PLT-05/06).

## Data safety

- **SAFE-01** The original source is never changed automatically.
- **SAFE-02** Edits and notes live in SwipeSort's working copy.
- **SAFE-03** Edited fields are visibly marked.
- **SAFE-04** Edited fields can be reverted to the original value.
- **SAFE-05** Export option: a new file with added "Decision" and "Notes" columns.
- **SAFE-06** Google Sheets export option: new columns in the original sheet or a new tab, only after explicit confirmation.

## Results

- **RES-01** Results segments: Accept, Reject, Maybe and Conflicts, each with counts.
- **RES-02** Each segment has search.
- **RES-03** Each segment has filters.
- **RES-04** Each segment has sorting.
- **RES-05** Shared lists: toggle between final decisions and my decisions.
- **RES-06** Any decision can be changed from results.

## Collaboration

- **COL-01** Invite any number of people via link or the system share sheet.
- **COL-02** Set the invitee's role while inviting.
- **COL-03** Invite link opens in the app if installed on Android or iOS.
- **COL-04** Otherwise the link opens in the web app, where the person can sign in, join and sort right away without installing.
- **COL-05** The web app offers an option to get the app.
- **COL-06** Joining shows who invited you, the list, your role, and a way to start sorting.
- **COL-07** Members screen: each member's progress.
- **COL-08** Members screen: change roles.
- **COL-09** Members screen: assign the Decision Maker.
- **COL-10** Members screen: remove a member.
- **COL-11** Members screen: transfer ownership.
- **COL-12** Members screen: leave a list.
- **COL-13** Conflict rule settings.
- **COL-14** One-by-one conflict resolution: swipe through conflicts with each member's decision and notes on the card.
- **COL-15** Bulk resolve with confirmation and summary.
- **COL-16** Every item shows who decided what.
- **COL-17** Activity feed and notifications for: someone joined.
- **COL-18** … someone finished sorting.
- **COL-19** … new conflicts.
- **COL-20** … conflicts resolved.
- **COL-21** … a new round started.
- **COL-22** … a role changed.
- **COL-23** Notification preferences.
- **COL-24** Pre-permission screen for push notifications.

## Export

- **EXP-01** Export to CSV.
- **EXP-02** Export to Excel.
- **EXP-03** Export to Google Sheets.
- **EXP-04** Share a plain-text summary.
- **EXP-05** Export everything or only Accept, Reject, Maybe or Conflict items.
- **EXP-06** Include decisions and notes.
- **EXP-07** Shared lists: include each member's decision.
- **EXP-08** Export success state.
- **EXP-09** Export failure state.
- **EXP-10** Google write confirmation.

## Settings

- **SET-01** Profile.
- **SET-02** Connected accounts (Google).
- **SET-03** Backup status.
- **SET-04** Theme: system, light, dark.
- **SET-05** Haptics.
- **SET-06** Notification preferences.
- **SET-07** Language (English only for now).
- **SET-08** Privacy information.
- **SET-09** Help and feedback.
- **SET-10** About.
- **SET-11** Sign out.
- **SET-12** Account deletion (required by both app stores).

## Branding

- **BRD-01** Simple logo.
- **BRD-02** Wordmark.
- **BRD-03** App icon.
- **BRD-04** Android adaptive icon.
- **BRD-05** Brand assets work at small sizes and in light and dark contexts.

## Screens

Every screen is designed with all applicable states: default, empty, loading, error, offline, web-unavailable
where relevant, and screen-specific states named in the features (**SCR-00**).

- **SCR-01** S01 Splash
- **SCR-02** S02 Onboarding with an interactive gesture demo
- **SCR-03** S03 Sign up / sign in (Google, email; Apple on iOS)
- **SCR-04** S04 Forgot password
- **SCR-05** S05 Sign-in prompt from guest mode (sharing or backup) and moving lists to the account
- **SCR-06** S06 Settings and all its sub-pages
- **SCR-07** S07 Profile, connected accounts and account deletion
- **SCR-08** S08 Home (first-run empty state with a sample-list option, not-backed-up indicator)
- **SCR-09** S09 List overview (solo and shared variants)
- **SCR-10** S10 List management: rename, duplicate, archive, delete, leave; archived lists
- **SCR-11** S11 Source picker (including web-unavailable tiles)
- **SCR-12** S12 Pre-permission explainers (contacts, photos, notifications) and permission-denied recovery
- **SCR-13** S13 Contacts import
- **SCR-14** S14 File import (CSV and Excel)
- **SCR-15** S15 Google Sheets connection and sheet/tab selection
- **SCR-16** S16 Plain-text import
- **SCR-17** S17 Manual entry
- **SCR-18** S18 Photos import (gallery on mobile, file upload on web)
- **SCR-19** S19 Field mapping
- **SCR-20** S20 Duplicate review
- **SCR-21** S21 Add items to an existing list
- **SCR-22** S22 Template library
- **SCR-23** S23 Template editor with live preview
- **SCR-24** S24 Start a round (item selection and card order)
- **SCR-25** S25 Sorting screen (coach marks, note entry, undo, offline, web version with keyboard hints)
- **SCR-26** S26 Item detail, editing and notes
- **SCR-27** S27 Round summary
- **SCR-28** S28 Results
- **SCR-29** S29 Filter and sort sheet
- **SCR-30** S30 Round history
- **SCR-31** S31 Invite (sender side)
- **SCR-32** S32 Opening an invite link (app installed, and web app in a browser)
- **SCR-33** S33 Join a list
- **SCR-34** S34 Members and roles
- **SCR-35** S35 Conflict rule settings
- **SCR-36** S36 Conflicts: one-by-one resolution
- **SCR-37** S37 Bulk resolve: confirmation and summary
- **SCR-38** S38 Activity and notifications
- **SCR-39** S39 Export flow
- **SCR-40** S40 Dialogs (all destructive confirmations), snackbars, offline banner, sync notice, generic error and not-found screens, desktop-browser frame

## Out of scope (designed only up to the hand-off point)

- **OUT-01** Native system dialogs (permission prompts, share sheet, file and date pickers, keyboard) are not designed; only the screens leading into them.
- **OUT-02** Status bar, safe areas and OS-level gestures use platform defaults.
- **OUT-03** No tablet or wide desktop layouts.
- **OUT-04** No backend, APIs, data storage or sync mechanics.
- **OUT-05** No analytics, crash reporting or push infrastructure.
- **OUT-06** No monetization, paywalls or subscriptions.
- **OUT-07** No translations.
- **OUT-08** No marketing website.

## Sample data

- **SMP-01** One shared sample data file used everywhere; realistic data, never placeholders.
- **SMP-02** About 100 contacts: name, phone, email, photo for some, family side, relationship.
- **SMP-03** Contact edge cases: very long names, missing phone numbers, duplicates, several phone numbers.
- **SMP-04** About 20 products: photo, price, rating, store.
- **SMP-05** About 30 photos: date and location.
- **SMP-06** Shared-list data: three members with different decisions, several conflicts, shared and private notes, items at every status.
- **SMP-07** Images are local placeholders or generated illustrations; never hotlinked.

## Deliverables

- **DEL-01** `design/README.md` — how to navigate; start here.
- **DEL-02** `design/HANDOFF.md` — guide for the coding agent (HTML is visual reference; specs/navigation/domain are behavior truth; build with RN Reusables + NativeWind + tokens; where to find everything; build order).
- **DEL-03** `00-brief/brief.md` verbatim, `requirements.md`, `assumptions.md`.
- **DEL-04** `01-foundations/design-principles.md`.
- **DEL-05** `01-foundations/tokens.json` as single source of truth; `tokens.css` (light and dark, shadcn naming); `tailwind.config.js` usable by NativeWind; `tokens.ts`.
- **DEL-06** `01-foundations/design-system.html` — colors, type, spacing, radii, elevation, icons, text-expansion rules.
- **DEL-07** `01-foundations/components.html` — every component in every variant and state.
- **DEL-08** `01-foundations/components.md` — anatomy, variants, states, props, accessibility; mapped to RN Reusables.
- **DEL-09** `01-foundations/motion.md` — thresholds, velocities, timings, easing, haptics, reduced-motion fallbacks.
- **DEL-10** `01-foundations/brand/` — logo, wordmark, app icon, Android adaptive icon (SVG).
- **DEL-11** `02-architecture/navigation-map.md` — every screen ID, connections, tabs, stacks, modals, deep links.
- **DEL-12** `02-architecture/domain-model.md` — entities, fields, statuses.
- **DEL-13** `02-data/sample-data.json`.
- **DEL-14** `03-screens/Sxx-name.html` with all frames side by side; `Sxx-name.md` spec following the 9-part template.
- **DEL-15** `04-explorations/` — sorting directions not chosen.
- **DEL-16** `04-prototype/index.html` clickable prototype; `swipe-demo.html` working swipe (touch, mouse, keyboard) implementing the motion spec.
- **DEL-17** `05-qa/` — screenshots (light and dark of every frame), `a11y-report.md`, `coverage.md`, `traceability.md`, `review-report.md`.
- **DEL-18** Screen HTML: plain HTML + compiled Tailwind, offline fonts/icons, no JS frameworks, small vanilla scripts only.
- **DEL-19** Screen HTML uses only tokens and mapped utilities; no hard-coded colors, sizes or fonts.
- **DEL-20** Each frame has a visible label (e.g. "S25 · Conflict state · dark").
- **DEL-21** Screen HTML uses real content from sample-data.json.
- **DEL-22** Prototype flow 1: first launch → onboarding → import contacts as a guest → map fields → review duplicates → sort → round summary.
- **DEL-23** Prototype flow 2: re-sort the Maybe pile → results → export to Google Sheets.
- **DEL-24** Prototype flow 3: invite a partner → sign-in prompt → partner opens link in web app → both sort → conflicts → Decision Maker bulk resolves → export.
- **DEL-25** Prototype flow 4: create a list from CSV with a custom template.

## Process

- **PRC-01** Commit after each phase with a clear message; never push.
- **PRC-02** QA uses Playwright via the npm scripts; flow tests in `/tools/flows` cover all four main flows, swipe drags in each direction on swipe-demo.html, and fail on console errors.
- **PRC-03** QA writes review-report.md; fixes and re-runs until no blocking issues remain.

## Success criteria

- **SUC-01** coverage.md shows every screen as Done.
- **SUC-02** traceability.md maps every requirement ID to at least one screen, with no gaps.
- **SUC-03** QA report has no open blocking issues; a11y report has no serious or critical violations; all flow tests pass.
- **SUC-04** A first-time user imports a list and makes a first decision in under a minute without an account (prototype flow 1).
- **SUC-05** An invited partner joins and sorts from a web browser without installing anything (prototype flow 3).
- **SUC-06** A product shortlist can be used without wedding-specific wording.
- **SUC-07** "X / Y decided" and per-decision counts are visible whenever sorting.
- **SUC-08** Every gesture has a visible, accessible button equivalent.
- **SUC-09** The source picker takes a new source by adding one tile.
- **SUC-10** A coding agent can implement any screen from its HTML, spec, architecture files and foundations alone.
