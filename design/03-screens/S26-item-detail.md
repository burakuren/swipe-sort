# S26 Item detail, editing and notes

Frames: `S26-item-detail.html` (generator: `tools/generators/S26-item-detail.py`). Opened over
`S25-sorting.html` as a bottom sheet and pushed from `S28-results.html` / `S36-conflicts.html`.
Data: `contacts` c077, c014, c007, c045, c002, c006, c012, c079; `products` p03 (Desk setup);
`trips` tr13, tr14 (Trip ideas); `apartments` a07; `shared.items`, `shared.notes`, `shared.edits`, `productDecisions`.

## 1. Purpose and requirements

Show everything about one item (all fields, its image, my decision, notes and, on shared lists, who
decided what), let the user fix a field on the spot without fear (edits are marked and revertible; the
source is never changed), and let them decide or change their decision.

Covers: SRT-10 (notes from detail), SRT-11, SRT-12, SAFE-01, SAFE-02, SAFE-03, SAFE-04, DM-01, DM-02,
DM-03–DM-05, DM-18, DM-19, DM-20, COL-16, RES-06, SRC-13 (multi-value display and editing), GOAL-02,
GOAL-03, PLT-01–PLT-06, PLT-13–PLT-17, PLT-21, PLT-23, STK-06, STK-07, VIS-09, VIS-13, SUC-06, SCR-26.

## 2. Entry points and exits

| From | Presentation | How |
| --- | --- | --- |
| S25 sorting | Bottom sheet over the stack (`S26-default`) | Tap the card, menu "Open item details", card action "Open details", Enter on desktop web |
| S28 results | Pushed screen (`S26-product`, `S26-shared-conflict`) | Tap a row |
| S36 conflicts | Pushed screen | "Details" on the conflict card |
| S40 sync outcome | Pushed screen (`S26-edit-replaced`) | "View" on the snackbar `S40-outcome-edit-replaced` (D-09 row 1): my edit was replaced by a later one |

| To | How |
| --- | --- |
| Back to S25 | Close (`x`), swipe the sheet down, Android back, Esc on web; or decide with Reject / Maybe / Accept in the sheet (the card then runs its commit) |
| Back to S28 / S36 | Back arrow, Android back, iOS edge swipe |
| Full-screen detail | Expand button or drag the sheet up (`S26-expanded`); collapse with `chevron-down` |
| Edit mode | "Edit", tap any field, or "Add phone" on an empty field |
| Revert dialog, delete-note dialog | "Revert to original", "Delete" on my note |
| S36 | "Review conflicts" on a conflict item |
| S10 | "Restore list" on archived lists |
| External browser | Link field values open the browser (in-app browser tab on Android/iOS) |

Route: `list/[listId]/item/[itemId]` (pushed); the sheet uses the same component with `presentation: sheet`.

## 3. Layout and components

Same content in both presentations; only the container and the bottom bar differ.

**Container**
- *Sheet over S25*: BottomSheet (`bg-popover rounded-t-sheet shadow-sheet`, scrim 50%), first snap point
  at 85% of the screen, second at full screen. Header row: "Item details" (`text-label muted`), expand
  IconButton (`maximize-2`, "Open full screen"), close IconButton (`x`, "Close details"). Pinned
  **decide bar**: three pill Buttons in soft decision colors with icon + verb (Reject, Maybe, Accept), in
  that order.
- *Expanded / pushed*: small AppBar (back arrow or `chevron-down`, list name and round as a muted caption
  when expanded from S25, overflow menu when pushed). Pushed screens have no decide bar; My decision is a
  control instead (below).

**Content, top to bottom** (every text edge on the 20 dp gutter; section headers are not inset)
1. **Header**: person and generic templates show Avatar 64 (photo or initials) + title (`text-title-2`, wraps
   fully, never truncates) + subtitle field (`text-body muted`). Product and photo templates show the image
   first (`rounded-group`, 176–240 high; Photo template `object-cover`, products `object-contain` on `bg-muted` so
   the product is never cropped), then title and subtitle. Expanded person items show
   the photo as a 224-high image.
2. **My decision**: from S25, a row "My decision" + DecisionBadge ("Not decided yet" with `circle-dashed`).
   From Results / Conflicts, a **decision control**: three equal Buttons in a `radiogroup`, Reject / Maybe /
   Accept, unselected = outline with the icon in its decision color, selected = solid decision fill with
   icon + label; a muted line below ("Decided in Round 1, Oct 4." or the shared consequence).
3. **Who decided what** (shared lists only, COL-16): section header with the StatusBadge (Agreed / Pending /
   Conflict) and, when there is one, the final DecisionBadge; a ListGroup of MemberDecisions rows (Avatar 32,
   name, role caption for the Decision Maker, DecisionBadge or "Not decided"); me first as "Deniz (you)".
   Below, for conflicts: "Mert resolves conflicts as Decision Maker." + "Review conflicts" (rule-dependent
   copy in §6). While sorting with others' decisions hidden, the group is replaced by a muted note (SRT-12).
4. **Notes**: section header "Notes"; note cards (radius 12): shared notes on `bg-muted`, my private note
   with a dashed `border-input` outline, `lock` badge "Only you"; each card: author avatar 24 + name ("You"
   for me), date, text; my note has "Edit" and "Delete" text buttons (48 high). "Add note" (outline Button,
   `sticky-note`) when I have no note. Solo lists show "My note" with no avatar and no private option.
   Placement: Notes come before Fields when a note exists (it is what people come back for), after Fields
   when empty.
5. **Fields**: section header "Fields" with an "Edit" text button (`pencil`). ListGroup rows (min 48):
   label column 96 wide (`text-body-sm muted`), value (`text-body`, wraps, `tabular-nums`), optional
   trailing meta (phone label "Mobile", "2,870 reviews", image dimensions, `external-link` for links). Each
   row is a link into edit mode focused on that field. Multi-value fields list every value with its label.
   Missing values: "Add {field}" (`plus`, primary) when editable, "—" when read-only. Edited fields: under
   the value, an "Edited" (or "Edited by Mert") Badge with `pencil-line`, "Original: İstanbul" and the
   "Revert to original" text button (`undo-2`).
6. **Source line** (`info` icon, `text-body-sm muted`): where the item came from and that the source is not
   changed (SAFE-01, SAFE-02).

**Edit mode** (`S26-edit` and variants): the sheet title becomes "Edit {title}", the content becomes a
form: helper "Changes stay in SwipeSort. The source isn't changed.", then one Input per field with its label
above; the pinned bar becomes "Cancel" (outline) + "Save changes" (primary). Field types:

| Type | Control | Keyboard / picker |
| --- | --- | --- |
| text | Input | default, sentence case off for names |
| phone | Input `type=tel`; multi-value: rows of label Select (Mobile, Home, Work, Other) + Input + remove IconButton, "Add another phone" | phone pad |
| email | Input `type=email`, validated on Save | email keyboard |
| number | Input `inputmode=decimal`, unit suffix (EUR, MB) | numeric |
| date | Input showing the formatted value + `calendar` IconButton | system date/time picker (out of scope). No frame since D-32 (no date field in the sample lists in use, A-171); same layout as the link Input with its trailing button |
| link | Input `type=url` + `external-link` IconButton "Open link" | URL keyboard |
| image (contact photo) | Avatar 64 + "Remove" (outline, `trash-2`) + line "From Contacts. Removing it here doesn't change your contacts."; no photo: initials + "No photo in Contacts." No add or replace (D-32: no photo library or camera, A-170) | none |
| image (from a link: CSV, Google Sheets, manual entry) | The image link as an Input `type=url` with a leading `link` icon (every state) and a 36 thumbnail at its end once the link loads, helper "Paste a link to an image. Cards show the picture from this link." (same control as S17, A-160); clearing it removes the image | URL keyboard |

An edited field shows "Original: …" under its input while editing.

Components: BottomSheet, AppBar, Avatar, DecisionBadge, StatusBadge, Badge (Edited, Only you), MemberDecisions
(expanded), ListGroup + rows, Button, IconButton, Input, Label, Textarea, Switch, Select, Snackbar,
AlertDialog, Alert, Skeleton, OfflineBanner, Kbd.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S26-default` | Mia Andersson (c077) over S25: not decided, 6 fields, no notes, decide bar | Tap the card |
| `S26-expanded` | Full screen with the photo | Drag up / expand |
| `S26-photo` | tr13 "Alfama, Lisbon" (Trip ideas, Photo template) over `S25-photo`: image, Place, Country, Best time, Budget (EUR); source line names trip-ideas.csv | Photo template list |
| `S26-long-text` | c014: name and email wrap in full; Phone "Add phone"; my note first with Edit / Delete | Long values, missing value |
| `S26-edit` | Edit mode on c007, phone focused, "Original: +90 500 000 97 4" | Edit or tap a field |
| `S26-edit-error` | Invalid email "gokhan.dogan@example" | Save with an invalid value |
| `S26-saved` | Phone marked Edited with original and Revert; snackbar "Changes saved" | Save changes |
| `S26-edit-multi` | c002 phones: Mobile and Home, add/remove, label Select | Editing a multi-value field |
| `S26-edit-product` | p03: image link (with thumbnail), number with EUR suffix, rating, reviews, link | Product list |
| `S26-edit-image-link` | tr13: the Photo field edited as its image link (focused, thumbnail), Place, Country, Best time, Budget with EUR suffix (the input label drops the "(EUR)" the suffix already shows, as Price does in `S26-edit-product`; read mode keeps "Budget (EUR)"). Replaces `S26-edit-date` (D-32: the Trip ideas list has no date field, A-171) | Image field from a link |
| `S26-edited` | c045 City "Ankara", Edited, Original "İstanbul", Revert to original | Item with an edit (`shared.edits`) |
| `S26-edit-replaced` | c045 pushed from S09 Wedding guests: inline choice "Mert changed City after you" / "Your edit “Ankara” was replaced with Mert's “Eskişehir”. Keep your version or use Mert's?" with "Keep mine" / "Use Mert's"; City shows "Eskişehir", "Edited by Mert" | "View" on `S40-outcome-edit-replaced` (D-09 row 1, A-172) |
| `S26-edit-replaced-kept` | "Keep mine": City back to "Ankara" (Edited, Original İstanbul), alert gone, snackbar "Kept your edit" | "Keep mine" |
| `S26-edit-replaced-theirs` | "Use Mert's": City stays "Eskişehir" (Edited by Mert), alert gone, snackbar "Using Mert's edit" | "Use Mert's" |
| `S26-revert-confirm` | Dialog "Revert City to the original?" | Revert to original |
| `S26-reverted` | City back to İstanbul, snackbar with Undo | Confirm revert |
| `S26-note-edit` | Editing my note (solo list) with counter | Edit on my note |
| `S26-note-delete` | Dialog "Delete your note?" | Delete on my note |
| `S26-add-note` | c012: Selin's shared note; my composer with "Only visible to me" on | Add note on a shared list |
| `S26-private-note` | c006: my private note (dashed, lock, "Only you"); Agreed, all three accepted | Item with my private note |
| `S26-shared-conflict` | c002 pushed from Results: my decision Accept, Deniz Accepted, Mert Rejected, Selin Accepted, Conflict; two phones | Conflict item |
| `S26-shared-hidden` | c079 over S25 (shared): others' decisions hidden, Pending; Mert's note and "Edited by Mert" visible | Shared list, Show others' decisions off, not yet decided by me |
| `S26-product` | p03 from Results: decision control (Accept), fields incl. link | Product item from S28 |
| `S26-decision-changed` | Maybe selected, snackbar "Changed to Maybe" + Undo | Tap another decision |
| `S26-loading` | Skeleton for image, title, control and fields | Pushed screen while loading |
| `S26-offline-saved` | Offline banner; snackbar "Saved on this phone. It will sync when you're back online." | Save while offline (shared list) |
| `S26-not-found` | "This item isn't in the list anymore" (S40 error treatment) | Item removed by another member |
| `S26-read-only` | Archived Apartment viewings (a07): notice with Restore list, no Edit, Viewing "—", Final decision | Archived list |
| `S26-large-text` | 200%: labels above values, decide buttons as labeled tiles | Font scale ≥ 150% |
| `S26-ios`, `S26-ios-edit` | Page sheet with Edit / Done; editing with Cancel / Save | iOS |
| `S26-web-desktop` | Sheet in the centered column with keyboard hints | Enter on the card (desktop web) |

## 5. Interactions and transitions

- **Open from S25**: sheet slides up 300 ms (emphasized decelerate), scrim to 50%; the card under it stays in
  place (no tilt). Reduced motion: fade 150 ms. Haptic: none.
- **Snap points**: 85% and 100%. Dragging the handle or the header up past 30% expands; down past 30% of
  height or 800 dp/s closes. Content scrolls inside; at full screen the header turns into the AppBar.
- **Decide from the sheet**: Reject / Maybe / Accept close the sheet (200 ms) and then run the S25 button
  commit on the card (motion.md §2.7) with the usual haptic, counts and undo. On desktop web, ← ↑ → do the
  same while focus is not in a text field.
- **Edit**: "Edit" turns every field into an input in place (150 ms cross-fade); tapping a single field does
  the same and focuses that field. The decide bar is replaced by Cancel / Save changes. Unsaved changes +
  close or back ask "Discard changes to Gökhan Doğan?" (S40 `S40-discard-edits`: "Keep editing" / "Discard changes").
- **Save changes**: validates; on error the first invalid field gets focus and its message (no snackbar);
  on success the form returns to read mode, changed fields get the Edited badge, snackbar "Changes saved".
  Clearing a field that had an original value is an edit (original shown); the card updates immediately.
- **Revert to original**: AlertDialog (S40 `S40-revert-field`, destructive "Revert"); confirm restores the original value, removes the Edited badge, and
  shows "City reverted to İstanbul" with Undo (6 s). Undo restores the edit.
- **Multi-value**: the first value shows on the card ("+1" for more); the label Select offers Mobile, Home,
  Work, Other; removing the last value leaves the field empty ("Add phone").
- **Notes**: "Add note" opens an inline composer (Textarea, counter "37 / 1,000", on shared lists the
  "Only visible to me" Switch, off by default, with the consequence line "Mert and Selin won't see this
  note." when on); Save note → snackbar "Note saved". Edit replaces the card with the composer. Delete asks,
  then "Note deleted" + Undo. One note per member per item.
- **Change decision (from Results)**: tapping another segment changes my decision at once (no dialog),
  snackbar "Changed to Maybe" + Undo; the decision is recorded in the current round; on shared lists the
  list status recomputes and others get the change through sync (no notification unless it creates or
  resolves a conflict).
- **Others' decisions hidden** (SRT-12): while sorting a shared list with "Show others' decisions" off, the
  sheet hides them until I decide that item. Opened from Results or Conflicts they are always shown.
- **Offline**: every action works; edits, notes and decisions are saved locally and marked for sync; the
  snackbar says so once per session; a "Not synced" Badge is not shown per field (the S25/S09
  sync notice covers it).
- **Links** open in the in-app browser; phone numbers and emails are not actionable here (out of the
  sorting task; long-press copies the value with snackbar "Copied").

## 6. Copy

| Element | String |
| --- | --- |
| Sheet header | "Item details"; edit mode "Edit {title}" ("Edit Gökhan Doğan"); iOS "Details", "Edit fields" |
| Buttons (sheet) | "Open full screen", "Close details", "Back to sorting" (collapse), "Back to results" |
| My decision | "My decision"; "Not decided yet"; badges "Accepted", "Rejected", "Maybe"; read-only "Final decision" |
| Decision control | "Reject", "Maybe", "Accept"; lines "Decided in Round 1, Oct 4.", "Changed just now. Round 1 history keeps the original decision.", shared "Changing your decision updates the list status for everyone." |
| Decide bar | "Reject", "Maybe", "Accept" (group label "Decide this item") |
| Who decided what | "Who decided what"; "Deniz (you)", "Mert", "Selin"; role "Decision Maker"; "Not decided"; status badges "Agreed", "Pending", "Conflict", "Resolved by Mert" |
| Conflict line by rule | Decision Maker decides: "Mert resolves conflicts as Decision Maker." + "Review conflicts"; Everyone must agree: "Conflicts stay open until everyone chooses the same decision." + "Review conflicts"; Majority decides: "Waiting for 1 member. The majority decides." |
| Hidden decisions | "Others' decisions stay hidden until you decide, so they don't sway you." / "To see them while sorting, turn on Show others' decisions in the sorting menu." |
| Fields | "Fields"; "Edit"; empty field "Add phone", "Add email" ("Add {field name in lowercase}"); read-only "—" |
| Edited | Badge "Edited" / "Edited by Mert"; "Original: İstanbul"; "Revert to original" |
| Revert dialog | Title "Revert City to the original?"; body "City goes back to “İstanbul”, the value from Contacts. Your edit “Ankara” is removed."; buttons "Cancel", "Revert" (destructive variant: the edit is discarded; same as S40 `S40-revert-field`); snackbar "City reverted to İstanbul" + "Undo" |
| Source lines | "From Contacts on this phone. Edits stay in SwipeSort; your contacts aren't changed."; "From trip-ideas.csv. Edits stay in SwipeSort; the file isn't changed."; "From mert-family.csv. Edits stay in SwipeSort; the file isn't changed."; "From Google Sheets: Flat hunt 2026, tab Beşiktaş."; "Added by hand on Oct 4." |
| Edit mode | Helper "Changes stay in SwipeSort. The source isn't changed."; "Photo"; "Remove"; "From Contacts. Removing it here doesn't change your contacts."; "No photo in Contacts."; image link helper "Paste a link to an image. Cards show the picture from this link."; link that doesn't load "This link doesn't open an image. Check it, or leave the field empty." (A-160); "Add another phone"; "The first number shows on the card."; phone labels "Mobile", "Home", "Work", "Other"; "Remove this number"; "Choose date and time"; "Opens the date and time picker of your phone."; "Open link"; buttons "Cancel", "Save changes" |
| Validation | Email: "Enter a full email address, like name@example.com."; phone: "Enter a phone number with digits only, spaces allowed."; number: "Enter a number, like 429 or 4.5."; link: "Enter a full link, like https://example.com."; date: "Choose a date." |
| Discard dialog (S40 `S40-discard-edits`) | Title "Discard changes to {title}?" ("Discard changes to Gökhan Doğan?"); body "Your edits won't be saved. The item keeps its current values."; buttons "Keep editing", "Discard changes" (destructive) |
| Edit replaced (D-09 row 1) | Alert title "Mert changed City after you"; body "Your edit “Ankara” was replaced with Mert's “Eskişehir”. Keep your version or use Mert's?"; buttons "Keep mine", "Use Mert's"; snackbars "Kept your edit" / "Using Mert's edit"; while editing (A-70): "Mert changed City while you were editing. Keep your version or use Mert's?" |
| Snackbars | "Changes saved"; "Saved on this phone. It will sync when you're back online."; "Note saved"; "Note deleted" + "Undo"; "Changed to Maybe" + "Undo"; "Copied" |
| Notes | "Notes"; "No notes yet."; shared "No notes yet. Notes are visible to all members unless you make them private."; "Add note"; "My note" (solo); "You"; "Only you"; "Edit", "Delete"; composer label "Your note"; counter "37 / 1,000"; "Only visible to me"; "Mert and Selin won't see this note."; "Cancel", "Save note" |
| Delete note dialog | Title "Delete your note?"; body "“Flying in from Berlin. Ask about dates first.” will be deleted from this item."; buttons "Cancel", "Delete note" |
| Offline | Banner "You're offline. Changes are saved on this phone." |
| Not found (S40 `S40-item-gone` treatment) | "This item isn't in the list anymore" / "Mert removed it from Wedding guests. Its decisions and notes were removed with it." / "Back to results" |
| Archived | "Apartment viewings is archived" / "Restore the list to edit fields, change decisions or add notes." / "Restore list" |
| Loading | Screen reader: "Loading item" |
| Keyboard hints (desktop) | "Esc Close", "E Edit", "← ↑ → Decide" (one row) |
| Screen reader, field row | "City: Ankara, edited. Edit" |

## 7. Accessibility

- The sheet is a modal dialog labelled by its header; focus moves to the header on open and returns to the
  card on close. Focus order: header actions, title, My decision, Who decided what, Notes, Fields (Edit,
  rows), source line, decide bar.
- Field rows are links named "{Label}: {value}. Edit", with ", edited" when edited; Revert buttons are named
  "Revert City to the original, İstanbul".
- The decision control is a `radiogroup` "My decision"; each option is a radio with icon + label; selected
  state is announced, not only colored.
- Who decided what is a list labelled "Decisions by member"; each row reads "Mert, Decision Maker,
  Rejected". Status chips have icon + text.
- Private notes: "Your note, only you can see this" is part of the accessible name; the dashed border is
  not the only signal (lock icon + "Only you").
- Inputs have visible labels; errors use `aria-invalid` + `aria-describedby` and an icon; Save moves focus to
  the first invalid field and announces the message.
- Snackbars: `role=status` (alert for failures), at least 10 s with a screen reader running.
- Large text (`S26-large-text`): labels move above values, titles 28–40, decide buttons become 64-high tiles
  with icon above the label; the sheet opens at full screen when the font scale is ≥ 150%.
- Reduced motion: sheet and edit-mode transitions become 150 ms fades.
- Touch targets ≥ 48 (field rows 48+, text buttons 48 high, switch inside a 48 row).

## 8. iOS and web differences

- **iOS** (`S26-ios`, `S26-ios-edit`): page sheet (`presentation: 'formSheet'`) with grabber and medium /
  large detents; navigation bar "Edit" (leading) and "Done" (trailing, bold) instead of the header icons;
  edit mode switches the bar to "Cancel" / "Save" and moves to the large detent; no pinned Cancel / Save
  bar. Pushed detail uses the native stack with a back chevron "Results" and edge-swipe back. Destructive
  confirmations (Delete note, Revert) use the native alert with the same copy. Image fields work as on
  Android: Remove for contact photos, the image link for other image fields; no camera or library (D-32).
- **Web, mobile**: Android layout without system bars; browser back closes the sheet / pops the screen.
- **Web, desktop** (`S26-web-desktop`): Enter on the focused card opens the sheet; Esc closes; E enters edit
  mode; ← ↑ → decide (ignored while typing); Tab order as in §7; keyboard hints under the decide bar (web
  only). Image fields are the same as on mobile (image link or Remove); no file upload (D-32, A-170).
- Haptics are not used on this screen (deciding from the sheet uses the S25 commit haptic on Android/iOS).

## 9. Edge cases

- **Long text**: titles and values wrap fully (no truncation in detail); long emails and links break at any
  character when needed; notes wrap; the card keeps its own clamping (S25).
- **Missing values**: editable "Add {field}" rows; read-only "—"; missing image → initials avatar (person) or
  `image-off` placeholder (product, Photo template). Rows are never hidden in detail (they are on the card).
- **Multi-value**: all values listed with labels; the card shows the first + count.
- **Edited by someone else** (shared): "Edited by Mert"; anyone can revert (domain-model permissions); the
  revert dialog names who made the edit: "Mert's edit “Babaanne (Nermin Aydın)” is removed."
- **Concurrent edits** (shared): last save wins; if the field changed since edit mode opened, Save shows
  "Mert changed City while you were editing. Keep your version or use Mert's?" with "Keep mine" / "Use
  Mert's" (inline Alert above the form).
- **Edit replaced while I wasn't looking at the item** (D-09 row 1, A-172): when a later edit by another member
  overwrites mine at sync, I learn it from the S40 snackbar `S40-outcome-edit-replaced` ("Mert changed City on
  Alper Turan after you, so your edit was replaced." + View) on whatever screen I'm on. View opens this item
  (`S26-edit-replaced`), where the same "Keep mine / Use Mert's" choice waits above the fields until answered:
  "Keep mine" applies my value again as a new edit (it syncs like any edit), "Use Mert's" keeps the current
  value; either closes the alert with the snackbar "Kept your edit" or "Using Mert's edit". Leaving without
  answering keeps Mert's value and shows the choice again the next time the item opens, until answered. Several
  replaced fields on one item: one alert per field, in field order. If the item is open when the outcome
  arrives, the alert appears in place without a snackbar.
- **Computed fields** (for example image dimensions) are read-only and have no "Edit".
- **Image fields** (D-32, A-170): no photo library, camera or file upload. Contact photos can only be removed
  (Revert to original brings them back); image-link fields are edited as their link; a link that doesn't open
  an image shows the S17 inline error and the item can still be saved (the card falls back to its placeholder).
- **Others' private notes** are never shown or counted (e.g. Mert's private note on c021).
- **Very long notes**: 1,000 characters max; the counter turns `destructive` at the limit and the extra text
  is not accepted.
- **Offline**: all edits, notes and decisions are stored locally and sync later; conflicts with other
  members' edits are resolved on sync with the rule above.
- **Item removed while open**: the screen switches to `S26-not-found`; a sheet over S25 closes and S25
  skips the card with its snackbar.
- **Archived list**: read-only (`S26-read-only`), no decide bar or decision control.
- **Decision changed from Results in a finished round**: allowed; the round summary (S30) keeps the
  original counts and results show the latest decision (A-33).
