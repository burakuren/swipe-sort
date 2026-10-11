# S09 List overview

Frames: `S09-list-overview.html`. Generator: `tools/generators/S08-S10-lists.py`.
Components: AppBar (small; scrolled with title), ListGroup and rows, Progress, SegmentedProgress (decision
split and list status), DecisionBadge-style count chips, StatusBadge vocabulary, Badge (Owner, Decision
Maker, Collaborator, Archived), AvatarStack, Button, Alert (info, neutral), OfflineBanner, EmptyState,
Skeleton, Snackbar (S10 frames), Switch (BackupSwitchRow, Proposed).

## 1. Purpose and requirements

One list at a glance: where sorting stands, the single next step, and every place the list leads to. It is
where the decision model becomes visible: on a **solo list** my decision is the final decision (DM-01) and
the screen says so; on a **shared list** it separates **my progress** (DM-13) from **list progress**
(Agreed, Pending, Conflict; DM-14), names the conflict rule and who resolves conflicts, and adapts to the
member's role (Owner, Decision Maker, Collaborator). For a signed-in Owner of a solo list it is also where
the list's backup is switched on or off (D-33).

Covers: ACC-10, ACC-11, SCR-09, DM-01, DM-02, DM-03, DM-04, DM-05, DM-06, DM-09, DM-10 (entry to S34), DM-11, DM-12, DM-13,
DM-14, DM-15, DM-16, DM-20, SRT-13, SRT-16 (next actions after a round), RND-01 and RND-03 (entries to S24
and S30), RES-01 (entry to S28), TPL-13 (change the card template), SRC-18 (Sources group: a list combines several sources), SRC-19 (Add items), SAFE-01 (source details: the original is never changed), EXP-01–EXP-07
(entry to S39), COL-01 (Invite), COL-07 (members), COL-12 (Leave), COL-13 (conflict rule), COL-14 (Review
conflicts), COL-15 (Resolve all), COL-17–COL-22 (activity preview), ACC-02, ACC-03, ACC-04, GOAL-02,
GOAL-03, GOAL-04, VIS-08, VIS-09, VIS-14, TERM-01, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-06,
STK-07, DEL-23 (flow 2 start), DEL-24 (flow 3 start). D-33 (per-list backup: A-132, A-133, A-134, A-137, A-139),
D-08 (web storage line, A-137).

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
| S31 `S31-default` | Invite / Share list (signed in, backed-up list) | `share` (solo), `invite` (shared) |
| S10 `S10-share-backup` | Share list on a list that is on this phone only (`S09-new-list`, `S09-device-only`) | `share` |
| S10 `S10-backup-off` (iOS `S10-ios-backup-off`) | "Back up this list" switch turned off | — |
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
   Signed in, list on this phone only (A-137): `cloud-off` "On this phone only" as plain muted text (no link: the
   person chose it; the switch is in the Backup group). Web: "On this browser only", and on the web (signed in or
   not) a note line under the meta: `info` "Browsers can clear lists you haven't opened for a while. Back it up to
   keep it." (D-08). Backed-up lists show nothing.
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
   rows, swatch (matching the bar segment: solid `foreground`, `foreground/50`, outlined `muted`) + icon + status + one-line meaning + count: Agreed `check-check` "Everyone chose the same" 32;
   Conflict `git-compare-arrows` "Members chose differently" 15; Pending `clock` "Not everyone has decided" 53.
   Outline button "Review conflicts" (Owner) or "View conflicts" (Collaborator). Compact variant (one line of
   swatch + icon + count + word) on role views where another card leads.
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
   `copy` duplicated list; the Photos source is out of scope, D-32), title = the source label (file name, sheet
   name, "Contacts", "Manual entry"), description = item count + date ("88 items, imported Sep 28"; later sources
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
15. **Backup group** (D-33, A-132; header "Backup", the last group, under Sources): one **BackupSwitchRow**
   (Proposed; a ListGroup row with a Switch, min-h-16): state icon 20 muted, title "Back up this list", the state
   as description, a visual Switch (52×32, decorative). **The whole row is the switch** (as the S14/S15 switch
   rows): one `role="switch"` control, ≥ 64 high, named "Back up this list", `aria-checked`, and
   `aria-describedby` → the state line and the group footer (the disabled reason). Prototype:
   `data-action="toggle-backup"` on the row (on → `S10-backup-off`, off → `S09-backing-up`). Shown only to a **signed-in Owner**; not
   without an account (every list is on this phone, A-81), not on the sample (A-139), not to members who don't own
   the list, not on archived lists (restore first). States:

   | State | Icon | Description | Switch | Footer |
   | --- | --- | --- | --- | --- |
   | Backed up | `cloud-check` | "Backed up to deniz.yilmaz@example.com" | on | — |
   | On this phone only | `cloud-off` | "On this phone only" (web "On this browser only") | off | "Lists on this phone only don't move to a new phone. Back them up first." (mobile only; A-138) |
   | Backing up | `loader-circle` (spins) | "Backing up…" (`role=status`) | on, disabled until done | — |
   | Turned on offline | `cloud-upload` | "Backs up when you're online" | on | — |
   | Paused (connection lost) | `cloud-alert` | "Backup paused. It continues when you're online." | on | — |
   | Shared list | `cloud-check` | "Backed up to deniz.yilmaz@example.com" | on, disabled | "Shared lists are always backed up." |
   | Offline, backed up | `cloud-check` | "Backed up to deniz.yilmaz@example.com" | on, disabled | "Turning backup off needs a connection." |

   Disabled states keep the description and footer at full contrast; the title turns `muted-foreground` and the
   switch `opacity-50` (design-principles §11).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S09-default` | Solo list in progress, signed in, backed up: Trip ideas (`l-trips`, round `r-p1`, 12 / 30: 6 / 1 / 5; 30 items from trip-ideas.csv, Photo template; A-130) |
| `S09-solo-round-done` | Solo list after Round 1: Desk setup (`l-desk`, `r-d1`: 9 rejected, 6 maybe, 5 accepted); start of flow 2 |
| `S09-new-list` | List never sorted: Frontend hiring, Q4 (`l-candidates`, 12 items, template `t-candidate-compact`); signed in, on this phone only (A-139): header label "On this phone only"; Share opens `S10-share-backup` |
| `S09-empty` | List with 0 items (every item removed, or a manual list saved empty); illustrative "Gift ideas for Mum" |
| `S09-sample` | The first-run sample list (copy of products `p01`–`p20`) |
| `S09-guest-wedding` | Not signed in; Wedding guests is still solo (76 / 100: 17 / 11 / 48); start of flow 3 (Share → S05) |
| `S09-shared` | Shared, Owner (Deniz), rule Decision Maker decides (Mert); list status 32 / 53 / 15 (`r-w1`) |
| `S09-shared-scrolled` | Same, scrolled: Deciding together, Recent activity (`ev6`, `ev5`, `ev1`), actions, Sources |
| `S09-shared-added` | Back from S21 "Add to list": scrolled to Sources, mert-family.csv row "12 items, added just now" with a New badge, snackbar "Added 12 items" + Undo; Recent activity starts with "You added 12 items from mert-family.csv" |
| `S09-source-details` | A source row tapped: details sheet for mert-family.csv |
| `S09-shared-decision-maker` | Shared, Decision Maker (Mert, 85 / 100: 21 rejected, 14 maybe, 50 accepted): resolve call to action. Flow 3: Mert lands here after closing sorting on the web; "Resolve conflicts" carries `data-action="review-conflicts"` |
| `S09-shared-collaborator` | Shared, Collaborator (Selin, 43 / 100: 8 / 10 / 25): no Start a new round, rule read-only |
| `S09-shared-collaborator-scrolled` | Same, scrolled to the footer and Leave list |
| `S09-shared-waiting` | I decided every item (100 / 100: 18 rejected, 15 maybe, 67 accepted, A-123) while others are still sorting; member progress; "See results" |
| `S09-archived` | Archived list opened from Archived lists: read-only (Apartment viewings, `l-apartments`) |
| `S09-loading` | List not on the device yet (opened from a link or notification on a new device) |
| `S09-offline` | Offline on a shared list with changes waiting: banner, the S40 sync notice "Saved on this phone" under the header meta (`cloud-off`; screen reader "Saved on this phone, 4 changes not synced yet"; A-115), Invite disabled, list status timestamped "As of 9:24"; below the fold Conflict rule and Start a new round are disabled with "Needs a connection" (A-186) |
| `S09-unavailable` | The Owner deleted the list (or I was removed): what happened + Back to lists |
| `S09-device-only` | Frontend hiring, Q4 scrolled to the end: Backup group, switch off, "On this phone only" + footer (A-132) |
| `S09-backing-up` | Switch turned on: "Backing up…", switch disabled until done; Share opens the share sheet's busy state (`S10-share-backing-up`) |
| `S09-backed-up` | Done: "Backed up to deniz.yilmaz@example.com"; the header label is gone; snackbar "“Frontend hiring, Q4” is backed up" (4 s) |
| `S09-backup-queued` | Switch turned on while offline: "Backs up when you're online"; Share disabled ("needs a connection"); banner "You're offline. Changes are saved on this phone. Backing up and sharing need a connection." |
| `S09-shared-backup` | Shared list, Owner, scrolled to the end: switch on and disabled, footer "Shared lists are always backed up." (A-134) |
| `S09-backup-large-text` | 200%, scrolled to the end (title in the app bar): Sources and the Backup row grow; the visual switch scales to 64×40. In the header (not drawn) the meta pieces wrap and "On this phone only" keeps its icon |
| `S09-web-device-only` | Web, signed in: the same state for a list kept in this browser only: "On this browser only" + the D-08 note line (illustrative: Frontend hiring, Q4 as if made in the browser) |
| `S09-large-text` | Font scale 200% |
| `S09-ios`, `S09-ios-shared` | iOS |
| `S09-web`, `S09-web-desktop` | Web mobile (not signed in, "On this browser only" + the D-08 note line); desktop (shared, Owner) |

The overflow menu and every list-management dialog are S10 frames.

Turning backup **off** (confirmation, offline, Undo snackbar) and the "Back up this list to share it" sheet are S10
frames: `S10-backup-off`, `S10-ios-backup-off`, `S10-backup-off-offline`, `S10-backup-off-done`, `S10-share-backup`,
`S10-share-backing-up`, `S10-share-backup-offline`.

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
- **Back up** (not signed in) → S05 `S05-backup` (web `S05-web-backup`).
- **Back up this list switch** (signed-in Owner, solo): on → no confirmation (nothing is lost, A-132): the row
  shows "Backing up…" (the list moves with the moving-lists mechanism, D-10), then "Backed up to …" and the
  snackbar "“{name}” is backed up" (4 s); the header label disappears (200 ms fade). Offline it queues ("Backs up
  when you're online") and starts by itself. Off → S10 `S10-backup-off` (confirm, needs a connection); after
  confirming, the row shows "On this phone only", the header gains the label and the snackbar "“{name}” is on this
  phone only" + Undo (6 s) appears (`S10-backup-off-done`); Undo backs it up again. Switch thumb 150 ms; reduced
  motion: instant.
- **Share on a list that is on this phone only** → S10 `S10-share-backup` ("Back up this list to share it",
  A-133); "Back up and share" backs it up, then S31 opens.
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
| Meta | "30 items from trip-ideas.csv"; "12 items from candidates-q4.csv"; "Solo list"; not signed in "On this phone only" + "Back up" (web "On this browser only"); signed in, list on this phone only "On this phone only" (web "On this browser only"), no link; "You, Mert and Selin" / "Deniz, Mert and you" / "Deniz, Selin and you"; badges "Owner", "Decision Maker", "Collaborator", "Archived" |
| Web storage note (D-08) | "Browsers can clear lists you haven't opened for a while. Back it up to keep it." |
| Backup group | header "Backup"; "Back up this list"; "Backed up to deniz.yilmaz@example.com"; "On this phone only" (web "On this browser only"); "Backing up…"; "Backs up when you're online"; "Backup paused. It continues when you're online."; footers "Lists on this phone only don't move to a new phone. Back them up first.", "Shared lists are always backed up.", "Turning backup off needs a connection."; snackbars "“Frontend hiring, Q4” is backed up", "“Trip ideas” is on this phone only" + "Undo" (S40 §6.2) |
| Solo progress | "Round 1"; "Started Oct 8"; "12 / 30 decided"; "6 rejected", "1 maybe", "5 accepted"; "Only you sort this list, so your decisions are final."; "Continue sorting" |
| Round complete | "Round 1 complete"; "Oct 4"; "20 / 20 decided"; "Re-sort Maybe (6)" |
| Never sorted | "Not sorted yet"; "12 items"; "Every item is ready. Start sorting to make your first decisions; you can stop at any time and continue later."; "Start sorting" |
| Empty list | "No items yet" / "Add items from contacts, a file, Google Sheets or text, or type them yourself. Then start sorting." / "Add items" |
| Sample | "Desk setup (sample)"; "This is a sample list" / "20 sample items to practice on. Sort, change decisions, try Results. Delete it from the menu when you're done; nothing else changes."; "Swipe right to accept, left to reject, up for maybe. Or use the buttons." |
| Share card | "Decide together" / "Share this list so others can sort it on their own devices. You'll see where you agree." / "Share list" |
| Shared progress | "My progress"; "Round 1, shared"; "76 / 100 decided" |
| List status | "List status"; "All 3 members" (offline "As of 9:24"); "Agreed" "Everyone chose the same"; "Conflict" "Members chose differently"; "Pending" "Not everyone has decided"; compact "32 agreed", "15 conflicts", "53 pending"; "Review conflicts" / "View conflicts" |
| Decision Maker | "15 conflicts need your decision" / "You're the Decision Maker, so your choice becomes the final decision." / "Resolve conflicts" / "Resolve all with my decisions" / "12 have your decision. 3 stay open until you decide them." |
| Deciding together | header "Deciding together"; "Conflict rule" + "Decision Maker decides, Mert" (Owner); members: "Decision Maker decides. Mert resolves conflicts; Deniz sets the rule." / DM: "Decision Maker decides. You resolve conflicts."; "Members" + "3 members, you're the Owner" / "3 members" |
| Other rules (value) | "Everyone must agree"; "Majority decides" (with Decision Maker: "Majority decides, ties to Mert") |
| Activity | "Recent activity"; "See all"; "15 new conflicts" "Oct 3"; "Selin joined the list" "Oct 2"; "You started Round 1 with 88 items" "Sep 28" (the 12 items from mert-family.csv joined Round 1 later) |
| Actions | "Results" + "12 decided so far" / "5 accepted, 9 rejected, 6 maybe" / "No decisions yet" / "Final decisions and my decisions" / archived "Read-only"; "Start a new round" + "Choose items and card order" / "Starts for all 3 members"; "Rounds" + count or "None yet"; "Card template" + name; "Add items" + "From any source" / "New items join Round 1 for everyone"; "Export" + "CSV, Excel, Google Sheets or a text summary" / "Includes each member's decision" |
| Members footer | "Deniz, the Owner, starts new rounds for everyone." |
| Sources | header "Sources"; "Contacts" / "88 items, imported Sep 28"; "mert-family.csv" / "12 items, added today" (just added: "12 items, added just now" + badge "New"); "Manual entry" / "20 items, typed in Oct 4"; "trip-ideas.csv" / "30 items, imported Oct 8"; "candidates-q4.csv" / "12 items, imported Oct 8"; "Flat hunt 2026" / "Google Sheets, Kadıköy and Beşiktaş tabs, 8 items, imported Jul 2"; "Sample items" / "20 items, added with the sample"; "Copied from Trip ideas" / "30 items, today"; row accessible name "{label}, {description}" (+ ", new"); "Add items" + "From any source" / "New items join Round 1 for everyone" |
| Source details | "mert-family.csv"; "CSV file" (others: "Phone contacts", "Excel file", "Google Sheets", "Plain text", "Manual entry"); "Items" "12"; "Added" "Today by you"; "Fields" "Name, Phone, Email, Side, Relationship"; "Your original is never changed" / "Edits, notes and decisions stay in SwipeSort. Export when you want a file with them."; "Close" |
| Added (from S21) | snackbar "Added 12 items" + "Undo"; activity "You added 12 items from mert-family.csv" "Just now" |
| Leave | "Leave list" |
| Waiting | "You decided every item"; "100 / 100 decided"; "The list status settles as the others finish. Conflicts can be resolved now."; member rows "Mert" "85 / 100", "Selin" "43 / 100"; "See results" |
| Archived | "Archived Jul 21" / "This list is read-only. Restore it to sort, add items or change decisions." / "Restore list"; "8 items from Flat hunt 2026"; back "Back to archived lists" |
| Offline | "You're offline. Decisions are saved on this phone. Inviting needs a connection." (S40-offline; 16 gap below the banner); sync notice "Saved on this phone" (S40 §6.4) while changes wait, then "Syncing 4 changes…" / "Synced" when back online |
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
- Backup switch: the whole row is one `role="switch"` control (touch target the full row, ≥ 64) named "Back up
  this list"; its description (state) and the group footer are its accessible description (`aria-describedby`) ("Back up this list, switch, off. On this phone only. Lists on this phone
  only don't move to a new phone."). "Backing up…" and "Backs up when you're online" are polite live regions.
  Disabled (shared, offline, backing up) uses `aria-disabled` on the row and is announced with its reason
  ("dimmed. Shared lists are always backed up."). Large text (`S09-backup-large-text`, drawn scrolled to the end
  of the page): the row grows, the description wraps (the email may break), the visual switch scales to 64×40 and
  stays at the trailing edge.

## 8. iOS and web differences

- **iOS** (`S09-ios`, `S09-ios-shared`): back chevron with "Lists" and edge-swipe back; trailing Share
  (`share` glyph; "Invite" on shared lists) and a "…" (`circle-ellipsis`) button that opens the iOS action
  sheet (`S10-ios-action-sheet`) or a UIMenu; inset grouped rows (`rounded-control`). The Backup row uses the
  native UISwitch with the same strings; "On this phone only" stays "phone" on iOS (A-137). Turning backup off
  opens an alert, not an action sheet, because the consequence must be read first (`S10-ios-backup-off`, A-113).
  Everything else is identical.
- **Web, mobile** (`S09-web`): same as Android; without an account the list is "On this browser only", with the
  D-08 note line under the meta. Signed in, a list kept in this browser only shows the same label and line and
  the Backup row reads "On this browser only" (`S09-web-device-only`); the footer about new phones is left out.
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
- **Offline** (D-05): sorting, Results, Export to files, and on any list Card template and Add items from local
  sources work; on a shared list these changes are queued and sync later (the server checks them on arrival).
  Rename is queued too (S10). Invite / Share, Google Sheets import and export, joining, Start a new round on a
  shared list, the Conflict rule and member changes need a connection (they change what others may do or need the
  server's state); their controls are disabled with "needs a connection". List status shows when it was last
  updated. On a list on this phone only, everything works offline except Share and turning backup off (A-139).
- **List on this phone only** (signed in, A-132–A-139): it exists on this phone only, so the person's other devices
  and the web app never list it; it shows no sync notice (A-115); Duplicate keeps its storage mode; Delete says
  "…deleted from this phone." (S10). Turning backup on while another backup or a move is running waits its turn:
  the row says "Waiting to back up…", then "Backing up…".
- **Another device turned backup off** for a list that is open here: the screen is replaced by S08 with the S40
  snackbar `S40-outcome-device-only-elsewhere` ("You kept “Trip ideas” on another device only. It's no longer on
  this one."); unsynced changes made here are discarded with the list.
- **Sync outcomes on shared lists** (D-09, S40 §4.4a): if I was removed while offline, the open list is replaced by
  `S40-not-found-removed` with the line about decisions that weren't saved, and Home shows
  `S40-outcome-removed`; if I lost the Decision Maker role while offline, the callout is replaced by the inline
  alert `S40-outcome-dm-role-lost` and the page switches to the Collaborator view; resolutions dropped because
  members agreed show `S40-outcome-already-agreed`; Round 1 decisions synced after Round 2 started show
  `S40-outcome-late-round`; an edit replaced by a later one shows `S40-outcome-edit-replaced`.
- **Many sources** (5+): every row shows; the group never collapses. Two sources with the same file name
  are told apart by their dates.
- **Source dates**: relative within a week ("added today", "added 3 days ago"), then "Sep 28", then
  "Sep 28, 2025" (design-principles §10); so on Oct 10 mert-family.csv reads "added today".
- **Sample list**: sharing is hidden (no Invite in the bar) so the sample never leaves the device.
- **Archived list opened by a member** (shared archived by the Owner): same read-only banner without
  Restore; text "Deniz archived this list. It's read-only."
- **List deleted or access removed while open**: replaced by `S09-unavailable`.
