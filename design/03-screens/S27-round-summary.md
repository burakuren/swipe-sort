# S27 Round summary

Frames: `S27-round-summary.html` (generator: `tools/generators/S27-round-summary.py`). Previous screen:
`S25-sorting.html`. Data: `rounds` r-w1, r-d1, r-d2; `productDecisions`; `shared.summary`; `members`.

## 1. Purpose and requirements

Close a round with a calm moment of completion: show what I decided, what happened to the list (shared),
and offer the next step: review results, re-sort Maybe, start a new round, export.

Covers: SRT-16, SRT-09 (final counts), DM-01, DM-02, DM-13, DM-14, DM-15, DM-20, RND-01 (re-sort Maybe
entry), RES-01 (entry), EXP-01–EXP-04 (entry), COL-07 (others' progress), COL-14 (entry to conflicts), ACC-02
(not-backed-up indicator), GOAL-01, GOAL-02, PLT-01–PLT-04, PLT-13–PLT-17, PLT-21, PLT-23, VIS-03, VIS-09,
VIS-12, SUC-07, SCR-27.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S25 | 500 ms after the last decision of the round (replaces S25, success haptic) |
| S25 | menu "End round" → S40 end-round dialog → confirm (`S27-ended-early`) |
| S25 | "See summary" on a round with nothing left (`S25-nothing-left`) |
| S30 round history | tapping the latest round shows S28 filtered, not S27 (S27 is only shown at the end of a round) |

| To | Action | data-action |
| --- | --- | --- |
| `S28-results.html#S28-default` (solo) / `#S28-shared` | "Review results" | `review-results` |
| `S24-start-round.html#S24-maybe` | "Re-sort Maybe (14)" | `resort-maybe` |
| `S24-start-round.html#S24-default` | "Start a new round" | `new-round` |
| `S39-export.html#S39-default` / `#S39-shared` | "Export" | `export` |
| `S36-conflicts.html#S36-default` | The conflicts row ("15 conflicts", Mert resolves them); a Decision Maker finishing sees "Review 15 conflicts" as the primary | `review-conflicts` |
| `S25-sorting.html#S25-default` | "Continue Round 1" (ended early) | `continue-round` |
| `S05-sign-in-prompt.html#S05-backup` | "Back up" (guest lists) | `back-up` |
| `S09-list-overview.html#S09-default` (solo) / `#S09-shared` / `#S09-solo-round-done` | "Done", close `x`, Android back, iOS "Done" | `done`, `close` |

Prototype flows: Flow 1 ends at `S27-first-round` (85 imported contacts); Flow 2 `S27-desk-round-2` [`review-results`] → `S28-default`.
Flow 3 no longer passes through S27 (Mert stops at 85 / 100 and goes to S09-shared-decision-maker → S36).

## 3. Layout and components

Full-screen modal (it takes over the S25 modal; no bottom navigation). Single-purpose moment, so the top
part is centered (design-principles §6); actions are left-aligned rows.

1. **AppBar**: close IconButton only (`x`, "Close summary"). iOS: "Done" in the navigation bar.
2. **Hero**: `flag` in a 48 `primary-soft` circle (solo only; shared variants drop it to make room), title
   `text-title-1` ("Round 1 complete", "Round 1 ended", shared "Your Round 1 is done"), list name
   (`text-body muted`), "100 / 100 decided in 38 min" (`text-body-sm muted tabular-nums`). Duration is
   active sorting time across sessions (gaps over 5 minutes are not counted); hidden on shared lists.
3. **Counts**: three columns in the decision order Reject, Maybe, Accept: decision icon in a 40 soft circle,
   the number in `text-display tabular-nums`, the state label ("Rejected", "Maybe", "Accepted") in
   `text-label muted`. Under them a 8-high split bar (`bg-reject | bg-maybe | bg-accept`, 2 dp gaps,
   max 320 wide); undecided items leave the `muted` track visible. These are the only big numbers in the
   app (design-principles §15.9 exception: they inform the next decision).
4. Optional blocks, in this order:
   - **Not decided** notice (ended early): neutral Alert with `circle-dashed`, count, explanation and
     "Continue Round 1" (`play`).
   - **List totals after N rounds** (solo, from Round 2 on): split bar + DecisionBadges with counts across
     the list (latest decision per item, A-33).
   - **List status** (shared): segmented bar (agreed `foreground`, conflict `foreground/50`, pending
     `muted` track; same mapping as S09-shared) + a legend: one row per status with a swatch matching its
     segment, the status icon, label, description and count (Agreed 32, Conflict 15, Pending 53).
   - **Still sorting** (shared): MemberRows like S34 (Avatar 32, name, role line with icon, progress bar, "85 / 100").
5. **Next** (section header): ListGroup of action rows (icon 20, title, description, chevron). Solo:
   Re-sort Maybe (n) with the Maybe icon in `maybe-soft-foreground`, Start a new round (`list-restart`),
   Export (`file-down`). Shared Owner (`S27-shared`): conflicts row, Re-sort Maybe, Start a new round (both
   "Ends Round 1 for everyone" while others sort), Export. Shared Decision Maker / Collaborator (spec only, no
   frame): Review results, Export, and the line "Deniz, the Owner, starts new rounds."
6. **Bottom bar** (pinned, `border-t`): optional backup line for guest lists (`cloud-off` "Saved on this
   phone only" + "Back up"), the primary Button ("Review results", or "Review 15 conflicts" with
   `git-compare-arrows` for the Decision Maker when conflicts exist), ghost "Done".

Components: AppBar, DecisionBadge, StatusBadge, Progress (split and status variants), ListGroup + rows,
MemberRow, Alert, BackupIndicator, Button, OfflineBanner, Skeleton, Kbd.

## 4. States

| Frame | What it shows | Trigger |
| --- | --- | --- |
| `S27-default` | Wedding guests, solo, Round 1 complete on the full 100-item list: 100 / 100 in 38 min; 24 rejected, 14 maybe, 62 accepted; Re-sort Maybe (14), Start a new round, Export; backup line | Last decision of Round 1 on the full list (a later moment than flow 1) |
| `S27-first-round` | First round ever, end of flow 1: Wedding guests with the 85 imported contacts, not signed in: 85 / 85 in 31 min; 20 rejected, 12 maybe, 53 accepted; Re-sort Maybe (12), Start a new round, Export; backup line | First round after the first import (Flow 1) |
| `S27-count-up` | Entrance mid-animation: 10 / 6 / 27 at 250 of 500 ms (the accessible label always carries the final 20 / 12 / 53; reduced motion: final numbers at once) | Every round completion |
| `S27-desk-round-2` | Desk setup Round 2 (Maybe pile, 6 items, 2 min): 2 rejected, 1 maybe, 3 accepted; List totals after 2 rounds: 11 rejected, 1 maybe, 8 accepted | Re-sorted Maybe pile finished (Flow 2) |
| `S27-no-maybe` | Frontend hiring, Q4: 8 / 0 / 4; Re-sort Maybe disabled with "Nothing in Maybe this round" | Maybe count 0 |
| `S27-ended-early` | "Round 1 ended", 88 / 100; "12 items not decided" + Continue Round 1 | End round before finishing |
| `S27-shared` | Deniz (Owner, me) finished: 18 rejected, 15 maybe, 67 accepted (her open items c077–c100 decided like Mert where he decided, else Accept; computed in the generator from sample-data.json); list status recomputed: 32 agreed, 15 conflicts, 53 pending; Mert 85 / 100 and Selin 43 / 100 still sorting; conflicts row (Mert resolves), Re-sort Maybe (15) and Start a new round ("Ends Round 1 for everyone"), Export; primary "Review results" | Owner finishes on a shared list |
| `S27-shared-loading` | Status legend and member progress skeletons; Review results stays available | List status not yet fetched |
| `S27-offline` | Offline banner "You're offline. Decisions are saved on this phone.", status "As of 12 min ago" | Finished offline |
| `S27-large-text` | 200%: counts as labeled rows, left-aligned title | Font scale ≥ 150% |
| `S27-ios` | "Done" in the navigation bar, no ghost Done | iOS |
| `S27-web-desktop` | Deniz's shared summary in the desktop column, keyboard hints (Enter Review results, Esc Done) | Desktop browser |

There is no error state: the summary is computed from local data. If the list status cannot be fetched, the
offline variant is shown.

## 5. Interactions and transitions

- **Entrance** (the one orchestrated moment, motion.md §3 "Round summary"): S25 fades out (150 ms) as S27
  fades and rises 16 dp (500 ms, emphasized decelerate); the success haptic
  (`notificationAsync(Success)`) fires once; the three counts tick from 0 to their values over 500 ms
  (standard decelerate), together; the split bar grows with them. Nothing else animates, nothing loops, no
  confetti. Shown the same way for every round; reduced motion: final numbers and bar at once, 150 ms fade
  (looks like `S27-default`).
- **Re-sort Maybe** opens S24 with the Maybe pile and Shuffled preselected. **Start a new round** opens S24
  with defaults. On a shared list with others still sorting, the Owner's choices go through the end-round
  dialog in S24.
- **Review results / Review conflicts / Export** push their screens; back from them returns to S09 (S27 is
  not kept in the stack: it is a one-time moment). **Done** and close return to S09.
- **Continue Round 1** (ended early) reopens the round and S25 starts at the first undecided item; possible
  until a new round starts.
- **Shared**: list status and member progress update live while the screen is open (sync events), without
  animation beyond the progress bar width (250 ms).
- Desktop web: Enter triggers the primary action, Esc = Done.

## 6. Copy

| Element | String |
| --- | --- |
| Close label | "Close summary" |
| Titles | "Round 1 complete"; "Round 2 complete"; "Round 1 ended"; shared "Your Round 1 is done" |
| Progress line | "100 / 100 decided in 38 min"; "6 / 6 decided in 2 min"; under a minute "in less than a minute"; over an hour "in 1 h 12 min"; ended early "88 / 100 decided"; shared "100 / 100 decided" |
| Count labels | "Rejected", "Maybe", "Accepted" |
| List totals | "List totals after 2 rounds"; badges "11 rejected", "1 maybe", "8 accepted" |
| Not decided | "12 items not decided" (1: "1 item not decided") / "They aren't in any pile. Continue Round 1 to decide them, or include them in a new round." / "Continue Round 1" |
| List status | "List status"; "All 3 members"; legend "Agreed" / "Everyone chose the same", "Conflict" / "Members chose differently", "Pending" / "Not everyone has decided" with counts; offline "As of 12 min ago" |
| Still sorting | "Still sorting"; name on the first line ("Mert", "Selin"), role on its own line with its icon as in S34 ("Decision Maker" with `gavel`, "Collaborator" with `user`); "85 / 100", "43 / 100" |
| Section | "Next" |
| Rows | "Re-sort Maybe (14)" / "Sort the 14 Maybe items again in a new round" (1: "Sort the 1 Maybe item again in a new round"); disabled "Re-sort Maybe" / "Nothing in Maybe this round"; "Start a new round" / "Choose items and card order"; shared Owner "Ends Round 1 for everyone"; "Export" / "CSV, Excel, Google Sheets or a text summary"; "Review results" / "Final decisions and my decisions"; Owner conflicts row "15 conflicts" / "Mert resolves them as Decision Maker" (Everyone must agree: "Members change their decisions until they match"; Majority: "The majority decides when everyone has sorted") |
| Shared note | "Deniz, the Owner, starts new rounds." |
| Buttons | "Review results"; "Review 15 conflicts" (no conflicts: "Review results"); "Done" |
| Backup line (guest) | "Saved on this phone only" + "Back up" |
| Offline banner | "You're offline. Decisions are saved on this phone." (S40 wording) |
| Loading | Screen reader "Loading list status" |
| Keyboard hints | "Enter Review conflicts" / "Enter Review results", "Esc Done" |
| Screen reader on entry | "Round 1 complete. 24 rejected, 14 maybe, 62 accepted." (shared: "Your Round 1 is done. My decisions: 18 rejected, 15 maybe, 67 accepted. 15 conflicts.") |
| Activity (S38) | Others see "Deniz finished sorting" (COL-18) |

## 7. Accessibility

- On entry focus goes to the title; the announcement in §6 is made once (the count-up is not announced; the
  counts block is one `img` with a text label).
- Focus order: Close, title, counts, notices, list status, still sorting, action rows, primary, Done.
- Decision counts always show icon + label + number; the split bar is decorative (`aria-hidden`) because the
  numbers carry the same information. List status bar is an `img` with "32 agreed, 15 in conflict, 53
  pending".
- Disabled Re-sort Maybe row is `aria-disabled` with its reason readable at full contrast.
- Member progress bars are `progressbar` with "Deniz: 76 of 100 decided".
- Large text (`S27-large-text`): title left-aligned at 40, counts become a ListGroup of rows (icon 48, label,
  number), actions keep one per row and wrap, the primary button grows to 64; the content scrolls with the
  primary pinned.
- Reduced motion: no count-up, no rise; 150 ms fade.
- Touch targets ≥ 48 (rows 64, buttons 48).

## 8. iOS and web differences

- **iOS** (`S27-ios`): "Done" (bold, trailing) in the navigation bar replaces both the `x` and the ghost Done;
  primary button uses the iOS capsule shape; swipe-down to dismiss is off (the summary is the end of the
  modal flow; Done is explicit). Success haptic via Taptic Engine.
- **Android**: system back = Done.
- **Web, mobile**: Android layout without system bars; no haptics.
- **Web, desktop** (`S27-web-desktop`): centered column with keyboard hints (Enter, Esc); shows Deniz
  finishing her round in the browser.
- Export on web: Google Sheets and file download work; "share a plain-text summary" copies to the clipboard
  instead of the system share sheet (S39 owns the details).

## 9. Edge cases

- **Very small rounds** (1 item): counts still show three columns with zeros; the bar shows one segment.
- **All one decision** (e.g. every item rejected): the bar is one color; Re-sort Maybe is disabled with the
  reason.
- **Large numbers** (5,000+ items): numbers use thousands separators and shrink to `text-title-1` when any
  count has 5+ digits, so three columns always fit at 412 dp and at +40% label length.
- **Long list names** wrap to two lines in the hero.
- **Shared, no conflicts**: primary is "Review results" for everyone; the conflicts row is hidden.
- **Shared, everyone finished**: "Still sorting" is replaced by "Everyone has sorted Round 1" with the
  member AvatarStack; Owner rows lose the "Ends Round 1 for everyone" descriptions.
- **Decision Maker** (Mert, when he finishes): primary "Review 15 conflicts" (`git-compare-arrows`) → S36;
  rows Review results and Export; the line "Deniz, the Owner, starts new rounds."; no round actions.
- **Collaborator** (Selin): like the Decision Maker variant with "Review results" as primary (no conflict
  resolution role) and a conflicts row describing who resolves them.
- **Round ended by the Owner while I was sorting** (shared): S25 shows the "Deniz ended Round 1" sheet;
  "See summary" opens `S27-ended-early` with "Deniz ended Round 1" as the title, and no Continue action
  (only the Owner can reopen).
- **Offline**: my counts are local and exact; list status shows the last known values with "As of …".
- **Guest lists**: the backup line appears on every summary until the user signs in (ACC-02).
