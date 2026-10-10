# S09 List overview

Frames: `S09-list-overview.html`. Generator: `tools/generators/S08-S10-lists.py`.
Components: AppBar (small; scrolled with title), ListGroup and rows, Progress, SegmentedProgress (decision
split and list status), DecisionBadge-style count chips, StatusBadge vocabulary, Badge (Owner, Decision
Maker, Collaborator, Archived), AvatarStack, Button, Alert (info, neutral), OfflineBanner, EmptyState,
Skeleton, Snackbar (S10 frames).

## 1. Purpose and requirements

One list at a glance: where sorting stands, the single next step, and every place the list leads to. It is
where the decision model becomes visible: on a **solo list** my decision is the final decision (DM-01) and
the screen says so; on a **shared list** it separates **my progress** (DM-13) from **list progress**
(Agreed, Pending, Conflict; DM-14), names the conflict rule and who resolves conflicts, and adapts to the
member's role (Owner, Decision Maker, Collaborator).

Covers: SCR-09, DM-01, DM-02, DM-03, DM-04, DM-05, DM-06, DM-09, DM-10 (entry to S34), DM-11, DM-12, DM-13,
DM-14, DM-15, DM-16, DM-20, SRT-13, SRT-16 (next actions after a round), RND-01 and RND-03 (entries to S24
and S30), RES-01 (entry to S28), TPL-13 (change the card template), SRC-18 (Sources group: a list combines several sources), SRC-19 (Add items), SAFE-01 (source details: the original is never changed), EXP-01–EXP-07
(entry to S39), COL-01 (Invite), COL-07 (members), COL-12 (Leave), COL-13 (conflict rule), COL-14 (Review
conflicts), COL-15 (Resolve all), COL-17–COL-22 (activity preview), ACC-02, ACC-03, ACC-04, GOAL-02,
GOAL-03, GOAL-04, VIS-08, VIS-09, VIS-14, TERM-01, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-06,
STK-07, DEL-23 (flow 2 start), DEL-24 (flow 3 start).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S08 Home | tap a ListRow; "Try a sample list" (`S09-sample`) |
| S25 sorting | close (x); progress is already saved |
| S27 round summary | "Done" |
| S21 add items | "Add to list": `S09-shared-added` (snackbar "Added 12 items" + Undo, new source row) |
| S22 template (change mode) | after finishing, with a snackbar |
| S10 | Duplicate opens the copy (`S10-duplicated`); Restore |
| S33 join | "Open list" |
| Notifications / deep link `/l/<listId>` | opens directly |

| To | Element | `data-action` |
| --- | --- | --- |
| S08 `S08-default` | back arrow / system back / edge swipe | `back` |
| S25 `S25-photo`, `S25-shared`, `S25-default` | "Continue sorting" | `continue-sorting` |
| S25 `S25-candidate`, `S25-product` | "Start sorting" (never sorted) | `start-sorting` |
| S24 `S24-maybe` | "Re-sort Maybe (6)" on `S09-solo-round-done` | `resort-maybe` |
| S24 `S24-default` | "Start a new round" (Owner only on shared lists) | `new-round` |
| S28 `S28-default` / `S28-shared` | "Results" | `results` |
| S30 `S30-default` | "Rounds" | `rounds` |
| S22 `S22-default` | "Card template" | `card-template` |
| S21 `S21-default` | "Add items" (last row of the Sources group) | `add-items` |
| `S09-source-details` | a source row | `source` |
| S39 `S39-default` / `S39-shared` | "Export" | `export` (on `S09-solo-round-done`, shared) |
| S31 `S31-default` | Invite / Share list (signed in) | `share` (solo), `invite` (shared) |
| S05 `S05-share` | "Share list" when not signed in (`S09-guest-wedding`) | `share` |
| S05 `S05-backup` | "Back up" next to "On this phone only" | `back-up` |
| S34 `S34-default` | members avatars and names; Members row | `members` |
| S35 `S35-default` | Conflict rule row (Owner) | `conflict-rule` |
| S36 `S36-default` | "Review conflicts" (Owner), "View conflicts" (Collaborator), "Resolve conflicts" (Decision Maker) | `review-conflicts` (Owner and Decision Maker frames) |
| S37 `S37-confirm` | "Resolve all with my decisions" (Decision Maker) | `resolve-all` |
| S38 `S38-default` | "See all" on Recent activity | — |
| S10 `S10-default`, `S10-shared-owner-menu`, `S10-collaborator-menu`, `S10-archived-menu`; iOS `S10-ios-action-sheet` | overflow "List options" | `menu` |
| S10 `S10-leave` | "Leave list" row (members) | `leave` |
| S10 `S10-restored` | "Restore list" (archived) | `restore` |

## 3. Layout and components

Pushed over the tabs (no bottom navigation). Top to bottom; the page scrolls as one column (`px-4`,
sections 24 apart).

1. **AppBar (small)**: back arrow ("Back to lists"), empty title area, Invite/Share IconButton
   (`user-plus`), overflow IconButton (`ellipsis-vertical`, "List options"). When scrolled past the header,
   the list name appears in the bar with a hairline (`S09-shared-scrolled`).
2. **Header**: list name `text-title-1` (wraps, never truncates) and a meta line of separate labeled pieces
   with icons: item count (+ source when it is a single file: "12 items from candidates-q4.csv"), "Solo
   list", and for shared lists the **MembersLink** (Proposed: AvatarStack 28 + "You, Mert and Selin",
   underlined, opens S34) and a role Badge: Owner (`crown`), Decision Maker (`gavel`, primary-soft),
   Collaborator (`user`). Not signed in: `cloud-off` "On this phone only" + "Back up" (web "On this browser only").
3. **Progress card** (`rounded-group bg-card p-4`, the only place with a filled primary button):
   - Solo in progress: "Round 1" + "Started Oct 8"; "12 / 30 decided" (`text-title-3 tabular-nums`) + bar;
     **DecisionCountChips** (Proposed; DecisionBadge style with counts: "6 rejected", "1 maybe",
     "5 accepted", order Reject, Maybe, Accept); the solo rule line (`info`): "Only you sort this list, so
     your decisions are final." (DM-01); primary "Continue sorting".
   - Solo, round complete: `circle-check` "Round 1 complete"; "20 / 20 decided"; split bar (reject | maybe |
     accept segments, 2 dp gaps) + chips; primary "Re-sort Maybe (6)" when the Maybe pile is not empty,
     otherwise primary "Start a new round".
   - Never sorted: `circle-dashed` "Not sorted yet" + item count; one sentence; primary "Start sorting".
   - 0 items: EmptyState inside the card with primary "Add items".
   - Shared: titled "My progress" + "Round 1, shared"; same content with my counts; primary "Continue
     sorting" (Owner, Collaborator). For the Decision Maker it becomes an outline button, because resolving
     conflicts is their main job.
4. **List status card** (shared only, DM-14): "List status" + "All 3 members"; status bar (agreed
   `bg-foreground`, conflict `bg-foreground/50`, pending `bg-muted`); **ListStatusLegend** (Proposed): three
   rows, icon + status + one-line meaning + count: Agreed `check-check` "Everyone chose the same" 32;
   Conflict `git-compare-arrows` "Members chose differently" 15; Pending `clock` "Not everyone has decided" 53.
   Outline button "Review conflicts" (Owner) or "View conflicts" (Collaborator). Compact variant (one line of
   icon + count + word) on role views where another card leads.
5. **DecisionMakerCallout** (Proposed; Decision Maker only, above My progress): `gavel` in a primary-soft
   circle, "15 conflicts need your decision", "You're the Decision Maker, so your choice becomes the final
   decision.", primary "Resolve conflicts" (S36), ghost "Resolve all with my decisions" (S37) and the bulk
   summary line "12 have your decision. 3 stay open until you decide them." (DM-11, DM-12).
6. **Deciding together** group (shared): Conflict rule row (`git-compare-arrows`, value "Decision Maker
   decides, Mert"; read-only for members with the sentence "Mert resolves conflicts; Deniz sets the rule.")
   and Members row (AvatarStack + "3 members, you're the Owner").
7. **Recent activity** (shared): section header + "See all" (S38); up to 3 events (avatar or icon 32, text,
   relative time).
8. **Actions group** (ListGroup rows, icon 20 muted + title + description or value + chevron): Results
   ("12 decided so far" / shared "Final decisions and my decisions"), Start a new round (Owner; shared
   description "Starts for all 3 members"), Rounds (count), Card template (name), Export ("CSV, Excel, Google Sheets or a text
   summary"; shared "Includes each member's decision"). Members see a footer under the group: "Deniz, the
   Owner, starts new rounds for everyone." Add items is not in this group; it closes the Sources group.
9. **Sources group** (SRC-18; header "Sources", below the actions): one **SourceRow** (Proposed; a
   ListGroup navigation row) per source in import order: source-type icon 20 (`contact` contacts,
   `file-spreadsheet` CSV/Excel, `sheet` Google Sheets, `file-text` plain text, `keyboard` manual entry,
   `image` photos, `copy` duplicated list), title = the source label (file name, sheet name, "Contacts",
   "Photos", "Manual entry"), description = item count + date ("88 items, imported Sep 28"; later sources
   "12 items, added today"; Google Sheets adds the tabs). A source added in this session shows a "New"
   badge (primary-soft) and "added just now". The last row is **Add items** (`plus`, label in
   `text-primary`, description "From any source" / shared "New items join Round 1 for everyone"). Archived
   and sample lists show their sources without Add items; an empty list shows none (Add items is in the
   card).
10. **Source details sheet** (`S09-source-details`, BottomSheet): type icon tile 40 + source label
   `text-title-3` + type ("CSV file"), Close button; the sheet and its scrim extend under the system bars; a definition list (Items, Added, Fields); an info Alert
   (`shield-check`) "Your original is never changed" + one sentence. Read-only: sources can't be removed
   one by one in this version (remove items in Results instead).
11. **Share card** (not signed in, solo): `users` "Decide together", one sentence, outline "Share list".
12. **Leave list** (members): destructive row in its own group at the end (also in the overflow menu).
13. **Archived banner** (archived lists): card with `archive` "Archived Jul 21", "This list is read-only.
    Restore it to sort, add items or change decisions." and primary "Restore list". Only Results
    (read-only), Rounds and Export remain in the actions group.
14. **Sample banner**: Alert info (`flask-conical`) "This is a sample list" + one sentence.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S09-default` | Solo list in progress, signed in: March photos clean-up (`l-photos`, round `r-p1`, 12 / 30: 6 / 1 / 5) |
| `S09-solo-round-done` | Solo list after Round 1: Desk setup (`l-desk`, `r-d1`: 9 rejected, 6 maybe, 5 accepted); start of flow 2 |
| `S09-new-list` | List never sorted: Frontend hiring, Q4 (`l-candidates`, 12 items, template `t-candidate-compact`) |
| `S09-empty` | List with 0 items (every item removed, or a manual list saved empty); illustrative "Gift ideas for Mum" |
| `S09-sample` | The first-run sample list (copy of products `p01`–`p20`) |
| `S09-guest-wedding` | Not signed in; Wedding guests is still solo (76 / 100: 17 / 11 / 48); start of flow 3 (Share → S05) |
| `S09-shared` | Shared, Owner (Deniz), rule Decision Maker decides (Mert); list status 32 / 53 / 15 (`r-w1`) |
| `S09-shared-scrolled` | Same, scrolled: Deciding together, Recent activity (`ev7`, `ev6`, `ev5`), actions, Sources |
| `S09-shared-added` | Back from S21 "Add to list": scrolled to Sources, mert-family.csv row "12 items, added just now" with a New badge, snackbar "Added 12 items" + Undo; Recent activity starts with "You added 12 items from mert-family.csv" |
| `S09-source-details` | A source row tapped: details sheet for mert-family.csv |
| `S09-shared-decision-maker` | Shared, Decision Maker (Mert, 85 / 100: 21 rejected, 14 maybe, 50 accepted): resolve call to action. Flow 3: Mert lands here after closing sorting on the web; "Resolve conflicts" carries `data-action="review-conflicts"` |
| `S09-shared-collaborator` | Shared, Collaborator (Selin, 43 / 100: 8 / 10 / 25): no Start a new round, rule read-only |
| `S09-shared-collaborator-scrolled` | Same, scrolled to the footer and Leave list |
| `S09-shared-waiting` | I decided every item (100 / 100) while others are still sorting; member progress; "See results" |
| `S09-archived` | Archived list opened from Archived lists: read-only (Apartment viewings, `l-apartments`) |
| `S09-loading` | List not on the device yet (opened from a link or notification on a new device) |
| `S09-offline` | Offline on a shared list: banner, Invite disabled, list status timestamped "As of 9:24" |
| `S09-unavailable` | The Owner deleted the list (or I was removed): what happened + Back to lists |
| `S09-large-text` | Font scale 200% |
| `S09-ios`, `S09-ios-shared` | iOS |
| `S09-web`, `S09-web-desktop` | Web mobile (not signed in, "On this browser only"); desktop (shared, Owner) |

The overflow menu and every list-management dialog are S10 frames.

## 5. Interactions, gestures and transitions

- **Primary action** opens S25 (full-screen modal, slide up 300 ms emphasized decelerate) at the next
  undecided item of the current round. Coming back from S25 shows the updated counts; changed numbers tick
  (250 ms). Reduced motion: fade 150 ms and no tick.
- **Re-sort Maybe** opens S24 with the Maybe pile preselected (`S24-maybe`); **Start a new round** opens
  S24 with "All" preselected. On a shared list only the Owner sees Start a new round (DM-15); a round in
  progress asks to end it first (S24/S40).
- **Rows** push their screens (shared axis X 300 ms).
- **Share / Invite**: signed in → S31 sheet; not signed in → S05 sheet (`S05-share`), and after sign-in the
  original action continues to S31. Offline → the button is disabled; its name explains "needs a
  connection" and the banner says it.
- **Back up** (not signed in) → S05 `S05-backup`.
- **Overflow** → DropdownMenu (Android, web) / action sheet (iOS) from S10.
- **Live updates** (shared): my progress, list status and activity update as members sort; the status bar
  segments animate their widths (250 ms standard; reduced motion: instant).
- **Pull to refresh** (signed in): syncs now.
- **Scrolling**: the name moves into the app bar once the header scrolls out (150 ms fade).
- **Source row** → details sheet (300 ms enter; drag down, scrim, back or Close dismiss). **Add items** →
  S21 (list context). On return S09 scrolls to the Sources group, the new row fades in (200 ms; reduced
  motion: instant) and the snackbar "Added 12 items" + Undo appears (6 s; Undo removes the added items and
  the source). The "New" badge stays until the list is closed.
- **Restore list** (archived) → S10 `S10-restored`; the list becomes editable immediately and returns to
  Lists.
- **Deleted elsewhere**: if the list is deleted while open, the screen is replaced by `S09-unavailable`.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | back "Back to lists"; "Share list" (solo) / "Invite" (shared); "List options"; offline "Invite, needs a connection" |
| Meta | "30 items"; "12 items from candidates-q4.csv"; "Solo list"; "On this phone only" + "Back up" (web "On this browser only"); "You, Mert and Selin" / "Deniz, Mert and you" / "Deniz, Selin and you"; badges "Owner", "Decision Maker", "Collaborator", "Archived" |
| Solo progress | "Round 1"; "Started Oct 8"; "12 / 30 decided"; "6 rejected", "1 maybe", "5 accepted"; "Only you sort this list, so your decisions are final."; "Continue sorting" |
| Round complete | "Round 1 complete"; "Oct 4"; "20 / 20 decided"; "Re-sort Maybe (6)" |
| Never sorted | "Not sorted yet"; "12 items"; "Every item is ready. Start sorting to make your first decisions; you can stop at any time and continue later."; "Start sorting" |
| Empty list | "No items yet" / "Add items from contacts, a file, Google Sheets, text or photos, or type them yourself. Then start sorting." / "Add items" |
| Sample | "Desk setup (sample)"; "This is a sample list" / "20 sample items to practice on. Sort, change decisions, try Results. Delete it from the menu when you're done; nothing else changes."; "Swipe right to accept, left to reject, up for maybe. Or use the buttons." |
| Share card | "Decide together" / "Share this list so others can sort it on their own devices. You'll see where you agree." / "Share list" |
| Shared progress | "My progress"; "Round 1, shared"; "76 / 100 decided" |
| List status | "List status"; "All 3 members" (offline "As of 9:24"); "Agreed" "Everyone chose the same"; "Conflict" "Members chose differently"; "Pending" "Not everyone has decided"; compact "32 agreed", "15 conflicts", "53 pending"; "Review conflicts" / "View conflicts" |
| Decision Maker | "15 conflicts need your decision" / "You're the Decision Maker, so your choice becomes the final decision." / "Resolve conflicts" / "Resolve all with my decisions" / "12 have your decision. 3 stay open until you decide them." |
| Deciding together | header "Deciding together"; "Conflict rule" + "Decision Maker decides, Mert" (Owner); members: "Decision Maker decides. Mert resolves conflicts; Deniz sets the rule." / DM: "Decision Maker decides. You resolve conflicts."; "Members" + "3 members, you're the Owner" / "3 members" |
| Other rules (value) | "Everyone must agree"; "Majority decides" (with Decision Maker: "Majority decides, ties to Mert") |
| Activity | "Recent activity"; "See all"; "Mert resolved 3 conflicts" "Yesterday"; "15 new conflicts" "Oct 3"; "Selin joined the list" "Oct 2" |
| Actions | "Results" + "12 decided so far" / "5 accepted, 9 rejected, 6 maybe" / "No decisions yet" / "Final decisions and my decisions" / archived "Read-only"; "Start a new round" + "Choose items and card order" / "Starts for all 3 members"; "Rounds" + count or "None yet"; "Card template" + name; "Add items" + "From any source" / "New items join Round 1 for everyone"; "Export" + "CSV, Excel, Google Sheets or a text summary" / "Includes each member's decision" |
| Members footer | "Deniz, the Owner, starts new rounds for everyone." |
| Sources | header "Sources"; "Contacts" / "88 items, imported Sep 28"; "mert-family.csv" / "12 items, added today" (just added: "12 items, added just now" + badge "New"); "Manual entry" / "20 items, typed in Oct 4"; "Photos" / "30 items, imported Oct 8"; "candidates-q4.csv" / "12 items, imported Oct 8"; "Flat hunt 2026" / "Google Sheets, Kadıköy and Beşiktaş tabs, 8 items, imported Jul 2"; "Sample items" / "20 items, added with the sample"; "Copied from March photos clean-up" / "30 items, today"; row accessible name "{label}, {description}" (+ ", new"); "Add items" + "From any source" / "New items join Round 1 for everyone" |
| Source details | "mert-family.csv"; "CSV file" (others: "Phone contacts", "Excel file", "Google Sheets", "Plain text", "Manual entry", "Photos"); "Items" "12"; "Added" "Today by you"; "Fields" "Name, Phone, Email, Side, Relationship"; "Your original is never changed" / "Edits, notes and decisions stay in SwipeSort. Export when you want a file with them."; "Close" |
| Added (from S21) | snackbar "Added 12 items" + "Undo"; activity "You added 12 items from mert-family.csv" "Just now" |
| Leave | "Leave list" |
| Waiting | "You decided every item"; "100 / 100 decided"; "The list status settles as the others finish. Conflicts can be resolved now."; member rows "Mert" "85 / 100", "Selin" "43 / 100"; "See results" |
| Archived | "Archived Jul 21" / "This list is read-only. Restore it to sort, add items or change decisions." / "Restore list"; "8 items from Flat hunt 2026"; back "Back to archived lists" |
| Offline | "You're offline. Decisions are saved on this phone. Inviting needs a connection." (S40-offline; 16 gap below the banner) |
| Unavailable | "This list was deleted" / "Deniz deleted “Wedding guests” for everyone today. Its items, decisions and notes were deleted with it." / "Back to lists"; removed variant: "You were removed from “Wedding guests”" / "Deniz removed you from this list. Ask Deniz for a new invite if this was a mistake." |
| Loading | screen reader "Loading list" |

## 7. Accessibility

- Focus order: Back, Invite/Share, List options, list name (heading level 1), meta (MembersLink, Back up),
  callout (DM), progress card (heading "My progress"/"Round 1", values, chips, note, primary button), list
  status (heading, bar, legend, button), Deciding together, Recent activity, actions, Leave list.
- Each card is a `section` labelled by its heading. Progress bars are `progressbar` ("12 of 30 decided");
  split and status bars are images with a full text label ("9 rejected, 6 maybe, 5 accepted"; "32 agreed,
  15 in conflict, 53 pending") and are always followed by visible text, so color is never the only signal.
- Decision chips: icon + count + word in decision color (VIS-09). Status legend: icon + word + meaning +
  count.
- Value rows announce the value: "Card template, Photo"; "Rounds, 1".
- MembersLink's name is the visible text ("You, Mert and Selin"); avatars are decorative.
- Large text (`S09-large-text`): name `text-display` and wraps; decision counts stack one per line with
  24 icons; buttons grow to 64 high with `text-title-3`; row descriptions wrap.
- Touch targets ≥ 48 (buttons 48–56, rows ≥ 56, links inside meta are 48-high).
- Reduced motion: no number ticks or bar width animation; transitions become fades.
- Screen-reader announcement when live data changes while focused: "List status updated: 16 conflicts."
  (polite, at most every 10 s).

## 8. iOS and web differences

- **iOS** (`S09-ios`, `S09-ios-shared`): back chevron with "Lists" and edge-swipe back; trailing Share
  (`share` glyph; "Invite" on shared lists) and a "…" (`circle-ellipsis`) button that opens the iOS action
  sheet (`S10-ios-action-sheet`) or a UIMenu; inset grouped rows (`rounded-control`). Everything else is
  identical.
- **Web, mobile** (`S09-web`): same as Android; without an account the list is "On this browser only".
- **Web, desktop** (`S09-web-desktop`): phone column centered; hover states on rows; the overflow menu is a
  popover. Keyboard: Enter on the primary button starts sorting; arrow-key sorting hints appear only in S25.

## 9. Edge cases

- **Long list names**: wrap in the header (no limit on lines); app bar title truncates when scrolled.
- **Long source names and values**: value rows keep the label and truncate the value ("Candidate, comp…"); source titles truncate to one line.
- **Very large lists**: counts with thousands separators ("1,204 / 5,000 decided"); chips wrap to 2 lines.
- **Maybe pile empty after a round**: primary becomes "Start a new round"; no Re-sort Maybe.
- **All decided on a shared list but conflicts open**: list status shows 0 pending; the Owner's primary is
  "Review conflicts" until conflicts are resolved (or the rule makes them final).
- **Rule Everyone must agree**: no Decision Maker callout; every member sees "Review conflicts" and can
  change their own decision there (DM-07). **Majority decides**: conflicts waiting for a member show in
  Pending's meaning line "Waiting for 1 member" (A-25); ties go to the Decision Maker's callout.
- **No Decision Maker** (role turned off): callout hidden; rule row value says "Decision Maker decides,
  nobody assigned" with a hint for the Owner "Choose a Decision Maker" (S34).
- **Member joined mid-round** (DM-16): their progress starts at 0 / 100 for the current round.
- **Items added mid-round** (shared): total increases for everyone ("76 / 112 decided"); a snackbar on
  return "12 items added to Round 1".
- **Offline**: sorting, Results, Card template, Add items from local sources and Export to files work;
  Invite, Google Sheets import/export and joining need a connection. List status shows when it was last
  updated.
- **Many sources** (5+): every row shows; the group never collapses. Two sources with the same file name
  are told apart by their dates.
- **Source dates**: relative within a week ("added today", "added 3 days ago"), then "Sep 28", then
  "Sep 28, 2025" (design-principles §10); so on Oct 10 mert-family.csv reads "added today".
- **Sample list**: sharing is hidden (no Invite in the bar) so the sample never leaves the device.
- **Archived list opened by a member** (shared archived by the Owner): same read-only banner without
  Restore; text "Deniz archived this list. It's read-only."
- **List deleted or access removed while open**: replaced by `S09-unavailable`.
