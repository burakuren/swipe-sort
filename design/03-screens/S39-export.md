# S39 Export flow

Frames: `S39-export.html` (generator: `tools/generators/S39-export.py`, helpers from `group_e_common.py`).
Data: `lists` l-desk, l-wedding, l-apartments, l-candidates; `products` p01–p20 with `productDecisions`
round1 + round2 (latest decision per item, A-33); `shared.items`, `shared.notes`, `members`; `apartments`
a01–a08 (Google Sheets source "Flat hunt 2026", tabs Kadıköy and Beşiktaş); `me.signedIn`
(deniz.yilmaz@example.com) for Desk setup and Apartment viewings; `members` u-mert (mert.aydin@example.com, Decision
Maker) for every `S39-shared*` frame, because in Flow 3 Mert exports right after his bulk resolve.

## 1. Purpose and requirements

Get decisions out of SwipeSort in the form people need: a file for a spreadsheet app, a Google Sheet, or a
short text to paste into a message. Exports are always copies; the original source changes only when the
user picks it as the destination and confirms exactly what will be written.

Covers: EXP-01 (CSV), EXP-02 (Excel), EXP-03 (Google Sheets), EXP-04 (plain-text summary), EXP-05 (all items
or only Accept, Reject, Maybe or Conflict items), EXP-06 (decisions and notes), EXP-07 (each member's
decision on shared lists), EXP-08 (success), EXP-09 (failures), EXP-10 (Google write confirmation),
SAFE-01, SAFE-05, SAFE-06, DM-01 (solo: my decision is final), DM-04, DM-08, DM-09 (final decision column on
shared lists), RES-05 (final vs. member decisions in the export), A-33 (latest decision per item),
TERM-01, PLT-03/PLT-04 (iOS, web), SCR-39.

## 2. Entry points and exits

S39 is a full-screen modal stack (`list/[listId]/export`). It opens over its origin and returns there.

| From | How | Frame |
| --- | --- | --- |
| S28 Results | "Export" in the app bar (Flow 2, Desk setup). The current segment preselects the scope (Maybe segment → Maybe) | `S39-default` |
| S27 Round summary | "Export" row | `S39-default` (solo) / `S39-shared` |
| S37 Bulk resolve summary | "Export" (Flow 3, Wedding guests) | `S39-shared` |
| S09 List overview | "Export" action (also on archived, read-only lists) | `S39-default`, `S39-apartments` |

| To | Trigger | data-action |
| --- | --- | --- |
| Exporting sheet → file ready sheet | "CSV file" / "Excel file" row | `format-csv`, `format-excel` |
| `#S39-google-destination` (solo list not from Google Sheets) / `#S39-shared-google-destination` (shared list) / `#S39-apartments-destination` (list from Google Sheets) | "Google Sheets" row | `format-google` |
| `#S39-success-shared` → `S09-list-overview.html#S09-shared` | "Export to Google Sheets" on the shared confirmation, then "Done" | `confirm-write`, `done` |
| `#S39-google-not-connected` | "Google Sheets" row when no Google account is connected on this device | `format-google` |
| `#S39-text-summary` | "Text summary" row | `format-text` |
| `#S39-google-confirm` | "Continue" on the destination step | `continue` |
| `#S39-success-google` | "Export to Google Sheets" on the confirmation (after Google's permission, when needed) | `confirm-write` |
| System share sheet / save dialog (native, out of scope) | "Share file", "Save to device", "Share summary" | `share-file`, `save-file`, `share-summary` |
| Google Sheets app or browser | "Open in Google Sheets" | `open-sheet` |
| Origin (S28, S27, S37 or S09) | Close `x`, "Done", Android back on step 1 | `close`, `done` |

Prototype flows (navigation-map §6):
- **Flow 2**: `S28-default` [`export`] → `S39-default` [`format-google`] → `S39-google-destination`
  [`continue`] → `S39-google-confirm` [`confirm-write`] → `S39-success-google` [`done`] → `S28-default`.
- **Flow 3** (Mert, Decision Maker): `S37-summary` [`export`] → `S39-shared` [`format-google`] →
  `S39-shared-google-destination` [`continue`] → `S39-shared-google-confirm` [`confirm-write`] →
  `S39-success-shared` [`done`] → `S09-shared`. Wedding guests data and Mert's Google account throughout;
  the Flow 2 chain is separate and unchanged.
- File path (not a numbered flow): `S39-accepted` [`format-csv`] → `S39-file-exporting` → `S39-file-ready`
  [`share-file`] → `S39-success-file`.

## 3. Layout and components

Full-screen modal; no bottom navigation. Two levels at most: step 1 decides everything a file needs;
Google Sheets adds a destination step and a confirmation step; Text summary adds a preview.

**Step 1, Export** (`S39-default`):
1. **AppBar (modal)**: close IconButton (`x`, "Close export"), title "Export", list name as subtitle.
2. **Items**: section header + scope chips (radiogroup, wrap). Chips use the DecisionSegments look
   (components.md): 36 high inside a 48 hit area, `rounded-full`, icon + label + count (`tabular-nums`);
   unselected `border-input bg-card` with the decision icon in its soft-foreground color, selected
   `bg-foreground text-background`. Order: All items, then Rejected, Maybe, Accepted (decision order), then
   Conflicts (shared lists only). Helper line under the chips explains which decision counts ("Each item
   has its latest decision from 2 rounds." / shared: "Counts are final decisions…").
3. **Columns**: ListGroup of switch rows (whole row toggles, M3 switch). Solo: Notes (on), Each round's
   decision (off; only when the list has 2+ rounds). Shared: Each member's decision (on), Notes (on).
   Footer: what is always included.
4. **Export as**: ListGroup of format rows (icon 24 in `text-primary`, title, one-line description).
   CSV and Excel act at once (no chevron); Google Sheets and Text summary open a step (chevron). Same
   visual language as the S11 source tiles: import picks a source, export picks a format.
5. **Safety line**: `shield-check` + "Exporting creates a copy. Nothing in Desk setup changes." (SAFE-01).

**File ready sheet** (BottomSheet, `rounded-t-sheet`, `shadow-sheet`): title, file card (file icon on a 40
`primary-soft` square, file name, "8 items, 1 KB"), the column list, primary "Share file" (`share-2`),
outline "Save to device" (`download`). The exporting state is the same sheet with a spinner.

**Text summary** (pushed): back AppBar, "Preview" header, the text in a `rounded-group bg-card` block
(rendered exactly as it will be shared, body text, bold headings), footer explaining what is listed,
bottom bar with primary "Share summary" and outline "Copy text".

**Google destination** (pushed): back AppBar "Export to Google Sheets" + list name.
- Lists not from Google Sheets: "New spreadsheet" with a Name input (default "{List name} decisions") and a
  footer explaining why it's the only destination.
- Lists from Google Sheets: "Write to" radiogroup in a group: New tab in {spreadsheet} (default, with a
  nested "Tab name" input, default "Decisions"), New columns in {spreadsheet}, New spreadsheet.
- **Google account** row (avatar 40, email, "Signed in with Google", "Switch" → S15 account sheet).
- **Columns** preview (Proposed component: ColumnPreview): "Your fields" as outline chips (`rounded-sm`),
  "Added by SwipeSort" as `primary-soft` chips with `plus`, plus one line on rows and values.
- Bottom bar: primary "Continue".

**Google confirmation** (pushed; Proposed component: WriteConfirmation): title as the action question
(`text-title-2`), lead "Nothing is written until you confirm.", a fact group (rows: icon 20 muted, label
`text-label`, value `text-body muted`): Creates / Adds / Writes, per-tab column letters, "Doesn't change",
"Not exported" (shared), "Checked first" (new columns). Info Alert (`primary-soft`, `shield-check`) "Google
asks for permission next" only when the needed write scope isn't granted yet. Bottom: primary "Export to
Google Sheets" / "Export to {spreadsheet}", ghost "Back". Full screen rather than a dialog: the content is
too long for a dialog and needs to stay readable at 200%.

**Exporting / success / failure**: centered state (56 circle with icon, `text-title-2` or `text-title-1`
title, one or two sentences, `max-w-xs`), bottom actions. Success icon is `circle-check` on `primary-soft`
(never accept green: decision colors mean decisions only). Failure icon on `muted` with `text-destructive`.
Partial failure adds a per-tab status group.

Components: AppBar (modal, back, iOS), FilterChip/DecisionSegments (scope), ListGroup + switch rows,
format rows (ListRow variant), RadioGroup rows, Input, Avatar, Alert (info), BottomSheet, Snackbar,
Button (primary, outline, ghost), EmptyState/ErrorState pattern, OfflineBanner, Spinner. Proposed:
**ColumnPreview**, **WriteConfirmation** (fact rows), **FileCard** (also usable by S14).

### What an export contains

| | Solo list | Shared list |
| --- | --- | --- |
| Rows | One per item in the chosen scope, in the list's original order | Same |
| Field columns | Every field of the list, in field order, including hidden fields; working-copy values (edits applied). Image fields are left out (no file to put in a cell). Multi-value fields joined with "; " | Same |
| Decision columns | "Decision": Accepted / Rejected / Maybe / Not decided. With "Each round's decision": "Round 1", "Round 2"… (empty when the item wasn't in that round) | "Final decision": Accepted / Rejected / Maybe / Conflict / Pending. With "Each member's decision": "Decision (Deniz Yılmaz)", "Decision (Mert Aydın)", "Decision (Selin Yılmaz)" (Owner first, then join order); empty when not decided |
| Notes | "Notes": my note | "Notes": every shared note as "Deniz: Mum insists. Seat near the family table.", several separated by a line break. Private notes are never exported, not even the exporter's own |
| Google Sheets source | "Tab" column first when the list combined tabs | — |

File names: `{list-name}-{scope}.csv|.xlsx`, lowercased, Turkish letters transliterated, spaces to hyphens
(`desk-setup.csv`, `desk-setup-accepted.csv`, `desk-setup-maybe.csv`, `-rejected`, `-conflicts`). CSV is
UTF-8 with BOM (Excel shows ğ, ş, ı correctly), comma-separated, header row. Excel: one sheet named after
the list (31 characters max), header row bold and frozen. Google Sheets values are written as plain values
(no formulas: `valueInputOption=RAW`).

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S39-default` | Desk setup after Round 2: All items 20, Rejected 11, Maybe 1, Accepted 8; Notes on; Each round's decision off; four formats | Export from S28 (Flow 2), S27, S09 |
| `S39-accepted` | Accepted (8) chosen | Tap the Accepted chip; or entry from the S28 Accepted segment |
| `S39-shared` | Wedding guests (shared), Mert exporting after his bulk resolve: All items 100, Rejected 10, Maybe 6, Accepted 28, Conflicts 3; Each member's decision on, Notes on | Export from S37 summary (Flow 3), S27-shared, S28-shared |
| `S39-apartments` | Apartment viewings (archived, from Flat hunt 2026): 8 / 4 / 1 / 3; Google row offers the original sheet | Export from the archived list's overview |
| `S39-empty-scope` | Frontend hiring, Q4: Maybe 0 selected; "No items in Maybe…"; formats unavailable | Entry from an empty Results segment, or choosing a chip with 0 |
| `S39-offline` | Offline banner; Google Sheets row unavailable ("Needs a connection"); files and text work | No connection |
| `S39-large-text` | 200% font scale: larger chips and rows, wrapping; the screen scrolls | Font scale ≥ 150% |
| `S39-file-exporting` | Sheet "Exporting…", "8 items to desk-setup-accepted.csv" | CSV/Excel tapped and writing takes over 300 ms |
| `S39-file-ready` | Sheet "Your file is ready" with Share file / Save to device | File written |
| `S39-success-file` | Back on step 1, snackbar "Exported 8 items to desk-setup-accepted.csv" | Share target chosen or file saved |
| `S39-error-file` | Sheet "Couldn't export", storage full, Try again | File couldn't be written |
| `S39-text-summary` | Preview of the summary; Share summary, Copy text | Text summary row |
| `S39-text-copied` | Snackbar "Summary copied" | Copy text |
| `S39-google-destination` | Desk setup: new spreadsheet "Desk setup decisions", account, columns | Google Sheets row (connected) |
| `S39-google-confirm` | "Export 20 items to a new spreadsheet?" with facts and the permission lead-in | Continue |
| `S39-google-exporting` | "Exporting…" "Writing 20 rows to Desk setup decisions." | Confirmed, permission granted |
| `S39-success-google` | "Exported to Google Sheets", Open in Google Sheets, Done | Write finished |
| `S39-shared-google-destination` | Wedding guests (Contacts + mert-family.csv, so New spreadsheet only, with the same explanation line as Desk setup): name "Wedding guests decisions", Mert's account, columns preview with Final decision, Decision (Deniz Yılmaz / Mert Aydın / Selin Yılmaz) and Notes | Google Sheets row on a shared list (Flow 3) |
| `S39-shared-google-confirm` | "Export 100 items to a new spreadsheet?": Creates in mert.aydin@example.com's Drive; Writes 100 rows with member columns and shared notes, private notes not exported; Who sees it; Doesn't change; permission lead-in (`drive.file`) | Continue on the shared destination |
| `S39-success-shared` | "Exported to Google Sheets", Wedding guests decisions in mert.aydin@example.com, Open in Google Sheets, Done → S09-shared | Shared write finished (Flow 3 end) |
| `S39-apartments-destination` | Write to: New tab (default, tab name "Decisions"), New columns, New spreadsheet | Google Sheets row on a list imported from Google Sheets |
| `S39-apartments-confirm-tab` | "Add a tab to Flat hunt 2026?" + permission lead-in (edit scope) | Continue with New tab |
| `S39-success-tab` | "Exported to Google Sheets", new tab Decisions | Tab written |
| `S39-apartments-confirm-columns` | "Add 2 columns to Flat hunt 2026?" columns G and H per tab, rows 1 to 5; what doesn't change; row check | Continue with New columns |
| `S39-google-not-connected` | Connect explainer (creates new spreadsheets; doesn't sign you in) | Google Sheets row, no Google account connected on this device |
| `S39-error-permission` | "SwipeSort can't write to Google Sheets" | Google consent declined or closed |
| `S39-error-network` | "Couldn't export to Google Sheets", nothing written | Timeout / 5xx / connection lost before the first write |
| `S39-error-sheet-missing` | "Flat hunt 2026 can't be found" | 404 or 403 on the original spreadsheet (deleted, trashed, unshared) |
| `S39-error-sheet-changed` | "Rows in Kadıköy have changed" | Row check fails before writing new columns (rows added, moved, deleted or tab renamed) |
| `S39-error-partial` | "Exported 4 of 8 items": Kadıköy done, Beşiktaş protected | One tab's write fails after another succeeded |
| `S39-ios` | iOS page sheet, `x` and centered title | iOS |
| `S39-ios-share` | CSV goes straight to the iOS share sheet; drawn only as a labeled system-UI placeholder (out of scope) | iOS, CSV/Excel tapped |
| `S39-ios-text` | iOS text summary with "Back" | iOS |
| `S39-web-desktop` | Desktop: formats say "Downloads…"; toast bottom-right (`w-80`, 6 s, pauses on hover/focus, A-117) after download | Desktop browser |
| `S39-web-google-popup` | Waiting for the Google permission popup | Desktop browser, Google write permission needed |

Not separate frames (spec only): Excel uses the CSV frames with `.xlsx`; the solo Google not-yet-granted
lead-in on the shared confirmation; the token-expired case (silent refresh; failure shows
`S39-google-not-connected` with "Connect again"); the web mobile Google redirect.

## 5. Interactions and transitions

- **Step 1 is a settings screen with the formats as actions.** Scope and columns apply to every format
  and persist per list (last choice remembered, except a scope preset by the entry point). Changing the
  scope updates the counts in Text summary and the file name.
- **CSV / Excel**: tap → the file is written on the device (local data; works offline). Under 300 ms no
  progress is shown; otherwise the sheet shows "Exporting…" (spinner). Then:
  - Android: "Your file is ready" sheet. **Share file** opens the system share sheet
    (`Intent.ACTION_SEND` with a FileProvider URI, chooser with an IntentSender callback). **Save to
    device** opens the system save dialog (`ACTION_CREATE_DOCUMENT`) with the file name prefilled.
  - iOS: no sheet; the share sheet (`UIActivityViewController`) opens directly; it includes Save to Files.
  - Web: the file downloads immediately (Blob + `download` attribute).
  - Success: when a share target is chosen, the file is saved, or (web) the download starts, the sheet
    closes and the snackbar "Exported 8 items to desk-setup-accepted.csv" shows (4 s). Cancelling the share
    sheet returns to the file-ready sheet without a message. Light success haptic is not used; only errors
    have haptics (motion.md §5).
- **Text summary**: preview is rendered from the scope. Share summary opens the system share sheet with
  plain text (web: Web Share API when available, otherwise the button reads "Copy text" only). Copy text
  copies to the clipboard and shows "Summary copied". After sharing: snackbar "Summary shared".
- **Google Sheets**:
  1. Not connected on this device → `S39-google-not-connected`; "Connect Google account" opens the Google
     account chooser (native) asking only for `drive.file`; then the destination step.
  2. Destination: Continue is enabled when the name (or tab name) is not empty. Name max 100 characters.
  3. Confirmation: nothing is written before **Export to Google Sheets**. If the needed scope isn't
     granted, Google's consent opens next (incremental authorization, `include_granted_scopes=true`):
     `drive.file` for a new spreadsheet (SwipeSort can only open files it created), `spreadsheets` for a
     new tab or new columns in an imported sheet (the import granted read-only access, S15). The lead-in
     Alert says which. Granted scopes are remembered; the Alert then disappears
     (`S39-apartments-confirm-columns`).
  - When the user signed in to SwipeSort with Google (Mert, Flow 3) but never connected Google Sheets, the
    destination preselects that sign-in account ("Signed in with Google") and the
    connect explainer is skipped: the only grant needed is `drive.file`, asked at the confirmation with
    the account preselected (`login_hint`). Users without a Google sign-in or connection get
    `S39-google-not-connected`.
  4. Exporting: writes in one `batchUpdate` per spreadsheet (new spreadsheet: create + values; new tab:
     addSheet + values; new columns: one update per tab, header in row 1). Before writing columns,
     SwipeSort re-reads the tab and checks every row still has the same title-field value at the same row
     number as at import; any mismatch stops before writing (`S39-error-sheet-changed`). Existing non-empty
     cells are never overwritten: new columns go after the last used column.
  5. Success: "Open in Google Sheets" opens the spreadsheet URL (Sheets app if installed, else browser), at
     the new tab when one was added. "Done" returns to the origin.
- **Back**: Android back / iOS edge swipe goes back one step; on step 1 it closes the modal. During
  "Exporting…" back is ignored for Google writes (they finish in seconds); for files it cancels.
- **Transitions**: steps push with the M3 shared axis X (300 ms) / iOS native push; sheets 300 ms
  emphasized decelerate; snackbar 250 ms. Reduced motion: fades only (150 ms); the spinner becomes a
  static `loader-circle` with the "Exporting…" text.
- **Haptics**: `notificationAsync(Error)` on any failure (Android, iOS). None on web.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Export"; subtitle = list name ("Desk setup", "Apartment viewings", "Frontend hiring, Q4"); close label "Close export"; back label "Back to Export" |
| Items header | "Items" |
| Scope chips | "All items 20", "Rejected 11", "Maybe 1", "Accepted 8", "Conflicts 3"; accessible names "All items, 20 items", "Maybe, 1 item" |
| Items helper | Solo after 2+ rounds: "Each item has its latest decision from 2 rounds."; one round: "Decisions from Round 1."; shared: "Counts are final decisions. Pending items are only in All items." |
| Empty scope | "No items in Maybe. Choose another group to export." (also "No items in Rejected…", "No items in Accepted…", "No conflicts. Choose another group to export.") |
| Columns header | "Columns" |
| Switch rows | "Notes" / "Adds a Notes column"; "Each round's decision" / "Adds Round 1 and Round 2 columns"; shared "Each member's decision" / "Adds a column for Deniz, Mert and Selin"; "Notes" / "Shared notes with their author" |
| Columns footer | Solo "All fields and a Decision column are always included."; shared "All fields and a Final decision column are always included. Private notes are never exported." |
| Export as header | "Export as" |
| Format rows | "CSV file" / "Opens in any spreadsheet app" (web "Downloads a .csv file"); "Excel file" / "For Excel and Numbers" (web "Downloads an .xlsx file"); "Google Sheets" / "A new spreadsheet in Google Drive" (from Google Sheets: "Add to Flat hunt 2026, or a new spreadsheet"); "Text summary" / "Counts and accepted items as text" |
| Offline | Banner "You're offline. Decisions are saved on this phone. Google Sheets needs a connection." (A-115; files and text summaries keep working); Google row "Needs a connection" |
| Safety line | "Exporting creates a copy. Nothing in Desk setup changes."; Google source "Exporting creates a copy. Flat hunt 2026 changes only if you choose it and confirm."; shared "Exporting creates a copy. Nothing in Wedding guests changes for anyone." |
| File exporting | "Exporting…" / "8 items to desk-setup-accepted.csv" |
| File ready | "Your file is ready"; file meta "8 items, 1 KB"; "Columns: Name, Price, Rating, Reviews, Store, Category, Link, Decision and Notes."; "Share file"; "Save to device"; close label "Close" |
| File success | "Exported 8 items to desk-setup-accepted.csv" (one item: "Exported 1 item to …") |
| File failure | "Couldn't export" / "This phone is out of storage. Free up some space and try again." / "Try again"; other file errors: "This file couldn't be saved there. Choose another place and try again." |
| Text summary | Title "Text summary"; header "Preview"; footer "Lists accepted and Maybe items. Rejected items are counted, not listed." (scope Rejected: "Lists rejected items."); "Share summary"; "Copy text"; snackbars "Summary copied", "Summary shared" |
| Summary text (sample) | "Desk setup" / "20 items after 2 rounds: 11 rejected, 1 maybe, 8 accepted." / "Accepted (8)" / "- Ergo Mesh task chair (€389)" … / "Maybe (1)" / "- Bookshelf speakers, pair (€249)". Item line = title + the card template's price or subtitle in parentheses. Shared lists use final decisions and add "3 conflicts and 53 pending items aren't listed." |
| Destination (new) | Title "Export to Google Sheets"; "New spreadsheet"; label "Name", default "Desk setup decisions"; footer "Desk setup wasn't imported from Google Sheets, so SwipeSort creates a new spreadsheet." |
| Destination (source) | "Write to"; "New tab in Flat hunt 2026" / "All 8 items on their own tab. Your tabs don't change."; label "Tab name", default "Decisions"; "New columns in Flat hunt 2026" / "Decision and Notes next to your rows in Kadıköy and Beşiktaş"; "New spreadsheet" / "A separate copy in your Google Drive" |
| Account | "Google account"; "deniz.yilmaz@example.com" / "Signed in with Google" / "Switch" (label "Switch Google account"); shared: "mert.aydin@example.com" / "Signed in with Google". One sublabel everywhere; it never says read-only on a step that writes |
| Destination (shared) | "New spreadsheet"; label "Name", default "Wedding guests decisions"; footer "Wedding guests wasn't imported from Google Sheets, so SwipeSort creates a new spreadsheet."; added columns "Final decision", "Decision (Deniz Yılmaz)", "Decision (Mert Aydın)", "Decision (Selin Yılmaz)", "Notes"; "100 rows, one per item. Final decision says Accepted, Rejected, Maybe, Conflict or Pending." |
| Column preview | "Columns"; "Your fields"; "Added by SwipeSort"; "Decision", "Notes" (shared "Final decision", "Decision (Deniz Yılmaz)"…); "20 rows, one per item. Decision says Accepted, Rejected or Maybe."; source "8 rows, one per item. The Tab column says which tab each item came from." |
| Continue | "Continue" |
| Confirm, new spreadsheet | "Export 20 items to a new spreadsheet?" / "Nothing is written until you confirm."; "Creates" / "Desk setup decisions, in the Google Drive of deniz.yilmaz@example.com"; "Writes" / "20 rows with your 7 fields, plus Decision and Notes"; "Doesn't change" / "Desk setup in SwipeSort, or any of your other spreadsheets" |
| Confirm, shared | "Export 100 items to a new spreadsheet?" / "Nothing is written until you confirm."; "Creates" / "Wedding guests decisions, in the Google Drive of mert.aydin@example.com"; "Writes" / "100 rows: your 6 fields, Final decision, a column per member and shared notes. Private notes aren't exported."; "Who sees it" / "Only people you share it with in Google Drive"; "Doesn't change" / "Wedding guests in SwipeSort"; permission lead-in (new spreadsheet) |
| Confirm, new tab | "Add a tab to Flat hunt 2026?"; "Adds" / "A tab named Decisions with 8 rows: Tab, Address, Rent, Rooms, Size, Viewing, Link, Decision and Notes"; "Doesn't change" / "The tabs Kadıköy, Beşiktaş, Archive 2025 and Notes" |
| Confirm, new columns | "Add 2 columns to Flat hunt 2026?" / "Nothing is written until you confirm. Existing cells are never overwritten."; "Kadıköy" / "Decision in column G and Notes in column H, rows 1 to 5"; "Beşiktaş" / same; "Doesn't change" / "Columns A to F, the tabs Archive 2025 and Notes, and formatting"; "Checked first" / "Each row still has the same address as when you imported it" |
| Permission lead-in | "Google asks for permission next" / new spreadsheet: "Allow SwipeSort to create this spreadsheet. It can open only the files it creates, not your other files."; original sheet: "Allow SwipeSort to edit your spreadsheets. It writes only what's listed here, and only when you confirm an export." |
| Confirm buttons | "Export to Google Sheets"; source: "Export to Flat hunt 2026"; "Back" (label "Back to destination") |
| Exporting | "Exporting…" / "Writing 20 rows to Desk setup decisions. This takes a few seconds." |
| Success | "Exported to Google Sheets" / "Desk setup decisions now has 20 rows with Decision and Notes columns."; tab: "Flat hunt 2026 has a new tab, Decisions, with 8 rows. Your other tabs didn't change."; columns: "Kadıköy and Beşiktaş have new Decision and Notes columns."; file card "Desk setup decisions" / "deniz.yilmaz@example.com", "Flat hunt 2026" / "Tab Decisions"; shared: "Wedding guests decisions now has 100 rows with the final decision, each member's decision and notes.", file card "Wedding guests decisions" / "mert.aydin@example.com"; "Open in Google Sheets"; "Done" |
| Not connected | "Connect Google Sheets" / "Choose the Google account where SwipeSort creates the spreadsheet."; "Creates new spreadsheets" / "SwipeSort can open only the files it creates. Your other files stay private."; "Doesn't sign you in" / "Connecting Google Sheets doesn't sign you in to SwipeSort or change your account."; "Disconnect any time" / "In Settings, under Connected accounts."; note "Next, Google asks you to choose an account and allow access."; "Connect Google account"; "Export a file instead" |
| Permission denied | "SwipeSort can't write to Google Sheets" / "Google didn't give SwipeSort permission to create the spreadsheet. Try again and choose Allow, or export a file instead." (original sheet: "…permission to edit Flat hunt 2026…"); "Try again"; "Export a file instead" |
| Network | "Couldn't export to Google Sheets" / "Google Sheets didn't respond. Check your connection and try again. Nothing was written."; "Try again"; "Export a file instead" |
| Sheet missing | "Flat hunt 2026 can't be found" / "It was deleted, or you no longer have access. Export to a new spreadsheet instead, or ask its owner to share it again."; "Export to a new spreadsheet"; "Export a file instead" |
| Rows changed | "Rows in Kadıköy have changed" / "Rows were added, moved or deleted since you imported them, so SwipeSort can't match items to rows. Add a new tab instead. Nothing in Flat hunt 2026 was changed."; tab renamed: "The tab Kadıköy was renamed or deleted…"; "Add a new tab instead"; "Back" |
| Partial | "Exported 4 of 8 items" / "Beşiktaş is protected in Google Sheets. Ask the owner of Flat hunt 2026 to let you edit it, then try again. Kadıköy keeps its new columns."; rows "Kadıköy" / "Decision and Notes added to 4 rows", "Beşiktaş" / "Protected tab. Nothing was added."; "Try Beşiktaş again"; "Open in Google Sheets"; "Done" |
| Token expired | "Connect Google Sheets again" / "Your Google connection expired. Connect again to finish the export." / "Connect again" |
| Too large | "Google Sheets can't hold this many cells. Export a CSV or Excel file instead." |
| Web popup | "Continue in the Google window" / "Allow SwipeSort to create the spreadsheet. The export continues here when you're done."; "Open the Google window again"; "Cancel"; blocked: "Your browser blocked the Google window" / "Allow pop-ups for swipesort.app in the address bar, then try again." |
| Screen reader | Exporting: "Exporting 8 items"; success: "Exported 8 items to desk-setup-accepted.csv"; Google: "Exported to Google Sheets" |

## 7. Accessibility

- Focus order step 1: Close, title, scope chips (one radiogroup "Items to export"; arrow keys move
  selection on web), helper, switches, format rows, safety line.
- Chips: `role="radio"` with `aria-checked`, labels include the count ("Accepted, 8 items"). Selection is
  shown by the inverted fill and announced; decisions keep icon + label (color never alone).
- Switch rows are single `role="switch"` targets with title and description as the name.
- Format rows are links/buttons named "CSV file, Opens in any spreadsheet app"; unavailable rows use
  `aria-disabled="true"` and keep the reason at full contrast ("Needs a connection", the empty-scope
  message above).
- Destination options are a `radiogroup` "Write to"; inputs have visible labels.
- The confirmation title is the dialog's accessible name; fact rows read as label + value.
- Exporting states use `role="status"` with the visible text; failures `role="alert"` and move focus to
  the title; success moves focus to the title ("Exported to Google Sheets").
- Snackbars are polite status messages; 4 s, never under 10 s with a screen reader running.
- Touch targets ≥ 48: chips are 36 visible inside 48 targets; all rows ≥ 64.
- Large text (`S39-large-text`): title `text-title-1`, chips 56 high, row text one step up; chips and rows
  wrap; nothing truncates except the account email. Step 1 scrolls; the destination and confirmation
  bottom bars stay pinned.
- Reduced motion: no slides; 150 ms fades; spinner replaced by a static icon with "Exporting…".
- The text preview is plain text in the accessibility tree (no layout tables), so screen readers read it
  as it will be shared.

## 8. iOS and web differences

- **iOS** (`S39-ios`, `S39-ios-share`, `S39-ios-text`): page sheet with grabber, `x` at the left and a
  centered title; pushed steps use "Back". CSV/Excel skip the file-ready sheet and open the share sheet
  directly (it already has Save to Files; Android's share sheet has no reliable save target, hence the
  extra sheet there). Google consent uses `ASWebAuthenticationSession` (system alert out of scope). Swipe
  down to dismiss is allowed on step 1 only (nothing is lost) and disabled while writing.
- **Android** (reference): file-ready sheet with Share file and Save to device; Google Identity Services
  consent sheet; predictive back.
- **Web, desktop** (`S39-web-desktop`, `S39-web-google-popup`): CSV/Excel download directly (no sheet);
  a toast at the bottom right of the window confirms (A-117). Google consent opens in a popup on the button click; the column shows a waiting
  state; a blocked popup shows the S15 blocked pattern with S39 copy. Text summary: "Copy text" is primary
  when the Web Share API is missing. Keyboard: Enter on a focused row exports, Esc closes.
- **Web, mobile**: like desktop, but Google consent uses the redirect flow (new tab →
  `swipesort.app/l/<listId>/export?google=done`), landing on the confirmation with the export starting.
  No frame: layout identical to Android without system bars.

## 9. Edge cases

- **Shared lists**: any member (Owner, Decision Maker, Collaborator) can export. The export reflects
  final decisions at that moment; open conflicts show "Conflict", undecided items "Pending". The
  Conflicts chip appears only on shared lists (and is hidden when the rule is Everyone must agree and
  there are none). Members who were removed with "Keep their decisions" still get a column, labeled with
  their name. Private notes are never exported.
- **Data used in Flow 3**: Mert exports, so every `S39-shared*` frame uses his Google account. S39-shared
  shows the counts after his bulk resolve (12 resolved, 3 open), so Conflicts is 3, not 15. Entering from S27-shared or S28-shared before the resolve shows 15.
- **Empty scope**: chips with 0 stay selectable so the entry preset can be explained; formats become
  unavailable until a non-empty scope is chosen. An empty list (0 items) shows the step with every chip
  at 0 and the message "This list has no items yet. Add items, then export."
- **Lists from Google Sheets where the user lost access** to the original: the original-sheet options are
  disabled with "You no longer have access to Flat hunt 2026"; New spreadsheet stays available.
- **Multi-source lists** (Wedding guests: contacts + mert-family.csv; Desk setup: manual): only a single
  Google Sheets source can be written back; lists combining sources other than one Google spreadsheet get
  New spreadsheet only.
- **Items added after import** (not in the original sheet): with New columns, they can't be matched to a
  row; the confirmation adds a fact "2 items aren't in Flat hunt 2026. They'll be left out; add a new tab
  to include them."
- **Tab name taken**: "Decisions" exists → default becomes "Decisions (2)"; inline error if the user types
  an existing name: "Flat hunt 2026 already has a tab named Decisions."
- **Spreadsheet name**: empty → Continue disabled with the hint "Enter a name". Google allows duplicate
  names; no check.
- **Large lists**: Google Sheets has a 10 million cell limit; SwipeSort checks before writing and shows
  the "Too large" message. Files up to 10,000 items export in under a second; above that the exporting
  sheet shows "Exporting 4,200 of 12,000 items…".
- **Formulas in data**: values starting with `=`, `+`, `-` or `@` are written as text (CSV: prefixed with
  `'`) to prevent formula injection.
- **Edited fields**: exports use the working copy (edits applied). The original source keeps its values
  even when columns are added (SAFE-01).
- **Archived lists**: exporting is allowed and doesn't restore the list.
- **Offline**: files and text work from local data; Google Sheets is unavailable; if the connection drops
  during a Google write, the network error states that nothing was written (single batch) or shows the
  partial state when one tab already succeeded.
- **Guest mode**: everything works; Google Sheets connection doesn't create a SwipeSort account (S15).
- **Account switched in Google**: the confirmation always names the account that will receive the data.
