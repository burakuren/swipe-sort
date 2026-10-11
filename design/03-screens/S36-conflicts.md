# S36 Conflicts: one-by-one resolution

Frames: `S36-conflicts.html`. Generator: `tools/generators/S35-S38-collaboration.py` (decisions and notes come
from `02-data/sample-data.json › shared`). Motion: `01-foundations/motion.md` (same gesture values as S25).
Related: S25 (sorting, quality reference), S26 (item detail), S35 (rule), S37 (bulk resolve), S28 (results).

## 1. Purpose and requirements

Go through the open conflicts of the current round one at a time, with every member's decision and the
notes on the card. Under **Decision Maker decides** (and for ties under **Majority decides**) the Decision
Maker sets the **final decision** with the same swipe and buttons as sorting. Everyone else reviews the
same deck read-only for the final decision and can change their **own** decision (the way conflicts close
under **Everyone must agree**).

Covers: COL-14, COL-16, COL-15 (entry "Resolve all"), DM-02, DM-05, DM-07, DM-08, DM-09, DM-12 (items the
Decision Maker never decided), DM-18, DM-19, DM-20, A-25, A-27, GOAL-01, GOAL-03, GOAL-04, PLT-02–PLT-06,
PLT-13–PLT-19, SRT-02–SRT-05 (gesture model reused), SRT-07, SRT-14, SCR-36.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S09 `S09-shared` | "Review conflicts" (conflicts row) |
| S09 `S09-shared-decision-maker` | Mert (Decision Maker, 85 / 100 decided) taps "Review 15 conflicts" (`data-action="review-conflicts"`); prototype flow 3 |
| S27 `S27-shared` | "Review 15 conflicts" (`data-action="review-conflicts"`) |
| S25 `S25-shared-conflict` | Snackbar "View" after a new conflict (opens on that item) |
| S26 `S26-shared-conflict` | "Review conflicts" |
| S34 `S34-decision-maker` | "Review 15 conflicts" |
| S35 `S35-decision-maker` | "Review 15 conflicts" |
| S37 summary / nothing | "Review 3 open conflicts" → `S36-remaining` |
| S38 / push "New conflicts" | Deep link `https://swipesort.app/l/<listId>/conflicts` |

| To | How |
| --- | --- |
| S37 `S37-confirm` | "Resolve all" (`data-action="resolve-all"`, Decision Maker only) |
| S26 `S26-shared-conflict` | Tap the card, menu "Open item details", Enter on web |
| Note sheet (in S36) | Note button, N on web |
| S35 `S35-decision-maker` | Menu "Conflict rule" |
| S28 `S28-shared`, S39 `S39-shared` | "See results", "Export" on `S36-all-resolved` |
| S09 `S09-shared-decision-maker` (Decision Maker) / `S09-shared` (others) | Back; "Back to list" |
| S25 `S25-shared` | "Continue sorting" on `S36-empty` |

Route: `list/[listId]/conflicts` (stack screen, no bottom navigation). Query `?item=c020` opens on an item.

## 3. Layout and components

Same skeleton as S25 so the gestures feel identical:

1. **AppBar (small)**: back, "Conflicts", subtitle "Wedding guests, Round 1", IconButton view toggle
   (`list` "Show as list" / `layers` "Show as cards"), overflow (`ellipsis-vertical`).
2. **Progress**: "3 / 15 resolved" (`text-label tabular-nums`) + Progress bar. Trailing: text Button
   "Resolve all" with `gavel` (Decision Maker only, 48 high). Under other rules or for members the label
   changes: "0 / 15 resolved by Mert", "0 / 15 agreed", "0 / 7 final", "0 / 1 tie resolved".
3. **CardStack** with the **ConflictCard** (Proposed: a SwipeCard variant; `rounded-hero shadow-hero`):
   - Item header: photo band (`h-[26%]`, cover) or a 64 initials avatar; title `text-title-1` (2 lines max);
     subtitle "Family, İstanbul"; StatusBadge (Conflict, or "Waiting for 1 member", "Tie", Agreed).
   - Optional hint line (`text-body-sm muted` with icon) or neutral Alert (item the Decision Maker never
     decided).
   - **Decisions**: MemberDecisions expanded, viewer first with "(you)": Avatar 32, first name, role caption
     (Owner / Decision Maker / Collaborator), DecisionBadge ("Accepted", "Rejected", "Maybe", "Not decided",
     others "Not decided yet").
   - **Notes**: all shared notes (muted box, author avatar 20 + first name) and only the viewer's own private
     note (dashed outline, `lock` "Only you"). Others' private notes are never sent to the device. Empty:
     "No notes on this item."
   - Next card behind: surface only (`scale-95 translate-y-10`), no content.
4. **Caption** above the bar: Decision Maker "Your choice is the final decision" (`gavel`); members "Your
   decision: Accept. Mert decides the final decision." etc.
5. **DecisionBar** (same as S25, no counts): Undo 48 · Reject 64 · Maybe 64 · Accept 64 · Note 48.
   Decision Maker: buttons set the final decision. Members: the button matching **my decision** is solid
   (`aria-pressed`), tapping another changes my decision.
6. Overlays: DecisionStamp "Final: Accept" + tint while dragging, Snackbar `bottom-28` directly above the
   decision buttons (it takes the caption's place; the caption is hidden while a snackbar shows, so no text
   is half covered), note
   BottomSheet, DropdownMenu, sync sheet.

**List view** (`S36-list`): sections "Open, 12" and "Resolved, 3" as ListGroups of ItemRows: avatar 40,
name, a text line spelling out who decided what ("You accepted, Deniz rejected, Selin hasn't decided", 2 lines max), chevron; resolved rows
show "Resolved by you" / "Resolved by Mert" and the final DecisionBadge. Tapping a row opens the card deck at
that item.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S36-default` | Mert (Decision Maker), rule Decision Maker decides, first conflict c002 Mehmet Yılmaz (Deniz Accept, Mert Reject, Selin Accept), 0 / 15 resolved, Undo disabled |
| `S36-drag-accept`, `S36-drag-reject` | Dragging past the threshold: stamp "Final: Accept" / "Final: Reject", tint 24%, button armed |
| `S36-resolved` | Released on Accept: next card c012 on top with its "You haven't decided this item" notice, 1 / 15, snackbar "Resolved: Accept for Mehmet Yılmaz" + Undo |
| `S36-dm-undecided` | c012 Gülşen Aydın: Mert has no decision (one of the 3 Resolve all skips); Selin's shared note "Haven't seen her in years, maybe skip?" |
| `S36-progress` | 3 / 15 (c002 Accept, c012 Reject, c015 Reject resolved); c020 Merve Kurt, Selin not decided yet |
| `S36-note`, `S36-note-saved` | Same 3 / 15 Merve Kurt state as `S36-progress` (last resolution: Reject on Cem Tekin, "Selin hasn't decided yet" notice): note sheet with "Only visible to me" on; the private note shows dashed with "Only you" |
| `S36-menu` | Overflow: Skip for now, Open item details, Show as list, Conflict rule |
| `S36-list` | List view at 3 / 15 |
| `S36-remaining` | After Resolve all: the 3 items Mert never decided (c012, c034, c056); "Resolve all" is hidden because it would skip all of them |
| `S36-all-resolved` | Last conflict resolved |
| `S36-non-dm` | Deniz under Decision Maker decides: info "Mert decides conflicts", own decision editable |
| `S36-everyone` | Rule Everyone must agree, Deniz on c043 Sinan Karakaya (Deniz Maybe, Mert Accept, Selin Maybe) |
| `S36-everyone-drag` | Deniz drags c043 right, armed: stamp "Accept" (no "Final:"), Accept button armed, caption "Release to change your decision to Accept." |
| `S36-everyone-agreed` | Selin changes c029 Murat Ekinci from Maybe to Accept: all three Accept, Agreed chip with the final "Accepted" badge next to it, snackbar |
| `S36-majority` | Rule Majority decides, Deniz on c020 Merve Kurt: Conflict chip with the hint "Waiting for 1 member: Selin. …" below it; 7 open (8 became final) |
| `S36-majority-tie` | Same item after Selin chooses Maybe: Reject/Maybe/Accept tie goes to Mert |
| `S36-empty` | No open conflicts |
| `S36-loading` | Skeleton card, buttons disabled |
| `S36-error` | Conflicts could not be loaded |
| `S36-offline` | No connection: resolving continues locally ("2 not synced"); Resolve all disabled |
| `S36-synced` | Back online: Sophie Laurent became Agreed (Selin changed to Accept) and 2 new conflicts arrived; total 16 |
| `S36-large-text` | 200%: card shows name, status and decisions only; buttons become a labeled grid; Resolve all, Undo and Note move to the menu |
| `S36-reduced-motion` | Drag without tilt or fly-out; stamp and tint remain |
| `S36-ios` | iOS |
| `S36-web-desktop` | Desktop browser with keyboard hints |

Order of the deck: conflicts in item order (c002, c012, c015, c020, …); skipped items move to the end;
items the viewer opened from a link come first.

## 5. Interactions, gestures and transitions

All gesture values are the S25 values (motion.md §2): thresholds `max(0.30 × W, 96)` horizontal and
`max(0.18 × H, 96)` up, fling ≥ 900 dp/s and ≥ 32 dp, down-swipe never decides, snap-back spring.

- **Decision Maker, swipe or button**: right = Accept, left = Reject, up = Maybe as the **final decision**.
  The stamp reads "Final: Accept". Commit: medium haptic, card exits (160–260 ms), next card springs up,
  progress ticks, snackbar "Resolved: Accept for Mehmet Yılmaz" with Undo (6 s). The item becomes
  **Resolved** (badge "Resolved by Mert" everywhere, final decision set). Members' own decisions stay.
- **Undo** (button or snackbar): the last resolution is removed, the card returns along its exit path
  (300 ms) and the item is a Conflict again. Undo steps back through this session's resolutions in order.
- **The Decision Maker's own earlier decision** is shown in their row ("Mert (you)", "Rejected"); the final
  decision may differ from it (c002: Mert rejected while sorting, resolves with Accept). Resolving does not
  change his own decision.
- **Item the Decision Maker never decided** (`S36-dm-undecided`): resolves like any other; the alert explains
  why Resolve all skips it. Resolving does not create a personal decision for him.
- **Conflict while a member is still sorting** (`S36-progress`): the Decision Maker can resolve it now; the
  resolution is final, and the member's later decision is recorded but does not reopen it.
- **Members (any rule)**: the deck is the same, but gestures and buttons **change my decision** on this
  item (same thresholds); nothing they do is a final decision. The stamp reads "Accept" etc., snackbar "Changed your decision to Accept on Freya Nielsen" + Undo. If all decisions now
  match, the status becomes Agreed (`S36-everyone-agreed`: snackbar "Murat Ekinci is now Agreed: Accept",
  the card stays 1 s with the Agreed badge, then leaves the deck). Tapping the button that is already my
  decision does nothing. A visible "Next" is not needed: swiping down is not a decision, so members advance
  with the menu "Skip for now" or the list view; the deck also advances after a change.
- **Majority decides**: conflicts with an undecided member show "Waiting for 1 member" and the hint spells
  out what each of their choices would do. When everyone has decided, the item becomes final by majority
  ("Majority" badge) and leaves the deck. A tie appears in the Decision Maker's deck (`S36-majority-tie`);
  without a Decision Maker it stays a Conflict for everyone (S35).
- **Note**: opens the note sheet (S25 pattern) with "Only visible to me". Saved notes appear on the card.
- **Tap the card**: S26 item detail as a sheet (Decision Maker sees the who-decided list and can resolve
  from there too).
- **Skip for now** (menu): the card moves to the end of the deck (no decision).
- **Resolve all**: opens the S37 confirmation sheet over this screen.
- **View toggle**: cross-fade (150 ms) between cards and list; position is kept.
- **Live updates**: when a member changes a decision on the card being shown, the row badge updates in
  place (200 ms fade); if the item stops being a conflict, a snackbar says "Sophie Laurent is no longer a
  conflict" and the deck moves on.
- **Offline**: resolutions and decision changes are saved on the phone (`syncState: 'pending'`) and synced
  later; "Resolve all" is disabled (S37 explains). On sync the server applies resolutions in order; if an
  item became Agreed before a resolution arrived, agreement wins and the sync sheet lists it.
- **Last conflict**: 500 ms after the last commit `S36-all-resolved` fades in.
- Reduced motion: as S25 (no tilt, 150 ms cross-fade commit; stamp and tint still shown).

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Conflicts"; "Wedding guests, Round 1"; back label "Back to Wedding guests"; "Show as list" / "Show as cards"; "More options" |
| Progress | "0 / 15 resolved"; members: "0 / 15 resolved by Mert"; Everyone: "0 / 15 agreed"; Majority: "0 / 7 final"; ties: "0 / 1 tie resolved"; offline: "2 not synced" |
| Resolve all | "Resolve all" |
| Card | "Decisions"; "Notes"; "(you)"; "Owner", "Decision Maker", "Collaborator"; badges "Accepted", "Rejected", "Maybe", "Not decided", "Not decided yet"; "Only you"; "No notes on this item." |
| Status | "Conflict"; "Waiting for 1 member"; "Tie"; "Agreed"; "Resolved by Mert"; "Majority" |
| Hints | Never decided: "You haven't decided this item" / "Resolve all skips it, so decide it here. Selin left a note." (without a note: "Resolve all skips it, so decide it here."); member still sorting: "Selin hasn't decided yet. Your choice is final either way; her decision is still recorded."; Everyone: "Final only when all three match. Mert chose Accept; you and Selin chose Maybe."; Majority: "Waiting for Selin. Accept or Reject from her makes the majority final. Maybe makes it a tie, and Mert decides."; tie: "Tie: one Reject, one Maybe, one Accept. As Decision Maker, you break it." |
| Member info | "Mert decides conflicts" / "You can still change your own decision. If everyone chooses the same, the item is Agreed." |
| Captions | "Your choice is the final decision"; "Your decision: Accept. Mert decides the final decision."; "Your decision: Maybe. Change it to match the others."; "Your decision: Accept. Everyone chose the same."; "Your decision: Reject. The majority decides once everyone has."; while dragging: "Release to change your decision to Accept." |
| Buttons | "Undo", "Reject", "Maybe", "Accept", "Note" |
| Stamps | Decision Maker: "Final: Accept", "Final: Reject", "Final: Maybe"; members: "Accept", "Reject", "Maybe" |
| Menu | "Skip for now", "Open item details", "Show as list", "Conflict rule" |
| Snackbars | "Resolved: Accept for Mehmet Yılmaz" + "Undo"; "Undid resolution on Mehmet Yılmaz"; "Changed your decision to Accept on Freya Nielsen" + "Undo"; "Murat Ekinci is now Agreed: Accept"; "Sophie Laurent is no longer a conflict"; "Note saved"; "Couldn't save the resolution. It's kept on this phone and will sync later." |
| Note sheet | "Note on Merve Kurt"; "Note"; "33 / 1,000"; "Only visible to me" / "Deniz and Selin won't see this note."; "Save note" |
| List view | "Open, 12"; "Resolved, 3"; "Resolved by you" / "Resolved by Mert" |
| All resolved | "All 15 conflicts resolved" / "Each one has a final decision. New conflicts show up here as Deniz and Selin keep sorting." / "See results", "Export", "Back to list" |
| Remaining | progress "0 / 3 resolved" (rest as default) |
| Empty | "No conflicts" / "When members decide an item differently, it shows up here. 15 items in Round 1 are still waiting for your decision." (Mert, 85 / 100; Deniz sees 24) / "Continue sorting", "Back to list" (when I have decided everything: "When members decide an item differently, it shows up here." / "Back to list") |
| Loading | (skeleton) screen reader "Loading conflicts" |
| Error (S40-error treatment, `cloud-alert`) | "Conflicts couldn't be loaded" / "SwipeSort didn't respond. Check your connection and try again." / "Your resolutions are saved on this phone." / "Try again", "Back to list" |
| Offline | "You're offline. Resolutions are saved on this phone." (S40 string) |
| Sync sheet | "Synced 2 resolutions" / "While you were offline, the conflicts changed." / "Sophie Laurent" — "Selin changed to Accept, so everyone agrees. No longer a conflict." / "2 new conflicts" — "Selin kept sorting. They're added to the end." / "Continue resolving". Agreement beat a resolution: "{Item} was agreed before your resolution synced, so it wasn't needed." |
| Large text | "1 note in item details" |
| Keyboard hints (web desktop) | "← Reject", "↑ Maybe", "→ Accept", "Z Undo", "N Note" |
| Rule changed while open | "Deniz changed the rule to Majority decides" / "8 conflicts are now final. The rest are below." / "Continue" |
| Screen reader after action | "Resolved Mehmet Yılmaz: Accept is final. 1 of 15 resolved." |

## 7. Accessibility

- The card's accessible label always reflects the decisions and status shown (e.g. tie: "Merve Kurt, Friend, İstanbul. Tie. You: Accept. Deniz: Reject. Selin: Maybe.").
- Focus order: Back, title, view toggle, More options, progress, Resolve all, card, Undo, Reject, Maybe,
  Accept, Note.
- The card is one focusable element: label "Mehmet Yılmaz, Family, İstanbul. Conflict. You: Reject. Deniz:
  Accept. Selin: Accept." followed by notes ("Selin's note: Haven't seen her in years, maybe skip?"; "Your
  private note: …"). Custom actions (TalkBack actions menu, VoiceOver rotor): **Accept as final, Reject as
  final, Maybe as final, Undo, Add note, Open details, Skip for now**; members get **Change my decision to
  Accept / Reject / Maybe**.
- Decision buttons: "Final decision: Accept" (Decision Maker), "My decision: Accept, selected" (members,
  `aria-pressed`).
- Announcements (polite): "Resolved Mehmet Yılmaz: Accept is final. 1 of 15 resolved."; undo result;
  agreement ("Murat Ekinci is now Agreed: Accept").
- Large text (`S36-large-text`): notes and photo leave the card (link "1 note in item details"), decision
  badges move under each name, the bar becomes a 3-column labeled grid; Resolve all, Undo and Note move into
  the menu (its label says so).
- Color is never the only signal: badges and stamps have icon + label; "my decision" is spelled out in the
  caption, not just by the solid button.
- Touch targets ≥ 48 (decision buttons 64).

## 8. iOS and web differences

- **iOS** (`S36-ios`): 44 pt bar, back chevron "Back", centered title "Conflicts" with "Round 1", trailing
  view toggle and `ellipsis` (UIMenu); edge-swipe back is disabled while a card is being dragged; note as an
  iOS page sheet (as `S25-ios-note`); haptics via Taptic Engine with the same mapping.
- **Web, mobile**: same layout without system bars; no haptics.
- **Web, desktop** (`S36-web-desktop`): phone layout centered; keyboard: → Accept, ← Reject, ↑ Maybe as final
  (Decision Maker) or as my decision (members), Z Undo, N Note, Enter details; hints under the bar (web only).
  Flow 3 continues here: `S27-shared` → `S36-default` → "Resolve all" → `S37-confirm`.

## 9. Edge cases

- **Long names**: title clamps to 2 lines on the card, full in S26; list rows truncate.
- **No photo**: 64 initials avatar in the header (c012 "GA").
- **Many members (6+)**: the decisions list shows the first 4 rows and "+2 more members" (opens S26).
- **Many conflicts (200+)**: progress uses thousands separators; list view is virtualized; only 3 cards render.
- **Decision Maker role moved while resolving**: sheet "Deniz made Selin the Decision Maker. You can no
  longer resolve conflicts." → the screen switches to the member view; resolutions already made stay. If the
  resolutions were made offline and the role moved before they synced, they are rejected (D-09 row 6): the screen
  switches to the member view with the inline alert `S40-outcome-dm-role-lost` at the top ("You're no longer the
  Decision Maker" / "…your 5 resolutions weren't applied. Those conflicts are still open.").
- **Members agreed before an offline resolution synced** (D-09 row 5, A-99): the agreement wins and the
  resolution is dropped; the snackbar `S40-outcome-already-agreed` ("Members agreed on 2 conflicts before your
  resolutions synced. Their agreement is final." + View → `S36-list`) shows above the decision bar (`bottom-32`).
- **Rule changed while resolving**: sheet (see copy), deck reloads.
- **Item removed from the list** while shown: snackbar "Mehmet Yılmaz was removed from the list", deck
  advances.
- **Private notes**: only the author's own private note is ever shown; others' private notes are not
  downloaded.
- **Offline for long**: unsynced count grows; resolutions sync in order; conflicts may change (`S36-synced`);
  outcomes the server reports on arrival use the S40 sync outcome messages (§4.4a).
- **Round ended by the Owner**: open conflicts stay in that round's results (S30) and remain resolvable;
  the header shows "Round 1, ended".
