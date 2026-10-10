# S28 Results

Frames: `S28-results.html` (generator: `tools/generators/S28-S30-results.py`). Filter and sort sheet:
`S29-filter-sort.md`. Round history: `S30-round-history.md`.
Data: `lists` l-desk, l-wedding, l-apartments; `products` p01–p20 with `productDecisions.round1/round2`;
`rounds` r-d1, r-d2, r-w1, r-a1; `contacts` + `shared.items`, `shared.myDecisions`, `shared.notes`, `shared.edits`;
`members` u-deniz (me, Owner), u-mert (Decision Maker), u-selin (Collaborator); `apartments` a01–a08.

## 1. Purpose and requirements

Show where every item ended up, one decision at a time, and let people find, narrow down and fix any
decision without starting a round. On shared lists, separate the list's final decisions from my own
choices so nobody mistakes "I accepted" for "we accepted".

Covers: RES-01, RES-02, RES-03, RES-04, RES-05, RES-06, COL-16, DM-01–DM-05, DM-09, DM-14, DM-18, DM-20,
RND-03 (round results view), SRT-16 (review results target), EXP (Export entry), SAFE-02, GOAL-02, GOAL-03,
GOAL-04, PLT-01–PLT-04, PLT-13–PLT-17, PLT-21, PLT-23, STK-06, STK-07, VIS-09, VIS-11, VIS-12, VIS-14,
TERM-01, TERM-02, SUC-06, SCR-28.

## 2. Entry points and exits

| From | How | Opens |
| --- | --- | --- |
| S27 round summary | "Review results" (`review-results`) | `S28-default` (Desk setup after Round 2), `S28-shared` from S27-shared |
| S09 list overview | "Results" row | latest results, Accept segment (shared: Final decisions) |
| S30 round history | "Latest results", or a round | `S28-default`, or round mode `S28-round-1` / `S28-round-2` |
| S38 activity | "Mert resolved 12 conflicts" (S38 links `S28-shared`; the resolved state is `S28-shared-resolved`) | Final decisions |
| S36 conflicts | "See results" | `S28-shared` |

| To | How |
| --- | --- |
| S26 item detail (pushed) | Tap a row or row menu "Open details" (`S26-product`, `S26-shared-conflict`, `S26-read-only`) |
| Change decision sheet (in S28) | Row menu "Change decision" ("Change my decision" on shared lists), long-press (Android), swipe action (iOS) |
| Note sheet (in S28) | Row menu "Add note" (same sheet as S25 `S25-note`) |
| S29 filter and sort sheet | "Filter" chip, Sort chip |
| S39 export | "Export" in the app bar (`export`) → `S39-default` (solo), `S39-shared`, `S39-apartments` |
| S30 round history | `history` icon button "Round history" |
| S36 conflicts | "Review 15 conflicts" (shared, Conflicts segment) |
| S25 sorting | "Continue sorting" in the Pending explainer |
| S24 start a round | "Re-sort Maybe (1)" under the Maybe segment; "Start a new round" in the empty Maybe segment |
| S09 list overview | Back arrow, Android back, iOS edge swipe |

Route: `list/[listId]/results?view=final|mine&segment=accept|maybe|reject|conflict|pending|none&round=<roundId>`.
The last segment, view, sort and filters are remembered per list and member until the app restarts.

## 3. Layout and components

Pushed screen in the list stack, no bottom navigation. Top to bottom:

1. **AppBar (small)**: back IconButton ("Back to {list}"), title "Results" with the list name as a caption,
   trailing IconButton `history` ("Round history") and the text action **Export** (`text-label-lg
   text-primary`, 48 high). Round mode: title "Round 1 results", no trailing actions.
2. **View toggle** (shared lists only, RES-05): SegmentedControl "Final decisions" / "My decisions"
   (radiogroup), `px-gutter pb-2`.
3. **DecisionSegments** (RES-01): one row of chip tabs, 40 high in a 48 row, icon 16 + label + count
   (`tabular-nums`). Selected `bg-foreground text-background`, others `bg-secondary`. The row scrolls
   horizontally; the selected tab is scrolled fully into view (Conflicts and Pending sit off-screen at first
   on shared lists). Segments by view:

   | View | Segments, in order |
   | --- | --- |
   | Solo list | Accept, Maybe, Reject |
   | Shared, Final decisions | Accept, Maybe, Reject (Agreed or resolved items), Conflicts, Pending |
   | Shared, My decisions | Accept, Maybe, Reject, Not decided |

   Results lead with **Accept** (the result people come for), then Maybe, then Reject; this is the one place
   where the decision order is not Reject, Maybe, Accept. Icons and labels stay, so meaning never depends on
   position. Conflicts exist only in Final decisions: in My decisions an item in conflict is still one of
   my Accept / Maybe / Reject items and carries the Conflict status on its row.
4. **Toolbar** (RES-02–RES-04): SearchField (48, pill, `bg-secondary`) with the placeholder naming the scope
   ("Search 8 items in Accept"); below it a chip row: **Filter** (`sliders-horizontal`; active = primary-soft
   with a count bubble), **Sort** (`arrow-up-down`, current sort as its label + `chevron-down`), then one
   **AppliedFilterChip** per filter ("Side: Groom's" + `x`). With applied chips the row wraps to a second line.
5. **Count line** (only while searching or filtering): "12 of 48 items" (`role=status`).
6. **Segment note** (optional, `text-body-sm muted`): Conflicts "Members chose differently. Mert resolves
   conflicts as Decision Maker." (rule-dependent, see §6); Pending explainer (muted panel radius 12 with
   `clock`, text and "Continue sorting"); resolve notice (`gavel`); offline line (`cloud-off`); round banner
   (`primary-soft`, `history`, "See latest results").
7. **ItemRows**, full-bleed on the canvas (not cards), dividers inset to the text column:
   - Lead: product/photo thumbnail 48 (`rounded-sm`), person avatar 40 (photo or initials), none for text-only
     templates (Generic).
   - Title: title field, `text-body`, up to 2 lines.
   - Meta (`text-body-sm muted`, up to 2 lines): solo = subtitle fields from the card template ("€389,
     Nordhaus"; contacts "Bride's, Family, İstanbul"); shared rows = **who decided what** as icon + text parts
     (MemberDecisionsText): `check` "You and Selin accepted", `x` "Mert rejected", `circle-dashed` "Selin
     hasn't decided", `clock` "Waiting for you and Selin". Each part has the decision icon in its soft decision color plus the
     decision word.
   - Trailing: DecisionBadge (solo and round mode), StatusBadge (shared: Agreed, Pending, Conflict, Resolved by
     Mert), nothing in Conflicts/Pending (the meta says it all).
   - Overflow IconButton (`ellipsis-vertical`, 48) → DropdownMenu. Read-only lists have none.
   - The whole row except the overflow button is one link to S26.
8. **Bottom action** (shared, Conflicts segment only): pinned primary "Review 15 conflicts" → S36.
9. Overlays: DropdownMenu (row menu), **ChangeDecisionSheet**, note sheet, Snackbar (bottom 16), S29 sheet.

**ChangeDecisionSheet** (Proposed; BottomSheet + the S26 decision control): title "Change decision" ("Change
my decision" on shared lists), close `x`; item summary (lead, title, meta); three equal Buttons in a
radiogroup in decision order **Reject, Maybe, Accept** (unselected outline with the icon in its soft
decision color, selected solid fill); on shared lists the other members' decisions (MemberDecisions
expanded: avatar, name, role, DecisionBadge); a consequence line.

Components: AppBar, SegmentedControl, DecisionSegments, SearchField, FilterChip/Toggle, AppliedFilterChip
(Proposed), ItemRow, Avatar, DecisionBadge, StatusBadge, MemberDecisionsText (Proposed), DropdownMenu,
BottomSheet, ChangeDecisionSheet (Proposed), Textarea, Snackbar, Alert, OfflineBanner, EmptyState,
ErrorState, Skeleton, FastScroller (Proposed), RowSwipeActions (Proposed, iOS), Kbd.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S28-default` | Desk setup after Round 2: Accept 8, Maybe 1, Reject 11; Accept rows newest decision first (p07, p04, p15 from Round 2, then p09, p06, p03, p02, p01) | S27 "Review results" (Flow 2), S09 |
| `S28-maybe` | Maybe segment: p18 (Maybe in both rounds) + "Re-sort Maybe (1)" | Tap Maybe |
| `S28-row-menu` | DropdownMenu: Open details, Change decision, Add note | Row overflow button |
| `S28-change-decision` | Sheet for p18, Maybe selected | Menu "Change decision", long-press |
| `S28-changed` | p18 now Accepted, row highlighted in place, counts Accept 9 / Maybe 0, snackbar "Changed to Accept" + Undo | Tap Accept in the sheet |
| `S28-empty-segment` | "Nothing in Maybe" empty state + "Start a new round" | Segment with 0 items (after the snackbar closes) |
| `S28-add-note` | Note sheet "Note on Bookshelf speakers, pair" | Menu "Add note" |
| `S28-search` | "lamp" in Accept: 1 of 8 (p15, match in bold) + "1 match in Reject" with Show | Typing in search |
| `S28-search-none` | "headphones": "No matches in Accept", "Show 1 match in Reject", "Clear search" | Search with no match in the segment |
| `S28-filtered` | Wedding guests, My decisions, Accept: Side Groom's + Relationship Friend → "12 of 48 items", two AppliedFilterChips, Filter with count 2 | "Show 12 items" in `S29-default` |
| `S28-sorted` | Accept sorted by Price, high to low (Sort chip "Price, high to low") | Sort chosen in `S29-sort` |
| `S28-shared` | Wedding guests, Final decisions, Conflicts 15: who decided what on each row, rule note, "Review 15 conflicts" | Tap Conflicts; S27-shared "Review results" |
| `S28-shared-accept` | Final decisions, Accept 22: Agreed items, field summary, Agreed badge | Tap Accept / Final decisions |
| `S28-shared-pending` | Pending 53: "Not final yet" explainer with per-member counts and Continue sorting; rows waiting for me first | Tap Pending |
| `S28-shared-mine` | My decisions, Accept 48 / Maybe 11 / Reject 17 / Not decided 24; every row has its list status; conflict rows say who chose differently | Tap My decisions |
| `S28-shared-change` | "Change my decision" for Isabella Rossi (c069): Accept selected, Mert Rejected, Selin Accepted, consequence "Choosing Reject makes this item Agreed." | Row menu on a shared row |
| `S28-shared-resolved` | After Mert's bulk resolve (S37): Final Accept 28, Reject 10, Conflicts 3; resolved rows show "Resolved by Mert" and where my decision differs (`x` "You chose Reject") | Activity "Mert resolved 12 conflicts", or opening Results after S37 |
| `S28-round-1` | Round mode: "Round 1 results", banner, Accept 5 / Maybe 6 / Reject 9; Maybe rows say what Round 2 did ("Changed to Accept in Round 2", "Still Maybe in Round 2") | S30 tap Round 1 |
| `S28-round-2` | Round mode for Round 2: Accept 3 / Maybe 1 / Reject 2 | S30 tap Round 2 |
| `S28-archived` | Apartment viewings (archived): notice, read-only rows (no menu), Export still available | S30-single-round, S09-archived |
| `S28-loading` | Skeleton segments, search and rows; Export hidden until counts exist | Opening a very large list |
| `S28-offline` | Offline banner + "List statuses from 12 min ago…"; everything else works | No connection (shared) |
| `S28-error` | "Results couldn't be opened" + Try again / Back to list | Working copy unreadable |
| `S28-large-list` | Scrolled: segments pinned under the app bar with a divider; FastScroller with letter bubble "M" (sorted by Name) | Scrolling a long segment |
| `S28-ios` | iOS nav bar; row swiped left: Maybe and Reject swipe actions | iOS |
| `S28-web-desktop` | Desktop column, row hovered, menu as a popover, keyboard hints | Desktop browser |
| `S28-large-text`, `S28-large-text-menu` | 200%: bigger rows, badge under the title, Export and Round history move into an overflow menu | Font scale ≥ 150% |

## 5. Interactions, gestures and transitions

- **Segments**: tap switches instantly (no animation on content; the selected chip fill cross-fades 150 ms).
  Android: horizontal swipe on the list does **not** switch segments (it would fight iOS swipe actions and
  the horizontal segment row); segments are switched by tapping only. Each segment keeps its own scroll
  position; search and filters apply to the segment shown and are kept when switching segments.
- **Counts** always reflect the whole segment (not the search or filter); the count line shows the narrowed
  number. Counts tick (250 ms; reduced motion: instant) when a decision changes.
- **Search** (RES-02): filters as you type (debounce 150 ms); matches the title, every field of the item
  (including hidden fields) and visible notes; ignores case and accents (ı/i, ş/s, ç/c, ğ/g, ö/o, ü/u), uses
  Turkish casing (İ/i). Matching text in the title is set in semibold. Below the results: "In other
  segments" rows ("1 match in Reject" + Show) switch segment and keep the query. Clear (`x`) empties the field
  and keeps focus. Android back first clears an active query, then leaves.
- **Filter / Sort chips** open S29 for the current segment. AppliedFilterChip tap removes that filter at once
  (no confirmation; snackbar "Filter removed" + Undo, 4 s). Filters persist per list and view.
- **Sort options** (S29): Recently decided (default; newest decision first), Original order, Name (title field)
  A to Z / Z to A, any other field ascending/descending; empty values last. Pending defaults to "Waiting for
  you first", then original order. Round mode defaults to card order of that round.
- **Row tap** pushes S26 (M3 shared axis X 300 ms; iOS native push). Back returns to the same segment and
  scroll position.
- **Change decision** (RES-06): row overflow → "Change decision" (Android long-press on a row opens the same
  menu; iOS long-press opens a context menu with the same items). The sheet applies the decision **on tap**
  (no confirm button) and closes (200 ms); the row stays in place with its new badge and `bg-accent` until the
  snackbar "Changed to Accept" + Undo (6 s) closes or the user scrolls, then collapses out of the segment
  (height 250 ms, emphasized accelerate; reduced motion: instant). Counts update immediately. Undo restores
  the previous decision and position. Tapping the current decision just closes the sheet.
  - Solo lists: the change is recorded as the item's latest decision (A-33). Round history keeps each round
    as it ended (S30 never changes).
  - Shared lists: it changes **my decision** only; list status recomputes for everyone after sync; a change
    that creates or ends a conflict is announced in Activity (S38). The final decision is never edited
    directly here; conflicts are resolved in S36/S37 by the Decision Maker.
  - Round mode: the sheet changes the item's current decision (not the past round) and says so: "Your Round 1
    decision stays in round history."
- **Add note**: opens the S25 note sheet for that item; "Save note" closes it with snackbar "Note saved".
- **Shared view toggle**: switching keeps the selected decision segment when it exists in the other view;
  Conflicts/Pending map to Accept in My decisions; Not decided maps to Pending in Final decisions.
- **Pending explainer**: "Continue sorting" opens S25 at my next undecided item of the current round.
- **Large lists**: rows are virtualized; the segment bar pins under the app bar (with a divider) while the
  toggle, search and chips scroll away and come back on any upward scroll (quick return). A FastScroller
  appears on the right edge after 3 screens of rows; dragging it shows a 56 bubble with the current letter
  (text sorts) or value (number/date sorts); released, it fades after 1.5 s.
- **Pull to refresh** (shared lists, online): re-syncs statuses; spinner under the app bar.
- **Export** opens the S39 modal with the current view's scope preselected (segment = scope, e.g. Accept →
  "Only Accept").

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Results"; caption "{List name}"; round mode "Round 1 results"; actions "Round history" (label), "Export" |
| Back labels | "Back to Desk setup" ("Back to {list}"); round mode "Back to round history" |
| View toggle | "Final decisions", "My decisions" (group label "Show decisions") |
| Segments | "Accept 8", "Maybe 1", "Reject 11", "Conflicts 15", "Pending 53", "Not decided 24" (tablist label "Decisions"; tab names read "Accept, 8 items") |
| Search placeholder | "Search 8 items in Accept"; "Search 1 item in Maybe"; "Search 15 conflicts"; "Search 53 pending items"; label "Search in Accept" |
| Chips | "Filter" (+ count "2"); sort labels "Recently decided", "Original order", "Name, A to Z", "Name, Z to A", "Price, low to high", "Price, high to low", "Waiting for you first"; applied "Side: Groom's", "Relationship: Friend", "Relationship: Friend or Family", "Price: €50 to €500"; remove label "Remove filter: Side is Groom's" |
| Count line | "12 of 48 items"; "1 of 8 items" |
| Search, other segments | "In other segments"; "1 match in Reject"; "3 matches in Reject"; "Show" |
| Search, none | "No matches in Accept" / "Nothing in Accept matches “headphones”. It matches 1 item in Reject." / "Show 1 match in Reject" / "Clear search"; nowhere: "No matches" / "Nothing in Desk setup matches “standing”. Check the spelling or try another word." |
| Row meta (shared) | "You and Selin accepted", "Mert rejected", "Selin chose Maybe", "Selin hasn't decided", "You haven't decided", "Waiting for Selin", "Waiting for you and Selin", "Waiting for you, Mert and Selin", "You chose Reject" |
| Badges | "Accepted", "Maybe", "Rejected", "Not decided"; "Agreed", "Pending", "Conflict", "Resolved by Mert", "Resolved by majority" |
| Row menu | "Open details", "Change decision" (shared: "Change my decision"), "Add note" ("Edit note" when I have one), shared conflicts also "Review in Conflicts"; overflow label "More options for {title}" |
| Change sheet | Title "Change decision" / "Change my decision"; group label "Decision for {title}"; buttons "Reject", "Maybe", "Accept"; lines: "Maybe in Round 1 and Round 2. The change applies at once and round history keeps both rounds as they were."; "Decided in Round 1, Oct 4."; round mode "Your Round 1 decision stays in round history."; shared "Changing your decision updates the list status for everyone. Choosing Reject makes this item Agreed." / "… Choosing Accept keeps this item in Conflict." |
| Snackbars | "Changed to Accept" / "Changed to Maybe" / "Changed to Reject" + "Undo"; "Filter removed" + "Undo"; "Note saved"; "Saved on this phone. It will sync when you're back online." (first change offline); error "Couldn't change the decision. Try again." + "Try again" |
| Maybe segment | "Still undecided after Round 2. Sort it again with a fresh look." / "Re-sort Maybe (1)" |
| Empty segments | Maybe: "Nothing in Maybe" / "Items you swipe up will wait here." / "Start a new round"; Accept: "Nothing accepted yet" / "Items you swipe right will show up here."; Reject: "Nothing rejected" / "Items you swipe left will show up here."; Conflicts: "No conflicts" / "Everyone who decided an item chose the same."; Pending: "Nothing pending" / "Every member has decided every item."; Not decided: "You've decided every item" |
| Conflicts note (rule) | Decision Maker decides: "Members chose differently. Mert resolves conflicts as Decision Maker."; Everyone must agree: "Members chose differently. Conflicts stay open until everyone chooses the same."; Majority decides: "Members chose differently. The majority decides once everyone has decided." |
| Conflicts action | "Review 15 conflicts" |
| Pending explainer | "Not final yet" / "These items get a final decision once every member has decided them. Waiting for Selin on 53, for you on 24 and for Mert on 12." / "Continue sorting" (hidden when I have nothing left) |
| Resolve notice | "Mert resolved 12 conflicts. 3 stay open because he hasn't decided them." |
| Round banner | "Decisions as they were when Round 1 ended on Oct 4. 6 items were sorted again in Round 2." / Round 2: "Round 2 sorted the 6 Maybe items from Round 1 on Oct 6. These are also the latest decisions for them." / "See latest results"; round rows "Changed to Accept in Round 2", "Changed to Reject in Round 2", "Still Maybe in Round 2" |
| Archived notice | "Apartment viewings is archived. Restore it to change decisions or add notes. Export still works." |
| Offline | Banner "You're offline. Changes are saved on this phone."; line "List statuses from 12 min ago. They update when you're back online." |
| Error | "Results couldn't be opened" / "Your decisions are safe. Try again, or go back and open Results from the list." / "Try again" / "Back to list" |
| Loading | Screen reader "Loading results" |
| Large text menu | "More options: Export, Round history" (button label); items "Export", "Round history" |
| iOS swipe actions | "Maybe", "Reject", "Accept" (the two decisions the item doesn't have); leading "Note" |
| Keyboard hints (desktop) | "/ Search", "F Filter and sort", "↑ ↓ Move", "Enter Open" |
| Screen reader, row | "Mehmet Yılmaz. You and Selin accepted, Mert rejected. Conflict. Opens details." |

## 7. Accessibility

- Focus order: Back, Round history, Export, view toggle, segment tabs, search, Filter, Sort, applied chips,
  count line, notes/banners, rows (row link, then its More options), bottom action.
- Segments are a `tablist`; each tab is named with label + count + "items" and `aria-selected`. Arrow keys
  move between tabs on web; the list is the tab panel.
- The view toggle is a `radiogroup` "Show decisions".
- Rows: one link per row whose name is title + meta + badge text; the overflow button is separate ("More
  options for {title}"). Custom accessibility actions on each row (TalkBack actions, VoiceOver rotor):
  **Change decision to Accept / Maybe / Reject**, **Add note**, **Open details** so the menu is never needed.
- Who decided what is always text (MemberDecisionsText) with icons; decision colors are never alone.
- The count line and search results are `role=status` (polite, announced once after typing stops).
- Change decision sheet: dialog labelled by its title; the decision control is a `radiogroup` with the
  current decision checked; after a change focus returns to the row and the snackbar is announced.
- Snackbars stay at least 10 s while a screen reader runs.
- Touch targets: rows ≥ 64, icon buttons 48, Export 48 high; segment tabs (40) and chips (36) sit in 48
  rows with hit slop (same as FilterChip in components.md).
- Large text (`S28-large-text`): titles `text-title-2`, meta `text-title-3`, the badge moves under the
  meta, thumbnails top-align, the app bar keeps Back + title + one overflow button (Export, Round history),
  chips grow to 48.
- Reduced motion: no row collapse animation, no count tick, sheet fades 150 ms.

## 8. iOS and web differences

- **iOS** (`S28-ios`): navigation bar with back chevron + list name, centered "Results", trailing Round
  history icon and "Export" text button; edge-swipe back. Rows have **swipe actions** (RowSwipeActions):
  trailing swipe reveals the two decisions the item doesn't have (in decision order, e.g. Maybe and Reject
  for an accepted item; full swipe applies the outer one), leading swipe reveals "Note". Long-press opens
  a context menu (Open details, Change decision, Add note) with a row preview. Change decision opens as a
  page sheet at the medium detent. No overflow button on iOS rows (swipe + context menu + VoiceOver actions).
- **Android**: overflow button + long-press menu; no swipe actions (M3 lists don't use them for non-dismiss
  actions; avoids conflict with the horizontal segment row).
- **Web, mobile**: Android layout without system bars; browser back pops to S09.
- **Web, desktop** (`S28-web-desktop`): centered column; rows highlight on hover; the row menu opens as a
  popover next to the button (not over other buttons); keyboard: `/` focuses search, `F` opens S29, ↑ ↓ move
  between rows, Enter opens details, Shift+F10 / context-menu key opens the row menu; hints under the list.
- No web-unavailable features on this screen.

## 9. Edge cases

- **Solo vs shared**: solo lists have no view toggle, no Conflicts or Pending segments and no status badges
  (my decision is final, DM-01).
- **Latest decision per item** (A-33): an item decided in several rounds appears once, in the segment of its
  latest decision; round mode shows the past.
- **Items never decided** (added mid-round, or round ended early): solo lists show a fourth segment "Not
  decided" after Reject when it has items; shared lists show them under Pending.
- **Resolved conflicts**: shown in Accept/Maybe/Reject of Final decisions with "Resolved by Mert" (or
  "Resolved by majority"); when my decision differs, the meta says "You chose Reject".
- **Others' private notes** are never searched, counted or shown.
- **Very large lists** (5,000+): counts use thousands separators ("1,204"); search runs on the local copy and
  stays under 100 ms; the FastScroller appears; filters/sorts never block the UI.
- **Long titles** wrap to 2 lines then truncate (full title in S26); meta wraps to 2 lines; badges never
  shrink; +40% labels make the segment row scroll further, never wrap.
- **Item removed by another member** while open: the row disappears with snackbar "{title} was removed from
  the list".
- **Archived lists** (`S28-archived`): read-only (no row menu, no swipe actions, no change sheet); search,
  filters, sort and Export work.
- **Offline**: everything works; decision changes on shared lists are queued and statuses recompute after
  sync; if another member's change conflicts on sync, Activity reports it.
- **Change while filtered**: an item that no longer matches the filters leaves the list after the snackbar,
  like a segment change.
- **Decision Maker** viewing Conflicts: the bottom action reads "Review 15 conflicts" for everyone; only the
  Decision Maker sees resolve actions inside S36/S37.
