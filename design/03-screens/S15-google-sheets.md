# S15 Google Sheets: choose a spreadsheet and its tabs

Frames: `S15-google-sheets.html`. Generator: `tools/generators/S11-S15-import.py`. Sample data: the
spreadsheet **Flat hunt 2026** with tabs Kadıköy and Beşiktaş (`apartments` a01–a08; source of
l-apartments "Apartment viewings"); account deniz.yilmaz@example.com (`me.signedIn`). Error and limit examples
use spreadsheets that exist only in these frames ("Newsletter subscribers", "Office budget 2025.xlsx").

## 1. Purpose and requirements

Import step 2 (Select items) for the Google Sheets source: choose one spreadsheet in **Google's file picker**,
choose one or more tabs (tabs with the same columns combine into one list), preview the rows, then map fields.
Writing back to a sheet happens only at export, after an explicit confirmation (S39).

Access model (D-17, ADR-0005, A-151): SwipeSort asks Google only for the non-sensitive **`drive.file`**
scope. With it, SwipeSort can open only the files the person chooses in Google's picker (and the spreadsheets
it creates at export). It never lists or searches the person's Google Drive, so the old in-app "Recent"
spreadsheet list, Drive search and their loading, empty and no-results states are gone. The same grant covers
reading the chosen sheet now and writing to it later, so the export to this sheet asks for nothing more.

Covers: SRC-01, SRC-07 (changed by D-17), SRC-18, SRC-23, SRC-25, SAFE-01, SAFE-06 (promise stated up front),
GOAL-03, PLT-03, PLT-04, PLT-16, PLT-21, VIS-13, OUT-01, SCR-15 (changed by D-17).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S11 / S21 Google Sheets tile | No Google account connected on this device → `S15-default`; already connected → `S15-connected` |
| S07 Connected accounts | "Connect Google Sheets" opens the `S15-default` layout outside the import as a variant (no frame): no stepper, app bar "Google Sheets", note "Next, Google asks you to choose an account.", primary "Connect Google account" (as `S39-google-not-connected`); the picker isn't opened and the flow ends back on S07 once the account is chosen |
| S39 account row "Switch" | `S15-account-switch` |

| To | Trigger |
| --- | --- |
| Google account chooser, then Google's file picker (Google's UI, out of scope) | "Choose spreadsheet" (`data-action="choose-sheet"`) |
| `S15-reading` → `S15-tabs` | A spreadsheet is chosen in the picker (prototype: straight to `S15-tabs`) |
| Back on the step, unchanged | The picker is closed or cancelled |
| `S15-preview` | "Continue with 8 rows" on tabs |
| `S19-field-mapping.html#S19-default` | "Continue with 8 rows" on the preview (`data-action="continue"`) |
| Google's picker again | "Change" on the file row, "Choose another spreadsheet" (`choose-sheet`) |
| `S14-file-import.html#S14-default` | "Import a CSV or Excel file" / "Import a CSV instead" (unsupported file, admin block) |
| `S11-source-picker.html#S11-default` | "Choose another source" |
| `S08-home.html#S08-default` | Close; asks "Discard import?" (S40) once tabs are chosen |

Removed frames (D-17): `S15-spreadsheets`, `S15-search`, `S15-loading`, `S15-no-spreadsheets`,
`S15-connecting`. New: `S15-connected`, `S15-picker-android`, `S15-reading`, `S15-too-many-rows`,
`S15-error-unsupported`, `S15-error-admin`.

## 3. Layout and components

Import modal: **AppBar (modal)** "Import" + **ImportStepper** "Select items, Step 2 of 5".

- **Choose a spreadsheet, first time** (`S15-default`): PermissionExplainer layout (see S12): 56 icon circle
  (`sheet`), title "Choose a spreadsheet", lead, three promise points (your other files stay private; writing
  only when you export; disconnect any time), note naming the next steps (Google account, then Google's
  picker), primary "Choose spreadsheet", ghost "Choose another source".
- **Choose a spreadsheet, connected** (`S15-connected`): **account row** (`rounded-group bg-card`: avatar 40,
  email, "Google account", text button "Switch" → account sheet), the icon, title and lead, a safety line at the
  bottom of the content, note "Google's file picker opens next.", same buttons.
- **Google's file picker** (Google's UI, not designed): drawn only as labeled placeholders
  (`S15-picker-android`: a browser tab; `S15-web-desktop`: an overlay over the page). It shows only Google
  Sheets files (`application/vnd.google-apps.spreadsheet`).
- **Reading** (`S15-reading`): file row without "Change", spinner line "Reading Flat hunt 2026…", one line of
  reassurance; Continue disabled, ghost "Cancel".
- **Tabs**: file row ("Flat hunt 2026", "4 tabs, edited Jul 21", "Change" reopens the picker), heading "Choose
  tabs", ListGroup of checkbox rows (name; "4 rows. Address, Rent, Rooms, Size, Viewing, Link"); empty tabs
  disabled; info Alert when 2+ tabs are selected explaining the Tab field; error Alert when the selected tabs
  pass the row limit.
- **Preview**: same pattern as S14 (file row, header-row switch, horizontally scrolling table with a Tab
  column first when tabs are combined).
- **Account sheet**: BottomSheet "Google account": current account with check, "Use another Google
  account", destructive row "Disconnect Google Sheets", footnote.
- **Bottom bar**: shared import pattern (top hairline, primary `h-14`, ghost secondary below).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S15-default` | Choose a spreadsheet, first time: no Google account connected on this device |
| `S15-connected` | Google account already connected: the picker opens straight from "Choose spreadsheet" |
| (no frame) picker cancelled | The person closes the picker or its browser tab: back on `S15-default` / `S15-connected` (or on the tabs step after "Change", with the previous file kept), nothing changes, no message |
| `S15-account-switch` | "Switch" on the account row (also from S39's account row) |
| `S15-picker-android` | Android: Google's picker in a browser tab (placeholder); choosing returns to SwipeSort, closing the tab cancels |
| `S15-reading` | A spreadsheet was chosen: SwipeSort reads its tabs and the first rows |
| `S15-tabs` | Flat hunt 2026: Kadıköy and Beşiktaş selected (8 rows), Archive 2025 unselected, Notes empty and disabled |
| `S15-tabs-large-text` | 200% font scale: the helper line and tab rows wrap; Continue stays pinned (content scrolls under it) |
| `S15-preview` | Combined preview of the two tabs, Tab column first |
| `S15-empty-tab` | Moving checklist: every tab is empty (one has only column names) |
| `S15-too-many-rows` | Newsletter subscribers: tabs 2025 (6,180 rows) and 2026 (8,070) selected = 14,250 rows, over the 10,000 limit (A-59): error Alert, primary "Import the first 10,000 rows" |
| `S15-error-unsupported` | The picked file isn't a Google Sheets spreadsheet (Office budget 2025.xlsx, an Excel file stored in Drive) |
| `S15-error-connection` | Google didn't respond or timed out (SRC-23) when opening the picker or reading the sheet |
| `S15-error-access` | Access removed in the Google account (401/403 when reading after the pick, or the token can't be refreshed) |
| `S15-error-admin` | The Google Workspace admin of the chosen account blocks SwipeSort (org policy error from Google) |
| `S15-offline` | No connection when the step opens (S11 normally prevents this; reached when the connection drops mid-step) |
| `S15-web-desktop` | Desktop browser: Google's JavaScript picker over the page (placeholder) |
| `S15-web-popup-blocked` | The browser blocked the Google sign-in window that comes before the picker |
| `S15-ios` | iOS page sheet: choose a spreadsheet (same flow as Android, to be verified) |

Too many columns (over 50) uses the S14 "Choose columns" pattern (`S14-error-too-many-columns`,
`S14-choose-columns`) with the sheet name; no separate frame.

## 5. Interactions

- **Choose spreadsheet** opens Google's flow. First time: Google asks for an account and consent to
  `https://www.googleapis.com/auth/drive.file` only (no read-only scopes, no Drive listing scope), then shows
  its file picker. Connected: the picker opens straight away for the remembered account. The picker is
  limited to Google Sheets files and to one file.
- **Platform flows** (D-17): web uses the Google Picker JavaScript API as an overlay on the page, after a
  Google Identity Services token popup (desktop) or redirect (mobile browsers). Android uses Google's
  documented "desktop and mobile apps" picker flow in the system browser (a Custom Tab, `trigger_onepick`, its
  own OAuth client ID): the browser tab returns to SwipeSort with the chosen file. iOS is expected to use the
  same browser flow (`ASWebAuthenticationSession`); to be verified when iOS work starts.
- **After the pick**: `S15-reading` reads the spreadsheet's tabs (names, row counts, header rows) and the
  first rows; then the tabs step. Nothing is imported until Continue on the preview.
- **Cancel**: closing the picker (or its browser tab) returns to where it was opened with nothing changed and
  no message, like dismissing any system picker.
- **Re-pick**: "Change" on the file row and "Choose another spreadsheet" reopen the picker; a new choice
  replaces the file and resets the tab selection; cancelling keeps the current file.
- Connecting Google Sheets does **not** sign the user in to SwipeSort; it works without an account. If the
  user later signs in with the same Google account, the connection shows under Settings › Connected accounts
  (S07).
- **Tabs**: tap a row to toggle. The Continue label counts rows of selected tabs. With 2+ tabs: same columns
  → combine; different columns → inline note "Beşiktaş has 2 columns Kadıköy doesn't have (Floor,
  Deposit). They become fields; other items leave them empty." and Continue stays enabled.
  A "Tab" field is added automatically (hideable in S19). Single tab: no Tab field. When the selected tabs
  pass 10,000 rows, the error Alert appears and the primary becomes "Import the first 10,000 rows" (rows are
  taken in tab order); unchecking a tab below the limit restores "Continue with {n} rows".
- **Preview**: identical to S14 (header switch re-renders; table scrolls sideways; record view at large
  text).
- **Switch account**: "Use another Google account" reopens Google's account chooser and then the picker; the
  current file and tab selection reset. "Disconnect Google Sheets" revokes the token (which also removes
  SwipeSort's access to every file chosen so far), returns to `S15-default` and shows the snackbar "Google
  Sheets disconnected". Lists already imported are unaffected; exporting to their original sheet later asks to
  choose it again (S39, A-158).
- **Errors**: error haptic on Android/iOS. "Try again" retries the last request; "Choose spreadsheet again"
  restarts the account and picker flow.
- **Web popup**: the token popup opens on the button click (user gesture). Closing it without finishing
  returns to the step silently; a blocked popup shows `S15-web-popup-blocked`.

## 6. Copy

| Element | String |
| --- | --- |
| Stepper | "Select items", "Step 2 of 5" |
| Title | "Choose a spreadsheet" |
| Lead | "You'll choose a spreadsheet in Google's file picker. SwipeSort can open only the files you choose." |
| Points (first time) | "Your other files stay private" / "SwipeSort can't list or search your Google Drive. It sees only the spreadsheet you choose."; "Writing only when you export" / "If you export decisions to this sheet later, SwipeSort asks first and shows what it will add."; "Disconnect any time" / "In Settings, under Connected accounts." |
| Note | first time "Next, Google asks you to choose an account, then opens its file picker."; connected "Google's file picker opens next." |
| Buttons | "Choose spreadsheet", "Choose another source" |
| Safety line (connected) | "SwipeSort imports a copy. Your spreadsheet isn't changed." |
| Account row | "deniz.yilmaz@example.com" / "Google account" / "Switch" (same label in S39) |
| Account sheet | "Google account" / "Deniz Yılmaz" "deniz.yilmaz@example.com" / "Use another Google account" / "Disconnect Google Sheets" / "Disconnecting doesn't change your lists or your spreadsheets. To export to a sheet later, you choose it again." |
| Disconnected snackbar | "Google Sheets disconnected" |
| Reading | file meta "Google Sheets"; "Reading Flat hunt 2026…"; "Large spreadsheets take a few seconds. Nothing is imported until you continue."; "Continue" (disabled), "Cancel" |
| Tabs | file meta "4 tabs, edited Jul 21"; "Change"; "Choose tabs" / "Pick one tab, or several with the same columns to combine them."; rows "Kadıköy" / "4 rows. Address, Rent, Rooms, Size, Viewing, Link"; "Archive 2025" / "11 rows. Address, Rent, Rooms, Size, Link"; "Notes" / "No rows, nothing to import" |
| Combine alert | "2 tabs become one list" / "A Tab field keeps track of where each item came from, so you can still tell Kadıköy from Beşiktaş." |
| Different columns note | "Beşiktaş has 2 columns Kadıköy doesn't have (Floor, Deposit). They become fields; other items leave them empty." |
| Continue | "Continue with 8 rows" (one row: "Continue with 1 row") |
| Too many rows | "14,250 rows selected" / "SwipeSort imports up to 10,000 rows at a time. Choose fewer tabs, or import the first 10,000 rows and add the rest to the same list later." / "Import the first 10,000 rows", "Choose another spreadsheet" |
| Preview | file meta "Kadıköy and Beşiktaş, 8 rows"; "First row has column names" / "Detected in both tabs"; "Preview" / "8 rows"; columns "Tab", "Address", "Rent", "Rooms", "Size", "Viewing", "Link"; empty "—" |
| Empty tabs | "Packing" / "Column names only, nothing to import"; "Utilities" / "No rows, nothing to import"; note "Nothing to import" / "Moving checklist has no rows yet. Add rows in Google Sheets, then refresh, or choose another spreadsheet." / "Choose another spreadsheet", "Refresh" |
| Unsupported file | "This file isn't a Google Sheets spreadsheet" / "Office budget 2025.xlsx is an Excel file in Google Drive. Choose a spreadsheet made in Google Sheets, or download the file and import it as a CSV or Excel file." / "Choose another spreadsheet", "Import a CSV or Excel file" |
| Connection failure | "Google Sheets didn't respond" / "Check your connection and try again. Nothing was imported." / "Try again", "Choose another source" |
| Access removed | "SwipeSort can't open Flat hunt 2026" / "Access was removed in your Google account. Choose the spreadsheet again to give SwipeSort access." / "Choose spreadsheet again" (reopens the account and picker flow, `S15-picker-android`), "Choose another source" |
| Admin block | "Your organization doesn't allow SwipeSort" / "The admin of your Google Workspace account blocks SwipeSort from opening files. Ask your admin, or download the sheet as a CSV file and import that." / "Import a CSV instead", "Use another Google account" |
| Offline | banner "You're offline. Changes are saved on this phone. Google Sheets needs a connection." / "Google Sheets needs a connection" / "Connect to the internet and try again, or import from another source. Contacts and files work offline." / "Try again", "Choose another source" |
| Popup blocked | "Your browser blocked the Google window" / "Allow pop-ups for swipesort.app in the address bar, then try again." / "Try again", "Choose another source" |

## 7. Accessibility

- Focus order: Close (or Back on iOS), title, stepper, account row (Switch) when connected, heading, lead,
  points, note, primary, secondary.
- When the picker closes, focus returns to "Choose spreadsheet" (cancelled) or to the "Choose tabs" heading
  (file chosen). The reading state uses `role="status"` with the visible text.
- Google's picker is Google's UI; its accessibility is Google's. SwipeSort's part is that every way out of it
  lands on a labeled state.
- Tab rows are checkboxes with the row count and column names in the label; disabled tabs include the
  reason.
- The combine Alert is `role="note"`; the row-limit Alert and the errors announce their title
  (`role="alert"`).
- Preview table: same as S14 (caption, headers, focusable scroll region; record view at ≥ 150% text).
- Large text (`S15-tabs-large-text`): tab rows grow to fit wrapped names and column lists; nothing truncates
  except the file name in the file row. The choose step uses the PermissionExplainer large-text behavior
  (`S12-contacts-large-text`): content scrolls, actions stay pinned.

## 8. Platform differences

- **Android** (reference): Google's picker opens in the system browser (Custom Tab) through Google's
  documented flow for mobile apps (`drive.file` only, separate OAuth client ID, `trigger_onepick`;
  `S15-picker-android`). The browser tab covers SwipeSort; closing it is a cancel.
- **iOS** (`S15-ios`): page sheet with "Back" (to Choose source) and `x`; the same browser flow through
  `ASWebAuthenticationSession` (the system alert "“SwipeSort” wants to use “google.com” to sign in" is
  native, out of scope). Google documents no iOS picker; this flow is expected to work and must be verified
  when iOS work starts (D-17).
- **Web, desktop** (`S15-web-desktop`): first a Google sign-in popup for the token (blocked →
  `S15-web-popup-blocked`), then Google's JavaScript picker as an overlay on the page. The column stays
  behind it.
- **Web, mobile**: the token step uses the redirect flow (new tab → `swipesort.app/new/google`), then the
  picker overlay fills the screen.

## 9. Edge cases

- **Large spreadsheets**: same limits as files (A-59): 10,000 rows and 50 columns per import, counted over the
  selected tabs. Rows: `S15-too-many-rows`. Columns: the S14 "Choose columns" step with the sheet name.
  Google's own size limits make a 20 MB check unnecessary.
- **Picked file isn't a Google Sheets file**: the picker is filtered to Google Sheets, but Android's browser
  picker flow may not honor the filter (unverified) and shortcuts can point elsewhere: `S15-error-unsupported`.
  Excel and CSV files stored in Drive are not read here (download and use S14).
- **Tabs with different header rows**: the header switch applies to all selected tabs; when only some tabs
  have a header the note says "Archive 2025 has no column names. Turn off the header row or choose tabs
  separately."
- **Formulas, dates, currency**: values import as displayed (formatted values API); "42,000" stays text
  until S19 sets the type.
- **Filtered or hidden rows** in Google Sheets import too (all rows, not the filtered view).
- **Access lost between pick and read** (file unshared or deleted in the meantime): `S15-error-access` copy
  variant "Flat hunt 2026 can't be opened anymore. It was deleted or unshared. Choose another spreadsheet." with
  "Choose another spreadsheet".
- **Token expiry**: refreshed silently; only a failed refresh shows `S15-error-access`.
- **Account blocked by a Workspace admin**: `S15-error-admin`; switching to a personal account is offered.
- **The same spreadsheet imported twice**: allowed (a second list, or Add items with duplicate review).
- **Offline mid-step**: what was read stays; actions that need the network show the offline banner and retry
  when back online.
- **Long spreadsheet or tab names** truncate in rows and wrap in headings.
- **Export later** (S39): lists whose Source is this spreadsheet can write a new tab or new columns to it after
  the write confirmation (SAFE-06), with no extra Google permission; if SwipeSort can't open it with the
  current account, S39 asks to choose it again in the picker (`S39-apartments-repick`).
