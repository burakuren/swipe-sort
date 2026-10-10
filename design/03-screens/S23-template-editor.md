# S23 Template editor

Frames: `S23-template-editor.html` (generator `tools/generators/S22-S23-templates.py`). Library and import finish:
`S22-template-library.md`. Components: `01-foundations/components.md` (SwipeCard, ListGroup, BottomSheet, Dialog,
AlertDialog, DropdownMenu, Snackbar, Select, Alert, Kbd). Data: `candidates` k01, k04, k09 and `templates`
t-candidate, t-candidate-compact in `02-data/sample-data.json`; list Frontend hiring, Q4 (`l-candidates`).

## 1. Purpose and requirements

Choose which fields appear on a list's cards and in what order, while watching the real card change. A template
has five slots in card order: **image area** (none, photo or initials, image on top, full image), **title**
(required), **subtitle**, **field rows** (0–6, ordered) and **tags** (0–3, ordered). Fonts, sizes and colors are
fixed by the SwipeCard and cannot be changed (TPL-04). Built-in templates are read-only and must be duplicated
first. Saved templates can be renamed, duplicated, deleted and used on any list.

Covers: TPL-02, TPL-03, TPL-04, TPL-05, TPL-06, TPL-07, TPL-08, TPL-09, TPL-10, TPL-11, TPL-12, TPL-01 (built-ins
read-only), SRC-10 (hidden fields stay off cards), GOAL-02, GOAL-03 (discard confirmation, Undo on delete),
VIS-02, VIS-05, VIS-11–VIS-14, TERM-01–TERM-03, PLT-01–PLT-04, PLT-13–PLT-17, PLT-21, PLT-23, SUC-06, DEL-25
(flow 4), SCR-23.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S22 pick mode | "Customize" (`data-action="customize-template"`) → `S23-default` (copy of the selected built-in, here Candidate for Frontend hiring, Q4) |
| S22 change mode | "Customize" (copy of the current built-in) or "Edit template" (current custom template) |
| S22 manage mode | tap a built-in tile → `S23-built-in`; tap a custom row or "Edit" in the actions sheet → `S23-edit-saved`; New template sheet → Continue → `S23-start` |

| To | How |
| --- | --- |
| Save dialog | "Save template" (`data-action="save-template"`) → `S23-save` |
| S22 pick mode | "Save" in the dialog (`data-action="confirm-save"`) → `S22-import-pick-custom` with the new template selected and snackbar "Template saved" |
| S22 change / manage | Save (changes apply to every list that uses it) or back without changes |
| Discard dialog | Back, close or edge swipe with unsaved changes → `S23-discard` (new template) or `S23-discard-changes` (saved template, = `S40-discard-template`) |
| Full-size preview | expand button on the preview → `S23-preview-full` |
| Field picker / image sheet | tap Title, Subtitle, "Add field row", "Add tag" → `S23-field-picker`; Image area → `S23-image-sheet` |
| Delete | overflow "Delete template" → dialog → S22 manage with "Template deleted" + Undo |

## 3. Layout and components

Pushed screen (inside the import modal stack in pick mode, in the Settings or list stack otherwise). Top to bottom:

1. **AppBar** small: back (`arrow-left`), title = template name ("New template" until saved) with a caption:
   "Copy of Candidate, not saved" / "Custom template" / "Built-in template" / "Custom template, not used by any
   list". Overflow IconButton only for saved custom templates (Rename, Duplicate, Delete template).
2. **Notice** (saved templates used by lists): info Alert (`layers`) "Used by Frontend hiring, Q4" / "Changes
   apply to that list too." Built-in: Alert (`lock`) "Built-in templates can't be changed" / "Duplicate this one
   to choose your own fields."
3. **Preview with** Select (only when opened from Settings, where there is no current list): the list whose items
   feed the preview; default = the list that uses the template, else the most recent list with matching fields.
4. **Preview** (pinned; does not scroll): the real SwipeCard from S25 (same markup and content rules) on the
   372 × 620 Android card box, drawn at 50% (`origin-top scale-50`) in a 320-high stage. Previous / Next
   IconButtons (outline, 48) at the left and right edges, vertically centered; expand IconButton
   (`maximize-2`, "See card at full size") top-right. Below: "Item 1 of 12" (`text-caption tabular-nums`,
   live region). Contextual helper (`text-body-sm muted`, centered) when the current item shows an edge case:
   missing values or long text. A hairline `border-b` separates the pinned preview from the scrolling slots.
5. **Slots** (scroll, `px-gutter`, sections 24 apart, section header `text-label muted` + counter right):
   - **Layout** ListGroup: rows "Image area" / value; "Title" (sub-label "Required") / field; "Subtitle" / field
     or "None". Each row opens a sheet. A subtitle bound to a hidden field shows `eye-off` "Hidden in this list,
     so cards leave it out".
   - **Field rows** "2 of 6": ListGroup of reorder rows: drag handle (`grip-vertical`, 36 wide, the drag target
     with the long-press anywhere on the row), field name (`text-body`) with the current item's value below
     (`text-body-sm muted`, 1 line), IconButtons Move up (`arrow-up`), Move down (`arrow-down`), Remove (`x`);
     first row's Move up and last row's Move down are disabled. Last row: "Add field row" (`plus`, primary).
   - **Tags** "1 of 3": same rows; "Add tag".
   - **Not on the card**: every remaining field: type icon, name, current value, text button "Add" (adds it as
     the last field row; when rows are full, as a tag; when both are full, disabled). Fields hidden in the list
     (S19) are listed last with `eye-off` "Hidden in this list" and no action. Footer: "Fields that aren't on the
     card still show in item details and exports."
6. **Bottom action**: Button lg (h-14) "Save template" (disabled for a saved template without changes). Read-only
   built-in: "Duplicate and edit".

### How the card renders each slot (same rules as S25 and components.md › SwipeCard)
- **Image area**: None → no image, content starts 28 from the top. Photo or initials (avatar) → the item's image
  cover-cropped in the top 46%; without an image, a 96 initials circle on `bg-muted`. Image on top (cover) →
  image in the top 46%; without one, a `bg-muted` block with `image-off`. Full image → the image fills the card;
  title (`text-title-2`), subtitle and the field rows joined into one line sit below it.
- **Title** `text-card-title`, up to 3 lines, then "…"; titles over 36 characters step down to `text-title-1`, up to 4 lines (as S25). **Subtitle** `text-body-lg muted`, 1 line.
- **Field rows**: with an image, rows are inline (64-wide label column, `text-body`) when every label fits the
  column (Phone, Email, City); otherwise, and always without an image, rows are stacked (label `text-body-sm muted`
  above value `text-title-3`), as in `S25-candidate`. Values truncate to 1 line. Rows without a value are left out.
  Rows that don't fit the card's height are dropped from the bottom (the item detail shows everything).
- **Tags**: secondary chips (`h-7`) pinned to the bottom; empty values left out.
- **Sparse cards (image area None, and Photo or initials when the item has no image; initials sit at the top of the block, 20 above the title)**: the title, subtitle and rows form one block that is vertically centered
  in the space above the tags (`my-auto`; when the block is taller than the space it starts at the top, 28 from
  the card edge). Templates with up to 3 field rows use larger values (`text-title-2`, rows 20 apart); 4–6 rows
  use `text-title-3`, 12 apart. A title-only card (no subtitle, no rows, e.g. plain text) uses `text-display` for
  the title. The size depends on the template's row count, not on the item, so it never jumps between cards when
  values are missing. Cards with an image are unchanged (the image takes the top 46%).
- Built-in Product renders its price and rating rows as the price line (`text-title-1` price, star rating with
  review count), as in `S25-product`. Built-in Photo shows file name and size as the line under the location.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S23-default` | Flow 4 after the edits: copy of Candidate for Frontend hiring, Q4. Image None, Title Name, Subtitle Location, rows Years of experience and Expected salary, tag Source. Preview Lena Hoffmann (k01) = `S25-candidate` |
| `S23-scrolled` | The same, scrolled: field rows, tags, Not on the card (Portfolio, Email, Role hidden) |
| `S23-start` | Just opened from "Customize": the unchanged copy of Candidate (avatar initials, subtitle Role is hidden in this list, 4 rows) |
| `S23-save` | "Save template": name Dialog, typed "Candidate, compact" (default suggestion "{built-in} copy") |
| `S23-save-error` | Save with an empty name (or a name already used: "You already have a template with this name. Choose another name.") |
| `S23-preview-missing` | Next to item 4, Marco Bianchi (k04): no salary, no portfolio. The card leaves both out; the rows say "No value for Marco Bianchi"; helper "2 empty fields are left out of this card." (TPL-06) |
| `S23-preview-long` | Item 9, Carolina Mendes Albuquerque de Souza (k09, 36 characters): the title wraps to 2 lines; rows truncate to 1 line; helper explains the rule (TPL-07) |
| `S23-preview-full` | Expand: the card at full sort size (372 × 620) with previous/next; close returns |
| `S23-loading` | Items for the preview are loading (large lists, first open): skeleton card, Save disabled |
| `S23-field-picker` | "Add field row" (the sheet hugs its content): available fields first with the preview item's values; fields already on the card show where they are (choosing one moves it); hidden fields disabled |
| `S23-image-sheet` | Image area options; Image on top and Full image are unavailable because the list has no Image field |
| `S23-reorder` | Dragging Expected salary to the top of 4 rows: lifted row (`bg-popover shadow-overlay`, primary ring, scale 1.02), dashed drop slot, the preview reorders live |
| `S23-validation` | Name moved from Title into field rows, then Save: Title row error, the preview marks the empty title slot ("No title", only in the preview) |
| `S23-discard` | Back from a new template that was never saved (import Customize) |
| `S23-discard-changes` | Back from a saved template with unsaved changes (same dialog as `S40-discard-template`) |
| `S23-built-in` | Built-in Candidate from Settings: read-only slots, "Preview with" list, "Duplicate and edit" |
| `S23-edit-saved` | Saved "Candidate, compact" from Settings or a list: used-by notice; Save disabled until something changes |
| `S23-menu` | Overflow: Rename, Duplicate, Delete template |
| `S23-rename` | Rename dialog → "Template renamed" |
| `S23-duplicated` | Duplicate: the editor switches to the copy "Candidate, compact (copy)" (not used by any list), scrolled to the field rows; snackbar |
| `S23-delete` | Delete a template in use: choose the replacement for Frontend hiring, Q4 (default Candidate, the built-in it was based on) |
| `S23-ios` | iOS: Cancel / Save in the navigation bar, no bottom button |
| `S23-web-desktop` | Desktop browser: keyboard reorder hint, visible focus on "Move Expected salary up" |
| `S23-large-text` | 200%: preview behind "See card preview", row controls labeled and moved under the field name |

Not applicable: offline (templates are local first; saving offline syncs later, no special UI), web-unavailable,
empty (a list always has at least a title field).

## 5. Interactions, gestures and transitions

- **Preview cycling**: Previous / Next step through the list's items in list order and wrap at both ends;
  swipe left/right on the preview does the same (no decisions are made here). The counter is a polite live region.
  Each change cross-fades the card (150 ms; reduced motion: instant).
- **Live update**: every slot change re-renders the preview at once (no Apply). Changes are kept in memory until
  "Save template"; nothing is written to the template or any list before that.
- **Reorder**: long-press the row or press the handle, then drag (row lifts: scale 1.02, `shadow-overlay`,
  150 ms; other rows shift with 200 ms standard easing; haptic selection tick on each slot change; drop 200 ms).
  Auto-scrolls near the edges. Move up / Move down buttons do the same one step at a time (screen-reader and
  switch-access path). Reduced motion: rows swap without sliding.
- **Remove** (`x`): the field moves to "Not on the card" immediately; no confirmation (Undo by adding it back;
  nothing is lost until Save).
- **Pickers**: Title / Subtitle / Add field row / Add tag open the field picker sheet; choosing a field that is
  already in another slot moves it (the old slot empties). Title can be emptied only by moving its field; Save
  then shows the validation state and focuses the Title row.
- **Limits**: 6 field rows, 3 tags. At the limit, "Add field row" / "Add tag" are disabled with "6 field rows at
  most. Remove one to add another." / "3 tags at most. Remove one to add another."; the Not on the card "Add"
  falls back to tags, then disables.
- **Image area**: options needing an Image field are disabled when the list has none, with the reason.
- **Save template**: new template → name dialog → Save → back to the origin (pick: `S22-import-pick-custom`,
  the new template selected; change: applied to the list; manage: listed first in Your templates). Snackbar
  "Template saved". Existing template → saves directly (no dialog), every list using it updates.
- **Back / close / edge swipe** with unsaved changes → discard dialog: new template "Keep editing" / "Discard template";
  saved template "Keep editing" / "Discard changes". Dialogs follow S40 (A-112): centered, initial focus on "Keep editing".
  Without changes → back immediately.
- **Built-in**: "Duplicate and edit" creates "{name} (copy)" and opens it (`S23-start` state, caption "Copy of
  Candidate").
- **Overflow** (saved custom): Rename (Dialog), Duplicate (switches to the copy, snackbar "Duplicated as “…”"),
  Delete template (AlertDialog with replacement Select for each list using it → S22 manage, "Template deleted" +
  Undo).

## 6. Copy

| Element | Text |
| --- | --- |
| App bar | "New template", "Copy of Candidate", "Copy of Candidate, not saved", "{template}", "Custom template", "Built-in template", "Custom template, not used by any list"; back "Back to Finish" / "Back to Card templates" / "Back to {list}"; "More options" |
| Used-by notice | "Used by Frontend hiring, Q4" / "Changes apply to that list too."; 2 lists: "Used by 2 lists" / "Changes apply to both."; 3+: "Used by 3 lists" / "Changes apply to all of them." |
| Built-in notice | "Built-in templates can't be changed" / "Duplicate this one to choose your own fields." |
| Preview | "Item 1 of 12"; "Previous item", "Next item", "See card at full size"; "Preview with {list}"; loading "Loading items…" |
| Preview helpers | "2 empty fields are left out of this card." / "1 empty field is left out of this card." / "Long titles wrap to 3 lines; very long ones get a smaller size and up to 4. Values end with … and show in full in item details." / preview-only slot "No title" |
| Full-size preview | "Card preview"; "Close preview"; "Item 1 of 12" |
| Section headers | "Layout", "Field rows" + "2 of 6", "Tags" + "1 of 3", "Not on the card" |
| Layout rows | "Image area" — "None" / "Photo or initials" / "Image on top" / "Full image"; "Title" + "Required"; "Subtitle" — field or "None"; "Hidden in this list, so cards leave it out" |
| Reorder rows | value line or "No value for {item title}"; a11y "Move {field} up", "Move {field} down", "Remove {field} from field rows" / "… from tags"; large text "Up", "Down", "Remove" |
| Add | "Add field row", "Add tag"; limits "6 field rows at most. Remove one to add another." / "3 tags at most. Remove one to add another." |
| Not on the card | "Add" (a11y "Add {field} as a field row"); "Hidden in this list"; footer "Fields that aren't on the card still show in item details and exports."; other list's field "Not in this list" |
| Field picker | "Add field row" / "Add tag" / "Title field" / "Subtitle field"; subtitle "Values from {item title}"; "On the card already: choosing one moves it here"; "Title", "Subtitle", "Field row", "Tag"; "Hidden in this list"; subtitle sheet adds "None" |
| Image sheet | "Image area"; "None" — "Text only. Rows get more room."; "Photo or initials" — "Shows the item's image, or initials when it has none." (no Image field: "Shows initials: this list has no Image field."); "Image on top" — "Shows the item's image above the title."; "Full image" — "The image fills the card, details below it."; unavailable: "Needs an Image field. This list has none." |
| Validation | "Choose a title field. Every card needs one."; Title value "Not set" |
| Save | "Save template"; dialog "Save template", "Template name", helper "You can use it on any list.", "Cancel", "Save"; errors "Enter a name for the template." / "You already have a template with this name. Choose another name."; success "Template saved" |
| Discard (new template) | "Discard this new template?" / "It hasn't been saved. The list keeps the template selected in the finish step." (from Settings: "It hasn't been saved.") / "Keep editing", "Discard template" (destructive) |
| Discard (saved template) | "Discard changes to “Candidate, compact”?" / "Your layout changes won't be saved. Frontend hiring, Q4 keeps the current layout." (2+ lists: "Lists using it keep the current layout.") / "Keep editing", "Discard changes" (destructive). Source of truth: `S40-discard-template` |
| Built-in action | "Duplicate and edit" |
| Overflow | "Rename", "Duplicate", "Delete template" |
| Rename | "Rename template", "Template name", "Cancel", "Rename"; "Template renamed" |
| Duplicate | copy name "{name} (copy)"; "Duplicated as “Candidate, compact (copy)”" |
| Delete | "Delete “Candidate, compact”?" / "Frontend hiring, Q4 uses this template. Its cards switch to the template you choose."; "Card template for Frontend hiring, Q4"; "Candidate is the template it was based on."; "Cancel", "Delete template"; result "Template deleted" + "Undo" |
| Web hint | "Alt + ↑ ↓ moves the focused row" |
| Large text | "See card preview" |
| Errors | Save failed (storage): "The template couldn't be saved. Your phone is out of storage. Free up space and try again." |

## 7. Accessibility

- **Preview**: `role="img"` with the full card text ("Card preview: Lena Hoffmann, Berlin. Years of experience 6.
  Expected salary €78,000. Tag Referral."), re-announced politely after each change, so screen-reader users hear
  the result of every edit. Item changes announce "Item 4 of 12".
- **Reorder**: drag is never required: Move up / Move down / Remove buttons on every row (48 targets); disabled at
  the ends with the real `disabled` attribute. After a move, focus stays on the moved row's button and a live
  region announces "Expected salary, row 1 of 4." Custom actions on the row for TalkBack/VoiceOver: "Move up",
  "Move down", "Remove". Web: Alt + ↑/↓ on a focused row.
- **Sheets/dialogs**: focus moves in; background inert; Escape/back closes. Disabled image options keep their
  reason as readable text (never dimmed below AA; only the radio and schematic use `opacity-50`).
- **Validation**: the Title row gets `aria-invalid`, the message is announced, focus moves to it. The error is
  icon + text + border, not color alone.
- Focus order: back, overflow, preview controls (previous, expand, next), slots top to bottom, Save.
- Large text (`S23-large-text`): preview behind a button (opens the full-size preview), layout rows stack label and
  value, row controls become labeled buttons under the field name, Save grows to 64.

## 8. iOS and web differences

- **iOS** (`S23-ios`): 12 dp between the navigation bar and the preview; navigation bar with "Cancel" (left) and "Save" (right, semibold) instead of the back arrow
  and the bottom button; Cancel with changes → native alert with the discard copy. Pickers are page sheets with a
  grabber and Cancel / Done. Overflow → action sheet. Reorder uses the same rows (handle + buttons); the system
  edit mode is not used so both platforms share one component.
- **Web mobile**: as Android.
- **Web desktop** (`S23-web-desktop`): phone column centered; drag rows with the mouse (cursor `grab`/`grabbing`);
  Alt + ↑/↓ reorders the focused row (hint shown under the slots, web only); ← / → are not bound here (they sort
  only in S25); visible focus ring on every control; pickers open as popovers anchored to the row.

## 9. Edge cases

- **Missing values** (k04): rows without a value are left out of the card; the editor shows "No value for …" on
  that row so the person understands the gap; the helper counts them.
- **Long text** (k09): title clamps at 3 lines with "…", rows at 1 line; long labels switch the card to stacked
  rows; full values in item details.
- **No Image field**: Image on top and Full image unavailable; Photo or initials shows initials.
- **Hidden fields** (S19): listed under Not on the card with "Hidden in this list"; a template slot bound to a
  hidden field is left out of the card and flagged in the editor (`S23-start`).
- **Template from another list** (TPL-12): slots whose field this list doesn't have show "Not in this list" and
  are left out of the card; Save keeps them for the lists that have them.
- **Too many rows for the card height** (6 stacked rows + 3-line title): rows that don't fit are dropped from the
  bottom of the card; the helper says "{n} rows don't fit on this card. They show in item details."
- **Large lists**: cycling loads items lazily; the counter shows the true total ("Item 1 of 1,240").
- **Offline**: editing and saving work offline; shared lists using the template receive the change when back online.
- **Shared lists**: saving a template used by a shared list changes the cards for every member; the used-by notice
  says so ("Used by Wedding guests. Changes apply for all 3 members.").
- **Built-ins** can never be saved over; Duplicate is the only path.

### Decisions
- **D-S23-1** The preview is pinned at the top at 50% scale; the full-size preview is one tap away (and the main
  preview for large text and screen readers).
- **D-S23-2** Image area options are named by what they do ("Photo or initials", "Image on top", "Full image")
  instead of avatar / cover / full.
- **D-S23-3** Rows are stacked (label above value) whenever the card has no image or a label is wider than the
  64 dp label column; this keeps `S25-candidate` and `S25-default` both valid outputs of one rule.
- **D-S23-4** Remove has no confirmation: the field moves to Not on the card and nothing is written until Save.
- **D-S23-5** New templates are named in a dialog at save time; saving an existing template needs no dialog.
- **D-S23-6** `S23-default` shows the edited state so flow 4 can go straight to Save; the first-open state is
  `S23-start`.
- **D-S23-8** Sparse cards are vertically balanced with larger values (rule in §3); S25-candidate follows the same rule.
- **D-S23-7** The used-by notice is shown for a template used by one list in the frames (sample data has no
  template used by two lists); the 2-list and 3+ copy is specified above.
