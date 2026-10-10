# S19 Field mapping

Frames: `S19-field-mapping.html`. Generator: `tools/generators/S19-field-mapping.py`. Components:
`01-foundations/components.md` (ImportStepper, AppBar modal, ListGroup, Switch, Select, BottomSheet, Alert).

## 1. Purpose and requirements

Step 3 of the import, shared by every source that brings its own fields (contacts, CSV, Excel, Google Sheets,
plain text). The user sees what SwipeSort detected, with sample values from the real records, and decides how
each field appears: name, type, shown on cards or hidden, and which field is the card title. Sources with fixed
or inline-defined fields (photos S18, manual entry S17) skip this step.

Covers: SRC-08, SRC-09, SRC-10, SRC-11, SRC-12, SRC-13, SRC-22 (too many columns), SRC-03/GOAL-05 (one mapping
step for every source), SRC-01, GOAL-02, GOAL-03, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-06, STK-07,
VIS-11, VIS-13, TERM-01, DEL-22 (flow 1), DEL-25 (flow 4), SCR-19.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S13 Contacts import | "Continue" with 88 contacts selected → `S19-contacts` |
| S14 File import (CSV, Excel) | "Continue" after the preview → `S19-csv` (candidates-q4.csv) |
| S15 Google Sheets | "Continue" after choosing tabs → `S19-default` (Flat hunt 2026, tabs Kadıköy and Beşiktaş) |
| S16 Plain text | "Continue" → `S19-text` |
| S21 Add items | not used: adding to an existing list maps columns to the list's fields in `S21-mapping` |
| Back from S20 / S22 pick | system back or iOS back chevron returns here with every choice kept |

| To | How |
| --- | --- |
| S20 Duplicate review | "Continue" when duplicates are found (`S19-contacts` → `S20-default`; `S19-csv` → `S20-none` in prototype flow 4) |
| S22 pick mode (Finish) | "Continue" when no duplicates are found (step 4 skipped automatically, A-23) |
| Previous step | Android system back; iOS back chevron or edge swipe |
| Close | `x` → "Discard import?" dialog (S40) when anything was selected; otherwise S08 |

Duplicate detection runs after mapping because phones and emails are compared in their mapped type
(normalized numbers, lower-case emails).

## 3. Layout and components

Full-screen modal (import stack). Top to bottom:

1. **AppBar (modal)**: close IconButton `x` ("Close import"), title "Import". Same as every import step (C1, C2).
2. **ImportStepper**: "Map fields", "Step 3 of 5" (plain text: "Step 3 of 4"), segmented bar.
3. **Intro** (`text-body muted`): source summary, e.g. "88 contacts with 7 fields. Rename fields, set their type
   and choose what shows on cards."
4. Optional **Alert** (too many columns, title errors) inside the gutter.
5. **Card title**: Label + Select trigger (`heading` icon, current title field) + helper text.
6. **Fields** group header: "{n} fields" left, "On cards" right (column label for the switches).
7. **ListGroup of FieldRows** (Proposed component **FieldMappingRow**):
   - name (`text-body` medium) + **Title** badge (`primary-soft`, `heading` icon) on the title field + rename
     IconButton (`pencil`, 48 target, "Rename Phone");
   - "From: Side" caption when renamed;
   - sample values (`text-body-sm muted`, one line, truncates; screen readers hear "Sample values: …"); image
     fields show 4 real thumbnails + "35 of 88 items have a photo";
   - type Select chip (icon + type name + chevron, 36 visual inside 48 target);
   - several-values Select chip on multi-value fields ("All numbers");
   - notes in `text-caption muted`: empties ("Empty in 5 items"), multi counts, why a field was added;
   - trailing Switch "Show {field} on cards" (48 target).
8. **Hidden by SwipeSort** collapsed row (`eye-off`, "Hidden by SwipeSort (1)", reason) at the end of the group;
   expands in place to show those rows with their switch off.
9. **Bottom action**: full-width primary `h-14` "Continue" above a hairline.
10. Overlays: BottomSheet (type, title, several values, choose columns), iOS pull-down menu, web popover.

Type icons: Text `type`, Number `hash`, Phone `phone`, Email `mail`, Date `calendar`, Link `link`, Image `image`.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S19-default` | Google Sheets: Flat hunt 2026, both tabs, 8 rows (apartments a01–a08). Title Address. "Tab" field added from tab names |
| `S19-contacts` | Contacts: 88 selected (c001–c088). Name title; Phone multi-value (8 items with 2+ numbers, 5 empty); Email (5 empty); Photo (35) |
| `S19-csv` | candidates-q4.csv (k01–k12). Role auto-hidden (same value in all 12) |
| `S19-text` | Plain text: one field "Text", always the title; tip to rename it |
| `S19-rename` | Pencil tapped on Side: inline input "Family side", Save (check) button, original name below |
| `S19-type-sheet` | Type chip of Expected salary tapped: radio list with examples; types that don't fit show "Doesn't fit 11 values" |
| `S19-title-picker` | Card title select tapped: radio list of eligible fields with samples and empties |
| `S19-multi-value` | "All numbers" chip on Phone: three options with a live example (Mehmet Yılmaz, c002) |
| `S19-hidden-collapsed`, `S19-hidden` | End of the CSV list: auto-hidden group collapsed, then expanded |
| `S19-error-no-title` | Continue tapped after the title field (Name) was hidden: title select in error |
| `S19-error-title-empty` | Title set to Portfolio, empty in k04 Marco Bianchi and k08 Jakub Nowak |
| `S19-too-many` | applicants-export.xlsx with 64 columns: first 50 imported, notice with "Choose columns" |
| `S19-choose-columns` | Column chooser sheet at the 50 limit: unselected columns disabled until one is removed |
| `S19-loading` | Reading fields and samples (skeleton rows, Continue disabled) |
| `S19-large-text` | 200% font scale |
| `S19-ios`, `S19-ios-type-menu`, `S19-ios-multi-value` | iOS bar, type pull-down menu, page sheet |
| `S19-web-desktop` | Desktop browser: type select opens as a popover (flips up near the bottom) |

Offline: mapping works on data already read; no offline state (Google Sheets data is fetched in S15).

## 5. Interactions, gestures and transitions

- **Detection** (on entry): field names from the header row / contact fields / tab names; type guessed from
  the values (≥ 90% of non-empty values fit: phone, email, date, link, number; image for contact photos and
  image URLs; otherwise text). Title = the first text field with a value in ≥ 90% of items (contacts: Name;
  plain text: the only field).
- **Auto-hide**: fields with the same value in every item, or empty in ≥ 90% of items, start hidden and sit in
  the "Hidden by SwipeSort" group. Fields the user hides stay in place (rows never jump while editing).
- **Rename**: pencil turns the name into a focused Input with a Save (check) button; Enter or Save commits,
  Escape/back cancels. Empty names are not allowed (reverts). Names must be unique: "That name is already used.
  Choose another." The original source is never renamed (SAFE-01).
- **Type**: chip opens the type sheet (Android), pull-down menu (iOS) or popover (web desktop). Choosing applies
  immediately and closes. Values that don't fit the chosen type are kept as text and shown as-is.
- **Title**: the Card title select opens the title sheet. Image fields are not offered. Choosing a field that is
  empty in some items shows the title-empty error inline.
- **Show on cards** switch: off = the field is kept in the working copy, item details and export, but not on
  cards (domain-model › Field.hidden). Hiding the title field unsets the title.
- **Several values** (multi-value fields): sheet with three options; default "All numbers in one field"
  (card shows the first value and "+1"; details show all). "First number only" keeps the first and leaves the
  rest out of the list. "One field per label" creates Mobile, Home and Work fields. Applies immediately; Done
  closes.
- **Too many columns**: up to 50 fields per list. The first 50 columns are selected; "Choose columns" opens a
  searchable checklist; at 50 selected the others are disabled until one is unselected.
- **Continue**: validates (title set, title not empty in any item or the user chose to skip those items), then
  runs duplicate detection (spinner on the button, "Checking for duplicates…") and goes to S20 or S22.
- Motion: sheets per motion.md §3 (300 ms emphasized decelerate in, 200 ms out); expand/collapse of the hidden
  group 200 ms standard; rename input swap is instant. Reduced motion: fades only (150 ms).

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; close label "Close import" |
| Stepper | "Map fields"; "Step 3 of 5" (plain text "Step 3 of 4") |
| Intro, Sheets | "8 rows from Flat hunt 2026, tabs Kadıköy and Beşiktaş. Rename fields, set their type and choose what shows on cards." |
| Intro, Contacts | "88 contacts with 7 fields. Rename fields, set their type and choose what shows on cards." |
| Intro, CSV | "12 rows and 8 columns from candidates-q4.csv. Rename fields, set their type and choose what shows on cards." |
| Intro, plain text | "12 lines from your text become 12 items with one field. It is the title of every card." |
| Intro, too many | "214 rows and 64 columns from applicants-export.xlsx." |
| Title select | Label "Card title"; helper "The largest text on each card. Every item needs a value here."; placeholder "Choose a field"; a11y "Card title: Name. Choose the title field" |
| Group header | "7 fields"; "8 fields, 1 hidden by SwipeSort"; "50 fields"; column label "On cards" |
| Row | Badge "Title"; "From: {original name}"; a11y "Sample values: …"; "Rename {field}"; "Type: Phone. Change the type of Phone"; "Show {field} on cards" |
| Row notes | "Empty in 5 items"; "Empty in 1 item"; "8 items have 2 or more numbers. Empty in 5 items."; "35 of 88 items have a photo"; "Added from the tab names, so you can tell the tabs apart"; "Same value in all 12 items"; "Hidden on cards. Kept for details and export." |
| Rename | Field label (sr) "Field name"; "Save name"; "Original name in the source: Side"; error "That name is already used. Choose another." |
| Type names | "Text", "Number", "Phone", "Email", "Date", "Link", "Image" |
| Type sheet | "Type of Expected salary"; "The type changes how values look, sort and filter."; "Example: 78,000"; "Doesn't fit 11 values" |
| Title sheet | "Card title"; "Choose the field shown as the largest text on each card."; "Photo can't be the title. Image fields show in the card's image area." |
| Several values chip | "All numbers", "First number", "One per label"; a11y "Several values: All numbers. Change how Phone handles several values" |
| Several values sheet | "Several phone numbers"; "8 items have 2 or more numbers, like Mehmet Yılmaz."; "All numbers in one field" / "Cards show the first number and how many more. Item details show all of them."; "First number only" / "Other numbers are left out of this list. Your contacts aren't changed."; "One field per label" / "Creates Mobile, Home and Work fields, each with one number."; "Done" |
| Hidden group | "Hidden by SwipeSort (1)"; "Role: same value in all 12 items" |
| Plain-text tip | "Give the field a name" / "Cards and exports use it. For this list, Book or Title reads better than Text." / "Rename Text" |
| Error, no title | "Choose a title field. Every card needs a title, and hiding Name removed it." |
| Error, title empty | Inline "Empty in 2 of 12 items."; alert "2 items have no Portfolio" / "Marco Bianchi and Jakub Nowak would have cards without a title." / "Choose another field" / "Skip 2 items" |
| Too many columns | "64 columns found" / "Up to 50 fields can be imported. The first 50 columns are selected." / "Choose columns" |
| Choose columns | "Choose columns"; "applicants-export.xlsx, 64 columns"; search placeholder "Search columns"; "50 of 50 selected. Unselect a column to choose another."; "Column 51"; "Columns 8 to 48 selected"; "Done" |
| Loading | "Reading fields from candidates-q4.csv…" |
| Continue | "Continue"; while checking "Checking for duplicates…" |

## 7. Accessibility

- Focus order: Close, step heading, intro, Card title select, each row (name, rename, type, several values,
  switch), hidden group, Continue.
- Each switch is named "Show {field} on cards" and announces on/off; the title row's switch also says "Title".
- Chips are buttons with full names ("Type: Phone. Change the type of Phone"), `aria-haspopup="dialog"`.
- Sheets are dialogs with titled headings; radio lists use `role="radiogroup"` with radio buttons.
- Errors: icon + text, `aria-invalid` on the title select, focus moves to the first error after Continue; the
  error alert is `role="alert"`.
- Large text (`S19-large-text`): rows stack (name, wrapping samples, chips, then a labeled "Show on cards"
  switch row); stepper text stacks; Continue grows to 64.
- Touch targets ≥ 48 (chips sit inside 48 targets; rename and switch are 48).
- Reduced motion: sheets fade.

## 8. iOS and web differences

- **iOS** (`S19-ios`): 44 pt bar with "Back" chevron (to Select items) at the left, centered "Import", close `x`
  at the right; edge swipe goes back a step. The type chip opens a **pull-down menu** (UIMenu) with a check on
  the current type (`S19-ios-type-menu`). Title and several-values choices open **page sheets** with Cancel /
  Done (`S19-ios-multi-value`).
- **Web, mobile**: same as Android without system bars; browser back = previous step.
- **Web, desktop** (`S19-web-desktop`): phone column centered; selects open as **popovers** (listbox) anchored to
  the chip, flipping up when there is no room below; keyboard: arrows move, Enter selects, Escape closes.

## 9. Edge cases

- **Long names and values**: field names wrap; samples truncate to one line (full in the type sheet); Turkish
  +40% text wraps chips to a second line.
- **Missing values**: shown as "Empty in N items"; a field empty in every item is auto-hidden.
- **Duplicate column names** ("Phone", "Phone"): second becomes "Phone 2".
- **No header row** (CSV): columns are named "Column 1…"; the user renames them.
- **Too many columns**: limit 50 per list (A-24 extension); excess columns are listed in the chooser.
- **Very large imports** (5,000 rows): samples come from the first 200 rows; empties are counted over all rows.
- **Plain text**: single field, cannot be hidden, type changeable (e.g. Link for a list of URLs).
- **Mixed types** (a "Phone" column with notes): type stays the best fit; non-fitting values are kept as text.
- **Several values in non-contact sources** (cells with "a; b"): treated as text in this version.
