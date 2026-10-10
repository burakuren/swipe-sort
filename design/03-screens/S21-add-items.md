# S21 Add items to an existing list

Frames: `S21-add-items.html`. Generator: `tools/generators/S21-add-items.py`. Reuses S11 tiles, S13–S18 select
steps and S20 (`S20-existing`).

## 1. Purpose and requirements

Add items to a list that already exists, from any source, without starting over. It is the same import flow
with list context: columns are matched to the list's existing fields, rows are checked against items already
in the list, and the new items join the current round so every member sorts them. A list can combine any
number of sources.

Covers: SRC-18, SRC-19, SRC-03, SRC-04, SRC-07, SRC-08, SRC-14, SRC-15, SRC-24
(partial), PLT-07, PLT-08, PLT-11 (web), DM-02, DM-16 (new items join the current round), COL-16, GOAL-03,
GOAL-04, GOAL-05, VIS-12, VIS-13, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-07, TERM-01, SCR-21.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S09 List overview | "Add items" (overflow menu and the Sources section) → `S21-default` |
| S11 | not used; S21 shows its own source grid with list context |

| To | How |
| --- | --- |
| Select step per source | CSV or Excel → `S21-file`; Contacts → S13 (`S13-select-default`, permission already granted for this list); Google Sheets → S15; Plain text → S16; Manual entry → S17 Add items (fields come from the list, Set up fields is skipped); Photos → S18 (`S18-web` on web) |
| Map fields | `S21-mapping` (all column sources) |
| Review duplicates | `S20-duplicate-review.html#S20-existing` |
| Confirm | `S21-confirm` → Add to list → `S21-adding` → S09 with snackbar (`S21-success`) |
| Partial | `S21-partial` → Done → S09 |
| Close | `x` → back to S09; if a file was chosen, "Discard adding items?" dialog (`S40-global-patterns.html#S40-discard-add-items`) |

## 3. Layout and components

Full-screen modal (`list/[listId]/add`). AppBar (modal) with close `x` and title "Add items"; ImportStepper with
steps Choose source, Select items, Map fields, Review duplicates, Add to list (5; steps a source doesn't need are
removed, e.g. manual entry: Choose source, Add items, Add to list).

1. **Choose source** (`S21-default`): `text-title-2` "Add items to Wedding guests", explanation; "In this list
   now" group (one row per current source with its item count); "Add from" SourceTile grid (same tiles and
   order as S11; a new source is one more tile); footnote about combining sources.
2. **Select items** (`S21-file`): file row (icon, name, rows and columns, "Change"), first rows preview group.
3. **Map fields** (`S21-mapping`, Proposed component **ColumnMatchRow**): header "Column in the file" / "Field in
   the list"; each row: column name + sample values (left 40%), Select of the target field (right) with the
   field type icon; new columns show a "New" badge and "New field" as the target, with the note that existing
   items leave it empty. Footnote for list fields without a column ("Photo has no column…").
4. **Confirm** (`S21-confirm`): `text-title-2` "Add 12 items to Wedding guests"; summary ListGroup (new items,
   matches with existing items, new fields, round, card template); shared-list notice (Alert info with member
   avatars); primary "Add to list".
5. **Adding** (`S21-adding`): same layout, primary button busy "Adding 12 items…", determinate progress
   "7 of 12 added".
6. **Success**: the real S09-shared screen (embedded from `S09-list-overview.html`) with Snackbar "Added 12 items"
   + Undo; S09's Recent activity gets "You added 12 items from mert-family.csv". S09 has no sources section, so the
   new source ("mert-family.csv, 12 items, added just now") is listed in S10 › list details / S09 overflow "Sources"
   (Group B to confirm); the item count in the S09 header reads 100 items.
7. **Partial** (`S21-partial`): result screen with error icon, title, list of rows not added with reasons,
   primary "Done", ghost "Add the file again".

## 4. States

| Frame | Trigger |
| --- | --- |
| `S21-default` | "Add items" on Wedding guests (shared, Round 1 in progress, 88 contacts) |
| `S21-file` | CSV or Excel tile → system file picker (out of scope) → mert-family.csv: 15 rows, 7 columns |
| `S21-mapping` | Columns matched by name and type (E-mail → Email); Address has no field → New field |
| `S21-field-select` | Target select of Address: New field, Don't import, or any list field |
| `S21-mapping-error` | The name column has a header SwipeSort can't match ("Ad Soyad"): Name has no column |
| `S20-existing` (in S20) | 3 rows match items already in the list (c003 Zeynep Kaya, c009 Oğuz Kılıç, c023 Onur Keskin) |
| `S21-confirm` | After review: 12 new items, 2 merged, 1 skipped, 1 new field, shared notice |
| `S21-adding` | "Add to list" tapped |
| `S21-success` | Done: back on S09-shared, snackbar "Added 12 items" with Undo |
| `S21-success-activity` | S09-shared scrolled: "You added 12 items from mert-family.csv", "Just now" at the top of Recent activity |
| `S21-partial` | 2 rows couldn't be read: "Added 10 of 12 items" |
| `S21-offline` | No connection: Google Sheets tile unavailable; local sources work |
| `S21-web` | Web: Contacts tile unavailable with "Get the app"; Photos becomes upload |
| `S21-ios`, `S21-ios-confirm` | iOS bar and back chevron |
| `S21-large-text` | 200% font scale on the confirm step |

## 5. Interactions, gestures and transitions

- **Source tiles** navigate to that source's select step with list context (the app bar keeps "Add items").
- **Matching**: a column matches a list field by name (case and accent folding, common synonyms such as
  "E-mail" → Email, "Mobile" → Phone) and then by type. Unmatched columns default to **New field** (type
  detected as in S19). The title field must have a column; otherwise the error alert offers the best guess
  ("Use Ad Soyad for Name").
- **Target select** (sheet on Android, pull-down menu on iOS, popover on desktop web): New field, Don't import,
  or any list field. Choosing a field already used by another column swaps them and shows "Phone was already
  filled by Mobile. Mobile is now Don't import."
- **New fields** are added to the list schema; existing items leave them empty; they are not added to the card
  template automatically (shown in item details; the confirm screen says so).
- **Duplicates** use `S20-existing`: Skip (default for identical rows), Merge (fills empty fields and adds new
  field values; keeps decisions, notes, edits), Keep both (adds a new item).
- **Add to list**: writes locally first, then syncs. New items get `addedInRoundId` = current round and appear
  at the end of the round's order (shuffled rounds: inserted at random positions among undecided items).
  Every member's progress total increases (76 / 88 → 76 / 100). Members get an activity event "Deniz added 12
  items to Wedding guests" (S38) and, on mobile, a push if enabled.
- **Undo** (snackbar, 6 s): removes the added items and the new field, restores merged items' previous values;
  available until the snackbar closes or someone decides one of the new items.
- **Partial**: rows that can't be read are listed with their row number and reason; the rest are added.
- **Offline**: local sources (contacts, files, text, manual, photos) work; Google Sheets is unavailable with
  "Needs a connection". On a shared list, items added offline sync later; the banner says so.
- Motion: standard import transitions (M3 shared axis X between steps, 300 ms); progress bar 250 ms;
  snackbar per motion.md. Reduced motion: fades.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Add items"; close "Close adding items" |
| Stepper | "Choose source", "Select items", "Map fields", "Review duplicates", "Add to list"; "Step 1 of 5" |
| Choose source | "Add items to Wedding guests"; "New items join Round 1, so every member sorts them. Decisions already made stay as they are."; "In this list now"; "Contacts" / "88 items"; "Add from"; "A list can combine items from any of these sources." |
| Tiles | "Contacts" / "From this phone"; "CSV or Excel" / "A .csv or .xlsx file"; "Google Sheets" / "From Google Drive"; "Plain text" / "Paste a list or a .txt file"; "Manual entry" / "Type items one by one"; "Photos" / "From your gallery" (iOS: "From your photo library", as S11-ios) |
| File | "mert-family.csv"; "15 rows, 7 columns"; "Change"; "First rows"; "Showing 4 of 15 rows. Every row is added; you can review matches in the next steps." |
| Map fields | "Match the 7 columns in mert-family.csv to fields in Wedding guests."; "Column in the file"; "Field in the list"; badge "New"; target "New field"; "Items already in the list leave it empty."; "Photo has no column in this file. New items show initials instead."; select a11y "Address goes to: New field. Change" |
| Target sheet | "Address goes to"; "Column in mert-family.csv"; "New field: Address" / "Added to every item; existing items leave it empty"; "Don't import" / "The column is left out"; "Name" / "Title. Already filled by Name"; "Already filled by {column}"; "No column yet"; swap note "Phone was already filled by Mobile. Mobile is now Don't import." |
| Mapping error | "Name has no column"; "Every item needs a title. Choose the column that holds the names."; "Use Ad Soyad for Name" |
| Confirm | "Add 12 items to Wedding guests"; "12 new items" / "From mert-family.csv"; "3 rows match items already in the list" / "2 merged, 1 skipped. Their decisions and notes stay."; "1 new field: Address" / "Items already in the list leave it empty."; "New items join Round 1" / "Every member sorts them. Decisions already made don't change."; "Cards use the Person template" / "Address shows in item details. Add it to cards in Card template." |
| Shared notice | "Mert and Selin will see 12 new items to sort"; "They get a notification. Their progress counts the new items." |
| Buttons | "Continue"; "Add to list"; busy "Adding 12 items…"; "7 of 12 added. You can leave; adding continues." |
| Success | Snackbar "Added 12 items" + "Undo"; undo result "Removed 12 items"; activity on S09 "You added 12 items from mert-family.csv" / "Just now"; source entry wherever sources are listed: "mert-family.csv" / "Added just now" / "12 items" |
| Partial | "Added 10 of 12 items"; "2 rows in mert-family.csv couldn't be added. The other 10 are in Wedding guests and join Round 1."; "Not added"; "Row 9" / "Has 9 values but the file has 7 columns."; "Row 14" / "Has characters that can't be read. Save the file as UTF-8."; "Fix these rows in the file and add it again. Rows already in the list show up as duplicates, so nothing is added twice."; "Done"; "Add the file again" |
| Offline | Banner under the app bar (as in S11-offline) "You're offline. Google Sheets needs a connection; other sources work. Items you add sync to Mert and Selin later."; tile "Google Sheets" / "Needs a connection" |
| Web | Tile "Contacts" / "Needs the Android or iOS app"; "Upload photos" / "Image files from this device" (same tile as S11-web); "Contacts import needs the Android or iOS app." + "Get the app" |
| Discard dialog (`S40-global-patterns.html#S40-discard-add-items`) | "Discard adding items?" / "Your choices for mert-family.csv will be lost. Nothing has been added to Wedding guests yet." / "Keep adding", "Discard" |
| Activity (S38) | "Deniz added 12 items to Wedding guests" |
| Solo list confirm | the shared notice is omitted; "New items join Round 1" reads "You'll sort them in Round 1." |

## 7. Accessibility

- Focus order follows the visual order; the stepper is a progressbar named "Step 3 of 5, Map fields".
- Unavailable tiles are buttons with names that include the reason ("Contacts, needs the Android or iOS app",
  "Google Sheets, needs a connection"); the explanation text is never dimmed with opacity.
- Column rows: the select's name includes the column and the current target.
- The adding progress is a progressbar plus a polite status line; success snackbar `role="status"`; partial
  result title is a heading with an error icon (icon + text).
- Large text (`S21-large-text`): summary rows wrap; the title wraps to two lines; button grows to 64.
- Touch targets ≥ 48 (tiles 112 high).

## 8. iOS and web differences

- **iOS** (`S21-ios`, `S21-ios-confirm`): 44 pt bar; first step has close `x` at the left; later steps show
  "Back" with edge-swipe back and close at the right. Target selects are pull-down menus; the discard
  confirmation is an action sheet.
- **Web** (`S21-web`): Contacts tile visible but unavailable (dashed, `monitor-smartphone`, reason, "Get the
  app"); Photos uploads files (S18-web). Desktop: centered column, same steps; selects are popovers.

## 9. Edge cases

- **Columns that match nothing and aren't wanted**: set to Don't import; nothing changes in the list.
- **More than 50 fields in total** after adding: new columns beyond the limit are set to Don't import with the
  note "This list has 50 fields, the most a list can have."
- **Type mismatch** (column of text mapped to a Number field): values that don't fit are kept as text and the
  row shows "3 values don't fit Number".
- **Archived or read-only list**: "Add items" is hidden on archived lists (S10).
- **Collaborator adding** on a shared list: allowed (domain-model permissions: Change template, add items); the
  activity event names them.
- **Round already complete**: new items start undecided; S09 offers "Sort 12 new items" (a new round with them
  preselected, S24 custom selection).
- **Very large additions** (5,000 rows): same limit as imports; adding runs in the background with progress on
  S09.
- **Same file added twice**: every row matches an existing item; Skip all identical leaves the list unchanged
  and the confirm step reads "No new items to add" with Done.
