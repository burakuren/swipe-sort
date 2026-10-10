# S24 Start a round

Frames: `S24-start-round.html` (generator: `tools/generators/S24-start-round.py`). Next screen: `S25-sorting.html`.
Data: `lists` l-wedding, l-desk, l-candidates; `rounds` r-w1, r-d1, r-d2; `contacts` (filter counts);
`members` (shared variants).

## 1. Purpose and requirements

Start the next sorting pass over a list: choose which items go in (all, the Maybe pile, accepted items to
narrow down, or a custom selection by field filters or by hand) and the card order (original, shuffled,
sorted by a field). The screen always states the size of the round before it starts, so nobody starts an
empty or unexpectedly large round.

Covers: RND-01, RND-02, DM-15, DM-20, SRT-16 (re-sort Maybe target), GOAL-02, GOAL-04, PLT-01–PLT-04,
PLT-13–PLT-16, PLT-21, PLT-23, STK-06, STK-07, VIS-09, VIS-12, VIS-14, TERM-01, TERM-02, SCR-24.

## 2. Entry points and exits

| From | How | Preselection |
| --- | --- | --- |
| S09 list overview | "Start new round" | Maybe pile when it has items, else All items; Original order |
| S27 round summary | "Re-sort Maybe (n)" | Maybe pile; Shuffled (`S24-maybe`) |
| S27 round summary | "Start a new round" | Same as from S09 (`S24-default`) |
| S38 activity | request "Selin asked for Round 2" (Owner only) | The options Selin proposed |

| To | How |
| --- | --- |
| S25 sorting | "Start round": the modal is replaced by S25 at the first card of the new round; snackbar "Round 2 started" (`S24-started`). Prototype: `S24-maybe` → `04-prototype/swipe-demo.html?deck=desk-maybe&next=S27-desk-round-2` |
| End-round dialog (S40 pattern) | "Start round" while a round is still open on a shared list (`S24-end-round-dialog`) |
| Hand-pick screen (inside the modal) | "Pick items by hand instead" (`S24-custom-pick`), back returns with the selection |
| S09 | Close (`x`), Android back, iOS Cancel; nothing is saved, no confirmation (the screen holds no user data) |

Route: `round/new?listId=…&preset=maybe|all` (full-screen modal, see navigation-map §1).

## 3. Layout and components

Full-screen modal, no bottom navigation. Top to bottom:

1. **AppBar (modal)**: close IconButton (`x`, "Close"), title "Start a round", list name as caption.
   Collaborators see the title "Suggest a round".
2. Optional **notice** (Alert, full width in the gutter, radius 12): shared Owner (`primary-soft`, AvatarStack
   of all members), round still open (neutral, `flag`, per-member progress), collaborator (neutral, `lock`).
3. **Items** (section header `text-label muted`; on shared lists a trailing caption "Based on final
   decisions"): a ListGroup used as a RadioGroup. Each option row (min 64): Radio (24), title `text-body`,
   description `text-body-sm muted`, trailing count. Counts for piles use a decision-colored count chip with
   the decision icon (Maybe `circle-help` on `maybe-soft`, Accepted `check` on `accept-soft`); All items is a
   plain muted number. Custom selection shows its count once filters exist.
4. **Custom selection panel** (inside the Custom row when selected, indented to the text column):
   "Items that match every filter", filter rows (outline, radius 12: field in `muted`, then "is Bride's",
   trailing remove IconButton 48), "Add filter" (link button, `plus`), the live match count (`layers` icon)
   and "Pick items by hand instead" (`list-checks`).
5. **Card order**: RadioGroup of Original order, Shuffled, Sorted by a field. When Sorted by a field is
   selected, its row expands with a **Select** trigger (label "Field", value, `chevron-down`) and a
   **SegmentedControl** for direction. Direction labels follow the field type: text "A to Z / Z to A"
   (`arrow-down-a-z`, `arrow-up-z-a`), number "Low to high / High to low" (`arrow-down-0-1`,
   `arrow-up-1-0`), date "Oldest first / Newest first".
6. **Summary bar** (pinned, `border-t`): `layers` + "Round 2 will have 11 items" (`text-body tabular-nums`,
   `role=status`, updates live), a detail line ("Maybe pile, in original order"), then the full-width
   primary Button "Start round". Optional reason line under the button.

Sheets and pickers:
- **Sort by** (BottomSheet, `S24-sort-field-sheet`): title, radio rows with the field type icon (`type`,
  `phone`, `mail`, `hash`, `calendar`, `link`), field name and type, check on the selected one, footer
  explaining the default direction. Image fields are not listed (cannot be sorted).
- **Add filter** (BottomSheet, `S24-add-filter`): Select "Field", SegmentedControl "Condition" (is / is not),
  "Values" as FilterChips (36 high in a 48 row) each with its count for the whole list, the live count
  "With this filter, 12 items match", primary "Add filter". Number and date fields replace the chips with
  two inputs ("From", "To"); text fields with more than 12 distinct values add a search field above the
  chips. Pseudo-fields at the top of the field list: **My decision** (Accepted, Rejected, Maybe, Not
  decided) and, on shared lists, **List status** (Agreed, Pending, Conflict).
- **Pick items** (pushed inside the modal, `S24-custom-pick`): back arrow ("Back to round options"), title
  and live "12 selected" caption, SearchField, SelectableRows (checkbox, avatar or thumbnail 40, title,
  subtitle field values, trailing DecisionBadge with my last decision), pinned primary "Use 12 items".

Components: AppBar, Alert, AvatarStack, ListGroup, RadioGroup, Select, SegmentedControl, FilterChip,
BottomSheet, SearchField, SelectableRow, DecisionBadge, Button, Snackbar, AlertDialog, Skeleton.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S24-default` | Wedding guests after Round 1: All items 100, Maybe pile 11 (selected), Accepted items 48, Custom; Original order; "Round 2 will have 11 items" | S09 "Start new round", S27 "Start a new round" |
| `S24-maybe` | Desk setup after r-d1: Maybe pile 6 preselected, Shuffled; Start round → swipe demo, then `S27-desk-round-2` | S09 / S27 "Re-sort Maybe" |
| `S24-sorted-by` | Accepted items 48, Sorted by a field: City, A to Z (content scrolled) | Choosing Sorted by a field |
| `S24-sort-field-sheet` | Sort by sheet with field types | Tapping the Field Select |
| `S24-custom` | Custom selection: Side is Bride's, Relationship is Family → 12 items match | Choosing Custom selection |
| `S24-add-filter` | Add filter sheet: Relationship, is, Family (25) selected → 12 match | "Add filter" or tapping a filter row |
| `S24-custom-none` | City is Tokyo + Relationship is Family → 0; reason under the filters; Start round disabled | Filters exclude every item |
| `S24-custom-pick` | Hand-pick list, 12 selected, my Round 1 decision per row | "Pick items by hand instead" |
| `S24-empty-option` | Frontend hiring, Q4 after Round 1 (4 accepted, 8 rejected, 0 maybe): Maybe pile disabled with "Nothing in Maybe. Items you swipe up wait here." | A pile with 0 items |
| `S24-loading` | Count skeletons, "Counting items…", Start round disabled | Counting (large lists, first open) |
| `S24-shared-owner` | Notice "Starts Round 2 for Deniz, Mert and Selin"; piles from final decisions | Owner of a shared list |
| `S24-round-in-progress` | Notice "Round 1 is still open" with each member's progress | Owner, shared list, current round not complete for everyone |
| `S24-end-round-dialog` | "End Round 1 for everyone?" | Start round from the previous state |
| `S24-collaborator` | "Suggest a round": "Only Deniz can start rounds", options usable, primary "Ask Deniz" | Collaborator or Decision Maker (not Owner) opens Start new round |
| `S24-collaborator-asked` | Snackbar "Asked Deniz to start Round 2" | "Ask Deniz" |
| `S24-offline` | Offline banner, Start round disabled, "Try again when you're online." | Shared list without a connection |
| `S24-start-failed` | Error snackbar with Try again | Server refused or timed out (shared) |
| `S24-started` | S25 at 0 / 11, Round 2, first Maybe item (Ayşe Demir c001), snackbar "Round 2 started" | Start round succeeded |
| `S24-large-text` | 200% text: counts under titles, pinned summary and button | System font scale ≥ 150% |
| `S24-ios`, `S24-ios-sort-menu` | Page sheet, Cancel, checkmarks; Field as a pull-down menu | iOS |
| `S24-web-desktop` | Desktop column, Select as a popover, keyboard hints | Desktop browser |

Solo lists never show the shared notice, the "Based on final decisions" caption or the member count in
the summary detail. Error state for counting is not needed: counts come from the local working copy.

## 5. Interactions and transitions

- Opens as a full-screen modal (M3: slide up 300 ms emphasized decelerate; iOS: page sheet). Reduced motion:
  fade 150 ms.
- Selecting an option updates the summary immediately (count tick 250 ms; reduced motion: instant).
  Exactly one items option and one order option are selected at all times.
- Disabled options (0 items) cannot be selected; their description is replaced by the reason, which stays at
  full contrast. If the preset option is empty, the first non-empty option is selected instead.
- Custom selection: filters combine with AND ("Items that match every filter"); values inside one filter
  combine with OR (Family or Friend). Tapping a filter row reopens Add filter for that filter; `x` removes it
  (no confirmation). Picking by hand replaces the filters (the panel then reads "12 items picked by hand"
  with "Change"); adding a filter afterwards asks nothing and clears the hand-picked set with a snackbar
  "Hand-picked items cleared" + Undo.
- Shuffled: the order is generated when the round starts and stored with the round (resume keeps it).
- Sorted by a field: items with no value for the field go last in either direction.
- Start round: the button shows a 16 spinner + "Starting…" only on shared lists (network). On success the
  modal is replaced by S25 (no back to S24), success haptic is not used (it is reserved for round complete).
  Snackbar "Round 2 started" on S25.
- Shared lists, Owner: if any member has not finished the current round, Start round first opens the
  end-round dialog; confirming ends the round for everyone and starts the new one. Every member gets the
  "Deniz started Round 2 (11 items)" notification (S38); a member who is sorting sees S25's "Deniz ended
  Round 1" sheet.
- Collaborator / Decision Maker: "Ask Deniz" sends an in-app request (activity event `roundRequested` to
  the Owner, push if enabled) with the chosen options; the Owner's notification opens S24 with those options
  preselected. Snackbar "Asked Deniz to start Round 2". The request expires when any new round starts.
- Close / back: closes without confirmation.

## 6. Copy

| Element | String |
| --- | --- |
| Title | "Start a round"; collaborator: "Suggest a round" |
| Close label | "Close" |
| Section headers | "Items", "Card order"; shared caption "Based on final decisions" |
| Items options | "All items" / "Every item in the list, decided or not"; "Maybe pile" / "Items marked Maybe in Round 1" (shared: "Final decision is Maybe"); "Accepted items" / "Narrow down what you accepted" (shared: "Final decision is Accept"); "Custom selection" / "Filter by a field or pick items by hand" |
| Empty pile reasons | Maybe: "Nothing in Maybe. Items you swipe up wait here."; Accepted: "Nothing accepted yet."; All items never empty |
| Order options | "Original order" / "As the items were imported"; "Shuffled" / "A new random order for this round"; "Sorted by a field" / "Choose a field and a direction" |
| Sorted controls | "Field"; "A to Z", "Z to A"; "Low to high", "High to low"; "Oldest first", "Newest first" |
| Sort by sheet | "Sort by"; field types "Text", "Number", "Phone", "Email", "Date", "Link"; "Text sorts A to Z, numbers from low to high and dates from oldest. Change the direction after choosing." |
| Custom panel | "Items that match every filter"; filter row "{Field} is {value}" / "{Field} is not {value}", several values "{Field} is Family or Friend"; "Add filter"; "12 items match" (1: "1 item matches"); "Pick items by hand instead"; after picking: "12 items picked by hand", "Change" |
| No match | "No items match these filters. Remove a filter or choose other values." |
| Add filter sheet | "Add filter" (editing: "Edit filter"); "Field"; "Condition"; "is", "is not"; "Values"; "Choose one or more. Counts are for the whole list."; number/date: "From", "To"; "Search values"; "With this filter, 12 items match"; button "Add filter" (editing: "Save filter") |
| Pseudo-fields | "My decision" (values "Accepted", "Rejected", "Maybe", "Not decided"); "List status" ("Agreed", "Pending", "Conflict") |
| Pick items | "Pick items"; "12 selected"; "Search 100 items"; "Your Round 1 decision is shown on the right"; "Use 12 items"; back label "Back to round options" |
| Summary | "Round 2 will have 11 items" (1: "1 item"); collaborator "Round 2 would have 11 items"; details "Maybe pile, in original order", "Maybe pile, shuffled", "Accepted items, sorted by City from A to Z", "Custom selection, in original order", shared suffix ", for 3 members"; zero: "Change the filters to include at least 1 item" |
| Loading | "Counting items…" |
| Button | "Start round"; progress "Starting…"; collaborator "Ask Deniz" |
| Shared Owner notice | "Starts Round 2 for Deniz, Mert and Selin" / "Everyone sorts the same items from the start. Round 1 stays in round history." |
| Round open notice | "Round 1 is still open" / "Starting Round 2 ends Round 1 for everyone. Decisions made so far are kept."; rows "You", "Mert", "Selin" with "76 / 100 decided" |
| End-round dialog | Title "End Round 1 for everyone?"; body "Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided." + "Round 2 then starts for all 3 members with 11 items."; buttons "Cancel", "End Round 1 and start" |
| Collaborator notice | "Only Deniz can start rounds" / "Rounds apply to every member, so the Owner starts them. Choose the items and order you'd like, then ask Deniz." |
| Snackbars | "Round 2 started"; "Asked Deniz to start Round 2"; "Hand-picked items cleared" + "Undo"; error "Couldn't start Round 2. Check your connection and try again." + "Try again" |
| Offline | Banner "You're offline. Starting a round for everyone needs a connection."; under the button "Try again when you're online." |
| Keyboard hints (web desktop) | "Esc Close", "Enter Start round" |
| Activity (S38, for the lead) | Owner receives "Selin suggested Round 2: Maybe pile, 11 items" with action "Review" |

## 7. Accessibility

- Focus order: Close, notice (if any), Items options top to bottom, Custom panel controls, Card order
  options, Field Select, direction, summary (live region), Start round.
- Each options group is a `radiogroup` with a label ("Items in Round 2", "Card order"); each option is a
  `radio` whose name includes the count and description: "Maybe pile, 11 items. Items marked Maybe in
  Round 1". Disabled options are announced as dimmed with their reason.
- The summary line is `role=status` (polite): changes are announced once, after 500 ms of no change.
- Count chips carry the decision icon and the number; the decision meaning is in the option title (never
  color alone).
- Filter rows: the row is a button "Edit filter: Side is Bride's"; remove button "Remove filter: Side is
  Bride's". After removal focus moves to the next filter or to "Add filter".
- FilterChips are toggle buttons (`aria-pressed`), 36 high inside a 48 row (hit slop 6 above and below).
  Segments are 40 high inside the 48 track; the whole track height is the target.
- Hand-pick rows are `checkbox` roles; "12 selected" is announced on change.
- Large text (`S24-large-text`): titles 28, descriptions 22; counts move under the title; options keep one
  per row; the summary and Start round stay pinned; content scrolls.
- Reduced motion: no slide, fades only; count changes are instant.
- Touch targets ≥ 48 (rows 64, icon buttons 48, button 48).

## 8. iOS and web differences

- **iOS** (`S24-ios`, `S24-ios-sort-menu`): presented as a page sheet with grabber (swipe down to cancel
  is allowed: nothing is lost); "Cancel" in the navigation bar instead of `x`; title centered with the list
  name below; selection uses trailing checkmarks (HIG) instead of radio buttons; the sort field is a
  pop-up button that opens a pull-down menu (UIMenu) and direction is a button that toggles; Start round
  stays at the bottom. Sheets (Add filter, Pick items) are page sheets at the large detent.
- **Android**: Select opens a bottom sheet (`S24-sort-field-sheet`); system back closes an open sheet first,
  then the modal.
- **Web, mobile**: Android layout without system bars; Select opens a bottom sheet.
- **Web, desktop** (`S24-web-desktop`): centered phone column; Select opens a popover listbox anchored to
  the trigger (flips above when there is no room below); keyboard: Esc closes (first the popover), Enter
  starts the round when focus is not in a text field; arrow keys move within radio groups.
- No web-unavailable features on this screen.

## 9. Edge cases

- **Shared lists**: piles count final decisions (Agreed, or resolved by the conflict rule). Items still
  Pending or in Conflict are in no pile; use Custom selection with List status = Conflict or Pending to
  include them. On "Everyone must agree" lists the Maybe pile therefore only holds agreed Maybe items.
- **Round still open on a solo list**: the notice reads "Round 1 is still open. 76 of 100 decided. Starting
  Round 2 ends Round 1." and the dialog (S40 `S40-end-round`) has no member names.
- **Round numbering**: always the next integer ("Round 3"), even if an earlier round was ended early.
- **Very large lists** (5,000+): counts use thousands separators ("1,204 items"); counting runs in the
  background with the loading state; hand-pick list is virtualized and search filters as you type.
- **Long field names and values** (+40%): filter rows wrap to two lines; chips wrap onto more lines; the
  Select shows the value on one line with ellipsis and the full value in the sheet.
- **Items added mid-round** (S21) appear in All items and in Custom counts; they are not in any pile until
  decided.
- **Owner changes while the screen is open** (shared): if ownership is transferred away, Start round turns
  into "Ask {new Owner}" and a snackbar says "Mert is now the Owner".
- **Offline, solo list**: everything works (local); only shared lists need a connection to start a round.
- **All piles empty after Round 1** (every item rejected): Maybe and Accepted are disabled with reasons; All
  items stays selected.
