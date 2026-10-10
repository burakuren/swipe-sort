# S14 File import (CSV and Excel)

Frames: `S14-file-import.html`. Generator: `tools/generators/S11-S15-import.py`. Sample data:
`candidates` (k01–k12) as **candidates-q4.csv** (source of l-candidates, "Frontend hiring, Q4"); `products`
as **office-furniture.xlsx**; `contacts` c001–c088 as **contacts-export.csv** (partial import example).

## 1. Purpose and requirements

Import step 2 (Select items) for the CSV or Excel source: pick a file, check what SwipeSort detected (header
row, separator, rows), choose Excel sheets, and recover from every file problem with a specific way
forward. The original file is never changed.

Covers: SRC-01, SRC-07, SRC-20, SRC-21, SRC-22, SRC-24, SRC-18, SAFE-01, GOAL-03, PLT-03, PLT-04, PLT-16,
PLT-21, VIS-13, OUT-01, DEL-25 (flow 4), SCR-14.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S11 CSV or Excel tile | `data-action="source-csv"` |
| S11 web unavailable sheet, S12 recovery, S13 empty/error | "Import a CSV instead" |

| To | Trigger |
| --- | --- |
| System file picker (out of scope) | "Choose file" (`data-action="choose-file"`) / "Browse files" (desktop) |
| `S14-csv-preview` | A readable file was picked (prototype: Choose file → preview) |
| `S19-field-mapping.html#S19-csv` | "Continue with 12 rows" on `S14-csv-preview` (`data-action="continue"`) |
| `S19-field-mapping.html#S19-default` | Continue from Excel sheets or a partial import |
| `S11-source-picker.html#S11-default` | "Choose another source" on errors |
| `S08-home.html#S08-default` | Close; asks "Discard import?" (S40) once a file has been read |

Field mapping (S19) then leads to S20 (duplicates) or S22 pick (finish). Final copy on success: "Imported
12 items"; with skipped rows: "Imported 84 of 88 items" (S22 snackbar).

## 3. Layout and components

Import modal: **AppBar (modal)** "Import" + **ImportStepper** "Select items, Step 2 of 5".

- **Start** (`S14-default`): heading `text-title-2`, one line on how rows/columns map to items/fields,
  ListGroup "What works" (3 info rows: .csv, .xlsx, limits), data-safety note pinned above the bottom bar,
  primary "Choose file".
- **File row** (after picking): `rounded-group bg-card`, 40 file icon on `primary-soft`, name (truncates in
  the middle on device: `ellipsizeMode="middle"`), meta "12 rows, 8 columns, 3 KB", text button "Change".
- **Detected settings** (ListGroup): switch row "First row has column names" (with how it was detected);
  select row "Separator" (Comma, Semicolon, Tab, Pipe) for CSV only; opens a bottom-sheet select.
- **Preview**: label "Preview" + row count; a table in a `rounded-group bg-card` container that scrolls
  horizontally: a muted header row, row numbers (`text-caption muted`), cells `text-body-sm` truncating at
  176 dp, empty cells "—" in muted. Shows the first 50 rows; the count says how many will import.
- **Excel sheets**: ListGroup of checkbox rows (name; "20 rows. Name, Price, …" as a one-line description);
  empty sheets are disabled with "No rows, nothing to import"; then the preview of the first selected
  sheet.
- **Choose columns**: search, "8 of 73 selected" + "Select first 50", checkbox rows with a sample value.
- **Errors**: ErrorState (32 muted icon, `text-title-3`, one or two sentences naming the file) with bottom
  actions (primary fix, ghost alternative below).
- **Partial import**: error Alert ("84 of 88 rows can be imported") with "Show skipped rows" → bottom sheet
  listing each skipped row and why.
- **Bottom bar** (identical to S16–S21): top hairline, optional note, primary `h-14` full width, ghost
  secondary below.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S14-default` | Entered from S11 |
| `S14-reading` | File picked, parsing (shown when it takes > 300 ms; determinate for files > 1 MB) |
| `S14-csv-preview` | candidates-q4.csv read: header detected, comma separator, 12 rows, 8 columns |
| `S14-no-header` | "First row has column names" off: columns become "Column A…H", the header row becomes item 1 (13 rows) |
| `S14-excel-sheets` | .xlsx with several sheets (office-furniture.xlsx: Shortlist 20, Last year 34, Price history 12, Notes empty) |
| `S14-csv-preview-large-text` | 200% font scale: the table becomes one row at a time ("Row 1 of 12", previous/next) |
| `S14-error-unreadable` | Corrupt, password-protected or binary file (SRC-20) |
| `S14-error-empty` | No data rows (only a header, or 0 bytes) (SRC-21) |
| `S14-error-too-many-columns` | More than 50 columns (SRC-22) |
| `S14-choose-columns` | "Choose columns" from the error above |
| `S14-error-too-large` | File over 20 MB |
| `S14-error-too-many-rows` | More than 10,000 rows |
| `S14-error-unsupported` | Not .csv/.tsv/.xlsx (e.g. .numbers, .xls, .ods, .pdf) |
| `S14-partial` | Some rows malformed (SRC-24): 84 of 88 readable |
| `S14-skipped-rows` | "Show skipped rows" sheet |
| `S14-web-desktop` | Desktop browser: drop zone with "Browse files" |
| `S14-web-desktop-drag` | A file dragged over the page |
| `S14-ios` | iOS page sheet; Files picker |

Mobile web is identical to Android (`S14-default` layout; "Choose file" opens the browser chooser); no
separate frame. Offline: not applicable, files are read locally.

## 5. Interactions

- **Choose file**: opens the system picker filtered to `text/csv`, `text/tab-separated-values`,
  `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Android also allows `*/*` via
  "Browse" so mislabeled CSVs can be picked; the type is checked after picking).
- **Detection**: encoding (UTF-8, UTF-16, Windows-1254/1252 fallback), separator (most consistent of
  comma, semicolon, tab, pipe across the first 50 lines), header row (first row all text and unique while
  later rows contain numbers/dates, or first row differs in type). Quotes per RFC 4180. Blank trailing
  rows and fully empty rows are ignored silently (not counted as skipped).
- **Header switch**: toggling re-renders the preview and the counts immediately (no reload).
- **Separator select**: bottom sheet with 4 radio rows; changing it re-parses.
- **Excel**: hidden sheets are listed last with "Hidden in Excel"; formulas import their last calculated
  value; merged cells take the top-left value; dates become ISO dates. Selecting several sheets with
  different columns shows an inline note "Last year has 1 column Shortlist doesn't have (Discount). It
  becomes a field; other items leave it empty." and adds a "Sheet" field (same rule as Google tabs).
- **Too many columns**: "Choose columns" opens the column chooser (max 50; selecting a 51st shows the
  helper "You can choose up to 50 columns." and the checkbox doesn't toggle); "Continue with the first 50"
  imports columns 1–50.
- **Partial**: rows that can't be parsed are listed with the reason; "Continue with 84 rows" continues.
- **Reading**: "Cancel" stops parsing and returns to `S14-default`.
- **Errors**: error haptic (`notificationAsync(Error)`) on Android and iOS; the primary action re-opens the
  picker.
- **Desktop**: the whole page accepts a drop (the drop zone highlights when a file enters the window);
  dropping several files imports the first and shows the snackbar "Import one file at a time. SwipeSort
  used budget.csv."
- Transitions: shared axis X between start → preview → S19 (300 ms; reduced motion 150 ms fade).

## 6. Copy

| Element | String |
| --- | --- |
| Heading | "Choose a CSV or Excel file" |
| Sub line | "Each row becomes an item and each column a field. Column names, like Name or Price, go in the first row." |
| What works | header "What works"; ".csv" / "Comma, semicolon or tab separated"; ".xlsx" / "Excel workbooks; you choose the sheets"; "Up to 10,000 rows and 50 columns" / "Files up to 20 MB" |
| Desktop compact line | "Works with .csv and .xlsx files up to 20 MB, 10,000 rows and 50 columns." |
| Safety note | "Your file isn't changed. SwipeSort imports a copy." |
| Primary | "Choose file"; desktop "Browse files" |
| iOS note | "Opens Files. iCloud Drive and other locations work." |
| Drop zone | "Drop a CSV or Excel file here" / "or"; dragging "Drop the file to import it" / ".csv or .xlsx, up to 20 MB" |
| Reading | "Reading office-furniture.xlsx…" / "Large files take a few seconds. Nothing is imported until you continue." / "Cancel" |
| File row | "candidates-q4.csv" / "12 rows, 8 columns, 3 KB" / "Change" |
| Header switch | "First row has column names" / "Detected in candidates-q4.csv"; off: "Off: the first row is imported as an item" |
| Separator | "Separator" / "Comma" (options "Comma", "Semicolon", "Tab", "Pipe") |
| Preview | "Preview" / "12 rows"; generic columns "Column A" … ; empty cell "—" |
| Continue | "Continue with 12 rows"; "Continue with 13 rows"; "Continue with 20 rows"; "Continue with 84 rows" |
| Excel | "Choose sheets" / "Pick one, or several with the same columns to combine them." / "20 rows. Name, Price, Rating, Store, Category, Link" / "No rows, nothing to import" / meta "4 sheets, 2.4 MB" |
| Large text record | "Row 1 of 12"; "Previous row", "Next row"; empty value "Empty" |
| Unreadable | "This file can't be read" / "budget-final.xlsx may be damaged or protected with a password. Open it in a spreadsheet app, save it as .csv or .xlsx, and try again." / "Choose another source", "Choose another file" |
| Empty | "This file has no rows" / "plants.csv has column names but nothing below them. Add rows and try again, or choose another file." (0-byte file: "plants.csv is empty. Add rows and try again, or choose another file.") |
| Too many columns | "This file has 73 columns" / "SwipeSort imports up to 50 columns per list. Choose the columns you need, or continue with the first 50." / "Continue with the first 50", "Choose columns" |
| Choose columns | "Choose up to 50 columns"; search "Search columns"; "8 of 73 selected"; "Select first 50"; row sample "For example: Ece Doğru"; "Continue with 8 columns"; limit helper "You can choose up to 50 columns." |
| Too large | "This file is too large" / "crm-export-full.csv is 48 MB. SwipeSort imports files up to 20 MB. Remove columns you don't need or split the file, then try again." / "Choose another source", "Choose another file" |
| Too many rows | "This file has 14,250 rows" / "SwipeSort imports up to 10,000 rows per file. Import the first 10,000 now and add the rest to the same list later." / "Choose another file", "Import the first 10,000 rows" |
| Unsupported | "SwipeSort can't open .numbers files" / "Export it from Numbers as CSV or Excel, then choose it again. SwipeSort opens .csv and .xlsx files." / "Choose another source", "Choose another file". Generic variant: "SwipeSort can't open .{ext} files" / "Save it as CSV or Excel, then choose it again." |
| Partial alert | "84 of 88 rows can be imported" / "4 rows don't match the columns and will be skipped. The other rows are fine." / "Show skipped rows" |
| Skipped sheet | "4 skipped rows" / "To keep these rows, fix them in a spreadsheet app and import the file again." / "Row 23" "Has 6 cells; the file has 4 columns"; "Row 41" "A quote mark isn't closed"; "Row 57" "Has 5 cells; the file has 4 columns"; "Row 88" "Has 6 cells; the file has 4 columns" / "Choose another file", "Continue with 84 rows" |
| Multiple files dropped | "Import one file at a time. SwipeSort used budget.csv." |
| Finish snackbars (S22) | "Imported 12 items"; "Imported 84 of 88 items" |

## 7. Accessibility

- Focus order: Close, title, stepper, file row (name, Change), settings rows, preview region, Continue.
- The preview table is a real table with a caption, column headers (`scope="col"`) and a hidden "Row"
  header; its scroll container is focusable (`tabindex="0"`, `role="region"`, label "Preview of
  candidates-q4.csv, scrolls sideways") so keyboard users can scroll it.
- The header switch is one `switch` element (row-sized target) labeled by its text.
- Error states: the title is announced (`role="alert"` on the error container on arrival); the file name is
  in the text, never only in the icon.
- Large text (≥ 150%): the table is replaced by the record view with previous/next buttons (48 targets);
  the switch row wraps.
- Disabled sheet rows (empty sheets) are real disabled checkboxes with the reason in their label.

## 8. iOS and web differences

- **iOS** (`S14-ios`): page sheet with "Back" (to Choose source) and `x`; "Choose file" opens the Files document picker
  (`UIDocumentPickerViewController`, types CSV/TSV/XLSX); the note under the action mentions iCloud Drive.
  Swipe-down dismiss is disabled once a file has been read.
- **Web, mobile**: identical to Android; the browser's file chooser opens.
- **Web, desktop** (`S14-web-desktop`, `-drag`): a drop zone above the limits replaces the bottom "Choose
  file" button; the whole window accepts drops; keyboard: the drop zone's "Browse files" is the primary
  button and Enter opens the chooser.
- Android: the Storage Access Framework picker; Google Drive files are allowed (downloaded first, shown as
  `S14-reading`).

## 9. Edge cases

- **Encoding**: Turkish characters in Windows-1254 exports are detected; if unsure, the preview shows a
  select row "Text encoding" (UTF-8, Turkish (Windows-1254), Western (Windows-1252)).
- **Duplicate column names** ("Phone", "Phone"): kept as "Phone" and "Phone 2"; S19 can merge them into a
  multi-value field.
- **Empty column names**: "Column C" (spreadsheet letter).
- **Long cell text**: truncated in the preview, imported in full (field values up to 10,000 characters;
  longer values are cut with a note in S19).
- **Missing values** (k04 Marco Bianchi has no salary or portfolio): shown as "—"; items keep the field
  empty and cards hide the row.
- **Numbers and dates**: imported as text here; S19 suggests types from the values.
- **Exactly 50 columns / 10,000 rows**: allowed without a warning.
- **File changed after import**: SwipeSort never re-reads it; adding more rows later goes through S21.
- **Very large but valid files** (8 MB, 9,800 rows): `S14-reading` is determinate; the preview shows the
  first 50 rows and the full count.
- **Combining sources**: a CSV can be added to a list that came from contacts (Wedding guests: 88 contacts
  + mert-family.csv 12 rows) via S21; duplicates are reviewed in S20.
- **Offline**: not relevant (local file); a Google Drive file that isn't downloaded yet shows "This file is
  in Google Drive and needs a connection to download. Try again when you're online."
