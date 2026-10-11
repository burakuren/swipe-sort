# S25 Sorting screen

Frames: `S25-sorting.html`. Live interaction: `04-prototype/swipe-demo.html`. Motion: `01-foundations/motion.md`.

## 1. Purpose and requirements

The heart of the product: decide one item at a time with gestures or buttons, fast, calm and safe.

Covers: SRT-01–SRT-17, VIS-01–VIS-07 (no decorative gradients anywhere on the screen), DM-01, DM-02, DM-13, DM-16, DM-18, DM-19, PLT-05, PLT-06, PLT-09, PLT-14–PLT-19,
PLT-21, PLT-23, VIS-03, VIS-05, VIS-08–VIS-10, GOAL-01, GOAL-02, SAFE-03, COL-16, SUC-06, SUC-07, SUC-08,
SCR-25.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S22 import finish (pick mode) | "Start sorting" (first sort shows coach marks) |
| S09 list overview | "Continue sorting" / "Start sorting" |
| S24 start a round | "Start round" |
| S08 home | resume chip on a list in progress |
| S33 join a list | "Start sorting" (member sorts every item of the current round, DM-16) |
| Notification "New round started" | deep link `/l/<id>/sort` |

| To | How |
| --- | --- |
| S26 item detail | tap the card, menu "Open item details", or Enter on web (bottom sheet over S25) |
| Note sheet (in S25) | Note button, N on web, card action "Add note" |
| S27 round summary | after the last decision (replaces S25) or "End round" |
| S09 list overview | close (`x`); progress is already saved, no confirmation |
| S22 template library (change mode) | menu "Card template" |
| S40 end-round dialog | menu "End round" |
| S36 conflicts | snackbar "View" after a new conflict (shared lists) |
| S27 `S27-ended-early` | "See summary" in the "Deniz ended Round 1" sheet (`S25-round-ended`) |
| S26 `S26-edit-replaced` | "View" in the S40 edit-replaced snackbar (D-09 row 1) |
| S08 Home | the list left this device (`S40-outcome-device-only-elsewhere`) or the member was removed (`S40-not-found-removed` first) |

## 3. Layout and components

Full-screen modal, no bottom navigation. Top to bottom:

1. **AppBar (sorting)**: close IconButton (`x`), list name (`text-title-3`, truncates) with round name below
   (`text-caption`, "Round 1" or "Round 1, shared"), overflow IconButton.
2. **Progress**: "76 / 100 decided" (`text-label tabular-nums`) + Progress bar (`h-1.5`). Trailing slot:
   member AvatarStack (shared), offline/sync status.
3. **CardStack**: fills the remaining height. Top SwipeCard (`inset-x-gutter`, 20 from the bottom of the
   area, `rounded-hero`, `shadow-hero`) and the next card behind (same size, `scale 0.95`, `translateY 40`,
   origin top, hairline border, `shadow-raised`) so 12 dp of the next card peek below the top card.
4. **DecisionBar**: UndoButton (48), DecisionButton Reject, Maybe, Accept (64, with label and running
   count), Note button (48). Order is fixed: left, up, right.
5. Overlays: DecisionStamp + tint on the card while dragging, Snackbar 128 above the bottom, note BottomSheet,
   DropdownMenu, CoachMark.

Card content follows the list's card template (components.md › SwipeCard). Frames show Person (wedding
list), Product (Desk setup), Photo (Trip ideas: image link, Place, Country, Best time, Budget; D-32, A-130,
A-131) and the custom "Candidate, compact" template.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S25-default` | Sorting a solo list (guest or signed in). Mia Andersson (c077), 76 / 100, counts 17 / 11 / 48 |
| `S25-drag-accept-start` | Dragging right below the threshold: small tilt, faint tint, stamp fading in, Accept button ring |
| `S25-drag-accept`, `-reject`, `-maybe` | Past the threshold (armed): full stamp, tint 24%, button solid, next card promoting |
| `S25-commit` | Released: card exits, next card (c078) is on top, progress 77, Accept count ticks to 49 |
| `S25-undo` | Undo pressed: card returns, snackbar "Undid Accept on Mia Andersson" |
| `S25-coach-1…4` | First sort ever (per account or device), here the 85 contacts just imported (0 / 85). Each step demonstrates one gesture |
| `S25-note`, `S25-note-saved` | Note button → sheet; saved note shows on the card with a `sticky-note` line |
| `S25-menu` | Overflow menu on a solo list |
| `S25-shared` | Shared list, others' decisions hidden (default, SRT-12) |
| `S25-shared-others` | "Show others' decisions" on: a small panel top-right of the card lists each other member with avatar, name and decision badge (icon + word) |
| `S25-shared-menu` | Shared list menu with the switch |
| `S25-shared-conflict` | After my decision differs from someone's: snackbar reveals the conflict, "View" opens S36 |
| `S25-product`, `S25-photo`, `S25-candidate` | Other templates (any kind of list). `S25-photo`: Trip ideas, Round 1 at 12 / 30 (6 / 1 / 5), card tr13 "Alfama, Lisbon", next card tr14 "Göreme, Cappadocia"; the same card as `S40-end-round` |
| `S25-round-ended` | Shared, Selin was sorting Round 1 offline while Deniz started Round 2; at sync the "Deniz ended Round 1" sheet adds "Your 8 decisions from Round 1 were saved." (D-09 row 2); "See summary" → `S27-ended-early` |
| `S25-long-text` | Name clamps to 3 lines; missing phone omitted; note preview |
| `S25-no-photo` | 96 initials avatar instead of an image block |
| `S25-edited` | Edited field marker (city changed, SAFE-03) |
| `S25-loading` | Opening a large list: skeleton card, buttons disabled |
| `S25-offline` | No connection: banner + "4 not synced"; sorting continues (SRT-14) |
| `S25-syncing` | Connection back: "Syncing 4 decisions…" then disappears |
| `S25-error` | Local data could not be read |
| `S25-last-card` | 99 / 100: no next card behind; deciding it opens S27 |
| `S25-resume` | Shown only when the round changed elsewhere while away (e.g. decided on web); otherwise S25 opens directly at the next undecided item |
| `S25-nothing-left` | Opening a round where every item is decided |
| `S25-large-text` | 200% font scale: image hidden, 2 rows max, buttons become a labeled grid, Note moves to the menu |
| `S25-reduced-motion` | Reduced motion: drag without tilt; commit cross-fades |
| `S25-screen-reader` | Annotation of the card's accessibility actions |
| `S25-ios`, `S25-ios-note` | iOS variants |
| `S25-web`, `S25-web-desktop` | Web mobile; desktop with keyboard hints |

## 5. Interactions, gestures and transitions

All values in `motion.md §2`. Summary:

- **Drag** (any direction except down): card follows the finger; rotation `dx / W × 12°` around the bottom
  center; tint `bg-{decision}` up to 18% (24% armed); stamp fades in from 15% to 60% progress; matching
  DecisionButton rings, then fills when armed; next card promotes with progress.
- **Thresholds**: horizontal `max(0.30 × W, 96)` ≈ 112 dp; up `max(0.18 × H, 96)` ≈ 100 dp; up wins when
  `-dy > 1.2 × |dx|`. Fling: ≥ 900 dp/s and ≥ 32 dp in the direction commits early.
- **Release below threshold**: spring back (damping 18, stiffness 220), tint and stamp fade.
- **Commit**: medium haptic, card exits in 160–260 ms (emphasized accelerate), next card springs to top,
  count ticks, progress advances, screen-reader announcement. Decision saved locally immediately.
- **Buttons** run the same commit (24 dp nudge with full stamp, then 240 ms exit). A tap during an exit is
  queued for the next card.
- **Undo**: last card returns along its exit path (300 ms, emphasized decelerate); unlimited steps back
  through this round's history; disabled with nothing to undo.
- **Tap** (< 8 dp movement, < 250 ms): opens S26 as a bottom sheet over the stack.
- **Note**: opens the note sheet; keyboard pushes the sheet up; Save note closes it and shows "Note saved".
  On shared lists the sheet has the "Only visible to me" switch (private notes, DM-19); on solo lists the
  switch is hidden.
- **Close**: returns to S09 immediately. Progress, undo history and the current position persist (SRT-13).
- **Last decision**: 500 ms after the last commit, S27 replaces S25 with the round-complete transition
  (success haptic).
- **Coach marks**: 4 steps; the card demonstrates each gesture (loops twice, then waits); Skip ends; "Start
  sorting" on the last step. Replay from the menu.
- **Shared lists**: decisions are independent; others' decisions hidden unless the member switches them on
  (per member, per list, remembered). After deciding, if the item became a conflict, a snackbar says so.
- **Offline**: everything works; the progress row shows unsynced count; sync is automatic.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "{List name}"; "Round 1"; shared: "Round 1, shared" |
| Close / menu labels | "Close sorting"; "More options" |
| Progress | "76 / 100 decided" |
| Buttons | "Undo", "Reject", "Maybe", "Accept", "Note" (counts follow the label) |
| Stamps | "Accept", "Reject", "Maybe" |
| Menu | "Show others' decisions" (shared), "Card template", "Show the tutorial again", "Open item details", "End round" ("End round" only for the Owner on shared lists) |
| Coach 1 | "Swipe right to accept" / "Or tap the check button below the card." |
| Coach 2 | "Swipe left to reject" / "Or tap the cross button." |
| Coach 3 | "Swipe up for maybe" / "Not sure yet? Maybe items wait in their own pile, so you can sort them again later." |
| Coach 4 | "Tap the card for details" / "Undo is always one tap away. Your progress saves as you go." |
| Coach buttons | "Skip", "Next", "Start sorting" |
| Note sheet | "Note on {title}"; field label "Note"; counter "62 / 1,000"; "Only visible to me" (shared); "Save note" |
| Snackbars | "Undid {Decision} on {title}"; "Note saved"; "Mert chose Maybe on Mia Andersson. This is now a conflict." + "View" |
| Offline | "You're offline. Decisions are saved on this phone."; "4 not synced" |
| Syncing | "Syncing 4 decisions…" |
| Loading | (skeleton; screen reader: "Loading cards") |
| Error | "This list couldn't be opened" / "Your decisions are safe. Close the list and open it again. If it keeps happening, restart SwipeSort." / "Try again" / "Back to list" |
| Resume | "Pick up where you left off" / "76 of 100 decided. 24 items left in Round 1." / "Continue sorting" |
| Nothing left | "Every item is decided" / "Round 1 is complete. See the summary or change any decision in Results." / "See summary" |
| Round ended (shared) | "Deniz ended Round 1" / "See summary"; after sorting offline: body "Deniz started Round 2 while you were offline. Your 8 decisions from Round 1 were saved." (1 decision: "Your 1 decision from Round 1 was saved.") |
| Large text | "1 more field in details" |
| Keyboard hints (web desktop) | "← Reject", "↑ Maybe", "→ Accept", "Z Undo", "N Note" |
| Screen reader after action | "Accepted Mia Andersson. 77 of 100 decided." |
| Card hint | "Swipe right to accept, left to reject, up for maybe, or use the buttons." |

## 7. Accessibility

- Focus order: Close, list title, More options, progress, card, Undo, Reject, Maybe, Accept, Note.
- The card is one focusable element (`role` group/card) with label = title, subtitle and visible fields,
  plus custom actions **Accept, Reject, Maybe, Undo, Add note, Open details** (TalkBack actions menu,
  VoiceOver rotor). Gestures are never required.
- Decision buttons are labeled with their count: "Accept, 48 accepted". Undo names what it undoes.
- Announcements (polite): result + progress after each decision; undo result.
- Large text: at ≥ 150% the image area hides; at 200% the decision bar becomes a 3-column grid of labeled
  buttons with Undo full-width below; Note moves into the menu.
- Reduced motion: no tilt/fly-out; tint and stamp still show while dragging; commit = 150 ms cross-fade.
- Color never alone: stamps and buttons have icon + label; others' decisions have icons in the dots and a
  full text label.
- Touch targets ≥ 48 (decision buttons 64).

## 8. iOS and web differences

- **iOS** (`S25-ios`): 44 pt bar with centered title; the modal disables swipe-down-to-dismiss while
  sorting (the up-swipe would conflict); notes open as an iOS page sheet with Cancel / Save
  (`S25-ios-note`); overflow menu is a UIMenu; haptics via Taptic Engine (same mapping).
- **Web, mobile** (`S25-web`): same layout without system bars; no haptics (silently ignored); browser back =
  close.
- **Web, desktop** (`S25-web-desktop`, Mert at 85 / 100 in flow 3): phone layout centered; in the prototype the decision buttons open the live demo with Mert's undecided items, and Close returns to `S09-shared-decision-maker`; keyboard hints under the decision bar (web
  only); arrow keys and Z work; Enter opens details, N opens the note; mouse drag works like touch.

## 9. Edge cases

- **Long text**: title clamps to 3 lines, rows to 1 line with ellipsis; full values in S26.
- **Missing values**: rows omitted; no photo → initials avatar; product without rating → "No rating".
- **Multi-value fields**: first value + "+1".
- **Edited values**: `pencil-line` marker after the value.
- **Very large lists** (5,000+ items): only the top 3 cards are rendered; progress bar stays smooth;
  "1,204 / 5,000 decided" uses thousands separators.
- **Rapid sorting**: taps during an exit are queued; keyboard repeat is ignored.
- **Offline for long**: unsynced count grows; nothing blocks; conflicts are computed after sync and
  announced in Activity.
- **Item edited or removed by another member mid-sort**: the card updates in place; if removed, it is skipped
  with a snackbar "Mehmet Yılmaz was removed from the list".
- **Joined mid-round** (shared): the member starts at the first item of the current round (DM-16).
- **Round ended by the Owner while sorting** (shared): sheet "Deniz ended Round 1" with "See summary".
  When the member sorted offline and the news arrives with the sync (D-09 row 2: late Round 1 decisions are
  accepted into Round 1), the sheet's body reads "Deniz started Round 2 while you were offline. Your 8 decisions
  from Round 1 were saved." (`S25-round-ended`). This replaces the S40 snackbar `S40-outcome-late-round`, which
  shows on Home or S09 when the person isn't sorting that list.
- **Field edit replaced while sorting** (shared, D-09 row 1): the card updates in place to the later value; the
  S40 snackbar `S40-outcome-edit-replaced` ("Mert changed City on Alper Turan after you, so your edit was
  replaced." + View) shows above the decision bar (`bottom-32`); View opens S26 `S26-edit-replaced`.
- **List leaves this device while it is being sorted**: if the list's backup was turned off on another device
  of the same account (D-33, A-134), sorting closes to Home with the S40 snackbar
  `S40-outcome-device-only-elsewhere` ("You kept “Trip ideas” on another device only. It's no longer on this
  one."); decisions made here that hadn't synced yet are dropped with it (D-09 row 7: writes to deleted data
  are dropped). If the member was removed from a shared list
  (D-09 row 4), the screen switches to `S40-not-found-removed` with the line about unsaved decisions, then Home.
