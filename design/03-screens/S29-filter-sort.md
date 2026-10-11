# S29 Filter and sort sheet

Frames: `S29-filter-sort.html` (generator: `tools/generators/S28-S30-results.py`). Opened over
`S28-results.html`. Data: `fields.contacts`, `fields.products`; `contacts` + `shared.items` +
`shared.myDecisions` (Wedding guests, My decisions, Accept: 48 items); `products` + `productDecisions`
(Desk setup, Accept: 8 items); `shared.notes`, `shared.edits`; `members`.

## 1. Purpose and requirements

Narrow down and order the items of one Results segment by any field, without leaving Results. The sheet
always shows what a choice will leave ("Show 12 items") so nobody applies a filter that empties the list by
surprise. Uses the same filter vocabulary as S24 (Custom selection): filters combine with AND across
fields and OR within a field; "My decision" and "List status" are pseudo-fields (A-67).

Covers: RES-03, RES-04 (and RES-02 within the value picker), DM-03–DM-05, DM-18, COL-16 (filter by a
member's decision), SAFE-03 (Edited filter), GOAL-02, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-06,
STK-07, VIS-11, VIS-12, TERM-01, SCR-29.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S28 Results | "Filter" chip (opens at the top), Sort chip (opens the Sort by page, `S29-sort`), `F` on desktop web |
| S28 applied chips | Tapping an AppliedFilterChip removes it (it does not open the sheet) |

| To | How |
| --- | --- |
| S28 filtered | "Show 12 items" applies sort + filters and closes (`S28-filtered`, `S29-applied`, `S28-sorted`) |
| S28 unchanged | Close `x`, swipe down, scrim tap, Android back, Esc, iOS "Cancel": discards changes made in this visit (no confirmation; nothing is lost) |
| Value picker / Sort by pages | Inside the sheet (pushed pages with a back arrow "Back to filters"); back returns to the main page with choices kept |

## 3. Layout and components

BottomSheet (`bg-popover rounded-t-sheet shadow-sheet`, scrim 50%), opens at 92% of the screen height
(top 48 dp), drag handle; content scrolls; the footer is pinned.

1. **Header**: "Filter and sort" (`text-title-3`), scope caption ("My decisions in Accept, 48 items";
   solo "Accept, 8 items"), close IconButton. When content is scrolled the header gets a hairline divider.
2. **Sort by**: a Select trigger (56 high, label "Sort by" + value + `chevron-down`) that opens the **Sort
   by page** (`S29-sort`): a radiogroup of rows (icon by type, field name, type caption, check on the
   selected one). The selected row expands a SegmentedControl for direction. Rows: Recently decided
   (Decision time), Original order (As imported), then every visible field of the list in the template's
   order (title field first). Image fields are not listed. Direction labels follow the type: text "A to Z /
   Z to A", number "Low to high / High to low", date "Oldest first / Newest first", decision time "Newest
   first / Oldest first". Original order has no direction.
3. **Filters** heading + "Items must match every filter. Counts update as you choose."
4. **Field groups**, one per filterable field, each a `group` with a label and FilterChips (36 high; 12 dp
   between wrapped lines so each chip reaches a 48 hit area):
   - **Text fields with ≤ 8 values** (Side, Relationship, Store, Category): all values as chips with counts.
   - **Text fields with more values** (City: 14): the 6 most common values + "Show all 14" → **value picker
     page** (`S29-value-picker`): SearchField "Search 14 cities", all values as chips sorted by count then
     A–Z, values that would leave 0 items dimmed and disabled; header "City" + "2 selected".
   - **Number fields** (Price): two Inputs "From" / "To" with the unit suffix (EUR), placeholders = min and
     max in the segment, helper "Prices in Accept go from €24 to €649." Rating uses single-choice chips "Any",
     "4 and up", "4.5 and up" (`star`) with the note about items without a rating.
   - **Date fields** (e.g. Apartment viewings "Viewing"): "From" / "To" date inputs (system date picker) + chips "Last 7 days",
     "Last 30 days".
   - **Pseudo-fields**: shared lists: **List status** (Agreed `check-check`, Pending `clock`, Conflict
     `git-compare-arrows`, Resolved `gavel` when any) and **Decided by a member** (member Select, default
     the first other member, + chips Accepted, Rejected, Maybe, Not decided). In the Final decisions view the
     pseudo-field **My decision** (Accepted, Rejected, Maybe, Not decided) is added; in My decisions it is
     the segment itself and not repeated.
   - **Notes and edits**: "Has a note" (`sticky-note`; my notes and others' shared notes), "Edited"
     (`pencil-line`). Hidden when no item in the segment has either.
   - Sections without at least one value in the segment are hidden; fields hidden from the card are still
     filterable (they are in the working copy).
5. **No-results preview** (only when the current choices match 0 items): bordered panel at the top of the
   content, `role=status`: `search-x` + "No items match these filters", reason, "Reset filters".
6. **Footer** (pinned, `border-t`): "Reset" (outline; disabled when nothing differs from the default) +
   primary "Show 12 items" (count live; disabled "Show 0 items" at zero).

Chip counts are **faceted**: each value shows how many items of the segment would remain if it were added,
given the other fields' filters (within the same field, values combine with OR). Values that would leave 0
items are dimmed and disabled unless already selected.

Components: BottomSheet, Select (trigger) + radio list, SegmentedControl, FilterChip (Toggle, `aria-pressed`),
radio chips, Input with suffix, SearchField, Alert (neutral), Button. iOS: page sheet with nav bar buttons.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S29-default` | Wedding guests, My decisions, Accept (48): Sort Recently decided; Side Groom's (12) and Relationship Friend (12) selected; City top 6 + "Show all 14"; "Show 12 items" | Filter chip in `S28-shared-mine` |
| `S29-shared-scrolled` | Same sheet scrolled: List status (Agreed 9, Pending 1, Conflict 2), Decided by a member: Mert Aydın (Accepted 11, Rejected 1, Maybe 0, Not decided 0), Notes and edits (Has a note 1, Edited 2) | Scrolling |
| `S29-value-picker` | City page: search, 14 chips, İstanbul and Ankara selected, zero values dimmed; "Show 6 items" | "Show all 14" |
| `S29-products` | Desk setup, Accept (8): Store, Category, Price (empty inputs), Rating "Any"; Reset disabled; "Show 8 items" | Filter chip in `S28-default` |
| `S29-number-range` | Price From 50 To 500 (To focused), counts re-faceted (Oakline 0, Desk 0); "Show 5 items" | Typing a range |
| `S29-sort` | Sort by page: Price selected with "Low to high / High to low" | Sort chip, or the Sort by trigger |
| `S29-no-results` | Oakline + Price 100–500 → no-results panel, "Show 0 items" disabled | Choices that match nothing |
| `S29-applied` | Back on S28: Filter (1), "Price: €50 to €500" chip, "5 of 8 items", snackbar "Filters applied" | "Show 5 items" |
| `S29-ios` | iOS page sheet: Cancel / "Filter and sort" / Reset in the bar, single "Show 5 items" | iOS |
| `S29-web-desktop` | Desktop column, keyboard hints in the sheet footer | Desktop browser |
| `S29-large-text` | 200%: full-screen sheet without handle, larger chips that wrap, buttons stacked | Font scale ≥ 150% |

No loading, error or offline state: values and counts come from the working copy on the device. On lists
over 5,000 items the primary button shows a 16 spinner + "Counting…" for up to a second after a change
(the previous count stays readable).

## 5. Interactions, gestures and transitions

- Opens with the standard sheet motion (300 ms emphasized decelerate; reduced motion: 150 ms fade).
- Choices are **staged**: nothing changes in S28 until "Show N items". Counts in chips and the button update
  immediately (250 ms count tick; reduced motion: instant). Number inputs update the count 300 ms after
  typing stops; From > To swaps the values on blur.
- Chips toggle on tap (`aria-pressed`). Rating chips are single choice.
- "Show all 14" pushes the value picker inside the sheet (shared axis X, 250 ms); search narrows chips as you
  type (accent-insensitive); back keeps the selection.
- Sort by page: tapping a row selects it and shows its direction control; the default direction is the
  first label. Back (or the arrow) returns to the main page. Sort is applied with "Show N items".
- **Reset** returns every choice to the default (Recently decided, no filters) on the sheet; S28 changes only
  after "Show N items". "Reset filters" in the no-results panel resets filters but keeps the sort.
- **Show N items**: closes the sheet and applies; S28 shows the count line, AppliedFilterChips and scrolls to
  the top; snackbar "Filters applied" (only when filters changed; not for sort alone).
- Dismissing (close, swipe down past 30% or 800 dp/s, scrim tap, back, Esc, Cancel) discards staged changes.
- Filters and sort are stored per list, view and member (not per segment): they apply to whichever segment
  is selected, so switching segments in S28 keeps them.

## 6. Copy

| Element | String |
| --- | --- |
| Title / caption | "Filter and sort"; "My decisions in Accept, 48 items"; "Final decisions in Conflicts, 15 items"; "Accept, 8 items"; "Accept, 1 item" |
| Sort trigger | "Sort by"; values as below |
| Sort by page | Title "Sort by"; caption "Empty values always go last."; rows "Recently decided" / "Decision time", "Original order" / "As imported", "{Field}" / "Text", "Number", "Date", "Phone", "Email", "Link"; directions "A to Z", "Z to A", "Low to high", "High to low", "Oldest first", "Newest first"; back label "Back to filters" |
| Filters | "Filters"; "Items must match every filter. Counts update as you choose." |
| Field groups | "{Field}" (e.g. "Side", "Relationship", "City", "Store", "Category", "Price", "Rating", "Taken"); "Show all 14" |
| Pseudo-fields | "List status": "Agreed", "Pending", "Conflict", "Resolved"; "Decided by a member" + "Filter by what another member chose." + member name ("Mert Aydın") + "Accepted", "Rejected", "Maybe", "Not decided"; "My decision": "Accepted", "Rejected", "Maybe", "Not decided" |
| Notes and edits | "Notes and edits"; "Has a note"; "Edited" |
| Number range | "From", "To"; unit suffix from the field ("EUR"); helper "Prices in Accept go from €24 to €649." ("{Field} in {segment} goes from {min} to {max}.") |
| Rating | "Any", "4 and up", "4.5 and up"; "Items without a rating are left out when you choose one." |
| Date range | "From", "To", "Last 7 days", "Last 30 days"; "Choose a date" |
| Value picker | Title "{Field}" ("City"); caption "2 selected" ("1 selected", "None selected"); search "Search 14 cities" ("Search {n} values" for fields without a plural); "Choose one or more. Values that would leave no items are dimmed." |
| No results | "No items match these filters" / "Remove a filter or choose other values. Oakline items in Accept cost €39 and €649." (the second sentence only when one filter clearly causes it) / "Reset filters" |
| Footer | "Reset"; "Show 12 items" ("Show 1 item", "Show 0 items" disabled); progress "Counting…" |
| Snackbar | "Filters applied" |
| iOS bar | "Cancel", "Filter and sort", "Reset" |
| Keyboard hints (desktop) | "Esc Close", "Enter Show items", "Tab Next control" |
| Screen reader | Chip "Groom's, 12 items, selected"; footer "Show 12 items"; count change "12 items match" |

## 7. Accessibility

- The sheet is a modal dialog labelled "Filter and sort"; focus moves to the title on open and returns to the
  Filter chip on close.
- Each field is a `group` labelled by its heading; chips are toggle buttons (`aria-pressed`) named with value
  and count; disabled chips are announced as dimmed with "0 items". Rating is a `radiogroup`.
- Sort by rows are a `radiogroup`; the direction control is a `radiogroup` "Direction".
- Inputs have visible labels; the unit suffix is part of the accessible description ("From, EUR").
- The live count is announced once (polite) 500 ms after the last change: "12 items match".
- The no-results panel is `role=status`; "Show 0 items" is a real `disabled` button and the panel explains why.
- Touch targets: chips 36 high in 48 rows (hit slop 6), rows 48+, buttons 48, icon buttons 48.
- Large text (`S29-large-text`): the sheet opens full screen without a handle; chips use `text-title-3`
  and grow to 48+; labels never truncate (chips wrap); footer buttons stack (primary first).
- Reduced motion: fades only; counts change instantly.

## 8. iOS and web differences

- **iOS** (`S29-ios`): page sheet (large detent, grabber); navigation bar with "Cancel" (leading),
  centered title, "Reset" (trailing); one full-width "Show 5 items" at the bottom; Sort by and the value
  picker push inside the sheet's navigation stack (back chevron "Filter and sort"). Swipe down = Cancel.
- **Android**: M3 bottom sheet; system back closes a pushed page first, then the sheet.
- **Web, mobile**: as Android without system bars.
- **Web, desktop** (`S29-web-desktop`): sheet inside the centered column; Esc closes, Enter applies (when
  focus is not in a text field), Tab / Shift+Tab move through controls, Space toggles a chip; hints under
  the footer.

## 9. Edge cases

- **Many values** (> 8): top 6 + "Show all"; over 200 values the picker lists values in a virtualized
  list with checkboxes instead of chips (same counts).
- **Long values** (+40%, e.g. "Abbasağa, Ihlamurdere Cd. 33"): chips wrap onto more lines; a single value
  longer than the sheet truncates in the middle with the full value as the accessible name.
- **Empty values**: a chip "No value" (muted, `circle-dashed`) appears last when some items have no value for
  the field.
- **Multi-value fields** (several phones): an item matches when any value matches.
- **Edited fields**: filters use the working-copy value (SAFE-02), not the original.
- **Numbers without a value** (p15 has no rating): left out by any rating or range filter; included with "Any".
- **Shared lists, filtering by a member who left**: their decisions stay filterable (A-77) with "(left)"
  after the name.
- **Segment changes after applying** (a decision changed in S28): filters stay; counts in S28 recompute.
- **Others' private notes** are never counted in "Has a note".
- **Round mode** (S28 round results): the same sheet; decisions refer to that round; "Recently decided" is
  replaced by "Card order" as the default sort.
