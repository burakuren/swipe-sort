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
  are fixed or defined inline. _Superseded in part by A-129 (photos removed, D-32)._
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
- **A-35** Guest lists are labeled "On this phone only" with a `cloud-off` icon (the not-backed-up indicator). _Superseded by A-137._
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

- **A-46** Before sign-in the device holds 4 lists (Wedding guests + the 3 in `me.guest.deviceLists`); S05 says "4 lists moved to your account". Lists move one at a time, starting with the list being shared; a list counts as moved only after server confirmation; the local copy stays usable. Moving into an account with lists adds them (same name gets " (2)"). _Superseded in part by A-135 and A-143 (lists can stay on this phone, D-33) and A-144 (sample never moves, D-10)._
- **A-47** Splash: Android SplashScreen API (static mark, wordmark as branding image); iOS launch screen shows the mark only; web loader only after 300 ms. An invite link at cold start skips onboarding (S32-app).
- **A-48** Onboarding demo uses 4 neutral cards (p02, ph09, p05, ph05); gestures in any order with a checklist; recap opens 700 ms after the third different gesture; no undo/notes/counts in the demo (coach marks teach those); Skip goes to S08-first-run. _Superseded in part by A-149 (photo cards become place cards, D-32)._
- **A-49** Email sign-in and create-account are separate forms. Password: ≥ 8 characters with a number or symbol; live rules, errors on submit; lock after 5 wrong attempts in 15 minutes; no blocking email verification.
- **A-50** Password reset: same "sent" screen whether or not an account exists; links last 1 hour, single use; 60 s resend cooldown; reset signs out other devices.
- **A-51** Official Google "G" and native Apple buttons are the only non-token colors allowed (brand requirements); mockups use stand-ins. _Superseded in part by A-140 and A-141 (Apple on every platform, D-13)._
- **A-52** Settings: Haptics is an inline switch; Appearance sub-page (System default, per device); Notifications: master push switch + six per-event switches (per account); on web the switches control the in-app Activity badge. Sign out removes backed-up lists from the phone; unsynced changes trigger a separate "Sign out anyway" dialog. Backup states: Backed up, Backing up…, Backup paused, Not backed up. _Superseded in part by A-136 and A-147 (lists on this phone only at sign-out, D-33)._
- **A-53** Profile: email read-only in v1; connected accounts are labeled "Sign-in methods"; the last sign-in method cannot be disconnected; re-authentication after 5 minutes for sensitive actions. _Superseded in part by A-141 (Apple on every platform, D-13)._
- **A-54** Account deletion: per owned shared list, transfer ownership (default: the Decision Maker) or delete for everyone; the person's decisions and notes are removed from shared lists; confirmation word "delete"; Apple token revoked; web deletion route `swipesort.app/account/delete` (Google Play requirement). Store links use `https://swipesort.app/get`. _Updated by A-148 (lists on this phone only at account deletion, D-33)._

## Phase 3: Group C1 (S11–S15)

- **A-55** The source grid is data-driven: each Source definition has name, icon, description, availableOn, needsConnection, needsPermission, selectStep, hasFieldMapping, webReplacement. `S11-new-source` shows a future "Calendar" tile. S11 has no loading/error state (static, local). _Superseded in part by A-150 (photos removed, `selectMode`, D-32/D-18)._
- **A-56** On web the Contacts tile stays visible but unavailable (sheet: "Get the app" or "Import a CSV instead"); Photos becomes "Upload photos". Offline, only Google Sheets is unavailable. "Get the app" links to `https://swipesort.app/get` (store redirect, QR on desktop). _Superseded in part by A-129 (no "Upload photos", D-32)._
- **A-57** Permission explainers sit at stepper step 2. The notifications explainer is a standalone modal shown once after a list is first shared or joined (not during joining), then only from Activity or Settings. Android has denied-once and don't-ask-again recovery; iOS goes to Settings. Denials use muted icons and no error haptic; every recovery offers an alternative (CSV for contacts, system photo picker for photos). Limited access designed for photos and iOS 18 contacts. _Superseded by A-153._
- **A-58** Contacts start all selected (the select step removes junk such as service numbers); the sample address book has 96 contacts (c001–c088 + 8 service numbers) → 88 imported. Search ignores accents and matches name, phone digits and email; Turkish collation; fast-scroll index above 200 contacts; max 10,000 contacts per import. _Superseded by A-154._
- **A-59** File limits: 20 MB, 10,000 rows, 50 columns per file or sheet; .csv/.tsv/.xlsx supported. Too many columns → "Choose columns" or "Continue with the first 50"; too many rows → import the first 10,000. Partial imports are caught at preview ("84 of 88 rows can be imported"), finishing with "Imported 84 of 88 items". At ≥150% text the preview table becomes a record view.
- **A-60** Several Excel sheets or Google tabs combine into one list with an automatic Tab/Sheet field. Google Sheets import uses read-only scopes; the write scope is requested at export. Connecting Google Sheets does not sign in to SwipeSort (works without an account). Web OAuth: popup on desktop (popup-blocked state), redirect on mobile. _Superseded by A-151._
- **A-61** Import chrome (all import screens): modal app bar "Import" / "New list" / "Add items", ImportStepper under it, primary h-14 at the bottom with a ghost secondary below it; iOS: first step `x` only, later steps "Back" + `x`. Closing with progress asks "Discard import?".

## Phase 3: Group C2 (S16–S21)

- **A-62** Step counts: contacts / CSV / Google Sheets 5; plain text 4 (duplicate lines handled on S16); manual entry 4 (Choose source, Set up fields, Add items, Finish); photos 3; Add items 5 ending with "Add to list". One import is capped at 5,000 items for text and photos (photos warn at 1,000+). A list has at most 50 fields. _Superseded in part by A-129 and A-150 (no photos stepper, D-32)._
- **A-63** Field detection: a type is chosen when ≥ 90% of non-empty values fit; the title is the first text field present in ≥ 90% of items; constant or ≥ 90%-empty fields start in a collapsed "Hidden by SwipeSort" group. Hiding the title field unsets it. Several phone numbers default to "All numbers in one field" (card shows first + "+1"); options "First number only", "One field per label".
- **A-64** Duplicates are detected after mapping. Merge / Keep both / Skip is a per-group radiogroup; unreviewed groups import as separate items (nothing lost by default). Merge combines multi-value fields and keeps the first record's other values unless changed.
- **A-65** Add items (S21): new columns default to "New field" (empty for existing items, not added to the card template); Merge fills empty fields of existing items and never overwrites edits; decisions and notes stay; identical rows default to Skip. Sample: mert-family.csv has 15 rows → 12 added (c089–c100), 1 skipped, 2 merged; the list grows from 88 to 100. New items join the current round, members get an activity event; "Added 12 items" has Undo.
- **A-66** Manual entry: item form is a sheet ("Add another" saves and stays; "Add item" saves and closes); deletes are immediate with Undo. Plain text has Text / Preview tabs; duplicate lines are kept unless "Remove duplicates". Photos are grouped by day in a 4-column grid; web uploads accept JPG/PNG/HEIC/WebP up to 25 MB and resume after going offline. _Superseded in part by A-129 (photos removed, D-32)._

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

## Phase 3: Group B (S08–S10)

- **A-79** "Try a sample list" creates "Desk setup (sample)": a local copy of products p01–p20 with the Product template, unsorted, with a "Sample" badge; one at a time, can't be shared, only Delete. Offered on first run only. _Superseded in part by A-139 and A-144 (the sample stays on the device at sign-in, D-10)._
- **A-80** Home rows are ordered by latest activity (including other members') and never re-order while visible. Rows with a round in progress have a "Resume" button opening S25 at the next undecided item. The conflict chip shows open conflicts ("15 conflicts"), or "3 new conflicts" + unread dot since the last visit. Search matches list names (word prefix, case- and accent-insensitive); archived lists form their own group. "Archived lists" is the last row, hidden at 0.
- **A-81** The not-backed-up indicator is one line under the "Lists" title (web: "Lists are in this browser only"), hidden with no lists or only the sample. Signed-in lists are always backed up and show no per-list label. _Superseded by A-137 (per-list label for signed-in lists on this phone only, D-33) and A-183 (web copy, D-08)._
- **A-82** S09 has one progress card holding the single filled button (Continue sorting, Start sorting, Re-sort Maybe (N), Start a new round, Add items, or Restore list). Solo lists say "Only you sort this list, so your decisions are final." Shared lists show "My progress" and "List status" cards; the status card lists Agreed, Conflict, Pending with meaning and count.
- **A-83** Conflicts entry by role: Owner "Review conflicts"; Collaborator "View conflicts" (read-only); the Decision Maker gets a top callout "Resolve conflicts" + "Resolve all with my decisions" ("12 have your decision. 3 stay open"). Only the Owner sees "Start a new round" and edits the conflict rule.
- **A-84** Menus by role: solo Owner — Rename, Duplicate, Archive, Delete list; shared Owner — plus Leave list; Collaborator / Decision Maker — Duplicate, Leave list. Rename: 1–80 characters, duplicates allowed, "List renamed".
- **A-85** Duplicate always creates a solo list owned by the duplicator: "Items only" (items, fields, sources, template, edits) or "Items with my decisions and notes" (my latest decision per item becomes Round 1; private notes become normal). Name "{name} (copy)".
- **A-86** Archive: solo immediate with Undo; shared asks and archives for everyone (members keep read-only access). Archived lists open read-only (Results, Rounds, Export; "Restore list"). Delete is Owner-only, always confirmed, committed when the "List deleted" Undo snackbar closes (6 s, 10 s with a screen reader); shared delete reads "Delete for everyone" and offers making someone else Owner instead. Sources are never changed.
- **A-87** Leaving a list: the member's decisions stay and count; items they haven't decided stop waiting for them; shared notes stay, private notes are deleted; no Undo (rejoining needs a new invite). If the Decision Maker leaves the role is empty and conflicts stay open. The Owner must transfer ownership first.
- **A-88** Offline: rename, duplicate, archive, restore and solo delete work offline; shared archive/delete/leave and invite need a connection (shown disabled with "Needs a connection"); shared list status shows "As of 9:24". _Superseded by A-159 (S21), A-169 (S22) and A-186 (S09/S10): queued, not blocked, on shared lists (D-05)._

## Phase 3: Group H (S39)

- **A-89** Export step 1 holds scope chips (All, Rejected, Maybe, Accepted; Conflicts on shared lists), column switches and the four formats as actions. CSV/Excel export immediately; Google adds Destination and Confirm steps; Text summary adds a preview.
- **A-90** Results and exports use the latest decision per item: Desk setup = 11 rejected, 1 maybe, 8 accepted ("Exported 8 items to desk-setup-accepted.csv"). S39-shared shows counts after the bulk resolve (3 open conflicts).
- **A-91** Google destinations: lists from Google Sheets offer New tab (default), New columns in the original sheet, or New spreadsheet; other lists offer New spreadsheet only, with an explanation. Write permission is requested at the confirm step: `drive.file` for a new spreadsheet, `spreadsheets` for the original sheet. New columns go after the last used column, never overwrite cells, and each row's address is checked before writing (mismatch → "sheet changed" error). _Superseded by A-157._
- **A-92** A person who signs in to SwipeSort with Google gets that account preselected for export (no separate connect screen); others see "Connect Google Sheets". Flow 3: Mert exports from his own account (mert.aydin@example.com).
- **A-93** Shared exports add a Final decision column (Accepted / Rejected / Maybe / Conflict / Pending) and, optionally, one "Decision (Name)" column per member; shared notes include their author; private notes are never exported; any member can export.
- **A-94** Files: Android shows a "Your file is ready" sheet (Share file, Save to device); iOS opens the share sheet (has Save to Files); web downloads directly; success is a snackbar. Export contents leave out image fields, use edited values, CSV is UTF-8 with BOM, values starting with `=` are written as text.
- **A-95** Plain-text summary lists accepted and Maybe items and only counts rejected ones (counts in Reject, Maybe, Accept order).

## Phase 3: Group G2 (S35–S38)

- **A-96** Majority numbers from sample data: switching to Majority makes 8 of 15 conflicts final (6 Accept, 1 Reject, 1 Maybe); 7 wait for one member. Bulk resolve: Mert's 12 decided conflicts are 6 Reject, 6 Accept; c012 Gülşen Aydın, c034 Buse Altun, c056 Tuğba Sönmez stay open. S36 starts at 0 / 15.
- **A-97** Changing the conflict rule always confirms, recalculates only open conflicts (resolved items stay resolved, members' own decisions never change), offers Undo for 6 s, needs a connection, and adds an in-app `ruleChanged` activity entry (no push). Picking "Decision Maker decides" with no Decision Maker shows the S34 switches inline; one dialog sets both.
- **A-98** Two-member lists under Majority: every disagreement is a tie.
- **A-99** Conflict cards (S36): the Decision Maker's stamp reads "Final: Accept"; the bar is S25's without counts, captioned "Your choice is the final decision". The final decision may differ from the Decision Maker's own earlier decision, which never changes. Other members use the same deck to change their own decision. A Decision Maker resolution is final even if someone decides later. If members agree before an offline resolution syncs, the agreement wins. "Skip for now" is in the menu; list view groups Open / Resolved.
- **A-100** Bulk resolve is blocked offline (one-by-one still works); Undo is on the summary and asks to confirm; partial failure keeps saved items and retries only failed ones.
- **A-101** Activity: tabs All / Conflicts / Members; unread clears on open or "Mark all as read" (badge = unread rows); new-conflict pushes are batched to one per list per hour; no in-app banners while sorting or resolving. conflictsResolved opens S28; newConflicts opens S36 (members get the read-only view). New activity types: roundRequested, ruleChanged, itemsAdded, memberLeft (domain-model.md).
- **A-102** S09 shows a "Sources" group (type icon, label, count, date; "Add items" as its last row, hidden on archived and sample lists); tapping a source opens a details sheet ("Your original is never changed"). Single sources can't be removed in v1; Undo on "Added 12 items" removes the added items and their source.

## Phase 3: Group D (S22–S23)

- **A-103** The import finish preview renders the S25 card at 50% (`aspect-card`) with an expand button; pick mode shows the first item, the editor cycles items. Tile order: recommended/current first, then custom templates, then other built-ins; recommendation rules per source in S22 §4. The list name is prefilled from the source and selected on arrival. The step total stays fixed when duplicates are skipped ("No duplicates found").
- **A-104** Change mode applies immediately with Undo; on shared lists it applies to all members (no activity event). Deleting a template in use asks for a replacement per list (default: the built-in it was based on). _Extended by A-169 (offline template change on shared lists is queued, D-05)._
- **A-105** Image area options: "None", "Photo or initials", "Image on top", "Full image" (last two need an Image field). Rows stack (label above value) when the card has no image or a label is wider than 64 dp; otherwise inline. Hidden fields show under "Not on the card". Removing a field needs no confirmation; a new template is named when saved.
- **A-106** Sample data: Photo template rows are File name and Size; the custom "Guest with table side" template is not in use until the user switches to it (S22-change-applied). _Superseded in part by A-131 and A-165 (Photo template rows, D-32)._

## Phase 3: Group F (S28–S30)

- **A-107** Results segments lead with Accept, then Maybe, Reject (results people look for first; icons + labels + counts kept); shared Final view adds Conflicts and Pending (never hidden; Pending explains "Not final yet"); My decisions view adds Not decided and shows each row's list status. Search, filter and sort apply to the current segment and persist across segments; search covers title, fields and visible notes, accent-insensitive.
- **A-108** Filter sheet stages changes until "Show N items"; chip counts preview results, zero-result values are disabled; fields with more than 8 values show 6 + "Show all". Shared-only filters: Decided by a member, List status.
- **A-109** Change decision applies on tap in a sheet; the row keeps its new badge until the Undo snackbar ends. On shared lists only my decision changes (final decisions are resolved in S36/S37). iOS uses swipe actions + context menu; Android overflow + long-press.
- **A-110** Round mode: a round from S30 opens S28 "Round 1 results" with decisions as they were at round end ("Changed to Accept in Round 2" on rows); rounds never change afterwards. Results sort by "Recently decided"; Pending sorts "Waiting for you first".
- **A-111** Illustrative data: Round 2 shuffled order p15, p04, p18, p13, p07, p16; Apartment viewings decisions a01/a03/a05 accepted, a07 maybe, others rejected; post-bulk-resolve finals Accept 28 / Reject 10 / Conflicts 3. "Frontend hiring, Q4" is never sorted in sample data; S24-empty-option shows it after a first round (A-72) as an illustrative later state.

## Phase 3: Group I (S40) and lead decisions

- **A-112** S40 is the source of truth for every confirmation, snackbar, banner and error; where a screen spec disagrees, S40 wins. Confirm buttons are destructive (red) when the action deletes, discards, replaces, removes access or signs out; primary when nothing is lost (end round, new round, archive for everyone, transfer ownership, change the rule). Dialogs have no icon, are vertically centered, max width 384; buttons stack when labels don't fit; initial focus on the dismiss button; the scrim does nothing on delete account and unsynced sign-out.
- **A-113** iOS: action sheets for destructive actions chosen in context; alerts when the person must read first. Remove member on iOS = two red actions ("Remove and keep/discard Selin's decisions").
- **A-114** Snackbars: 4 s, 6 s with an action, ≥ 10 s with a screen reader; a new one replaces the current (a replaced Undo commits); `bottom-24` above bottom navigation, `bottom-32` above the decision bar; lasting errors are inline alerts.
- **A-115** Offline banner: "You're offline." + what is saved (+ what needs a connection), after 2 s offline, not dismissible. Sync: "Saved on this phone" / "Syncing N decisions…" / "Synced" (4 s) / failed alert after 3 retries; never on lists of people who aren't signed in.
- **A-116** App update required exists: once per session below the minimum sync version; "Not now" keeps local use with a persistent "Update SwipeSort to sync your changes." banner; web gets a "SwipeSort was updated." + Reload snackbar.
- **A-117** Not-found never reveals whether an inaccessible list exists. Desktop web: nothing in the muted margins; the column is the window height; minimum height 568 (below that the page scrolls); S25 below 680 hides the card image; web toast `w-80` bottom-right, 6 s, pauses on hover/focus.
- **A-118** Copy uses straight apostrophes (') everywhere; curly double quotes (“ ”) only around object names in titles.

## Phase 4: QA round 1 decisions

- **A-119** Flow 1 imports 88 contacts; duplicate review merges 3 pairs and keeps 1 pair → 85 items. The first round is 0 / 85 (coach marks) and ends at `S27-first-round`; the prototype's live sort stops after 6 cards ("Done for now … The prototype skips the rest of the round").
- **A-120** Flow 3: Mert sorts on the web at 85 / 100 (the desktop frame's decision buttons open the live demo with his 15 undecided items) and closes sorting to `S09-shared-decision-maker`, then resolves conflicts (12 resolved, 3 open because he never decided them). He is made Decision Maker by Deniz after joining (`S34-dm-changed`). `S27-shared` shows Deniz finishing her own round.
- **A-121** Count badges (unread Activity) use `primary`, not `destructive`. Keyboard hints use Inter (no monospace). FilterChip and SegmentedControl segments specify `hitSlop` to reach 48.
- **A-122** Others' decisions on a card (opt-in) are a small panel listing each member with avatar, name and a decision badge (icon + word), not overlapping avatar dots.
- **A-123** Replaces A-72's Mert numbers: `S27-shared` shows Deniz finishing (18 rejected, 15 maybe, 67 accepted; her remaining decisions copy Mert's where he decided, else Accept); list status stays 32 / 53 / 15. `S27-first-round` = 85 / 85: 20 rejected, 12 maybe, 53 accepted. A former Owner variant of S27-shared was removed; `S27-count-up` added.
- **A-124** Web desktop Home has no FAB: a filled "New list" button sits in the app bar next to search. Duplicating a list stays on the original list with "Duplicated as “…”" + Open.
- **A-125** Sparse-card rule (image area None): content block vertically centered above pinned tags; ≤ 3 rows use text-title-2 values, 4–6 rows text-title-3; title-only uses text-display; decided by the template's row count. Duplicated templates are named "{name} (copy)".
- **A-126** Extends A-112: "Undo Resolve all" is destructive (it discards final decisions); "Make Mert Owner" stays primary.
- **A-127** The committed screenshots are rendered at scale 1 (92 MB for 1,686 PNGs); scale 2 would add ~300 MB to the repository. `npm run shots` regenerates them at scale 2 on demand.

## Design update after build planning (2026-10-11)

Applies the design update register in `docs/build-decisions.md` §7. For this update the build decisions
(D-xx) override the brief and earlier assumptions wherever the register says so. Lead decisions first
(A-128–A-139), then group decisions.

- **A-128** D-02 is skipped: `docs/build-decisions.md` names no final product name yet ("Open, process
  decided"). "SwipeSort" and `swipesort.app` stay in every string, A-54, A-56 and navigation-map §4 until the
  founder picks a name; then one find-and-replace pass covers the brand assets and the S07, S32, S39 copy.
- **A-129** D-32 (Photos out of scope): the Photos tile and the web "Upload photos" tile leave S11 entirely
  (no "later" tile: `S11-new-source` already shows how a future source appears, with Calendar). The photos
  explainer, denied and limited-access frames leave S12. S18 stays as a retired file marked "Out of scope
  (D-32)" in its HTML header, spec and coverage; nothing links to it and no flow passes through it. Contact
  photos and image fields stay. Supersedes the photo parts of A-24, A-56, A-57, A-62 and A-66.
- **A-130** D-32: the sample list "March photos clean-up" (Photos source) is replaced everywhere by
  **"Trip ideas"**: 30 places from `trip-ideas.csv` (fields Photo (image link), Place (title), Country, Best
  time, Budget (EUR)), Photo card template, solo, Round 1 in progress at 12 / 30 (6 rejected, 1 maybe, 5
  accepted), same position and dates in the sample world. It is image-led, so the Photo template keeps a real
  example, and unrelated to weddings, so the samples still show that any list works (GOAL-02). In the
  signed-in sample world it is backed up; in the guest world it is one of the 4 device lists.
- **A-131** D-32: the built-in **Photo** card template stays. Spreadsheets and CSVs often carry image links
  (trips, listings, products, portfolios) and Photo is the only built-in that leads with a full image. Its
  sample rows are no longer gallery metadata (File name, Size) but the example list's own fields (Best time,
  Budget). It is recommended when a source has an Image field and at most three other fields besides the title
  (A-166). Supersedes
  A-106's Photo rows.
- **A-132** D-33 Q1 (where and what): a signed-in Owner of a **solo** list controls backup per list with a
  **Switch row "Back up this list"** in S09 (list overview, its own "Backup" group under Sources). On: the list
  is in the account ("Backed up to deniz.yilmaz@example.com"). Off: the list is **on this phone only**. Turning
  it on needs no confirmation (nothing is lost): the row shows "Backing up…" and a snackbar says "“{name}” is
  backed up". New lists made while signed in get the same switch, on by default, at the import finish step
  (S22 pick mode), so a private list never has to touch the server. Not shown to people without an account
  (their lists are all on this phone, A-35/A-81) or on the sample list. S06 › Backup lists the lists that are
  on this phone only, each with "Back up". The domain keeps a per-list storage mode: `backedUp` or
  `deviceOnly` (domain-model › List).
- **A-133** D-33 Q2 (sharing): sharing needs backup. Share or Invite on a list that is on this phone only
  opens a sheet "Back up this list to share it" ("Members sort a shared list on their own devices, so it needs
  to be in your account.") with "Back up and share" and "Not now"; the list backs up (one ListMoveRow with
  progress), then S31 opens. Offline, the sheet says sharing needs a connection. A shared list can't be on
  this phone only.
- **A-134** D-33 Q3 (turning backup off): turning the switch off asks first, because it deletes the account
  copy: "Keep “{name}” on this phone only?" / "The copy in your account is deleted and the list leaves your
  other devices. If you lose this phone or move to a new one, the list can't be recovered." / "Cancel" /
  "Keep on this phone only" (destructive, A-112). It needs a connection (it deletes account data; D-05 T3).
  Done: snackbar "“{name}” is on this phone only" with Undo (backs it up again). Shared lists can't turn backup
  off: the switch is disabled with "Shared lists are always backed up." Once the Owner has removed every
  member and turned off every invite link, the list is solo again and the switch works. Members who don't own
  a list never see the switch (they can Duplicate it and keep the copy on this phone only). Other devices of
  the same account remove the list on their next sync and say so once (S40 snackbar).
- **A-135** D-33 Q4 (sign-in): lists on this phone still move to the account by default, but the S05 prompt
  offers "Choose lists" (a checklist, all on). The list being shared is locked on ("Needed to share"); the
  sample never moves (D-10, A-139). Lists left unchecked stay on this phone only and now belong to the
  account. The result says "3 lists moved to your account. 1 stays on this phone only." Supersedes A-46's
  "every list moves".
- **A-136** D-33 Q5 (sign-out and other accounts): signing out removes backed-up lists from the phone
  (A-52). Lists on this phone only stay on the phone, **hidden while signed out**, and come back when the same
  account signs in on this phone again. Another account signing in on the same phone never sees them; nor
  does anyone using the app without an account. The sign-out dialog names them when they exist: "“Frontend
  hiring, Q4” stays on this phone, hidden until you sign in again." Removing the app deletes them like any
  data on the phone. Extends A-52.
- **A-137** D-33 Q6 (labels): for signed-in users, a list on this phone only carries a per-list label
  "On this phone only" (`cloud-off` 16, muted) on its Home row and in its S09 header meta, because it is the
  exception; backed-up lists show nothing (A-81). On the web the label reads "On this browser only" and S09
  adds the D-08 line "Browsers can clear lists you haven't opened for a while. Back it up to keep it." People
  without an account keep the single Home indicator line (A-81, copy updated for D-08). The label "On this
  phone only" and the action "Keep on this phone only" are fixed terms (GLOSSARY.md) and read the same on iOS;
  running sentences on iOS follow S40 §3.2 ("If you lose this iPhone…", "stays on this iPhone"). Supersedes A-35 and the "always backed up" sentence of A-81.
- **A-138** D-33 Q7 (account deletion, new phone): lists on this phone only are not in the account, so
  deleting the account does not delete them: S07's deletion summary says "“Frontend hiring, Q4” is on this
  phone only. It stays on this phone, without an account." Afterwards they behave like lists made without an
  account (every device does the same at its next start). A new phone never receives them; the turn-off
  confirmation (A-134) and the S06 › Backup footer say so ("Lists on this phone only don't move to a new
  phone. Back them up first.").
- **A-139** D-10 and D-33 details: the sample list stays on the device at sign-in, is never moved or backed
  up, has no backup switch and stays visible whatever the account state until deleted (supersedes A-79's and
  S08's "signing in moves it like any list"). A list on this phone only never shows sync states (A-115), and
  everything on it works offline except Share and turning backup off (turning it on queues until a connection returns); Duplicate keeps the original's storage mode; Add
  items, Export, rounds and templates work as on any solo list. In the signed-in sample world, "Frontend
  hiring, Q4" (candidate CVs, the privacy case D-33 names) is on this phone only.

### Group A: accounts (S01–S07)

- **A-140** D-13: sign-in button order and style per platform.
  - iOS: Apple, Google, email. Apple is the system `AppleAuthenticationButton` (black on light, white on
    dark), first per App Store guideline 4.8 and the HIG, as before.
  - Android and web: Google, Apple, email. Every Android phone has a Google account, and flow 3's web member
    signs in with Google, so Google is the expected first choice there. Apple sits second, at the same size
    and weight.
  - On Android and web, Apple uses Apple's "white with outline" style in light mode, which matches the
    outline Google button so neither is less prominent and no black slab dominates an Android screen. In dark
    mode it uses Apple's "white" style, because Apple doesn't allow its black button on dark backgrounds.
  - Web uses the Android order on every device (one predictable layout; no detection of Apple devices).
  - S07's sign-in methods follow the same order. Mockups draw the Apple logo with the Lucide `apple`
    stand-in (A-51 extended to Apple's Android and web artwork).
- **A-141** D-13: on Android and web, Apple uses Supabase OAuth with an Apple Services ID:
  - Android: a Custom Tab, returning by deep link;
  - web: a popup on desktop, a redirect on phones.

  The browser page is out of scope to draw, like the native sheets. Busy, cancelled and failed states reuse
  the Google pattern, on the Apple button. The name Apple returns on first sign-in is saved. Every platform
  can connect and disconnect Apple in S07 (the sample account has Apple "Not connected" on Android and
  connected on iOS). Disconnect follows A-53. The blocked dialog keeps "Add a password first" with its original body; when Apple is the only method it reads "Apple is your only way to sign in. Add a password so you can still sign in after disconnecting Apple." New error: "This Apple ID is already linked to another SwipeSort account." Supersedes the
  "Apple on iOS" parts of A-51 and A-53.
- **A-142** D-33 (Choose lists pattern, A-135). The S05 prompt's first reason ends with a text link "Choose
  lists" (48 high).
  - It swaps the sheet content to a checklist, "Choose lists to move". Each row is a SelectableRow: leading
    checkbox, list tile, name, count. A live summary reads "3 of 4 lists move", and a primary "Done" closes
    the step. iOS uses an in-sheet nav row (Back / Choose lists / Done) and round checkmarks.
  - All rows start checked. The list being shared is checked and disabled with "Needed to share" (`lock`
    icon). The sample list is never listed.
  - Done returns to the prompt, whose reason reads "3 of your 4 lists on this phone move to your account. 1
    stays on this phone only." The choice is forgotten on "Not now".
  - Choosing lists is a step before sign-in, so the provider buttons keep one place and the default path
    (all lists move) adds no step.
- **A-143** D-33: moving with kept lists.
  - The moving list still shows the kept list, with the neutral status "On this phone only" (`cloud-off`,
    muted; web "On this browser only").
  - The progress counts only the lists that move ("2 of 3 moved").
  - Result: "3 lists moved to your account" / "1 stays on this phone only. You can back it up anytime in
    Settings › Backup. Now you can share “Wedding guests”."
  - With every list unchecked (backup origin only), the reason reads "None of your 4 lists move. They stay on
    this phone only." and there is no moving step. Extends A-46.
- **A-144** D-10 / A-139 in S05 and S06: the sample list is never moved, counted ("Your 4 lists" excludes it),
  listed in Choose lists, in Backup or in the moving list, or removed at sign-out. When it is the only list on
  the device, signing in has no moving step.
- **A-145** D-28: S06 › Privacy starts with a group holding the Switch row "Share anonymous usage data" (on
  by default).
  - Description: "Events like finishing a round, with no ID that follows you. Never list contents, names or
    anything you type."
  - Footer: "Applies on this phone. The privacy policy lists every event." (web: "Applies in this browser.")
  - The switch is **per device**, like Appearance and Haptics: events carry no account or user ID, people
    without an account need the switch too, and signing in or out must never flip it.
  - Off stops sending immediately; queued events are dropped.
  - It sits at the top of the page because it is the only control there; the explanations follow it.
- **A-146** D-32 / D-18: the Privacy paragraphs become What SwipeSort keeps, **Contacts**, **Lists on this
  phone only** (new), Shared lists, Your original files.
  - Contacts: "SwipeSort reads only the contacts you choose to import and keeps only the fields you map. On
    newer phones you choose them in your phone's own contact picker, so SwipeSort sees only the ones you
    pick."
  - Lists on this phone only: "A list you keep on this phone only never leaves it. It isn't backed up, so it
    can't be recovered if you lose the phone."
- **A-147** D-33: S06 Backup and sign-out (A-132, A-136, A-138).
  - The root Backup row reads "Backed up. 1 list on this phone only" while such lists exist. Web shows none
    in the sample world, because device-only lists are per device.
  - The Backup page renames "Lists" to "Backed-up lists" and adds a group "On this phone only": one row per
    list with "Back up" (no confirmation; the row shows "Backing up…", then the snackbar "“{name}” is backed
    up"; offline "Backs up when you're online"). The group footer reads "Lists on this phone only don't move
    to a new phone. Back them up first." Web says "On this browser only" plus the D-08 line.
  - Sign-out dialog with such lists (same copy as S40, A-187): "Lists backed up to {email} are removed from this
    phone until you sign in again. “Frontend hiring, Q4” stays on this phone, hidden until you sign in again."
  - The iOS action sheet uses "iPhone" in these sentences, per S40 §3.2. The label term stays "On this phone
    only" (A-137).
  - Supersedes A-52's "Sign out removes backed-up lists" wording only where device-only lists exist.
- **A-148** D-33 / D-19: account deletion with lists on this phone only (A-138).
  - "Deleted for good" counts only backed-up lists ("4 lists only you use").
  - Each device-only list is a row under "Not changed".
  - The final dialog uses the S40 copy (A-187): "“Frontend hiring, Q4” is on this phone only. It stays on this
    phone, without an account." The confirm summary lists it under "Not changed", and the deleted screen says it
    "stays on this phone".
  - After deletion, "Done" opens Home with those lists as lists without an account (`S08-guest`), or
    `S08-first-run` when there are none.
  - If the account is signed in on other devices, "Not changed" adds the footer "Lists kept on your other
    devices only stay on those devices." (spec only, not drawn).
  - Updates A-54.
- **A-149** D-32 in onboarding: the S02 demo deck keeps its images, but the two gallery photos become place
  cards on the Photo template (place as title, "Türkiye, best in spring/autumn"), like Trip ideas. The welcome
  says "people, places, things to buy and ideas", and the web note mentions only phone contacts. Supersedes
  A-48's "photo" cards (same IDs p02, ph09, p05, ph05).

### Group B1: import (S11–S21, S39)

- **A-150** D-32. S11 and S21 show five source tiles. When the number of sources is odd, the last tile spans
  both columns (same vertical tile layout and row height), so the grid never shows a hole. With an even
  number, every tile takes one cell (`S11-new-source` with Calendar). Step totals are 5 for sources with field
  mapping and 4 for manual entry and plain text; the 3-step photos stepper is gone. The Source definition's
  `webReplacement` stays for future sources (no source uses it now). `needsPermission` applies only to
  contacts on Android 16 and lower. A new `selectMode` (`permissionList`, `systemPicker`, `googlePicker`)
  chooses the select step. S18 carries a page-level "Out of scope (D-32)" notice in its HTML (title "S18
  Photos import (retired)") and spec, and nothing links into it. Extends A-129. Supersedes the photo parts of
  A-55 and A-62 together with A-129.
- **A-151** D-17. Several Excel sheets or Google tabs combine into one list with an automatic Tab/Sheet field.
  Google Sheets uses only the non-sensitive `drive.file` scope, for import and for every export. The person
  chooses one spreadsheet in Google's file picker, and SwipeSort can open only the files chosen there plus
  the spreadsheets it creates. There is no in-app spreadsheet list, no Drive search and no separate read and
  write scope. The picker on each platform:
  - Web: Google's JavaScript picker over the page, after a Google sign-in popup on desktop (with a
    popup-blocked state) or a redirect on mobile browsers.
  - Android: Google's documented picker flow for mobile apps in the system browser (a Custom Tab with its own
    OAuth client ID).
  - iOS: the same browser flow, to be verified when iOS work starts.

  Connecting Google Sheets doesn't sign in to SwipeSort (it works without an account). Supersedes A-60.
- **A-152** D-17. S15 starts with a "Choose a spreadsheet" step: an explainer the first time
  (`S15-default`), and later the remembered account with "Switch" (`S15-connected`). "Choose spreadsheet"
  opens Google's picker, which is drawn only as labeled placeholders. The picker lists only Google Sheets
  files. Excel and CSV files stored in Drive are not read here: `S15-error-unsupported` sends people to S14
  after a download. Cancelling the picker returns to the step with nothing changed and no message. "Change"
  and "Choose another spreadsheet" reopen the picker. After a pick: `S15-reading`, then tabs, preview and
  S19 as before. Limits follow A-59, counted over the selected tabs (`S15-too-many-rows` offers "Import the
  first 10,000 rows"; too many columns uses S14's column chooser). Errors:
  - Google didn't respond (SRC-23).
  - Access removed in the Google account ("Choose spreadsheet again").
  - A Google Workspace admin blocks SwipeSort ("Import a CSV instead", "Use another Google account").
  - Offline.

  "Disconnect Google Sheets" revokes the token and with it SwipeSort's access to every file chosen so far.
  Lists already imported are unaffected (export to their original sheet re-picks, A-158).
- **A-153** D-18 and D-32. Permission explainers sit at stepper step 2 and exist only where a system
  permission is asked: contacts on Android 16 and lower (`READ_CONTACTS` with `maxSdkVersion="36"`) and
  notifications. On Android 17 and later and on iOS, contacts are picked in the system contact picker without
  a permission. An intro in the same PermissionExplainer layout replaces the explainer ("Choose contacts",
  "No permission needed…"). The notifications explainer is a standalone modal, shown once after a list is
  first shared or joined (not during joining), then only from Activity or Settings. Android has denied-once
  and don't-ask-again recovery; iOS goes to Settings. Denials use muted icons and no error haptic. Every
  recovery offers an alternative (CSV for contacts). There is no photos permission (D-32). The iOS contacts
  explainer, denied and limited-access frames are fallback only (A-156). Supersedes A-57.
- **A-154** D-18. Android 16 and lower: contacts start all selected, and the select step removes junk such as
  service numbers. The sample address book has 96 contacts (c001–c088 plus 8 service numbers), and 88 are
  imported. Android 17 and later and iOS: the person picks in the system picker, and the review list shows
  exactly the picked contacts, all included ("88 contacts picked"). It has search, unchecking ("87 of 88
  included") and "Add more", which reopens the picker and ignores contacts already picked. It has no Select
  all. In the sample, Deniz picks the same 88, so both paths reach `S19-contacts` with 88. On both paths:
  - Search ignores accents and matches name, phone digits and email.
  - Contacts sort in Turkish collation.
  - A fast-scroll index appears above 200 contacts.
  - One import takes at most 10,000 contacts.
  - Contacts already in the list (S21) start unchecked.
  - Duplicates go to S20.

  Supersedes A-58.
- **A-155** D-18. Design assumption: Android 17's contact picker lets people select many contacts in one
  session. This is unverified until the D-18 spike. If the picker needs one tap per contact, Android 17 and
  later keep `READ_CONTACTS` and use the Android 16 frames unchanged, and the picker path stays for iOS. Picker
  access is temporary, so picked contacts are copied into the import draft as soon as the picker returns.
  Cancelling the picker or picking nothing returns to the intro (or to the review list after "Add more")
  unchanged, with no message. Picked contacts without a phone number import with the details they have. A
  note counts them and can filter the list to them (`S13-picked-missing`).
- **A-156** D-18. The iOS contacts explainer and denied frames (`S12-contacts-ios`, `S12-contacts-denied-ios`)
  and the iOS full and limited-access lists (`S13-ios`, `S13-ios-limited`) are kept as **fallback frames**.
  They sit in their own sections labeled "Fallback only (D-18)", and nothing links into them. Reason: D-18
  names them as the fallback if full access is ever requested. They cost nothing to keep, and removing them
  would mean redesigning iOS's ask-once and iOS 18 limited-access behavior from scratch if the fallback is
  ever used. The photos frames were deleted instead, because D-32 removes the whole source.
- **A-157** D-17. Google destinations:
  - Lists from Google Sheets offer New tab (default), New columns in the original sheet, or New spreadsheet.
    Other lists offer New spreadsheet only, with an explanation.
  - Everything uses the one `drive.file` scope. Writing to the sheet chosen in Google's picker at import
    needs no new permission, and new spreadsheets are created under the same scope.
  - Google's consent appears after the confirmation only when the Google account hasn't granted `drive.file`
    yet (Flow 3: Mert, who signed in with Google but never connected Google Sheets). Only then does the
    "Google asks for permission next" alert show.
  - New columns go after the last used column and never overwrite cells. Each row's address is checked
    before writing; a mismatch shows the "sheet changed" error.

  Supersedes A-91.
- **A-158** D-17. When SwipeSort can't open a list's original sheet with the current Google account, S39's
  destination step asks to choose the sheet again in Google's picker (`S39-apartments-repick`: alert "Choose
  Flat hunt 2026 again", primary "Choose Flat hunt 2026"). This happens when:
  - the list was imported with another Google account, or on another device whose grant isn't shared;
  - Google Sheets was disconnected;
  - access was removed in the Google account.

  Choosing the same file continues to the confirmation. Choosing another file shows the snackbar "That's not
  Flat hunt 2026. Choose it, or export to a new spreadsheet." New spreadsheet never needs the re-pick. Drive
  answers "not found" both for a missing grant and for a deleted or unshared file, so the re-pick is offered
  first. A file that is really gone can't be chosen. `S39-error-sheet-missing` stays for a sheet that
  disappears between the check and the write.
- **A-159** D-05 (S21 part of an updated A-88). Adding items (S21) works offline on every list. On shared
  lists it is queued, not blocked: "Add to list" saves the items on this phone, and they reach the account and
  the members when the connection is back (S40 sync notice "Saved on this phone" → "Syncing…" → "Synced").
  Members' notifications and the S38 activity event go out when the items sync. Undo works while the items are
  queued. Copy:
  - Banner: "You're offline. Items you add are saved on this phone. Google Sheets needs a connection."
  - Shared notice: "Mert and Selin see the 12 new items when you're back online" / "Until then they're saved
    on this phone. Members get a notification once the items sync."
  - Snackbar: "Added 12 items. Members see them when you're back online." + "Undo".

  Starting a source that needs a connection (Google Sheets) still needs one. Extends A-88.
- **A-160** D-32. There is no photo-library access at all for now (D-32: no Photo Picker path), so manual
  entry's Image field (Desk setup's "Photo") takes an **image link** instead of a photo picker or camera. It
  works like CSV image links (A-131), and it is the same control as S26's image-link edit.
  - **Control**: a `link` icon leads in every state, then the URL input, then a 36 slot at the end. The helper
    line is `text-body-sm`: "Paste a link to an image. Cards show the picture from this link."
  - **Loading** (`S17-image-link-loading`): the slot shows a spinner and the helper reads "Loading the
    picture…".
  - **Loaded**: the slot shows the thumbnail.
  - **Offline** (`S17-image-link-offline`): no error. The link is kept, the slot shows `image-off`, the helper
    reads "You're offline. The link is saved, and the picture loads when you're back online.", and the item
    saves. The image downloads when online, like A-167; until then the card shows the `image-off`
    placeholder.
  - **Error** (online only, `S17-validation`): "This link doesn't open an image. Check it, or leave the field
    empty." It doesn't block saving: the item saves without a picture.

  Two frames were added (`S17-image-link-loading`, `S17-image-link-offline`) and the error is drawn in
  `S17-validation`. I chose this over removing the Image type from manual entry: that would drop the sample
  Desk setup product images, and with them the Product and Photo templates' examples, in screens other groups
  own. No other photo-picker or camera entry exists in S11–S21 or S39.

### Group B2: sample data, templates, sorting (S22–S26)

- **A-165** D-32 sample data for "Trip ideas" (implements A-130).
  - `trips` tr01–tr30 come from `trip-ideas.csv`.
  - Each row reuses the generated landscape image with the same number, so the scene fits the place.
  - tr13 "Alfama, Lisbon" (Portugal, Apr to Jun, €900) is the card on S25/S26.
  - tr14 "Göreme, Cappadocia" (Türkiye, Apr to May, €700) reuses ph12 and is the next card (as in
    `S40-end-round`).
  - Countries use their current English names ("Türkiye").
  - Best time is a month range ("Apr to Jun").
  - Budget is whole euros in a number field "Budget (EUR)".
  - Round 1 keeps the list's original order; tr01–tr12 are decided.
  - The `photos` dataset stays only for the retired S18 and the S02 demo images.
  - Every list carries `storage` (`backedUp` | `deviceOnly`) with `backedUp` derived from it. Both describe the
    signed-in world, where only "Frontend hiring, Q4" is `deviceOnly`; `me.guest.deviceLists` describes the guest
    world. Together with A-131, this supersedes A-106's Photo rows.
- **A-166** D-32 / A-131: the Photo template on cards and in the recommendation.
  - Photo puts a caption panel under the full image: title, subtitle, then its rows as compact label/value pairs
    (as in `S25-photo` and `S40-end-round`).
  - A number field whose name ends in a currency code in parentheses shows on cards under its name without the
    code and with the currency symbol ("Budget €900"). Item details keep the full name; edit mode labels the input "Budget" with the code
    as its suffix.
  - Recommendation order at import finish: Person (contacts, or phone/email + name) → Product (image + a
    price-like number) → Photo → Candidate → Task → Generic.
  - Photo is recommended for an Image field, the title and at most three other fields. A-131's "at most three
    other fields" is read as besides the title, so its own example qualifies. Hidden fields don't count.
  - Built-in description: "The image fills the card".
- **A-167** D-32: import finish with image links (replaces the photos partial copy in S22).
  - Images from image links (CSV, Google Sheets) are downloaded when "Start sorting" creates the list.
  - Every item is created even when a link fails. The step stays open once (`S22-import-pick-partial`): the
    summary reads "28 of 30 images downloaded.", a neutral status Alert says "2 images couldn't be downloaded" /
    "The image links in rows 14 and 27 don't open an image. Those 2 cards show without one. You can change a
    link in item details.", and the button is "Start sorting".
  - Offline, items are created at once and images download when a connection returns. Until then, cards show the
    `image-off` placeholder.
- **A-168** D-33 / A-132: "Back up this list" at the import finish step (S22 pick mode).
  - Shown only to signed-in people, never for the sample list. It is the same BackupSwitchRow as S09, placed
    under the import summary and on by default.
  - On reads "Backed up to deniz.yilmaz@example.com". Off reads "It stays on this phone only. You can back it up
    later." On the web, off reads "It stays in this browser only. Browsers can clear lists you haven't opened for
    a while."
  - The switch only sets the new list's storage mode: nothing is sent before "Start sorting", and there is no
    confirmation either way.
  - The choice survives Back, Customize and the editor, and is forgotten when the import is discarded.
  - Both positions work offline; "on" queues the upload.
  - It is offered on the web as well (one rule per account, matching S09's web switch). The browser wording
    carries the D-08 risk.
  - With the row shown, the preview shrinks to 36% so the template row stays visible.
- **A-169** D-05 (S22 part of A-88 and A-104): changing the card template of a shared list works offline and is
  queued, not blocked.
  - It applies on this phone at once, Undo works locally, and members see it once the change syncs.
  - Shared notice offline: "The new template applies on this phone now. All 3 members see it once it's synced."
  - Snackbar: "Card template changed. Saved on this phone until it syncs." with Undo.
  - Concurrent changes: the last to arrive wins (D-09 per-field rule), with no outcome message, because the
    result is visible on every card. Solo lists offline behave as online. Extends A-104.
- **A-170** D-32 (no photo library, camera or file upload): image fields in S26 edit mode.
  - A contact photo can only be removed: "Remove" plus "From Contacts. Removing it here doesn't change your
    contacts."; with no photo, "No photo in Contacts." "Revert to original" brings a removed photo back.
  - An image field from a link (CSV, Google Sheets, manual entry) is edited as its link, with S17's control
    (A-160): URL input, 36 thumbnail, the S17 helper and error.
  - The iOS image action sheet and the web "Upload image" are removed.
  - Contact photos stay exactly as they come from the source.
- **A-171** D-32: `S26-edit-date` is replaced by `S26-edit-image-link` (tr13). The Photo-template list now has no
  date field. The only other date field in the sample world, Apartment viewings › Viewing, is on an archived
  list, which is read-only. The date control (formatted value plus a `calendar` IconButton that opens the system
  picker) stays specified in S26 §3 without a frame; it has the same layout as the link input with its trailing
  button.
- **A-172** D-09 row 1 (extends A-70): a person who wasn't looking at the item learns about an overwritten edit
  from the S40 snackbar `S40-outcome-edit-replaced`.
  - View opens the item (`S26-edit-replaced`), where "Keep mine / Use Mert's" waits above the fields until
    answered.
  - "Keep mine" re-applies my value as a new edit. "Use Mert's" keeps the current value.
  - The snackbars are "Kept your edit" / "Using Mert's edit". There is one alert per replaced field.
  - If the item is open when the outcome arrives, the alert appears in place without a snackbar.
- **A-173** D-09 row 2 in S25: when the sync shows that the Owner started Round 2 while a member sorted Round 1
  offline, the existing "Deniz ended Round 1" sheet carries "Deniz started Round 2 while you were offline. Your 8
  decisions from Round 1 were saved." (`S25-round-ended`) instead of the S40 snackbar. A list that leaves the
  device while being sorted closes to Home:
  - another device turned backup off: `S40-outcome-device-only-elsewhere`;
  - the member was removed: `S40-not-found-removed` first.

### Group C: lists, round summary, global patterns (S08–S10, S27, S40)

- **A-175** D-33 (S09 Backup group). Per-list backup is a BackupSwitchRow in a "Backup" group at the end of S09,
  below Sources. It has a state icon, "Back up this list", the state as its description, and a Switch.
  - States: "Backed up to {email}" (on); "On this phone only" (off; web "On this browser only"); "Backing up…"
    (switch disabled until done); "Backs up when you're online" (turned on offline, queued); "Backup paused. It
    continues when you're online."; shared lists disabled with the footer "Shared lists are always backed up.";
    offline on a backed-up list disabled with "Turning backup off needs a connection.".
  - The off state has the footer "Lists on this phone only don't move to a new phone. Back them up first." (same
    copy as S06, A-138; mobile only).
  - Shown only to a signed-in Owner. Hidden without an account, on the sample, for members who aren't the Owner,
    and on archived lists (restore first).
  - In the header, the signed-in label "On this phone only" is plain muted text, not a link. The person chose it,
    so the header doesn't nag; the switch is the one control.
  - Extends A-132 and A-137.
  - QA round: the whole row is the switch (at least 64 high, the state line and footer or disabled reason as its
    accessible description); disabled states use `aria-disabled` with the reason.
- **A-176** D-33 (turning backup off; menus).
  - Android and web use the A-134 destructive dialog. **iOS uses an alert with stacked buttons, not an action
    sheet**, because the consequence ("can't be recovered") must be read first (A-113).
  - Progress verb "Keeping on this phone…". Failure line: "Couldn't keep “{name}” on this phone only. Check your
    connection and try again.".
  - Web copy: "Keep “{name}” in this browser only?" / "…If this browser's data is cleared, the list can't be
    recovered." / "Keep in this browser only"; snackbar "…is in this browser only".
  - On iOS the label and action keep "phone" (fixed terms), while sentences say "this iPhone" (A-137).
  - The overflow menu, the S08 row sheet and the iOS action sheet do **not** repeat the backup action. Backup is a
    state with one visible switch (S09) and one list (S06 › Backup).
  - Extends A-134.
- **A-177** D-33 (share needs backup, sheet details). The "Back up this list to share it" sheet has a 48
  `cloud-upload` mark, the A-133 sentence, one ListMoveRow ("On this phone only" → "Backing up…"), primary "Back
  up and share" and ghost "Not now".
  - When the backup is confirmed, S31 opens with the snackbar "“{name}” is backed up" (the action keeps its name).
  - "Not now" during the backup closes the sheet: the backup finishes in the background, and S31 doesn't open.
  - Offline, Share/Invite is disabled in the app bar as on any list. The sheet's offline state ("You're offline.
    Backing up and sharing need a connection. The list stays on this phone until then.", primary disabled)
    appears when the connection drops while the sheet is open.
  - The S08 row sheet's "Share list" opens the same sheet.
  - Extends A-133.
- **A-178** D-33 (where lists on this phone only appear).
  - Such a list exists on one device only. The account's other phones and the web app never list it: S08 web
    desktop and S40's desktop frames leave Frontend hiring, Q4 out.
  - The per-list label appears only on the device that holds it.
  - When another device turns backup off, this device removes the list at its next sync and shows the snackbar
    "You kept “{name}” on another device only. It's no longer on this one." once (4 s). Unsynced changes made here
    to that list are discarded with it.
  - Delete on such a list says "…will be deleted from this phone.".
  - Turning backup on needs no confirmation and shows "“{name}” is backed up" (4 s).
  - Extends A-134, A-137 and A-139.
- **A-179** D-09 row 11 (form of sync outcome messages, S40 §3.4a). An outcome the server reports is shown once.
  - When nothing was lost or it can be put back: a **snackbar** that says what happened, with View / Open when
    there is somewhere to act.
  - When the person's own work was not applied: an **inline outcome alert** (card, context icon, title, body,
    Dismiss `x`) at the top of the screen where the work would have been. That is Home when the list left the
    device. It stays until dismissed.
  - **Never a dialog.**
  - Rows of the same kind merge into one message with a count. A screen the outcome invalidates changes first
    (not-found, Collaborator view); then the message shows.
  - Outcome messages are not Activity events of their own.
  - QA round: different outcomes arriving together never point to Activity: inline alerts stack, each with its
    own Dismiss, and snackbars show one after another.
- **A-180** D-09 row 1 (overwritten edit).
  - Snackbar: "Mert changed City on Alper Turan after you, so your edit was replaced." + "View" (6 s), on any
    screen except that item. The plural form is "…changed 2 fields…".
  - View opens S26 for that item. A-70's inline "Keep mine / Use Mert's" choice waits there until answered, so a
    missed snackbar loses nothing.
  - Extends A-70.
- **A-181** D-09 rows 2 and 5.
  - Late Round 1 decisions: "Deniz started Round 2 of “{list}”. Your 8 decisions from Round 1 were saved." +
    "Open" (6 s) on Home or S09. In S25, the existing "ended Round 1" sheet carries the second sentence instead.
  - Resolutions dropped because members agreed first (A-99): "Members agreed on 2 conflicts before your
    resolutions synced. Their agreement is final." + "View" (→ S36 list view), above the S36 decision bar or on
    S09.
- **A-182** D-09 rows 4 and 6.
  - Removed while offline, with queued work rejected: the list and its data leave this phone, and Home shows the
    inline alert "You were removed from “{list}”" / "Deniz removed you while you were offline, so the 6 decisions
    you made since 9:24 weren't saved. To join again, ask Deniz for a new invite.".
  - If the list was open, `S40-not-found-removed` shows first, with the line "The 6 decisions you made since 9:24
    couldn't be saved.".
  - With nothing queued: the snackbar "Deniz removed you from “{list}”.". S38 keeps the removal event as the
    lasting record.
  - Role moved while resolving offline: "You're no longer the Decision Maker" / "Deniz made Selin the Decision
    Maker while you were offline, so your 5 resolutions weren't applied. Those conflicts are still open." It is an
    inline alert on S09, which switches to the Collaborator view, and on S36, which switches to the member view.
  - QA round: the removed state has one title everywhere, "You were removed from “{list}”"; with unsynced
    decisions the not-found screen adds the lost-decisions line (`S40-not-found-removed-unsynced`).
- **A-183** D-08 (web indicator and S09 line).
  - People without an account on the web see, under the "Lists" title: `cloud-off` "Browsers can clear lists you
    haven't opened for a while." + "Back up" (→ `S05-web-backup`, which says that signing in keeps them).
  - On S09 web, under the header meta (with or without an account): "Browsers can clear lists you haven't opened
    for a while. Back it up to keep it.".
  - S27's web backup line reads "Saved in this browser only".
  - A wiped browser database opens the first-run Home, with no error.
  - Supersedes A-81's web copy ("Lists are in this browser only").
- **A-184** D-08 (S27 web nudge).
  - After the first round finished in a browser by someone without an account, S27 shows a card once (per
    browser): "Back up your lists" / "Browsers can clear lists you haven't opened for a while. Signing in backs up
    {list} and your {n} decisions." with an outline "Back up" (→ `S05-web-backup`) and Dismiss.
  - It replaces the bottom backup line on that summary.
  - It is not shown on mobile, never as a dialog, never again after dismissing or signing in, and not for signed-in
    lists kept in this browser only.
- **A-185** D-32 (Trip ideas in lists and catalog).
  - In S08–S10 and S40, Trip ideas is a CSV list: meta "30 items from trip-ideas.csv", source row
    "trip-ideas.csv".
  - Deletes say "trip-ideas.csv isn't changed.". S40's source-line table drops the Photos and web-upload variants.
  - Rename examples: "Trip ideas" (10 / 80), the too-long name (89), renamed to "Trip ideas 2027". Duplicate
    default "Trip ideas (copy)" (17 / 80).
  - The S08 search example becomes "tr" (Trip ideas), plus a new `S08-search-archived` ("b" → Book club picks),
    because no active and archived list share a word start any more.
  - The S40 Photo-template card shows Place, Country, Best time and Budget (Alfama, Lisbon / Portugal / Apr to Jun
    / €900).
  - "Old phone screenshots" in the many-lists example becomes "Board games to buy".
  - Extends A-130.
- **A-186** D-05 (S09/S10 part of an updated A-88).
  - Offline, these work and sync later: Rename (solo and shared; queued, the latest to arrive wins), Duplicate,
    Archive/Restore/Delete of solo lists, and on any list Card template and Add items from local sources.
  - These need a connection and are disabled with "Needs a connection": Invite/Share, joining, Google Sheets
    import and export, Start a new round on a shared list, the Conflict rule, member changes, shared Archive,
    shared Restore, Delete for everyone and Leave.
  - On a list on this phone only, Share and turning backup off need a connection; turning backup on is queued.
  - Shared list status shows "As of 9:24".
  - Supersedes A-88's S09/S10 part.
- **A-187** D-33 / A-136 / A-138 (S40 copy).
  - `S40-sign-out` reads "Lists backed up to {email} are removed from this phone until you sign in again." +
    "“Frontend hiring, Q4” stays on this phone, hidden until you sign in again.". Without such lists, the old
    sentence stays.
  - `S40-delete-account` counts "Your other 4 lists (2 of them archived)" and adds "“Frontend hiring, Q4” is on
    this phone only. It stays on this phone, without an account.".
  - Implements A-136 and A-138 in the catalog.

### Lead decisions from QA

- **A-188** D-32 (no photo-library or camera access, extended to the profile): S07 no longer offers "Take
  photo", "Choose from gallery" or web "Upload photo". The profile photo comes from the Google account when one is connected (Apple shares no photo), otherwise initials; S07 offers "Remove photo", then "Use Google photo" to bring it back ("Connect Google to use its photo." when no account photo exists); frame IDs `S07-change-photo`, `S07-photo-uploading`, `S07-no-photo`, `S07-web-change-photo` are kept and relabeled. Supersedes the photo
  actions in A-53's profile. Reason: D-32 says "no photo-library access at all for now", and a camera or
  gallery path would add a permission and a Data safety entry for a cosmetic feature.
