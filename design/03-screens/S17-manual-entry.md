# S17 Manual entry

Frames: `S17-manual-entry.html` (generator `tools/generators/S17-manual-entry.py`). Components:
`01-foundations/components.md`. Next step: `S22-template-library.html#S22-import-pick`.

## 1. Purpose and requirements

Create a list by typing items in. Because there is no source to map, the user first defines the fields (Set up
fields), then adds items one at a time with a form, with a fast "Add another" path. Field mapping (S19) and
duplicate review (S20) are skipped (A-24). Sample: "Desk setup" (`l-desk`, a manual list) with products p01–p04.

Covers: SRC-01 (manual entry), SRC-03, SRC-04, SRC-07 (items are entered instead of selected), SRC-09/SRC-11/
SRC-12 (name, type and title defined inline), SRC-16/SRC-17 (hand-off to S22 pick), GOAL-02, GOAL-03 (undo
delete), GOAL-05, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, VIS-11–VIS-14, TERM-01, SCR-17.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S11 source picker | Tile "Manual entry" (`S11-source-picker.html#S11-default`) |
| S21 add items | Tile "Manual entry" in list context: the field step is skipped (fields come from the list) and the item form shows the list's fields |
| S22 pick (back) | System back / iOS back returns to Add items with all items kept |

| To | How |
| --- | --- |
| S22 template library, pick mode | "Continue" on Add items (`S22-template-library.html#S22-import-pick`, `data-action="continue"`) |
| S11 | System back from Set up fields |
| S08 home | Close (`x`). With fields changed or items added, the S40 "Discard import?" dialog asks first (`S40-global-patterns.html#S40-discard-import`) |

## 3. Layout and components

Full-screen import modal, app bar title "New list" (no source is imported).

**Set up fields** (`S17-fields`):
1. AppBar (modal): close, "New list".
2. ImportStepper: "Set up fields", "Step 2 of 4" (Choose source, Set up fields, Add items, Finish).
3. Heading "Fields for your items" + one sentence.
4. ListGroup of field rows: name (`text-body` medium), Title badge on the title field, type chip (Select trigger
   styled as a 36 chip inside a 48 target; the title's chip is a static locked badge), trailing IconButton:
   rename (`pencil`) for the title, remove (`x`) for others. Tapping a field name renames it inline (same pattern
   as S19-rename).
5. Button `outline` full width "Add field" → Add field sheet.
6. "Suggestions": FilterChip-style buttons "+ Rating", "+ Category", "+ Date" (add with a guessed type).
7. Bottom: Button lg "Continue".

**Add field sheet** (`S17-field-sheet`): BottomSheet "Add field": Input "Field name", radio list "Type" with 7
types (icon + name), Button "Add field".

**Add items** (`S17-default`):
1. AppBar, ImportStepper "Add items", "Step 3 of 4".
2. Fields summary line "5 fields: Name, Price (€), Store, Photo, Link" + link "Edit fields" (back to Set up fields).
3. Header row: "3 items" (`text-title-3`) + Button outline "Add item" (`plus`).
4. ListGroup of ItemRows: 40 thumbnail (Image field; initials or `image-off` placeholder without one), title
   (up to 2 lines, then truncates), meta line (next two non-empty fields, comma separated; numbers keep the unit from the field name, e.g. "€389, Nordhaus"), IconButtons Edit (`pencil`) and
   Delete (`trash-2`).
5. Bottom: Button lg "Continue".

**Item form** (sheet, `S17-add-item`): tall BottomSheet "New item": one input per field in field order (Name
required; Number fields use the numeric keyboard; Link uses the URL keyboard; Image fields take an **image link**: a URL
input with a leading `link` icon and the placeholder "Image link", a helper line, and a 36 thumbnail at the
right end of the input once the link loads. There is no photo picker or camera (D-32, A-160).) Actions side by side: Button `secondary` "Add another" and Button
`default` "Add item".

**Empty state** (`S17-empty`): EmptyState with `list-plus`, title, sentence and primary "Add item". The bottom
Continue is hidden in this state so there is only one primary button.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S17-fields` | First screen after choosing Manual entry. Starts with Name only; frame shows 5 fields defined |
| `S17-field-sheet` | "Add field" or a suggestion with a typed name |
| `S17-empty` | Fields confirmed, no items yet |
| `S17-default` | 3 items added (p01–p03) |
| `S17-add-item` | "Add item" opens the form; filled for p04 |
| `S17-add-another` | After "Add another": the item is saved, the form is cleared, Name has focus, status line confirms |
| `S17-validation` | "Add item" / "Add another" with an empty Name, a non-numeric Price and an image link that doesn't open an image (keystone.example/p/1111, a product page) |
| `S17-image-link-loading` | An image link was pasted: spinner in the 36 slot, helper "Loading the picture…" |
| `S17-image-link-offline` | Offline (banner under the app bar): the link is kept, `image-off` placeholder in the slot, neutral helper; no error; the item saves |
| `S17-edit-item` | Edit IconButton on a row: same form titled "Edit item" with Save changes and Delete item |
| `S17-deleted` | Delete IconButton (or Delete item in the form): row removed, snackbar with Undo |
| `S17-large-text` | 200% font scale on the item list |
| `S17-ios-add-item` | iOS page sheet for the form |

Loading, offline and error apply only to the Image field, because an image link needs a connection (A-160):
loading (`S17-image-link-loading`), offline (`S17-image-link-offline`), error (`S17-validation`). Everything
else is local and instant. Web-unavailable: none (the Photo field is an image link on every platform).

## 5. Interactions, gestures and transitions

- **Fields**: Name is always the title and always text (title can be renamed, not removed or retyped). Other
  fields: tap the chip to change type (same type sheet as S19), `x` removes (no confirmation while there are no
  items; with items, S40 dialog (`S40-global-patterns.html#S40-remove-field`) "Remove Price (€)?" / "3 items have a value in Price (€). The values are removed with the field." /
  "Cancel", "Remove field"; after removing, snackbar "Removed Price (€)" with "Undo" restores the field and its values). Max 50 fields (same limit as imports). Field names must be unique; duplicate name
  error "A field with this name already exists."
- **Suggestions** add a field in one tap with a guessed type (Rating → Number, Category → Text, Date → Date) and
  disappear from the suggestions.
- **Add item**: opens the sheet (motion.md §3: 300 ms emphasized decelerate; reduced motion: fade 150 ms), focus
  in Name, keyboard up. Return on each input moves to the next field; Return on the last field = "Add another".
- **Add another**: validates, saves, clears the form, keeps the sheet open, returns focus to Name, shows the
  status line "Added {title}. {n} items." (polite announcement). Fast entry never closes the keyboard.
- **Add item**: validates, saves, closes the sheet; the new row appears at the end of the list and scrolls into
  view.
- **Validation** runs on submit, then live per field once shown. Errors: icon + text under the field, `border-2
  border-destructive`, focus moves to the first invalid field. Only Name is required.
- **Edit**: Edit IconButton (or tap the row) opens the form filled; "Save changes" saves and closes; closing with
  unsaved changes asks "Discard changes to Walnut sit-stand desk, 140 × 70 cm?" (S40, `S40-global-patterns.html#S40-discard-edits`) with "Your edits won't be saved. The item keeps its current values." / "Keep editing", "Discard changes".
- **Delete**: immediate, with snackbar "Deleted {title}" + "Undo" (6 s, motion.md §3). Undo restores the item at
  its position.
- **Continue**: hands the list (fields + items) to S22 pick mode, where the card template is suggested from the
  field types (Image + Number → Product) and the list is named.
- **Close**: S40 "Discard import?" (`S40-global-patterns.html#S40-discard-import`) when anything was entered.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "New list"; close label "Close" |
| Stepper | "Set up fields" / "Add items"; "Step 2 of 4", "Step 3 of 4" |
| Fields heading | "Fields for your items" |
| Fields body | "Every item needs a title. Add fields you want to compare, like a price or a link." |
| Title badge | "Title" |
| Locked type (screen reader) | "Text, the title is always text" |
| Field row labels | "Rename Name", "Remove Price (€)", "Type: Number. Change the type of Price (€)" |
| Add field | "Add field" |
| Suggestions | "Suggestions"; "Rating", "Category", "Date" (labels "Add field Rating") |
| Field sheet | "Add field"; "Field name"; "Type"; types "Text", "Number", "Phone", "Email", "Date", "Link", "Image"; "Add field" |
| Field errors | "Enter a field name." / "A field with this name already exists." / "Up to 50 fields." |
| Remove field dialog (`#S40-remove-field`) | "Remove Price (€)?" / "3 items have a value in Price (€). The values are removed with the field." / "Cancel", "Remove field"; snackbar "Removed Price (€)" + "Undo" |
| Summary | "5 fields: Name, Price (€), Store, Photo, Link"; "Edit fields" |
| Empty state | "No items yet" / "Add the first item. You can add more one after another." / "Add item" |
| List header | "3 items" ("1 item") ; "Add item" |
| Row actions | "Edit {title}", "Delete {title}" |
| Item sheet | "New item" / "Edit item"; field labels from the fields ("Name (required)", "Price (€)", "Store", "Photo", "Link") |
| Photo (image field) | placeholder "Image link"; helper (`text-body-sm`) "Paste a link to an image. Cards show the picture from this link."; loading "Loading the picture…"; offline "You're offline. The link is saved, and the picture loads when you're back online."; error "This link doesn't open an image. Check it, or leave the field empty." |
| Form buttons | "Add another", "Add item"; "Save changes", "Delete item" |
| Status after Add another | "Added Low-profile mechanical keyboard. 4 items." |
| Validation | "Enter a name. Every item needs a title." / "Enter a number, like 389." / "Enter a full link, like oakline.example/p/1037." / "Enter a full email address, like name@example.com." / "Enter a date, like Oct 12, 2026." |
| Snackbar | "Deleted Ergo Mesh task chair" + "Undo" |
| Discard edit dialog (`#S40-discard-edits`) | "Discard changes to {item name}?" / "Your edits won't be saved. The item keeps its current values." / "Keep editing", "Discard changes" |
| Primary | "Continue" |
| iOS sheet | "Cancel", "New item", "Add" |

## 7. Accessibility

- Focus order (Add items): Close, step indicator, fields summary, Edit fields, list header, Add item, each row
  (title, Edit, Delete), Continue. In the sheet: title, Close, inputs in field order, Add another, Add item.
- Sheets are modal dialogs (`aria-modal`), focus moves to the first input on open and back to "Add item" on close.
- Edit and Delete IconButtons have names that include the item title; targets are 48.
- Validation errors are linked with `aria-describedby`, `aria-invalid`; the first invalid field receives focus.
- The status after "Add another" and the delete snackbar are polite live regions; Undo is reachable by keyboard
  and stays ≥ 10 s with a screen reader running.
- Type options are a `radiogroup` of radio buttons with icon + name (color never carries meaning).
- Large text (`S17-large-text`): titles wrap instead of truncating; Edit and Delete become labeled buttons under
  each row; the app bar title grows to `text-title-2`.

## 8. iOS and web differences

- **iOS** (`S17-ios-add-item`): bar with a back chevron to Set up fields (edge swipe back) and close `x` at the
  right. The item form is a page sheet with "Cancel" and "Add" in its own bar (Add = save and close); "Add another"
  is a full-width secondary button under the form. Field type uses a pull-down menu (as S19-ios-type-menu).
  Destructive confirmations use an action sheet with the same copy.
- **Web** (mobile and desktop): same as Android, including the image-link Photo field; Enter on the last field = Add another, Ctrl/Cmd+Enter = Add item. No separate frame needed.

## 9. Edge cases

- **Long titles** (Walnut sit-stand desk, 140 × 70 cm): rows truncate to 1 line; the form input scrolls; large
  text wraps.
- **Missing values**: only Name is required; rows skip empty fields in the meta line; no photo → placeholder.
- **Image fields** (D-32, A-160): no photo-library access at all for now, so an Image field takes an image
  link (like CSV image links, A-131). The control: `link` icon leading in every state, URL input, a 36 slot at
  the end, helper line in `text-body-sm` (the same control as S26's image-link edit).
  - **Loading**: after a paste or on blur, the slot shows a spinner and the helper reads "Loading the
    picture…" (`role="status"`). Loaded: the slot shows the thumbnail and the helper returns.
  - **Offline**: no check is possible, so there is no error. The link is kept, the slot shows `image-off`, the
    helper says the picture loads when the connection is back, and the item saves. The image downloads when
    online, like import links (A-167); until then the card shows the `image-off` placeholder.
  - **Error** (online, the link answers but isn't an image, or doesn't answer): inline error under the field,
    red border, `image-off` in the slot. It doesn't block saving: "Add item" saves the item without a picture
    (the link is cleared) unless the person fixes it. Error haptic is not used (it's not a failed action).
  - Links are stored as text; the image is fetched and cached like other image fields (D-15).
- **Many items** (hundreds): the list virtualizes; header count updates; Continue always visible.
- **Limit**: 5,000 items per list created this way (same as imports); at the limit "Add item" is disabled with
  "Up to 5,000 items in one import."
- **Duplicate titles**: allowed (manual entry is intentional); no duplicate review for manual lists.
- **Editing fields after items exist**: removing or retyping a field asks first; retyping keeps values that fit
  and reports "2 values don't fit Number and were kept as text in item details" (values are never deleted
  silently).
- **App closed mid-entry**: the draft (fields + items) is saved locally and restored next time the user opens
  Manual entry ("Continue where you left off?" handled by S40 resume pattern).
- **Add items to an existing list (S21)**: the form uses the list's fields; Set up fields is skipped; button
  "Add to list" replaces Continue (see S21).

## Decisions

- **D-S17-1** Manual entry has 4 steps: Choose source, Set up fields, Add items, Finish. Set up fields takes the
  place of Map fields; Review duplicates is skipped for typed items.
- **D-S17-2** App bar title "New list" (nothing is imported).
- **D-S17-3** The title field is always "Name", always text and cannot be removed; it can be renamed.
- **D-S17-4** Items are entered in a sheet with "Add another" (save, clear, keep open) and "Add item" (save, close);
  Return on the last field = Add another, for fast entry.
- **D-S17-5** Delete is immediate with Undo (no confirmation dialog), consistent with GOAL-03 and the snackbar
  pattern.
- **D-S17-6** In the empty state the bottom Continue is hidden so the empty-state "Add item" is the only primary.
