# S10 List management

Frames: `S10-list-management.html`. Generator: `tools/generators/S08-S10-lists.py`.
Components: DropdownMenu, BottomSheet (actions), iOS action sheet and alert, Dialog (rename, duplicate),
AlertDialog (archive shared, delete, leave, owner leave, delete forever), Input with counter, RadioGroup,
Snackbar, ListGroup + archived rows, EmptyState, Skeleton, OfflineBanner. Backgrounds are inert copies of
S09 and S08.

## 1. Purpose and requirements

Manage a list as an object: rename, duplicate, archive, delete, leave; and the Archived lists screen to
open, restore or delete archived lists. Every destructive step names the list, states what goes and what
stays safe, and uses the same action word from button to message. Permissions follow the role
(domain-model › Permissions): the Owner manages the list; members can duplicate and leave.

Covers: SCR-10, COL-11 (transfer ownership before leaving), COL-12 (leave a list), ACC-02 (lists on this
phone), GOAL-03, GOAL-04, SAFE-01 (sources never changed), VIS-11, VIS-12, VIS-13, VIS-14, TERM-01,
DM-17 (the parallel rule for leaving: decisions are kept), PLT-02, PLT-03, PLT-04, PLT-13, PLT-14, PLT-15,
PLT-16, PLT-21, PLT-23, STK-06, STK-07.

## 2. Entry points and exits

| From | How | Frame |
| --- | --- | --- |
| S09 overflow (solo, Owner) | "List options" | `S10-default` |
| S09 overflow (shared, Owner) | "List options" | `S10-shared-owner-menu` |
| S09 overflow (Collaborator, Decision Maker) | "List options" | `S10-collaborator-menu` |
| S09 iOS "…" | action sheet | `S10-ios-action-sheet` |
| S08 row long press | actions sheet | `S10-row-sheet` |
| S08 "Archived lists" row | push | `S10-archived` |
| S09 "Leave list" row (members) | dialog | `S10-leave` |
| S09 archived "Restore list" | restore | `S10-restored` |

| Action | Leads to |
| --- | --- |
| Rename → Save | S09 with "List renamed" (`S10-renamed`) |
| Duplicate → Duplicate | the new list's S09 with "Duplicated as “…”" (`S10-duplicated`) |
| Archive (solo) | S08 with "List archived" + Undo (`S10-archived-snackbar`) |
| Archive (shared) → Archive | confirm (`S10-archive-shared`) → S08 with the same snackbar |
| Delete list → Delete list / Delete for everyone | S08 with "List deleted" + Undo (`S10-deleted-snackbar`) |
| Leave list → Leave list | S08 with "You left “Wedding guests”" (`S10-left-snackbar`) |
| Leave list (Owner) → Choose new Owner | S34 `S34-default` (transfer ownership, then leave there) |
| Share list (row sheet, not signed in) | S05 `S05-share` |
| Resume sorting (row sheet) | S25 |
| Archived row | S09 `S09-archived` (read-only) |
| Archived row › Restore | `S10-restored` ("View" → S08) |
| Archived row › Delete forever | `S10-delete-forever` → `S10-archived-empty` when it was the last one |

`data-action` values: `rename`, `duplicate`, `archive`, `delete`, `leave` (menu items); `save`,
`confirm-duplicate`, `confirm-archive`, `confirm-delete`, `confirm-leave`, `choose-owner`, `undo`, `view`,
`restore`, `delete-forever`, `options-apartments`, `options-books`, `share`, `back`.

## 3. Layout and components

- **DropdownMenu** (Android, web): anchored over the overflow button (top-right, 8 from the edge), width 256,
  `bg-popover rounded-control shadow-overlay`, 48-high items with a 20 icon. Non-destructive items first,
  a separator, then destructive items in `text-destructive` (Leave list, Delete list). Disabled items
  (offline) keep their title in `muted-foreground` with the reason as a second line ("Needs a
  connection"), never dimmed with opacity.

  | Role | Items |
  | --- | --- |
  | Owner, solo list (signed in or not) | Rename, Duplicate, Archive, — , Delete list |
  | Owner, shared list | Rename, Duplicate, Archive, — , Leave list, Delete list |
  | Collaborator / Decision Maker | Duplicate, — , Leave list |
  | Archived list (Owner) | Open, Restore, Duplicate, Delete forever (sheet in Archived lists; the same in S09-archived's menu) |

- **Row actions sheet** (S08 long press, Android BottomSheet): handle, list name `text-title-3` + progress
  line, then 56-high rows: Resume sorting (when a round is in progress), Share list, Rename, Duplicate,
  Archive, Delete list (destructive). Members see Resume sorting, Duplicate, Leave list.
- **iOS action sheet**: title = list name; Rename, Duplicate, Archive, Delete list (destructive red); Cancel
  in its own block.
- **Rename Dialog**: title "Rename list"; Input (label "List name", value selected on open, focus ring)
  with a counter "21 / 80" right-aligned under it; error line with `circle-alert` on the left; actions
  Cancel (ghost) + Save (primary). Save is `disabled` while the name is empty after trimming or longer than
  80; the counter turns `text-destructive` past 80.
- **Duplicate Dialog**: title "Duplicate “{name}”"; Input "Name of the copy" (default "{name} (copy)",
  then "(copy 2)" if taken); shared lists add a muted note (`user` icon) "The copy is a new solo list that
  only you can see. Mert and Selin aren't added."; RadioGroup "What to copy" with two options and
  descriptions; Cancel + Duplicate (primary).
- **AlertDialogs** (title names the object, body states consequence and what stays safe, specific verb):
  archive shared (primary "Archive"), delete solo ("Delete list", destructive), delete shared (a 48
  `triangle-alert` circle on `secondary` above the title, "Delete for everyone", plus the alternative
  "make someone else the Owner and leave" as a link to S34), leave (destructive "Leave list"), owner leave
  (primary "Choose new Owner"), delete forever (destructive "Delete forever").
- **Snackbar** (inverse, 12 above the bottom navigation; the ExtendedFab moves up above it).
- **Archived lists screen**: small AppBar "Archived lists" with back; one explanatory line; ListGroup of
  archived rows: name `text-title-3`, "Archived Jul 21, 8 items", the round's decision counts (Reject,
  Maybe, Accept with words), and a trailing options IconButton ("Options for Apartment viewings") opening the
  archived actions sheet. Rows open the list read-only.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S10-default` | Overflow on a solo list (March photos clean-up, `l-photos`), Owner |
| `S10-shared-owner-menu` | Overflow on Wedding guests (`l-wedding`) as Owner (Deniz) |
| `S10-collaborator-menu` | Overflow as Collaborator (Selin) or Decision Maker (Mert) |
| `S10-row-sheet` | Long press on a Home row (not signed in; `S08-guest`) |
| `S10-ios-action-sheet` | iOS "…" on S09 |
| `S10-rename` | Rename tapped: name selected |
| `S10-rename-empty` | Name cleared: error, Save disabled |
| `S10-rename-too-long` | 86 characters: error, counter red, Save disabled |
| `S10-renamed` | Saved: S09 with the new name ("March 2026 photos") and snackbar |
| `S10-ios-rename` | iOS alert with a text field |
| `S10-duplicate` | Duplicate a solo list: name + Items only (default) / Items with decisions and notes |
| `S10-duplicate-shared` | Duplicate a shared list: becomes a solo list; "Items with my decisions and notes" |
| `S10-duplicated` | The copy opens (never sorted, Items only) with snackbar |
| `S10-archived-snackbar` | Solo list archived: Home without it, Archived lists 3, snackbar with Undo |
| `S10-archive-shared` | Owner archives a shared list: confirmation for everyone |
| `S10-delete` | Owner deletes a solo list |
| `S10-delete-shared` | Owner deletes a shared list: stronger copy, "Delete for everyone" |
| `S10-deleted-snackbar` | After delete: Home with "List deleted" + Undo (6 s) |
| `S10-leave` | Collaborator leaves |
| `S10-leave-decision-maker` | Decision Maker leaves: role becomes empty, open conflicts stay open |
| `S10-leave-owner-blocked` | Owner taps Leave list: must choose a new Owner first |
| `S10-left-snackbar` | After leaving: Selin has no other lists; signed-in empty Home with the snackbar |
| `S10-archived` | Archived lists (Apartment viewings `l-apartments`, Book club picks `l-books`) |
| `S10-archived-menu` | Options on an archived row |
| `S10-restored` | Restored: row removed, "List restored" + View |
| `S10-delete-forever` | Delete an archived list forever |
| `S10-archived-empty` | No archived lists |
| `S10-archived-loading` | Archived lists loading (signed in, not on the device yet) |
| `S10-offline` | Offline menu on a shared list: Archive, Leave, Delete disabled with the reason |
| `S10-delete-large-text` | 200% font: stacked full-width buttons |
| `S10-ios-archived` | iOS Archived lists: swipe actions Restore / Delete on a row |
| `S10-web-desktop` | Desktop browser: delete dialog inside the phone column |

## 5. Interactions, gestures and transitions

- **Menu**: opens with a 150 ms fade + scale 0.9 → 1 from the anchor (M3); closes on item tap, outside tap,
  back or Escape. Reduced motion: fade only.
- **Dialogs**: scrim fades to 50%, dialog fades + scales 0.95 → 1 (200 ms emphasized decelerate). Back,
  Escape and scrim tap cancel, except while saving. The first focus goes to the input (rename, duplicate)
  or to Cancel (destructive dialogs), so Enter never destroys by accident.
- **Rename**: validation runs as you type; the error appears after the first change (not on open).
  Leading/trailing spaces are trimmed; line breaks are removed. Save closes the dialog, updates the name
  everywhere and shows "List renamed". On shared lists other members see the new name live and in
  Activity ("Deniz renamed the list to …").
- **Duplicate**: creates the copy locally (instant for typical sizes; for 1,000+ items the button shows
  "Duplicating…" with a spinner), then pushes the new list's S09 and shows "Duplicated as “…”". The copy is
  always a solo list owned by me, stored like the original (account or this phone). Items only: same items,
  fields, sources, card template and field edits; no decisions, notes or rounds. Items with decisions and
  notes: also my latest decision per item (as the copy's Round 1, complete or in progress) and my notes
  (including private ones, which become ordinary notes on a solo list). Round history is not copied.
- **Archive**: solo → immediate; the list leaves Home with a 200 ms collapse and the snackbar "List
  archived" + Undo (6 s; 10 s with a screen reader). Shared → confirmation first; it is archived for every
  member (read-only, still visible in their Archived lists; Activity: "Deniz archived Wedding guests").
  Archiving never deletes anything; sorting, adding items and editing stop until restored.
- **Delete**: Owner only. After confirming, Home shows "List deleted" + Undo. The deletion is held for the
  snackbar's duration and committed when it closes (or when the app goes to the background), so Undo
  restores everything exactly. Shared: members lose access when it is committed; their open S09 shows
  `S09-unavailable`, and Activity gets "Deniz deleted Wedding guests". Source files, contacts, photos and
  Google Sheets are never touched (SAFE-01).
- **Leave**: the member's decisions stay and keep counting toward Agreed, Pending and Conflict (the same
  default as "Keep their decisions" in S34), so other members' results don't change unexpectedly. Items they
  haven't decided stop waiting for them (Pending items may become Agreed or Conflict). Their shared notes
  stay; private notes are deleted. A Decision Maker who leaves leaves the role empty (as when removed in
  S34); open conflicts stay open until the Owner picks someone. The list disappears from their Home with
  "You left “Wedding guests”" (no Undo: rejoining needs a new invite). Other members get "Selin left" in
  Activity.
- **Owner leave**: blocked with "Choose a new Owner first"; "Choose new Owner" opens S34 where the Owner
  transfers ownership and can leave in the same step.
- **Archived lists**: tap opens S09-archived; options open the sheet; Restore removes the row (200 ms) and
  shows "List restored" + "View" (opens Lists). Delete forever confirms, then shows "List deleted" + Undo
  like any delete.
- **iOS**: action sheet slides up (system); rename is a system alert with a text field; Archived lists rows
  support swipe left → Restore (primary) and Delete (destructive, then the confirmation).

## 6. Copy

| Element | String |
| --- | --- |
| Menu | "Rename", "Duplicate", "Archive", "Leave list", "Delete list"; archived: "Open", "Restore", "Duplicate", "Delete forever"; disabled reason "Needs a connection" |
| Row sheet | "{list name}"; "76 / 100 decided, Round 1"; "Resume sorting", "Share list", "Rename", "Duplicate", "Archive", "Delete list" |
| iOS action sheet | title "{list name}"; "Rename", "Duplicate", "Archive", "Delete list", "Cancel" |
| Rename | "Rename list"; label "List name"; counter "21 / 80"; "Cancel", "Save"; errors "Enter a name for the list." / "Use 80 characters or fewer."; success "List renamed"; iOS subtitle "1 to 80 characters" |
| Duplicate | "Duplicate “March photos clean-up”"; label "Name of the copy"; default "March photos clean-up (copy)"; group "What to copy"; "Items only" / "A fresh start: no decisions, notes or rounds. Edits to fields are kept."; "Items with decisions and notes" / "Keeps your decisions from the latest round, your notes and your edits."; "Cancel", "Duplicate"; progress "Duplicating…"; success "Duplicated as “March photos clean-up (copy)”" |
| Duplicate shared | "Duplicate “Wedding guests”"; "The copy is a new solo list that only you can see. Mert and Selin aren't added."; "Items only" / "A fresh start: no decisions, notes or rounds."; "Items with my decisions and notes" / "Your 76 decisions from Round 1 and your notes. Other members' decisions and notes aren't copied." |
| Archive | success "List archived" + "Undo"; undone "List restored" |
| Archive shared | "Archive “Wedding guests” for everyone?" / "Mert and Selin can still open it, but nobody can sort, add items or change decisions until you restore it. Nothing is deleted." / "Cancel", "Archive" |
| Delete solo (signed in) | "Delete “March photos clean-up”?" / "30 items, Round 1 and your decisions will be deleted from your account and this phone. Your photos stay in your gallery; nothing on your phone is deleted." / "Cancel", "Delete list" |
| Delete solo, other sources | contacts: "Your contacts aren't changed."; files: "The file you imported from isn't changed."; Google Sheets: "Your Google Sheet isn't changed."; not signed in: "…will be deleted from this phone." |
| Delete web | "…deleted from your account and every device. The photos you uploaded stay on your computer." |
| Delete shared | "Delete “Wedding guests” for everyone?" / "Mert and Selin lose access. All 100 items, every member's decisions and notes, and Round 1 are deleted for all 3 members. Your contacts and mert-family.csv aren't changed." / "To stop taking part without deleting it for others, make someone else the Owner and leave." / "Cancel", "Delete for everyone" |
| Deleted | "List deleted" + "Undo" |
| Leave (Collaborator) | "Leave “Wedding guests”?" / "You won't see this list anymore. Your 43 decisions stay and still count toward the list status. Items you haven't decided stop waiting for you, and your private notes are deleted. To come back, ask Deniz for a new invite." / "Cancel", "Leave list" |
| Leave (Decision Maker) | "Leave “Wedding guests”?" / "You won't see this list anymore. Your 85 decisions stay and still count toward the list status. You're the Decision Maker, so nobody will have this role until Deniz chooses someone. The 15 open conflicts stay open." |
| Owner leave | "Choose a new Owner first" / "“Wedding guests” needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead." / "Cancel", "Choose new Owner" |
| Left | "You left “Wedding guests”"; empty Home "No lists yet" / "Import a list to start sorting, or join one when someone shares it with you." / "Import a list" |
| Archived lists | title "Archived lists"; "Archived lists are read-only and hidden from Lists. Restore a list to sort or change it."; rows "Archived Jul 21, 8 items", counts "4 rejected", "1 maybe", "3 accepted"; "Options for {name}" |
| Restored | "List restored" + "View" |
| Delete forever | "Delete “Book club picks” forever?" / "12 items, Round 1 and your decisions will be deleted from your account. Nothing outside SwipeSort is changed." / "Cancel", "Delete forever" |
| Archived empty | "No archived lists" / "Archive a list to put it away without deleting it. It waits here, read-only, until you restore it." / "Back to lists" |
| Offline | banner "You're offline. Decisions are saved on this phone. Inviting needs a connection."; disabled items "Needs a connection" |
| Activity events (others see) | "Deniz renamed the list to “…”"; "Deniz archived Wedding guests"; "Deniz restored Wedding guests"; "Deniz deleted Wedding guests"; "Selin left" |
| Loading | screen reader "Loading archived lists" |

## 7. Accessibility

- Menus: `role="menu"`, items `menuitem`; focus moves to the first item; arrow keys move (web); Escape
  closes and returns focus to the overflow button. Disabled items are announced with their reason
  ("Delete list, dimmed, needs a connection").
- Dialogs: `alertdialog` for confirmations (labelled by the title, described by the body), focus trapped;
  initial focus on Cancel for destructive dialogs, on the input for rename/duplicate. The input's errors
  are linked with `aria-describedby` and `aria-invalid`; the counter is part of the description.
- Radio group labelled "What to copy"; each option's description is part of its name.
- Snackbars: `role="status"`, announced politely; Undo is reachable by keyboard and stays 10 s with a
  screen reader. After an action that removes the focused element (archive, delete, leave), focus moves to
  the snackbar's Undo, then to the next row.
- Archived rows: the row link and the options button are separate targets (48); options are labelled with
  the list name. iOS swipe actions are also exposed as accessibility custom actions ("Restore", "Delete").
- Large text (`S10-delete-large-text`): titles `text-title-2`, body `text-body-lg`, buttons stack full width
  (destructive first, Cancel below) and grow to fit the label.
- Color is never the only signal: destructive items have their verb, and the delete-for-everyone dialog has
  a warning icon plus explicit text.
- Reduced motion: menu and dialog appear with a 150 ms fade, row collapse is instant.

## 8. iOS and web differences

- **iOS**: the overflow is an action sheet (`S10-ios-action-sheet`) or UIMenu; destructive confirmations
  use the system alert with the same title, body and button words; Rename uses an alert with a text field
  (`S10-ios-rename`); Duplicate opens as a page sheet with Cancel / Duplicate in the navigation bar (same
  content as Android); Archived lists rows have swipe actions (`S10-ios-archived`); Home rows support swipe
  to Archive and a context menu on long press.
- **Web**: same as Android (menus as popovers, dialogs centered in the phone column on desktop,
  `S10-web-desktop`). Keyboard: Enter confirms only when focus is on the confirm button; Escape cancels.
  Without an account, "this phone" becomes "this browser".

## 9. Edge cases

- **Offline**: Rename, Duplicate, Archive, Restore and Delete of solo lists work and sync later. Anything that
  changes a shared list for other members (Archive, Delete, Leave) needs a connection and is disabled with
  "Needs a connection" (`S10-offline`). Renaming a shared list offline applies when back online; if
  another rename happened meanwhile, the latest wins.
- **Not signed in**: everything works locally; copy says "this phone" and nothing mentions an account.
- **Duplicate name**: allowed (lists have IDs); the default copy name increments "(copy 2)".
- **Very long names**: dialog titles wrap (no truncation); the copy's default name is cut to 80 characters
  before " (copy)" is added.
- **Delete while another member is sorting**: their sorting screen shows "This list was deleted" with Back
  to lists; decisions made in the last seconds are discarded with the list.
- **Undo after delete when the app is killed**: the deletion is committed; nothing half-deleted remains.
- **Leave as the last member besides the Owner**: the list stays shared (Owner only) until the Owner
  removes pending invites; the Owner sees "Selin left".
- **Owner is the only member**: Leave list is hidden (nothing to transfer), only Delete list.
- **Archived shared list**: members can open it read-only and leave it; only the Owner can restore it.
- **Restore while offline (signed in)**: allowed; the list is editable at once and syncs later.
- **Sample list**: Archive is hidden for the sample (Delete is enough); Rename and Duplicate are available.
