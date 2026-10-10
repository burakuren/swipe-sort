# S08 Home (Lists)

Frames: `S08-home.html`. Generator: `tools/generators/S08-S10-lists.py` (writes S08, S09 and S10).
Components: AppBar (large title, small, search), ListGroup, ListRow, Badge (Conflict status chip, Sample),
Progress, ExtendedFab, BottomNav, BackupIndicator, OfflineBanner, SyncNotice, Alert (error), EmptyState,
Skeleton, Snackbar (S10 frames). iOS: large-title navigation bar, UISearchController field, tab bar.

## 1. Purpose and requirements

The Lists tab and the app's home. It answers "where was I?" in one look: every list with its progress,
a one-tap way back into sorting, and a way to start a new list. On first run it invites the next action
(import, or try a sample list that is not about weddings). Without an account it quietly says that lists
live on this phone only and offers to back them up.

Covers: SCR-08, ACC-01, ACC-02, ACC-03, ACC-04 (entry to S05), DM-13 (my progress per list), DM-14 (conflict
count on shared rows), DM-20, SRT-13 (resume exactly where you stopped), COL-19 (new conflicts badge), SRC-04
(entry to the source picker), GOAL-02, GOAL-03, SUC-04, SUC-06, TERM-01, TERM-02, VIS-01, VIS-06, VIS-09,
VIS-11, VIS-12, VIS-14, PLT-01, PLT-02, PLT-03, PLT-04, PLT-13, PLT-14, PLT-15, PLT-16, PLT-21, PLT-23,
STK-06, STK-07, DEL-22 (flow 1 start), DEL-25 (flow 4 start).

## 2. Entry points and exits

| From | How | Frame |
| --- | --- | --- |
| S02 onboarding | "Get started" / "Skip" | `S08-first-run` |
| S01 splash (returning user) | automatic | `S08-default` / `S08-guest` |
| S06 sign out, S07 account deleted | after confirming | `S08-first-run` |
| S10 archive / delete / leave | after the action, with a snackbar | `S10-archived-snackbar`, `S10-deleted-snackbar`, `S10-left-snackbar` |
| Tab bar | "Lists" tab | any |

| To | How | `data-action` |
| --- | --- | --- |
| S11 `S11-default` | "Import a list" (first run) / ExtendedFab "New list" / iOS "+" | `import-list` (on `S08-first-run`), `new-list` (on `S08-default`) |
| S09 `S09-sample` | "Try a sample list" | `try-sample` |
| S03 `S03-default` | "Sign in" link on first run (returning user, new phone) | `sign-in` |
| S09 (`S09-shared`, `S09-default`, `S09-solo-round-done`, `S09-new-list`, `S09-guest-wedding`) | tap a ListRow | — |
| S25 (`S25-shared`, `S25-photo`, `S25-default`) | "Resume" on a row with a round in progress | `resume` (on `S08-guest`) |
| S05 `S05-backup` | BackupIndicator "Back up" (not signed in) | `back-up` |
| S10 `S10-row-sheet` | long press on a row | — |
| S10 `S10-archived` | "Archived lists" row | `archived` |
| `S08-search` | search button | `search` |
| S38, S06 | bottom navigation | — |

## 3. Layout and components

Top-level tab: bottom navigation visible (Lists active; Activity shows the unread badge, signed in only).

1. **Large-title AppBar**: trailing IconButton `search` ("Search lists"); title "Lists" (`text-title-1`).
   When the list scrolls, the title collapses into the small bar with a bottom hairline (`S08-many-lists`).
2. **BackupIndicator** (not signed in, at least one list that is not the sample): one line under the title,
   `cloud-off` 16 + "Lists are on this phone only" (`text-body-sm muted`) and "Back up" (`text-label
   text-primary`). The whole line is one 48-high link to S05. It is the only not-backed-up signal on Home
   (rows don't repeat it) so it stays subtle. Web: "Lists are in this browser only".
3. **SyncNotice / OfflineBanner / sync error** (signed in): appear in the same slot under the title.
4. **ListGroup** of **ListRows** (`rounded-group bg-card`, inset dividers), ordered by latest activity
   (the list's `updatedAt`, which includes other members' activity). Each row is one link to S09:
   - name `text-title-3`, 1 line with ellipsis (2 lines at large text);
   - status line `text-body-sm muted`, separate labeled pieces with icons (never middle dots):
     shared → `users` "Shared with 2" + Conflict chip "15 conflicts" (`bg-conflict`, `git-compare-arrows`);
     round in progress → `circle-dot` "Round 1 in progress"; finished → `circle-check` "Round 2 complete";
     never sorted → `circle-dashed` "Not sorted yet, 12 items";
   - progress: in progress → bar (`h-1.5 bg-primary` on `bg-muted`) + "76 / 100" (`text-caption
     tabular-nums`); finished → decision counts in Reject, Maybe, Accept order, each icon + count + word
     in its soft-foreground color ("11 rejected", "1 maybe", "8 accepted"); not sorted → nothing.
   - **ResumeButton** (Proposed): trailing pill (`h-9 rounded-full bg-secondary`, `play` 16 + "Resume")
     inside a 48 target, only when a round is in progress and the member still has items to decide. It is a
     sibling of the row link (not nested). Opens sorting at the next undecided item.
   - The progress shown is always **my** progress (DM-13). Shared lists add the open-conflict count
     (DM-14 in short; full list status lives in S09).
5. **Archived lists** row (ListGroup, `archive` icon, count value, chevron) after the lists; hidden when
   nothing is archived.
6. **ExtendedFab** "New list" (`bg-primary rounded-tile shadow-overlay`, 56 high, `plus` 24), 16 above the
   bottom navigation, right 16. Collapses to a 56 icon FAB while scrolling down; expands on scroll up. It
   moves up above a snackbar (M3).
7. **BottomNav**: Lists, Activity (badge = unread events, `bg-destructive`), Settings.

First run (`S08-first-run`): EmptyState centered between title and navigation: `layers` 32 muted, "No lists
yet" (`text-title-2`), one sentence, primary "Import a list" (`download` icon), ghost "Try a sample list",
a one-line list of the sources, and "Have an account? Sign in". No FAB and no search (nothing to search).

Search (`S08-search`): **SearchAppBar** (Proposed) replaces the large title: back arrow (closes search),
SearchField (`rounded-full bg-secondary`, `search` icon, clear button 48), results count (live region),
matching rows (same ListRow, the matched text highlighted with `bg-primary-soft`), then an "Archived" group
with archived matches (Badge "Archived"). Bottom navigation stays.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S08-first-run` | No lists on the device, not signed in (also after sign out or account deletion) |
| `S08-sample` | "Try a sample list" was used and the person came back to Home; the sample is the only list |
| `S08-default` | Signed in (Deniz), 4 active lists from sample data (`l-wedding`, `l-candidates`, `l-photos`, `l-desk`), 2 archived |
| `S08-guest` | Not signed in with 4 lists on the device (Group A decision): backup indicator, no Activity badge, Wedding guests is a solo list |
| `S08-new-conflicts` | New conflicts arrived on a shared list since I last opened it: unread dot, chip "3 new conflicts", Activity badge +1 |
| `S08-long-names` | Names wrap to 2 lines then ellipsis; Turkish name; long status lines wrap |
| `S08-many-lists` | More lists than fit; scrolled: small title bar with hairline, FAB collapsed to icon |
| `S08-search` | Search open, query "cl": 1 active match, 1 archived match |
| `S08-search-empty` | No list name matches |
| `S08-loading` | Cold start of a large account before local data is ready (normally Home renders instantly from the device) |
| `S08-offline` | No connection (signed in): banner; every list stays usable |
| `S08-syncing` | Connection back: "Syncing 12 decisions…" (sync notice), disappears 2 s after "Synced" |
| `S08-sync-error` | Sync failed after retries: inline alert with Try again; changes stay on the phone |
| `S08-error` | Local database couldn't be read |
| `S08-large-text` | Font scale 200% |
| `S08-ios`, `S08-ios-first-run` | iOS |
| `S08-web`, `S08-web-desktop` | Web mobile (not signed in), desktop (signed in) |

Related frames in S10: `S10-row-sheet` (long press), `S10-archived-snackbar`, `S10-deleted-snackbar`,
`S10-left-snackbar`.

## 5. Interactions, gestures and transitions

- **Tap a row**: push S09 (shared axis X, 300 ms standard; reduced motion: 150 ms fade). Bottom navigation
  hides inside the list stack.
- **Resume**: opens S25 as a full-screen modal (slide up 300 ms emphasized decelerate; reduced motion: fade)
  at the next undecided item of the current round (SRT-13). If the round changed elsewhere, S25 shows its
  resume state (`S25-resume`).
- **Long press a row** (500 ms, haptic tick): opens the actions bottom sheet (`S10-row-sheet`). The row
  shows the pressed state (`bg-accent`) while held. Screen readers get the same actions as custom actions
  on the row ("Resume sorting", "Share list", "Rename", "Duplicate", "Archive", "Delete list").
- **New list / Import a list / "+"**: opens the import modal at S11.
- **Try a sample list**: creates "Desk setup (sample)" (a local copy of the 20 sample products, Product
  template, not sorted) and opens `S09-sample`. If a sample already exists it opens that one instead of
  creating a second.
- **Back up**: opens the S05 sheet over Home; after moving lists, the indicator disappears.
- **Search**: the field gets focus and the keyboard opens; results filter on every keystroke (no submit).
  Matching: any word in the list name starts with the query, case- and accent-insensitive ("izmir" finds
  "İzmir", "cl" finds "clean-up" and "club"). Active matches first by latest activity, then archived.
  Clear (x) empties the field and keeps focus; back closes search and restores the scroll position.
- **Pull to refresh** (signed in only): syncs now; shows the sync notice. Not available for lists on this
  phone only.
- **FAB**: collapses on scroll down (200 ms standard), expands on scroll up. Reduced motion: no
  collapse animation, swaps instantly.
- **Sync notice**: appears when there are unsynced changes and a connection; spins `refresh-cw` (static with
  reduced motion); turns into `cloud-check` "Synced" and fades after 2 s (150 ms).
- **Live updates**: when a member decides or a conflict appears, the row's chip and progress update in place
  (count tick 250 ms); rows re-order only when the screen is not visible, never under the finger.
- **Unread state**: the dot and "N new conflicts" chip clear when the list is opened (S09).

## 6. Copy

| Element | String |
| --- | --- |
| Title | "Lists" |
| Search button | "Search lists" (accessible name) |
| Backup indicator | "Lists are on this phone only" / web "Lists are in this browser only"; action "Back up" |
| First run | "No lists yet" / "Import a list or try a sample to see how sorting works." / "Import a list" / "Try a sample list" / "Import from phone contacts, CSV, Excel, Google Sheets, plain text or photos, or type items yourself." / "Have an account?" "Sign in" |
| Sample row | "Desk setup (sample)"; "Not sorted yet, 20 items"; badge "Sample" |
| Sample footer | "The sample is for practice. Delete it from its menu whenever you like. Import your own list with New list." |
| Row status | "Shared with 2" (1: "Shared with 1"); "Round 1 in progress"; "Round 2 complete"; "Not sorted yet, 12 items" |
| Row progress | "76 / 100"; counts "11 rejected", "1 maybe", "8 accepted" |
| Conflict chip | "15 conflicts" (1: "1 conflict"); new since last visit: "3 new conflicts" |
| Resume | "Resume"; accessible name "Resume sorting {list name}" |
| Archived row | "Archived lists" + count |
| FAB | "New list"; collapsed accessible name "New list" |
| Search | field label "Search lists"; "Close search"; "Clear search"; result count "2 lists match" / "1 list matches"; group "Archived" |
| Search empty | "No lists match “budget”" / "Check the spelling, or search for another word in the list name." / "Clear search" |
| Offline | "You're offline. Changes are saved on this phone and sync when you're back online." |
| Syncing | "Syncing 12 decisions…" → "Synced" |
| Sync error | "Couldn't sync 12 decisions. They're safe on this phone." / "Try again" |
| Error | "Your lists couldn't be opened" / "They're still saved on this phone. Try again, or restart SwipeSort. If it keeps happening, contact us from Settings › Help." / "Try again" |
| Loading | screen reader "Loading lists" |
| Unread dot | screen reader "New activity." before the list name |
| iOS | "+" accessible name "New list"; search placeholder "Search" |
| Snackbars arriving from S10 | "List archived" + "Undo"; "List deleted" + "Undo"; "You left “Wedding guests”"; "List restored" |

## 7. Accessibility

- Focus order: Search, (Backup indicator), rows top to bottom (row link, then its Resume button),
  Archived lists, New list, bottom navigation.
- Each row link's accessible name reads in order: name, status, progress ("Wedding guests. Shared with 2.
  15 conflicts. 76 of 100 decided."). The progress bar is a `progressbar` with "76 of 100 decided";
  decision counts are text with their word, never icon only.
- Resume is a separate button named "Resume sorting Wedding guests" (label in name).
- Long-press actions are also exposed as custom accessibility actions on the row (TalkBack actions menu,
  VoiceOver rotor), so no gesture is required.
- Conflict chip: icon + text, inverted neutral (color not the only signal). Unread dot has a text
  equivalent.
- Live regions: search result count (polite), sync notice (polite), sync error (`alert`).
- Large text (`S08-large-text`): names `text-title-1` and wrap to 2 lines; status and counts wrap; the
  progress fraction stays at the end of the bar; Resume moves below the row content (full label); FAB keeps
  its label; bottom navigation labels grow. Rows grow, nothing truncates except the second line of names.
- Touch targets ≥ 48: rows ≥ 72, Resume 48 high, icon buttons 48, FAB 56.
- Reduced motion: no FAB collapse animation, no spinner rotation (static `refresh-cw`), push and modal
  transitions become 150 ms fades, skeleton pulse is static.
- Contrast: every text pair on `card`/`background` is a checked token pair; the highlight in search uses
  `primary-soft` + `primary-soft-foreground` (AA).

## 8. iOS and web differences

- **iOS** (`S08-ios`, `S08-ios-first-run`): large title that collapses natively; a search field under the
  title (UISearchController) instead of the search icon; **no FAB**: "+" in the navigation bar ("New list");
  inset grouped rows (`rounded-control`); standard tab bar (tint only, no pill). Long press opens a context
  menu (UIContextMenu) with the same actions as `S10-row-sheet`; swipe left on a row shows Archive (and
  Delete for the Owner) as swipe actions.
- **Web, mobile** (`S08-web`): same as Android without system bars. Lists made without an account live in
  this browser: "Lists are in this browser only" (clearing site data removes them). Long press = context
  menu via a right click or a long touch; an overflow button appears on hover/focus on desktop.
- **Web, desktop** (`S08-web-desktop`): the phone column centered; same layout; `/` focuses search.
  No haptics.

## 9. Edge cases

- **Long names**: 2 lines, then ellipsis; full name in S09 and in the accessible name.
- **Many lists** (hundreds): virtualized list; search is the main way to find one; Archived lists stays at the end.
- **Large numbers**: "1,204 / 5,000" with thousands separators; conflict chip "99+ conflicts" above 99.
- **Shared list with no conflicts**: chip hidden. **Rule "Majority decides"** waiting conflicts still count as conflicts.
- **A round finished by me but not by others** (shared): row shows "Round 1, waiting for 2 members" with my
  progress full and no Resume.
- **Sample list**: never counted for the backup indicator; signing in moves it like any list (it can be
  deleted at any time). Only one sample at a time.
- **Not signed in and offline**: no banner (nothing needs the network); sharing and backup explain it in S05.
- **Signed in, list not yet downloaded** (new phone): rows appear as they sync, with a skeleton for the
  missing ones; opening one shows `S09-loading`.
- **Removed from a shared list or list deleted by its Owner while on Home**: the row disappears with a
  snackbar "Deniz deleted “Wedding guests”"; opening a stale link shows `S09-unavailable`.
- **Archived lists**: never shown in the main group; included in search under "Archived".
- **Zero lists but signed in** (e.g. after leaving the only shared list): the empty state keeps "Import a
  list" but drops "Try a sample list" and the sign-in line (see `S10-left-snackbar`): "Import a list to
  start sorting, or join one when someone shares it with you." The sample is a first-run aid only.
