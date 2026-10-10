# S15 Google Sheets connection and sheet/tab selection

Frames: `S15-google-sheets.html`. Generator: `tools/generators/S11-S15-import.py`. Sample data: the
spreadsheet **Flat hunt 2026** with tabs Kadıköy and Beşiktaş (`apartments` a01–a08; source of
l-apartments "Apartment viewings"); account deniz.yilmaz@example.com (`me.signedIn`).

## 1. Purpose and requirements

Import step 2 (Select items) for the Google Sheets source: connect a Google account with read-only access,
pick a spreadsheet, choose one or more tabs (tabs with the same columns combine into one list), preview the
rows, then map fields. Writing back to a sheet happens only at export, after an explicit confirmation
(S39).

Covers: SRC-01, SRC-07, SRC-18, SRC-23, SAFE-01, SAFE-06 (promise stated up front), GOAL-03, PLT-03, PLT-04,
PLT-16, PLT-21, VIS-13, OUT-01, SCR-15.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S11 Google Sheets tile | Not connected → `S15-default`; already connected → `S15-spreadsheets` |
| S07 Connected accounts | "Connect Google Sheets" opens `S15-default` outside the import (ends back on S07) |

| To | Trigger |
| --- | --- |
| Google account chooser + consent (native, out of scope) | "Connect Google account" (`data-action="connect"`) |
| `S15-spreadsheets` | Connected |
| `S15-tabs` | Tap a spreadsheet (`data-action="pick-sheet"` on Flat hunt 2026) |
| `S15-preview` | "Continue with 8 rows" on tabs |
| `S19-field-mapping.html#S19-default` | "Continue with 8 rows" on the preview (`data-action="continue"`) |
| `S11-source-picker.html#S11-default` | "Choose another source" |
| `S08-home.html#S08-default` | Close; asks "Discard import?" (S40) once tabs are chosen |

## 3. Layout and components

Import modal: **AppBar (modal)** "Import" + **ImportStepper** "Select items, Step 2 of 5".

- **Connect explainer** (`S15-default`): PermissionExplainer (see S12): 56 icon circle (`sheet`), title, lead,
  three promise points (read-only; writing only when you export; disconnect any time), note naming the
  next step, primary "Connect Google account", ghost "Choose another source" below.
- **Account row** (`rounded-group bg-card`, inset by the gutter): avatar 40, email, "Google account,
  read-only", text button "Switch" → account sheet.
- **SearchField** "Search spreadsheets".
- **Spreadsheet list**: section "Recent", full-bleed rows (64): `sheet` icon on a 40 `bg-secondary` square,
  name, meta ("Edited yesterday", "Shared by Mert Aydın, edited Oct 2"), chevron. Sorted by last edit
  (Drive `modifiedTime`), including files shared with the user. 50 per page, infinite scroll.
- **Tabs**: file row ("Flat hunt 2026", "4 tabs, edited Jul 21", "Change"), heading "Choose tabs", ListGroup of
  checkbox rows (name; "4 rows. Address, Rent, Rooms, Size, Viewing, Link"); empty tabs disabled; info
  Alert when 2+ tabs are selected explaining the Tab field.
- **Preview**: same pattern as S14 (file row, header-row switch, horizontally scrolling table with a Tab
  column first when tabs are combined).
- **Account sheet**: BottomSheet "Google account": current account with check, "Use another Google
  account", destructive row "Disconnect Google Sheets", footnote.
- **Bottom bar**: shared import pattern (top hairline, primary `h-14`, ghost secondary below).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S15-default` | Google Sheets not connected on this device |
| `S15-connecting` | Returning from Google consent while the token is exchanged and the first page loads |
| `S15-spreadsheets` | Connected: recent spreadsheets |
| `S15-search` | Query "flat": Flat hunt 2026 and Flat hunt 2024 |
| `S15-loading` | Fetching the list (skeleton rows + "Loading spreadsheets…") |
| `S15-no-spreadsheets` | The account has no spreadsheets (or search across Drive returns none) |
| `S15-account-switch` | "Switch" on the account row |
| `S15-tabs` | Flat hunt 2026: Kadıköy and Beşiktaş selected (8 rows), Archive 2025 unselected, Notes empty and disabled |
| `S15-preview` | Combined preview of the two tabs, Tab column first |
| `S15-empty-tab` | Moving checklist: every tab is empty (one has only column names) |
| `S15-error-connection` | Google didn't respond or timed out (SRC-23), at connect or while loading |
| `S15-error-access` | Token revoked in the Google account (401/403 on refresh) |
| `S15-offline` | No connection when the step opens (S11 normally prevents this; reached when the connection drops mid-step) |
| `S15-web-desktop` | Desktop browser: Google OAuth popup open, SwipeSort waits |
| `S15-web-popup-blocked` | The browser blocked the popup |
| `S15-ios` | iOS page sheet with the spreadsheet list |
| `S15-tabs-large-text` | 200% font scale: tab rows grow, names and column lists wrap, the list scrolls under the pinned Continue |

## 5. Interactions

- **Connect**: native Google sign-in (Android Credential Manager / Google Identity; iOS
  `ASWebAuthenticationSession`; web OAuth popup) requesting only
  `https://www.googleapis.com/auth/drive.metadata.readonly` (list spreadsheets) and
  `https://www.googleapis.com/auth/spreadsheets.readonly` (read rows). The write scope
  (`spreadsheets`) is requested incrementally at export (S39), never here.
- Connecting Google Sheets does **not** sign the user in to SwipeSort; it works in guest mode. If the user
  later signs in with the same Google account, the connection is shown under Settings › Connected
  accounts (S07).
- **Spreadsheet list**: tap → tabs (shared axis X). Pull to refresh on Android/iOS. Search queries Drive by
  name (debounce 300 ms) and highlights the match.
- **Tabs**: tap a row to toggle. The Continue label counts rows of selected tabs. With 2+ tabs: same columns
  → combine; different columns → inline note "Beşiktaş has 2 columns Kadıköy doesn't have (Floor,
  Deposit). They become fields; other items leave them empty." and Continue stays enabled.
  A "Tab" field is added automatically (hideable in S19). Single tab: no Tab field.
- **Preview**: identical to S14 (header switch re-renders; table scrolls sideways; record view at large
  text).
- **Switch account**: "Use another Google account" reopens the Google chooser; on success the list reloads
  for the new account (selection resets). "Disconnect Google Sheets" revokes the token, returns to
  `S15-default` and shows the snackbar "Google Sheets disconnected". Lists already imported are unaffected.
- **Errors**: error haptic on Android/iOS. "Try again" retries the last request; "Connect again" restarts the
  consent flow.
- **Web popup**: the popup opens on the button click (user gesture). While open, the column shows the
  waiting state with "Open the Google window again" (focuses or reopens it). Closing the popup without
  finishing returns to `S15-default` silently.

## 6. Copy

| Element | String |
| --- | --- |
| Stepper | "Select items", "Step 2 of 5" |
| Connect title | "Connect Google Sheets" |
| Connect lead | "Sign in with Google to choose a spreadsheet. SwipeSort imports a copy of its rows." |
| Connect points | "Read-only" / "SwipeSort sees your spreadsheets to list them. It can't change them."; "Writing only when you export" / "If you export decisions to a sheet later, SwipeSort asks first and shows what it will add."; "Disconnect any time" / "In Settings, under Connected accounts." |
| Connect note | "Next, Google asks you to choose an account." |
| Connect buttons | "Choose another source", "Connect Google account" |
| Connecting | "Connecting to Google…" / "Finish in the Google window. This takes a few seconds." / "Cancel" |
| Account row | "deniz.yilmaz@example.com" / "Google account, read-only" / "Switch" |
| Search | label and placeholder "Search spreadsheets"; results "2 spreadsheets match “flat”"; one "1 spreadsheet matches “flat”" |
| List | section "Recent"; meta "Edited yesterday", "Edited 3 days ago", "Shared by Mert Aydın, edited Oct 2", "Edited Sep 14", "Edited Jul 21", "Edited Mar 2, 2024" |
| Spreadsheets (sample) | "Team offsite October", "Frontend hiring pipeline", "Home office budget", "Book club 2026", "Flat hunt 2026", "Moving checklist", "Lisbon trip ideas", "Running log", "Flat hunt 2024" |
| Loading | "Loading spreadsheets…" |
| No spreadsheets | "No spreadsheets in this account" / "Create one in Google Sheets, or switch to the account that has your sheet." / "Choose another source", "Switch account" |
| Account sheet | "Google account" / "Deniz Yılmaz" "deniz.yilmaz@example.com" / "Use another Google account" / "Disconnect Google Sheets" / "Disconnecting doesn't change your lists or your spreadsheets." |
| Disconnected snackbar | "Google Sheets disconnected" |
| Tabs | file meta "4 tabs, edited Jul 21"; "Choose tabs" / "Pick one tab, or several with the same columns to combine them."; rows "Kadıköy" / "4 rows. Address, Rent, Rooms, Size, Viewing, Link"; "Archive 2025" / "11 rows. Address, Rent, Rooms, Size, Link"; "Notes" / "No rows, nothing to import" |
| Combine alert | "2 tabs become one list" / "A Tab field keeps track of where each item came from, so you can still tell Kadıköy from Beşiktaş." |
| Different columns note | "Beşiktaş has 2 columns Kadıköy doesn't have (Floor, Deposit). They become fields; other items leave them empty." |
| Continue | "Continue with 8 rows" (one row: "Continue with 1 row") |
| Preview | file meta "Kadıköy and Beşiktaş, 8 rows"; "First row has column names" / "Detected in both tabs"; "Preview" / "8 rows"; columns "Tab", "Address", "Rent", "Rooms", "Size", "Viewing", "Link"; empty "—" |
| Empty tabs | "Packing" / "Column names only, nothing to import"; "Utilities" / "No rows, nothing to import"; note "Nothing to import" / "Moving checklist has no rows yet. Add rows in Google Sheets, then refresh, or choose another spreadsheet." / "Refresh", "Choose another spreadsheet" |
| Connection failure | "Google Sheets didn't respond" / "Check your connection and try again. Nothing was imported." / "Choose another source", "Try again" |
| Access removed | "SwipeSort can't see your spreadsheets" / "Access to Google Sheets was removed from your Google account. Connect again to choose a sheet." / "Choose another source", "Connect again" |
| File access lost (snackbar on tap) | "You no longer have access to Home office budget. Ask its owner to share it again." |
| Offline | banner "You're offline. Changes are saved on this phone. Google Sheets needs a connection." / "Google Sheets needs a connection" / "Connect to the internet and try again, or import from another source. Contacts and files work offline." / "Choose another source", "Try again" |
| Web popup waiting | "Continue in the Google window" / "Choose your account and allow read-only access. SwipeSort continues here when you're done." / "Open the Google window again" |
| Popup blocked | "Your browser blocked the Google window" / "Allow pop-ups for swipesort.app in the address bar, then try again." / "Choose another source", "Try again" |

## 7. Accessibility

- Focus order: Close, title, stepper, account row (Switch), search, list. Spreadsheet rows are links named
  "Flat hunt 2026, Edited Jul 21".
- Tab rows are checkboxes with the row count and column names in the label; disabled tabs include the
  reason.
- The combine Alert is `role="note"`; errors announce their title (`role="alert"`).
- Preview table: same as S14 (caption, headers, focusable scroll region; record view at ≥ 150% text).
- Large text (`S15-tabs-large-text`): tab rows grow to fit wrapped names and column lists; the spreadsheet
  list rows grow the same way; nothing truncates except the file name in the file row.
- Loading uses `role="status"` with the visible text; skeleton rows are hidden from assistive tech.
- The web popup waiting state keeps focus on "Open the Google window again".

## 8. iOS and web differences

- **iOS** (`S15-ios`): page sheet with "Back" (to Choose source) and `x`; sign-in through `ASWebAuthenticationSession` (the system alert
  "“SwipeSort” wants to use “google.com” to sign in" is native, out of scope). The rest is identical.
- **Android**: Google Identity Services consent sheet (native).
- **Web, desktop** (`S15-web-desktop`): OAuth in a popup window next to the column; the column shows a
  waiting state. If the popup is blocked → `S15-web-popup-blocked`.
- **Web, mobile**: the browser opens Google consent in a new tab and returns to
  `swipesort.app/new/google` (redirect flow, no popup), landing on `S15-connecting` then the list.

## 9. Edge cases

- **Large spreadsheets**: same limits as files (10,000 rows, 50 columns per import); over the limit the same
  messages as S14 (`S14-error-too-many-columns`, `S14-error-too-many-rows`) appear with the sheet name.
- **Tabs with different header rows**: the header switch applies to all selected tabs; when only some tabs
  have a header the note says "Archive 2025 has no column names. Turn off the header row or choose tabs
  separately."
- **Formulas, dates, currency**: values import as displayed (formatted values API); "42,000" stays text
  until S19 sets the type.
- **Filtered or hidden rows** in Google Sheets import too (all rows, not the filtered view).
- **Revoked file access** between list and tabs: snackbar (see Copy) and back to the list.
- **Token expiry**: refreshed silently; only a failed refresh shows `S15-error-access`.
- **Account without Drive** (Workspace admin blocked third-party access): `S15-error-access` with the lead
  "Your organization doesn't allow SwipeSort to read Google Sheets. Ask your admin, or export the sheet as
  CSV and import that."
- **Offline mid-step**: the list keeps what it loaded; actions that need the network show the offline banner
  and retry when back online.
- **Long spreadsheet or tab names** truncate in rows and wrap in headings.
- **Export later** (S39): only for lists whose Source is Google Sheets, SwipeSort offers "new columns in
  the original sheet" or "a new tab", after the write confirmation (SAFE-06).
