# S30 Round history

Frames: `S30-round-history.html` (generator: `tools/generators/S28-S30-results.py`). Opens Results in round
mode (`S28-round-1`, `S28-round-2`). Data: `rounds` r-d1, r-d2 (Desk setup), r-w1 (Wedding guests), r-a1
(Apartment viewings); `lists` l-desk, l-wedding, l-apartments, l-candidates (never sorted);
`productDecisions.round1/round2`; `members`.

## 1. Purpose and requirements

Keep every round of a list with its own results (RND-03): what was included, in which order, when, how long
it took and what was decided. It answers "what did we decide the first time?" and explains why Results (the
latest decision per item, A-33) can differ from an earlier round.

Covers: RND-01 (shows what was included), RND-02 (shows the card order), RND-03, DM-14, DM-15, DM-20,
COL-07 (per-member results of a round), SRT-16 (start a new round), GOAL-03, GOAL-04, PLT-01–PLT-03,
PLT-13–PLT-16, PLT-21, PLT-23, STK-07, VIS-09, VIS-14, TERM-01, SCR-30.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S09 list overview | "Rounds" row (`rounds`) → `S30-default` |
| S28 results | `history` IconButton "Round history" (`round-history`) |
| S27 round summary | (not linked: the summary itself is the latest round; S30 is reached from S09/S28) |

| To | How |
| --- | --- |
| S28 round mode | Tap a round (`open-round`) → `S28-round-1`, `S28-round-2`; in-progress shared round → `S28-shared`; archived → `S28-archived` |
| S28 latest | "Latest results" row (`latest-results`) → `S28-default` |
| Round detail (pushed, in S30) | Info IconButton on a round (`round-details`) → `S30-round-detail`, `S30-round-2-detail`, `S30-shared-detail` |
| S24 start a round | "Start a new round" (`new-round`; Owner and solo lists; hidden on archived lists) |
| S25 sorting | "Continue sorting" (round in progress), "Start sorting" (never sorted) |
| S09 | Back |

Route: `list/[listId]/rounds` and `list/[listId]/rounds/[roundId]` (detail).

## 3. Layout and components

Pushed screen, no bottom navigation.

1. **AppBar (small)**: back IconButton, title "Round history", list name as caption.
2. **Latest results** (solo and finished shared lists): one ListGroup row (radius 16, `bg-card`): "Latest
   results", "The latest decision on each of the 20 items", decision split bar, legend, chevron → S28.
   Hidden while the only round is still in progress (the round row is the same thing).
3. **Rounds, newest first** (section header) → ListGroup of **RoundRows** (Proposed), divided by hairlines:
   - Title "Round 2" (`text-title-3`) + optional status Badge ("In progress", `hourglass`, muted).
   - Meta (`text-body-sm muted`): date and sorting time "Oct 6, sorted in 2 min" (solo; shared rounds show
     who started it instead, A-71), then what was included and the card order: "Maybe pile from Round 1, 6
     items, shuffled", "All 20 items, original order", "Accepted items, 48 items, sorted by City from A to Z",
     "Custom selection, 12 items, original order".
   - Decision split bar (h-2, `bg-reject | bg-maybe | bg-accept` with 2 dp gaps) and the legend with icon +
     count + word ("2 rejected", "1 maybe", "3 accepted"), in the decision order Reject, Maybe, Accept like S27
     (only the Results segments lead with Accept, A-107).
   - Shared rounds in progress: "List status" split with the S09-shared mapping (`bg-foreground` Agreed,
     `bg-foreground/50` Conflict, `bg-muted` Pending) + a legend where every item starts with a swatch of its
     bar color, then the status icon and count (the round detail uses the S09 list legend: swatch, icon,
     label, description, count), and "Members" mini rows (Avatar 24, name, progress bar, "76 / 100").
   - Trailing info IconButton (48, `info`) "Round 2 details". The row itself is one link to S28 round mode.
4. **Footnote** (`text-body-sm muted`): what history keeps, or who can start rounds on shared lists.
5. **Bottom bar** (pinned, `border-t`): primary "Start a new round" (solo, Owner) or "Continue sorting"
   (current round not finished by me).

**Round detail** (pushed): AppBar "Round 1" + list caption; **Result** card (split bar + DecisionBadges with
counts; shared in-progress: List status card); **Details** ListGroup of label/value rows: Items, Card order,
Started, Finished, Sorting time (solo) or Started by, Conflict rule (shared); **Changed in a later round**
row (solo, when a later round re-decided items) → the later round's results; **Members** (shared): one row per
member with avatar, name, a role line as in S34 (`crown` Owner, `gavel` Decision Maker, Collaborator as text), "85 / 100 decided", own split bar and legend; **Items in card order**:
numbered rows (position, thumbnail/avatar, title wrapping to 2 lines, DecisionBadge from that round), first 5 + "See all 20
items"; pinned primary "See Round 1 results".

Components: AppBar, ListGroup, RoundRow (Proposed), Progress (decision split, list status), Badge,
DecisionBadge, Avatar, IconButton, Button, Alert (neutral, archived), EmptyState, Skeleton.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S30-default` | Desk setup: Latest results (11 rejected / 1 maybe / 8 accepted); Round 2 (Oct 6, 2 min, Maybe pile from Round 1, 6 items, shuffled, 2 / 1 / 3); Round 1 (Oct 4, 6 min, All 20 items, original order, 9 / 6 / 5); Start a new round | S09 Rounds, S28 Round history |
| `S30-round-detail` | Round 1 detail: 9 rejected, 6 maybe, 5 accepted; Items All items (20), Original order, Oct 4 10:00–10:06, 6 min; "Round 2 sorted the 6 Maybe items again"; items in card order p01–p05 | Info on Round 1 |
| `S30-round-2-detail` | Round 2 detail: Maybe pile from Round 1 (6), Shuffled, Oct 6 12:30–12:33, 2 min; card order p15, p04, p18, p13, p07 | Info on Round 2 |
| `S30-in-progress` | Wedding guests (shared), Round 1 in progress: "You started it on Sep 28", List status 32 agreed / 15 conflicts / 53 pending, members You 76, Mert 85, Selin 43 of 100; Continue sorting | Shared list with a round running |
| `S30-shared-detail` | Round 1 detail (shared): List status card, Started by You Sep 28 19:05, Conflict rule Decision Maker decides (Mert), members with their own splits (48/11/17, 50/14/21, 25/10/8) | Info on a shared round |
| `S30-single-round` | Apartment viewings (archived): notice, one finished round (Jul 21, All 8 items, 3 / 1 / 4), footnote; no Start button | List with one round; archived lists are read-only |
| `S30-never-sorted` | Frontend hiring, Q4: "No rounds yet" + Start sorting | List never sorted (`currentRound: null`) |
| `S30-loading` | Skeleton rounds | Opening a list with many rounds (rare: history is local) |
| `S30-ios` | iOS: back chevron "Desk setup", info buttons in the tint color (detail disclosure), Start a new round | iOS |
| `S30-large-text` | 200%: Latest results group kept; titles `text-title-1`, meta wraps, legend one item per line | Font scale ≥ 150% |

No offline state: history is stored with the list on the device; on shared lists rounds started by the
Owner arrive with sync like any other change. No error state beyond the S40 generic error.

## 5. Interactions, gestures and transitions

- Tap a round row → S28 in round mode (push, shared axis X 300 ms). The info button is a separate target
  → round detail (push). On iOS the info button is the native detail disclosure.
- "Latest results" → S28 normal mode.
- "Start a new round" → S24 (full-screen modal), preselected as from S09 (Maybe pile when it has items).
  Shared lists: only the Owner sees it; other members see the footnote "Only Deniz, the Owner, starts new
  rounds." and no button (they can suggest a round from S09 → S24 "Suggest a round").
- "Continue sorting" → S25 at my next undecided item of the current round.
- Round detail: "See Round 1 results" and "See all 20 items" → S28 round mode; "Round 2 sorted the 6 Maybe
  items again" → S28 round mode for Round 2.
- Nothing animates on open; numbers are static (no count-up here; the count-up belongs to S27).
- Pull to refresh (shared, online) re-syncs.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Round history"; caption "{List name}"; back label "Back to {list}" |
| Latest results | "Latest results" / "The latest decision on each of the 20 items" |
| Section | "Rounds, newest first"; single round "Rounds" |
| Round row | "Round 2"; "Oct 6, sorted in 2 min"; "Maybe pile from Round 1, 6 items, shuffled"; "All 20 items, original order"; "Accepted items, 48 items, sorted by City from A to Z"; "Custom selection, 12 items, original order"; legend "2 rejected", "1 maybe", "3 accepted"; badge "In progress"; "Ended early" (round ended before everyone finished); info label "Round 2 details" |
| Shared round | "All 100 items, original order. You started it on Sep 28." (others: "Deniz started it on Sep 28."); "List status"; "32 agreed", "15 conflicts", "53 pending"; "Members"; "You", "Mert", "Selin"; "76 / 100" |
| Footnotes | Solo: none; shared Owner: "Finished rounds stay here with their results. As the Owner, you start new rounds for everyone."; shared member: "Finished rounds stay here with their results. Only Deniz, the Owner, starts new rounds."; single round: "Each new round adds its results here. Earlier rounds never change." |
| Archived notice | "Apartment viewings is archived. Restore it from the list to start a new round." |
| Buttons | "Start a new round"; "Continue sorting"; "Start sorting"; "See Round 1 results"; "See all 20 items" |
| Round detail | Title "Round 1"; "Result"; badges "9 rejected", "6 maybe", "5 accepted"; "Details"; labels "Items", "Card order", "Started", "Finished", "Sorting time", "Started by", "Conflict rule"; values "All items (20)", "Maybe pile from Round 1 (6)", "Original order", "Shuffled", "Sorted by City, A to Z", list status legend "Agreed" / "Everyone chose the same", "Conflict" / "Members chose differently", "Pending" / "Not everyone has decided", "Oct 4, 10:00", "Oct 4, 10:06", "6 min", "You, Sep 28, 19:05", "Decision Maker decides (Mert)", "Everyone must agree", "Majority decides"; "Changed in a later round"; "Round 2 sorted the 6 Maybe items again" / "3 accepted, 2 rejected, 1 still Maybe"; "Items in card order"; shared "List status", "In progress", "Members", "Deniz (you)", roles "Owner", "Decision Maker", "Collaborator", "76 / 100 decided" |
| Empty | "No rounds yet" / "Sort the list once and the results of each round will be kept here." / "Start sorting" |
| Loading | Screen reader "Loading rounds" |
| Screen reader, round row | "Round 2, Oct 6, sorted in 2 minutes. Maybe pile from Round 1, 6 items, shuffled. 2 rejected, 1 maybe, 3 accepted. Opens Round 2 results." |

## 7. Accessibility

- Focus order: Back, Latest results, each round (row link, then its details button), footnote, bottom button.
- Round rows are links whose accessible name reads the whole row (see §6); the split bar is decorative
  (`aria-hidden`) because the legend states the numbers with icon + word.
- The info button is a separate control named "Round 2 details".
- Member mini rows are one image with a text label ("You 76 of 100 decided, Mert 85 of 100, Selin 43 of
  100") inside the row; in round detail each member is a list item with text.
- Items in card order are an ordered list (`ol`); positions are real sequence numbers.
- Large text (`S30-large-text`): titles 28, meta 18 and wrapping, legend one item per line (Latest results and every round), bottom button 64.
- Touch targets: rows ≥ 120, info buttons 48, buttons 48.
- Reduced motion: only push transitions, replaced by fades.

## 8. iOS and web differences

- **iOS** (`S30-ios`): back chevron with the list name, centered title, inset grouped list; the info button
  uses the tint color (detail disclosure, separate from the row tap, HIG); edge-swipe back.
- **Android**: M3 small app bar; info IconButton.
- **Web, mobile / desktop**: same layout as Android (desktop centered in the column); no keyboard shortcuts
  beyond Tab/Enter. No separate desktop frame: nothing differs from the Android layout except the column.

## 9. Edge cases

- **Rounds are immutable**: changing a decision later (S28, S26) never changes a past round; it changes the
  latest results. The round that last decided an item is where Results takes the decision from.
- **Round ended early** (Owner ended it, or a new round started while open): badge "Ended early", the split
  includes "not decided" as the muted remainder, legend adds "4 not decided".
- **Shared rounds**: the split of a finished round shows final decisions at the time it ended (Agreed /
  resolved); open conflicts at the end show as "15 conflicts" in the legend; each member's own split is in
  the detail.
- **Many rounds** (10+): the list scrolls; rows stay full height; no paging.
- **Items deleted later**: counts stay as they were; the round detail's items list shows "{n} items were
  removed from the list since" as a muted line.
- **Items added mid-round** (S21): they joined the current round; the include line reads "All 112 items,
  original order (12 added during the round)".
- **Never sorted**: empty state with Start sorting (`S30-never-sorted`); S09 shows "Rounds: None yet".
- **Archived lists**: read-only (no Start / Continue), results still open.
- **Sorting time** counts active time only (gaps over 5 minutes excluded, A-71) and is hidden on shared lists.
