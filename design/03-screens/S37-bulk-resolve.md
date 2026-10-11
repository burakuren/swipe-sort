# S37 Bulk resolve: confirmation and summary

Frames: `S37-bulk-resolve.html`. Generator: `tools/generators/S35-S38-collaboration.py` (all counts computed
from `02-data/sample-data.json`). Related: S36 (one by one, the screen under the sheet), S35 (rule), S39
(export), S09.

## 1. Purpose and requirements

The Decision Maker applies their **own earlier decisions** to every open conflict in the current round in
one action. Items they never decided stay open, and both the confirmation and the summary say how many and
which. The action keeps one name through the flow: **Resolve all → "Resolve 12 conflicts" → Resolving… →
"Resolved 12 conflicts"**.

Covers: COL-15, DM-09, DM-11, DM-12, DM-20, A-27, GOAL-03 (confirmation, undo, partial failure keeps data),
GOAL-04, PLT-02, PLT-03, PLT-13–PLT-16, STK-06, STK-07, SCR-37.

Sample numbers (list `l-wedding`, Round 1): 15 open conflicts. Mert decided 12 of them while sorting:
**6 Reject** (c002 Mehmet Yılmaz, c015 Cem Tekin, c037 Volkan Taş, c060 Liam O'Connor, c064 Mateo García,
c069 Isabella Rossi), **0 Maybe**, **6 Accept** (c020 Merve Kurt, c029 Murat Ekinci, c043 Sinan Karakaya,
c049 Yiğit Oral, c059 Sophie Laurent, c071 Freya Nielsen). **3 stay open** because Mert never decided them
(`shared.summary.conflictsDecisionMakerUndecided`): c012 Gülşen Aydın, c034 Buse Altun, c056 Tuğba Sönmez.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S36 `S36-default` (any card frame) | "Resolve all" (`data-action="resolve-all"`) → `S37-confirm` sheet |
| S09 `S09-shared` | Conflicts row, Decision Maker only → `S37-default` |
| S09 conflicts row / stale confirm | Bulk resolve opened when every open conflict is one Mert never decided → `S37-nothing` (S36 hides "Resolve all" in that case, `S36-remaining`) |

| To | How |
| --- | --- |
| `S37-summary` | "Resolve 12 conflicts" (`data-action="confirm-resolve"`) |
| S36 `S36-default` | Cancel; "Resolve one by one" |
| S36 `S36-remaining` | "Review 3 open conflicts" (`data-action="review-open"`) |
| S39 `S39-shared` | "Export" (`data-action="export"`) |
| S09 `S09-shared-decision-maker` | "Done"; close (`x`); back from `S37-default` |

## 3. Layout and components

- **`S37-default` (entry)**: stack screen. AppBar "Resolve conflicts" / "Wedding guests, Round 1". Heading
  "15 conflicts need your decision" (`text-title-2`) + one sentence. A Group "Your earlier decisions on these
  items" with rows Reject 6, Maybe 0, Accept 6 (decision icon in a soft circle + label + count) and a
  separated "Not decided 3". Then a ListGroup with two choices: "Resolve one by one" (`layers`) → S36,
  "Resolve all with my decisions" (`gavel`) → confirmation. Footer: decisions stay editable in Results.
- **`S37-confirm`**: BottomSheet (`rounded-t-sheet`, top 40 dp, scrim over S36). Title as a question
  (`text-title-2`), consequence sentence, bordered Groups (hairline in light and dark) "12 will be resolved" with the split by decision (order
  Reject, Maybe, Accept; zero counts shown muted), Group "3 stay open" with ItemRows (avatar 40, name,
  subtitle, DecisionBadge "Not decided"), then the actions pinned at the bottom: primary "Resolve 12
  conflicts" (56 high, `data-action="confirm-resolve"`) and ghost "Cancel". The sheet body scrolls; the
  actions stay visible.
- **`S37-resolving`**: primary shows spinner + "Resolving…" (`aria-busy`; the count is announced to screen
  readers only, no second visible line); scrim taps and back are ignored until done (≤ 2 s typical).
- **`S37-summary`**: full-screen result (replaces the sheet; centered single-purpose moment). App bar: close
  `x` and text Button "Undo". Icon 56 (`gavel` on `secondary`), "Resolved 12 conflicts" (`text-title-1`),
  one sentence, Group with the split, section "3 still open" with the same ItemRows, bottom actions:
  primary "Review 3 open conflicts", outline "Export", ghost "Done".
- Dialog for Undo (AlertDialog), Alert (error), neutral Alert (offline).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S37-default` | Decision Maker opens bulk resolve from S09 (explains both ways) |
| `S37-confirm` | "Resolve all" tapped: 12 resolved with Mert's decisions, 3 stay open |
| `S37-resolving` | Confirmed; server applies the 12 resolutions atomically per item |
| `S37-summary` | Done: "Resolved 12 conflicts" |
| `S37-nothing` | Every open conflict is on an item Mert never decided (after the first bulk resolve: c012, c034, c056) |
| `S37-error` | Partial failure: 9 of 12 saved, 3 failed (connection dropped); retry for the 3 |
| `S37-undo` | "Undo" on the summary: confirmation |
| `S37-undone` | Undone: back on S36 with 15 open conflicts, snackbar |
| `S37-offline` | Offline: Resolve all is blocked; one by one still works offline |
| `S37-not-allowed` | Opened by someone who isn't the Decision Maker (old link, role moved, or rule Everyone must agree) |
| `S37-large-text`, `S37-summary-large-text` | 200% font scale |
| `S37-ios` | iOS page sheet |

## 5. Interactions, gestures and transitions

- **Resolve all** opens the sheet (300 ms, emphasized decelerate). Counts are computed when it opens from
  the latest synced decisions; if they change while it is open (a member decides), the sheet updates in
  place and announces "Counts updated".
- **Resolve 12 conflicts**: one request; each item becomes Resolved with Mert's decision as the final
  decision ("Resolved by Mert"). Members' own decisions are untouched. Members are notified once (S38
  conflictsResolved: "Mert resolved 12 conflicts. 3 are still open."). The sheet morphs into the summary
  (cross-fade 300 ms); success haptic.
- **Undo (decided)**: available on the summary until it is closed (no time limit while it is open). Undo
  asks for confirmation (`S37-undo`) because it reaches every member; it restores the 12 items to Conflict
  exactly, removes the resolutions and sends no second notification (the Activity entry is updated to
  "Mert resolved 12 conflicts, then undid it"). After leaving the summary, single final decisions can still
  be changed in S28 Results or by re-resolving in S36.
- **Partial failure** (`S37-error`): successfully saved items stay resolved; the alert offers "Try again"
  for the rest, which retries only the failed items. Primary becomes "Review 6 open conflicts" (3 failed +
  3 undecided).
- **Nothing to resolve** (`S37-nothing`): no request is sent; primary goes to the remaining conflicts.
- **Offline (decided: blocked)** (`S37-offline`): Resolve all needs a connection because it must use
  everyone's latest decisions and is a large change for all members; the primary is disabled with the reason
  at the top of the sheet and "Resolve one by one" replaces Cancel. One-by-one resolutions work offline and
  sync later (S36).
- **Majority decides with ties**: Resolve all applies to the open ties only (same sheet, "Resolve 1 tie with
  your decision?"). **Everyone must agree**: no Resolve all anywhere (`S37-not-allowed` if reached).
- Back / scrim tap on the sheet = Cancel. On the summary, back = Done.
- Reduced motion: sheet and summary fade (150 ms); no spinner rotation (static `loader-circle` + text).

## 6. Copy

| Element | String |
| --- | --- |
| Entry | App bar "Resolve conflicts" / "Wedding guests, Round 1"; "15 conflicts need your decision" / "You're the Decision Maker, so you choose the final decision when members disagree."; "Your earlier decisions on these items"; "Reject", "Maybe", "Accept", "Not decided" with counts; "Resolve one by one" / "See every member's decision and notes, then choose the final decision for each item."; "Resolve all with my decisions" / "Your decision from sorting becomes final on the 12 items you decided. 3 stay open."; "Either way, you can change a final decision later in Results." |
| Confirm | "Resolve 12 conflicts with your decisions?" / "15 conflicts are open. You decided 12 of them while sorting; your decision becomes the final decision. Members see "Resolved by Mert"." / "12 will be resolved" / "3 stay open" — "You haven't decided these items. Decide them one by one afterwards." / badge "Not decided" / "Resolve 12 conflicts", "Cancel" |
| Confirm (1 conflict) | "Resolve 1 conflict with your decision?" / "Resolve 1 conflict" |
| Resolving | Button "Resolving…" only (screen reader status "Resolving 12 conflicts") |
| Summary | "Resolved 12 conflicts" / "Your decisions are now final. Deniz and Selin are notified." / "3 still open" / "Review 3 open conflicts", "Export", "Done"; app bar "Undo", close label "Close" |
| Summary, nothing left open | "Resolved 15 conflicts" / "Every conflict in Round 1 has a final decision. Deniz and Selin are notified." / "Export" (primary), "Done" |
| Nothing to resolve | "Nothing to resolve with your decisions" / "You haven't decided any of the 3 open conflicts, so there's no decision of yours to apply. Decide them one by one." / "Review 3 open conflicts", "Cancel" |
| Partial failure | "Resolved 9 of 12 conflicts" / "Deniz and Selin are notified." / section "Also open: 3 you haven't decided" / "3 conflicts couldn't be resolved" — "The connection dropped while saving. Your decisions on them are safe. Try again to resolve them." / "Try again" / "Review 6 open conflicts" |
| Undo dialog | "Undo Resolve all?" / "The 12 conflicts open again with every member's decision as it was. Deniz and Selin are notified." / "Cancel", "Undo Resolve all" (destructive: it discards 12 final decisions, A-112) |
| Undone snackbar | "Undid Resolve all. 12 conflicts are open again." |
| Offline | Banner "You're offline. Resolutions are saved on this phone. Resolve all needs a connection." (S40 pattern); "Resolve all needs a connection" — "It uses everyone's latest decisions, so it can't run offline. You can still resolve conflicts one by one; they sync later."; "Resolve 12 conflicts" (disabled), "Resolve one by one" |
| Not allowed | "Only Mert can resolve all conflicts" / "Mert is the Decision Maker. You can review the conflicts and change your own decisions." / "Review conflicts", "Back to list". Rule Everyone must agree: "Resolve all isn't used with Everyone must agree" / "Conflicts close when members change their decisions to match." |
| Failure (nothing saved) | Snackbar "Couldn't resolve the conflicts. Check your connection and try again." + "Try again" |
| Activity / push | "Mert resolved 12 conflicts. 3 are still open." |

## 7. Accessibility

- Sheet: `role="dialog"`, labelled by its title; focus moves to the title; order: title, consequence,
  "12 will be resolved" group (read as "Reject, 6. Maybe, 0. Accept, 6."), "3 stay open" list (each row
  "Gülşen Aydın, Family, Ankara, not decided"), primary, Cancel.
- Resolving: primary `aria-busy="true"`, status "Resolving 12 conflicts" announced; completion announces
  "Resolved 12 conflicts. 3 still open."
- Summary heading is the first focus; Undo is reachable as the second element.
- Large text (`S37-large-text`, `S37-summary-large-text`): every style reaches the 200% scale: titles `text-display`, body, item names and decision labels `text-title-2`, counts `text-title-1`, group and section labels `text-title-2` with 24 icons, badges `text-title-3` (40 high), buttons `text-title-2` at least 64 high; decision rows have 12 dp between the icon circles; subtitles of open items hide (name + badge remain); the sheet body scrolls while actions stay pinned.
- Color never alone: every count carries icon + label; "Not decided" badge has the dashed-circle icon.
- Touch targets ≥ 48 (primary 56).

## 8. iOS and web differences

- **iOS** (`S37-ios`): confirmation is a page sheet starting below the host's progress row, with grabber, "Cancel" in the sheet bar, title "Resolve
  all" in the bar, the question as a large heading, primary at the bottom. The summary is the same screen
  (pushed modally, swipe-down disabled while resolving). Undo confirmation uses a native alert.
- **Web**: same as Android (sheet over S36 in the centered phone column on desktop; Escape = Cancel, Enter on
  the primary). Flow 3 runs here on desktop: `S36-default` → `S37-confirm` → `S37-summary` → `S39-shared`.

## 9. Edge cases

- **The Decision Maker decided all conflicting items**: no "stay open" group; primary "Resolve 15 conflicts".
- **Only Maybe decisions**: the split shows Maybe only; resolving with Maybe is still final ("Maybe" final
  items stay in the Maybe pile for the next round).
- **Many open conflicts (100+)**: the open list shows the first 5 and "Show all 37" (expands in place).
- **A member decides an item during resolving**: the server resolves against the state at confirmation; the
  item is resolved anyway (Decision Maker decides is final).
- **Decision Maker role moved while the sheet is open**: the sheet closes with "Deniz made Selin the Decision
  Maker. You can no longer resolve conflicts."
- **Undo after members already changed their own decisions**: the undo restores the conflict state using
  the current member decisions; items that now agree become Agreed instead of Conflict.
- **Offline**: blocked (see §5); queued bulk actions are deliberately not supported (D-05: Bulk resolve stays
  online). One-by-one resolutions made offline instead can come back as sync outcomes: dropped because members
  agreed first (`S40-outcome-already-agreed`) or rejected because the role moved (`S40-outcome-dm-role-lost`);
  S40 §4.4a.
