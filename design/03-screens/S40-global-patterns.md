# S40 Global patterns

Frames: `S40-global-patterns.html` (58 frames). Generator: `tools/generators/S40-global-patterns.py`.
Components: `01-foundations/components.md` (AlertDialog, Snackbar, Alert/Banner, OfflineBanner, SyncNotice,
ErrorState). Motion: `01-foundations/motion.md` §3–4.

This is the one catalog. When a screen spec and this file disagree on a confirmation, snackbar, banner, error
or not-found string, **this file wins**. Screen specs reference these frames by ID.

## 1. Purpose and requirements

One consistent set of global patterns: every destructive or consequential confirmation (with exact copy,
button labels and the screens that open it), snackbars, the offline banner, the sync notice, generic error and
not-found screens, the app-update screen and the desktop-browser frame.

Covers: SCR-40, GOAL-03, VIS-01, VIS-05, VIS-06, VIS-11, VIS-12, VIS-13, VIS-14, TERM-01, TERM-03, DM-17,
COL-10, COL-11, COL-12, COL-13, SET-02, SET-11, SET-12, SCR-10, TPL-11, SAFE-01, SAFE-02, SAFE-04, SRT-14,
RND-01 (end the open round, A-34), PLT-03, PLT-04, PLT-06, PLT-10, PLT-12, PLT-13, PLT-14, PLT-15, PLT-16,
PLT-17, PLT-21, PLT-23, STK-06, STK-07, OUT-01, OUT-03.

## 2. Entry points and exits

S40 is not a route. Every pattern is opened by another screen; the **Opened from** column of the §4 tables
lists each one. Exits:

| Pattern | Confirm / action leads to | Cancel / dismiss leads to |
| --- | --- | --- |
| Dialogs | The result named in §4 (usually a snackbar on the screen below, or the next screen) | Back to the opening screen, unchanged |
| Snackbar action | Undo restores the previous state; Try again repeats the request; View / Open navigates | Times out (§5) |
| Offline banner | — (informational; disappears on reconnect, the sync notice takes over) | — |
| Sync failed alert | Try again re-runs sync | Stays until sync succeeds |
| Error screen | Try again reloads the same route; secondary goes back (`S08-default` or the previous screen) | System back |
| Not-found screen | Back to lists (`S08-default`), or the list (`S09-*`) for a missing item | System back |
| Update required | Store page (`https://swipesort.app/get` redirect) | Not now → `S08-default`, sync paused |
| Web toast | Opens the event target (same as the Activity row, S38) | Dismiss, or 6 s timeout |

Deep links that land here: `https://swipesort.app/l/<listId>` for a list the person can't open →
`S40-not-found` / `S40-not-found-deleted` / `S40-not-found-removed`; unknown web paths → `S40-web-not-found`;
invalid invite links → **S32** (`S32-invalid`, `S32-expired`, `S32-reset`, `S32-list-deleted`,
`S32-list-archived`; not repeated here).

## 3. Layout and components

### 3.1 AlertDialog (Android, web)

- Scrim `bg-scrim/50` over the whole screen (on desktop web: the whole browser viewport, margins included).
- Surface `bg-popover rounded-dialog shadow-dialog p-6`, full width inside a 24 margin, max width 384
  (`max-w-sm`), **vertically centered**. No icon: the title carries the meaning (calm, A-13).
- Title `text-title-3`: the action as a question naming the object (“Delete “March photos clean-up”?”).
- Body `text-body text-muted-foreground`, one or two paragraphs: consequence first, then what stays safe.
  An optional third line `text-body-sm` for an alternative (“make someone else the Owner and leave instead”).
- Optional content between body and actions: RadioGroup (remove member), Select (template replacement),
  a summary panel on `bg-secondary rounded-control` (conflict rule).
- Actions right-aligned: ghost dismiss (“Cancel”, or “Keep …” when it names what continues) then the
  confirm button. Heights ≥ 48.
- **Variant rule** (one rule for every screen):
  - `destructive` when confirming deletes, discards or replaces something the person made (lists, items,
    fields, notes, edits, templates, typed text, an import in progress), removes someone's access (remove,
    leave, reset link, disconnect) or signs out.
  - `primary` (default) when the change is consequential but nothing is lost: end round, start a new round,
    archive for everyone, transfer ownership, change conflict rule, change Decision Maker.
  - Edge cases decided (QA-120): **Undo Resolve all is destructive** (it discards 12 final decisions; members'
    own decisions are untouched but the resolutions are gone). **Transfer ownership stays primary**: the
    Owner keeps their membership, decisions, notes and access; only the role moves, nothing is deleted, and
    the body says how it is reversed ("Only Mert can make you the Owner again").
- **Stacking**: when both labels don't fit on one row (long labels, translations, ≥ 150% text) the actions
  stack full width, confirm on top, dismiss below (`S40-dialog-large-text`).
- One dialog at a time; dialogs never open on top of another dialog (a dialog that leads to a choice, like
  “Choose new Owner”, closes and opens the next screen or sheet).

### 3.2 iOS

- **Action sheet** (bottom, `inset-x-2`, grouped `rounded-dialog bg-popover`, centered `text-body-sm` title and
  message, actions `min-h-14 text-title-3 font-normal`, destructive actions in `text-destructive`, separate
  Cancel button below in `text-primary`): for destructive actions the person just chose in context —
  delete list, remove member, sign out, discard import / changes, leave list, delete note, delete template,
  reset link, disconnect.
- **Alert** (centered, `inset-x-12`, title `text-body font-semibold`, message `text-body-sm`, buttons
  `min-h-12` separated by hairlines; side by side for two short labels, stacked otherwise): when the person
  must read before deciding or nothing is destroyed — end round, new round, unsynced sign-out, change
  conflict rule, transfer ownership, delete account (final).
- Dialogs with an embedded control (remove member radio, template replacement select) become an action
  sheet with one destructive action per option (remove member) or a page sheet with the same content
  (template replacement).
- Same strings as Android, with “this phone” → “this iPhone” and “gallery” → “library”.

### 3.3 Snackbar

`bg-foreground text-background rounded-control shadow-overlay`, `min-h-12`, `inset-x-4`, text
`text-body-sm`, optional leading icon 20 (`circle-alert` for errors, `circle-check` for success with an
action, context icons like `git-compare-arrows`), at most one action (`text-label text-primary-inverse`,
48 high). Position: `bottom-24` (16 above the bottom navigation) on tab screens; `bottom-32` above the S25 /
S36 decision bar; 16 above a pinned bottom button, or 16 above the bottom edge (`bottom-4`) on screens without a
bottom bar. A visible FAB moves up above the snackbar (M3 behavior); when the snackbar is taller than two lines
(large text) the FAB hides until the snackbar closes, so it never covers content. At large text or when the text needs three lines, the action moves under the text, right
aligned (`S40-snackbar-large-text`).

### 3.4 OfflineBanner and SyncNotice

- **OfflineBanner**: full-width strip directly under the app bar (under the large title on tab screens),
  `bg-muted px-gutter py-2 text-body-sm`, `wifi-off` 16 + text. Persistent while offline. Not dismissible.
  Pushes content down (never overlays it).
- **SyncNotice**: one quiet line, `text-body-sm text-muted-foreground` + 16 icon. Placement: under the list
  header meta on S09; trailing slot of the progress row on S25 / S36 (`text-caption`); under the “Lists”
  title on S08 (all lists). States: Saved on this phone (`cloud-off`), Syncing (`refresh-cw`, spinning),
  Synced (`cloud-check`), Failed (inline Alert: card + `border-destructive/40` + `circle-alert` + Try again).
- Guest (signed-out) lists never show a sync notice; they show the BackupIndicator (S08, S06) instead.

### 3.5 ErrorState / not-found screens

The normal app bar (back or close) stays so the person can always leave. Content centered in the remaining
area: 32 icon `text-muted-foreground`, title `text-title-3`, body `text-body text-muted-foreground`
(`max-w-xs`), optional reassurance line `text-body-sm`, one `secondary` button that fixes it, optional ghost
button that leaves. No illustrations, no error codes.

### 3.6 Desktop browser frame

- Page background `muted`; the app is one 412-wide column (`bg-background`, hairline `border-x`) centered
  horizontally. Nothing is placed on the muted margins (no logo, links or QR). PLT-04, OUT-03.
- The column is exactly the window height. App bars, bottom navigation and pinned bottom buttons stay
  pinned; only the middle region scrolls (the page itself never scrolls) — `S40-desktop-short`.
- Very wide windows change nothing but the margins (`S40-desktop-wide`, about 2,000 px).
- Short windows: the large title collapses to the small app bar title (`S40-desktop-short`). Minimum
  supported height is 568 px; below it the column keeps 568 and the page scrolls. S25 below 680 px hides the
  card image area (same rule as large text, S25 §7) so the card keeps room for its title and fields.
- Overlays (dialogs, scrims, sheets) cover the **whole viewport** but surfaces stay inside the column
  width; sheets open from the bottom of the column.
- Keyboard: every interactive element shows `ring-2 ring-ring` on `:focus-visible` (offset 2 on isolated
  controls; `ring-inset` on rows inside a group, so the ring isn't clipped). Mouse clicks never show it.
- Web desktop Home has no FAB (A-124): a filled "New list" button sits in the app bar next to search; the
  short-window frame collapses the large title into that bar.
- In-app notification toast (push is unavailable on web, PLT-10): `bg-popover rounded-control
  shadow-overlay p-3`, 320 wide (`w-80`), bottom-right of the column, 16 from the right edge, above the
  bottom navigation (`bottom-24`) and above a snackbar when both show. Content: actor avatar with event badge, title
  `text-label`, detail `text-body-sm muted`, Dismiss (`x`, 48). Visible 6 s; hovering or focusing pauses
  the timer. On mobile web the same event appears as the S38 in-app banner (top, under the app bar).

## 4. States (the catalog)

### 4.1 Confirmations

| Pattern | Frame | Variant | Trigger | Opened from |
| --- | --- | --- | --- | --- |
| Delete list (solo) | `S40-default` | destructive | “Delete list” in a list menu | S09 menu (solo), S10 menu / row sheet (`S10-row-sheet`); iOS: `S40-ios-delete-list` |
| Delete list (shared) | `S40-delete-list-shared` | destructive | Owner: “Delete list” on a shared list (needs a connection) | S09 menu (shared Owner), S10 `S10-shared-owner-menu` |
| Delete archived list | `S40-delete-archived` | destructive | “Delete forever” on an archived list | S10 `S10-archived-menu`, S10 iOS swipe action |
| Archive shared list | `S40-archive-shared` | primary | Owner: “Archive” on a shared list (solo archive is immediate with Undo, A-86) | S09 menu, S10 menus |
| Leave list | `S40-leave-list` | destructive | Collaborator / Decision Maker: “Leave list” | S09 menu, S10 `S10-collaborator-menu`, S34 “Leave list” |
| Owner can't leave yet | `S40-leave-owner` | primary | Owner: “Leave list” | S10 shared Owner menu, S34 “Leave list” → S34 `S34-transfer-pick` |
| Remove member (DM-17) | `S40-remove-member` | destructive | Owner: “Remove from list” | S34 member sheet `S34-member-sheet`, S34 iOS actions → `S40-ios-remove-member` |
| Transfer ownership | `S40-transfer-ownership` | primary | Owner: “Make Owner” | S34 member sheet, S34 “Transfer ownership” (with “… and stay”) |
| End round (solo) | `S40-end-round` | primary | “End round” before every item is decided (drawn on the solo March photos clean-up, 12 / 30) | S25 menu `S25-menu` (any solo list, e.g. `S25-photo`) → S27 `S27-ended-early` |
| End round (shared) | `S40-end-round-shared` | primary | Owner: “End round” on a shared list | S25 menu `S25-shared-menu`; iOS `S40-ios-end-round` |
| New round while one is open, solo (A-34) | `S40-new-round` | primary | “Start round” while the current round is open (drawn on the solo March photos clean-up, 12 / 30) | S24, S27 “Start a new round”, S09 “Start a new round” |
| New round while one is open, shared (A-34, DM-15) | `S40-new-round-shared` (= S24 `S24-end-round-dialog`) | primary | Owner: “Start round” while the current shared round is open | S24 (`S24-round-in-progress`), S27 / S09 “Start a new round” on a shared list |
| Discard import | `S40-discard-import` | destructive | Close (`x`) with anything chosen, typed or read in an import | S12–S20, S22 pick mode (all import steps, A-61); iOS `S40-ios-discard-import` |
| Discard adding items | `S40-discard-add-items` | destructive | Close in Add items after a file or source was chosen | S21 |
| Replace typed text | `S40-replace-text` | destructive | Choosing a .txt file while the text box has text | S16 |
| Remove a field with values | `S40-remove-field` | destructive | Remove (`x`) on a field that has values (no dialog when no item has a value) | S17 |
| Discard template changes | `S40-discard-template` | destructive | Close / back in the template editor with unsaved changes | S23 saved template (`S23-discard-changes`); new template from import uses the variant in §6.1 (`S23-discard`) |
| Delete template | `S40-delete-template` | destructive | “Delete template” on a custom template | S22 actions (`S22-actions`, `S22-ios-actions`), S23 menu (`S23-delete`) |
| Discard item edits | `S40-discard-edits` | destructive | Close / back in edit mode with changes | S26 edit (`S26-edit`), S17 edit item sheet (`S17-edit-item`) |
| Revert edited field | `S40-revert-field` | destructive | “Revert to original” on an edited field | S26 (`S26-edited`) |
| Delete note | `S40-delete-note` | destructive | “Delete” on my note | S26 notes (`S26-long-text`, `S26-note-edit`) |
| Reset invite link | `S40-reset-invite-link` | destructive | “Reset link” | S31 (`S31-default`, `S31-collaborator`) |
| Change conflict rule | `S40-change-conflict-rule` | primary | Owner picks another rule | S35 (all rule dialogs follow it: `S35-confirm-majority`, `S35-confirm-everyone`, `S35-confirm-dm`, `S35-dm-none-confirm`) |
| Disconnect Google | `S40-disconnect-google` | destructive | “Disconnect” on Google in Sign-in methods | S07; blocked variant S07 `S07-disconnect-blocked` (“Add a password first”, primary) |
| Sign out | `S40-sign-out` | destructive | “Sign out” with everything backed up | S06; iOS `S40-ios-sign-out` |
| Sign out, unsynced | `S40-sign-out-unsynced` | destructive | “Sign out” with changes not backed up | S06; iOS `S40-ios-sign-out-unsynced` |
| Delete account (final) | `S40-delete-account` | destructive | “Delete account” on the confirm step after typing “delete” (A-54) | S07 `S07-delete-confirm` |
| Bulk resolve | link only: S37 `S37-confirm`, `S37-nothing`, `S37-offline` | primary | Decision Maker: “Resolve all with my decisions” | S36, S09, S27 |
| Undo Resolve all | link only: S37 `S37-undo` | destructive (QA-120) | “Undo” after Resolve all (after the snackbar closed: from S38 / S28) | S37 |
| Change Decision Maker | link only: S34 `S34-dm-confirm`, `S34-dm-self-confirm`, `S34-dm-off-confirm` | primary | Owner moves or turns off the role | S34, S35 |
| Google Sheets write | link only: S39 `S39-google-confirm` (a step, not a dialog) | primary | Export to Google Sheets | S39 |
| Large text | `S40-dialog-large-text` | — | ≥ 150% font scale or labels that don't fit | any dialog |
| Web, desktop | `S40-web-dialog` | — | Any dialog on desktop web | any |

Not confirmed on purpose (Undo snackbar instead, GOAL-03 without friction): solo archive, delete item in
manual entry (S17), change decision (S26/S28), resolve one conflict (S36), duplicate, rename, Mark all as
read (S38), remove photo (S07). Deletes that were confirmed also get an Undo snackbar (A-86).

### 4.2 iOS

| Frame | Form | Same strings as |
| --- | --- | --- |
| `S40-ios-delete-list` | Action sheet | `S40-default` (“this iPhone”, “library”) |
| `S40-ios-remove-member` | Action sheet, one destructive action per choice | `S40-remove-member` |
| `S40-ios-sign-out` | Action sheet without title (S06 `S06-ios-sign-out`) | `S40-sign-out` |
| `S40-ios-sign-out-unsynced` | Alert, stacked | `S40-sign-out-unsynced` |
| `S40-ios-end-round` | Alert, side by side | `S40-end-round-shared` |
| `S40-ios-discard-import` | Action sheet; Cancel button reads “Keep importing” | `S40-discard-import` |

### 4.3 Snackbars

| Frame | Kind | Duration | Example (owner screen) |
| --- | --- | --- | --- |
| `S40-snackbar` | Plain, above the bottom navigation | 4 s | “Feedback sent. Thanks for helping improve SwipeSort.” on S06 Settings |
| `S40-snackbar-undo` | With Undo | 6 s; the action is committed when it closes | “List deleted” + Undo on Home, March photos clean-up already gone from the list (S10, after `S40-default`) |
| `S40-snackbar-error` | Error (`role="alert"`, `circle-alert`) with Try again | 6 s | “Couldn't archive “Wedding guests”. …” |
| `S40-snackbar-success-action` | Success with an action (`circle-check`), screen without a bottom bar | 6 s | “Duplicated as “Desk setup (copy)”” + Open on the original Desk setup overview (A-124: duplicating stays on the original list) |
| `S40-snackbar-sorting` | Above the decision bar | 6 s | “Mert chose Maybe on Mia Andersson. This is now a conflict.” + View (S25) |
| `S40-snackbar-large-text` | Action under the text; FAB hidden | 6 s | same error at 200% |

Durations come from motion.md §3: 4 s without an action, 6 s with one, never under 10 s while a screen
reader is running. A new snackbar replaces the current one (the replaced Undo is committed). Errors that
need lasting attention are not snackbars: they are inline Alerts (sync failed, import errors, export
errors).

### 4.4 Offline and sync

| Frame | State | Trigger |
| --- | --- | --- |
| `S40-offline` | Offline banner + “Saved on this phone” | No connection (OS reachability + failed request) |
| `S40-offline-sorting` | Banner + compact “4 not synced” in the S25 progress row | Offline while sorting (same as `S25-offline`) |
| `S40-sync-syncing` | “Syncing 12 decisions…” | Connection back with queued changes |
| `S40-sync-synced` | “Synced”, visible 4 s, then the line hides | Queue empty |
| `S40-sync-failed` | Inline alert with Try again | 3 automatic retries over about a minute failed while online |

### 4.5 Errors and not found

| Frame | When | Example |
| --- | --- | --- |
| `S40-error` | A screen's data couldn't load from the server and nothing is cached | Shared list opened on a new device while the server is down |
| `S40-error-unknown` | Unexpected local failure (can't render or read local data) | Corrupt view state |
| `S40-not-found` | List link the account can't open (not a member, or it doesn't exist; the two are not distinguished, for privacy) | `swipesort.app/l/<id>` from someone else |
| `S40-not-found-deleted` | A member opens a list the Owner deleted (activity row, notification, recent link) | Selin after Deniz deleted Wedding guests (same strings as `S09-unavailable`) |
| `S40-not-found-removed` | A removed member opens the list (activity row, notification) | Selin after removal (S38 edge case) |
| `S40-item-gone` | An item opened from Activity, a notification or Results was removed | Same strings as `S26-not-found` |
| `S40-update-required` | The server reports the app is below the minimum sync version | After S01, once per session |
| `S40-web-not-found` | Unknown web address | Mistyped URL |
| Invite link invalid | — | See S32 (`S32-invalid`, `S32-expired`, `S32-reset`) |

**App update required: needed.** Shared lists depend on a sync protocol. When it changes incompatibly, an
old app must not write decisions the server can't merge. We never block local use (GOAL-03): the screen
appears once per session, “Not now” keeps the app usable with solo lists and sorting on this phone, and a
persistent offline-style banner says “Update SwipeSort to sync your changes.” + “Update”. Optional updates
are not announced in-app (the stores do that). Web always runs the latest build: after a deploy, the snackbar
“SwipeSort was updated.” + “Reload” appears once; the next navigation reloads automatically.

### 4.6 Desktop browser

| Frame | Shows |
| --- | --- |
| `S40-desktop-frame` | 1280 × 800: phone column centered on the muted page; keyboard focus ring on a list row |
| `S40-web-toast` | In-app notification toast (web replaces push) |
| `S40-web-dialog` | A dialog on desktop: scrim over the whole viewport, focus starts on Cancel |
| `S40-desktop-wide` | ~2,012 × 800: only the margins grow; S25 with keyboard hints |
| `S40-desktop-short` | 1280 × 568: large title collapsed, bars pinned, the list scrolls |
| `S40-web-not-found` | Unknown address |

## 5. Interactions, gestures and transitions

- **Dialog**: enter scale 0.96 → 1 + fade, 250 ms emphasized decelerate; exit fade 150 ms. Reduced motion:
  fade 150 ms. Android back / Esc / scrim tap = Cancel (except `S40-delete-account` and
  `S40-sign-out-unsynced`, where the scrim tap does nothing, so data loss always needs a deliberate button).
  Confirm button shows a spinner with the progress verb while a network request runs (“Deleting…”,
  “Removing…”, “Archiving…”, “Resetting…”); on failure the dialog stays open with an inline error line
  above the actions: “Couldn't {verb}. Check your connection and try again.”
- **Haptics**: none on open; destructive confirm on Android/iOS uses no extra haptic (calm). Web: none.
- **Snackbar**: enter translateY 16 → 0 + fade 250 ms; exit fade 200 ms; swipe sideways to dismiss
  (Android); timer pauses while touched, hovered or focused. Undo restores state and shows no second
  snackbar except where the screen spec names one (“List restored”).
- **Offline banner**: appears 2 s after connection loss (avoids flicker), slides down 200 ms (reduced motion:
  instant); on reconnect it disappears and the sync notice shows “Syncing …”.
- **Sync notice**: icon rotates 1,000 ms linear while syncing (reduced motion: static icon). “Synced” fades
  out after 4 s (150 ms).
- **Error screen**: Try again shows the screen's skeleton, then content or the error again.
- **Desktop**: Tab / Shift-Tab move through controls; inside a dialog focus is trapped; Enter activates the
  focused button; Esc = Cancel; focus returns to the control that opened the dialog. Toasts never take focus.

## 6. Copy

Straight apostrophes (') everywhere. Names, counts and list names are filled in from data; examples use the
sample data.

### 6.1 Dialogs

| Pattern | Title | Body | Buttons (dismiss, confirm) |
| --- | --- | --- | --- |
| Delete list (solo) | "Delete “{list}”?" | "{n} items, {rounds} and your decisions will be deleted from your account and this phone. {source line}" — not signed in: "…will be deleted from this phone." — web: "…from your account and every device." | "Cancel", "Delete list" |
| Source line | — | Photos: "The photos in your gallery aren't changed." Contacts: "Your contacts aren't changed." File: "{file name} isn't changed." Google Sheets: "Your Google Sheet isn't changed." Manual entry or text: "Nothing outside SwipeSort is changed." Web uploads: "The photos you uploaded stay on your computer." Several sources: "Your contacts and mert-family.csv aren't changed." | — |
| Delete list (shared) | "Delete “Wedding guests” for everyone?" | "Mert and Selin lose access. All 100 items, every member's decisions and notes, and Round 1 are deleted for all 3 members. Your contacts and mert-family.csv aren't changed." + "To stop taking part without deleting it for others, make someone else the Owner and leave." (link: "make someone else the Owner") | "Cancel", "Delete for everyone" |
| Delete archived list | "Delete “Book club picks” forever?" | "12 items, Round 1 and your decisions will be deleted from your account. Nothing outside SwipeSort is changed." | "Cancel", "Delete forever" |
| Archive shared list | "Archive “Wedding guests” for everyone?" | "Mert and Selin can still open it, but nobody can sort, add items or change decisions until you restore it. Nothing is deleted." | "Cancel", "Archive list" |
| Leave list (Collaborator) | "Leave “Wedding guests”?" | "You won't see this list anymore. Your 43 decisions stay and still count toward the list status. Items you haven't decided stop waiting for you, and your private notes are deleted." + "To come back, ask Deniz for a new invite." | "Cancel", "Leave list" |
| Leave list (Decision Maker) | "Leave “Wedding guests”?" | "You won't see this list anymore. Your 85 decisions stay and still count toward the list status. You're the Decision Maker, so nobody will have this role until Deniz chooses someone. The 15 open conflicts stay open." | "Cancel", "Leave list" |
| Owner can't leave yet | "Choose a new Owner first" | "“Wedding guests” needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead." | "Cancel", "Choose new Owner" |
| Remove member | "Remove Selin from “Wedding guests”?" | "Selin can't open the list anymore. Choose what happens to Selin's 43 decisions." Radio (default first): "Keep Selin's decisions" / "They still count toward Agreed, Pending and Conflict."; "Discard Selin's decisions" / "Item statuses are recalculated without them." Removing the Decision Maker adds: "Mert is the Decision Maker, so nobody will have this role." Member with no decisions: radio hidden, body "Selin can't open the list anymore. Selin hasn't decided any items yet." | "Cancel", "Remove Selin" |
| Transfer ownership | "Make Mert the Owner?" | "Mert will manage members, rounds and the conflict rule, and can rename or delete the list." + "You'll stay on the list as a Collaborator. Only Mert can make you the Owner again." | "Cancel", "Make Mert Owner" |
| End round (solo) | "End Round 1?" | "18 items aren't decided yet. Your 12 decisions are kept, and you can continue Round 1 from the summary until you start a new round." | "Cancel", "End Round 1" |
| End round (shared) | "End Round 1 for everyone?" | "Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided." + "Everyone sees the round summary." (all finished except me: "Mert and Selin have finished. …") | "Cancel", "End Round 1" |
| New round (solo) | "End Round 1 and start Round 2?" | "18 items in Round 1 aren't decided yet. Your decisions so far are kept. Round 2 starts with 5 items." (March photos clean-up, Accepted items) | "Cancel", "End Round 1 and start" |
| New round (shared) | "End Round 1 for everyone and start Round 2?" | "Mert and Selin are still sorting. Decisions made so far are kept, and items nobody decided stay undecided." + "Round 2 starts for all 3 members with 11 items." | "Cancel", "End Round 1 and start" |
| Discard import | "Discard import?" | Pattern "{What was chosen} will be lost. Nothing has been added to SwipeSort yet." Contacts: "Your selection of 88 contacts will be lost." File: "Your choices for candidates-q4.csv will be lost." Google Sheets: "Your choices for Flat hunt 2026 will be lost." Text: "Your text will be lost." Manual entry: "The 3 items you added will be lost." Photos: "Your selection of 30 photos will be lost." Finish step: "Your choices so far will be lost." | "Keep importing", "Discard import" |
| Discard adding items | "Discard adding items?" | "Your choices for mert-family.csv will be lost. Nothing has been added to Wedding guests yet." | "Keep adding", "Discard" |
| Replace typed text | "Replace the text in the box?" | "The 6 lines you typed are replaced by book-club.txt." | "Cancel", "Replace" |
| Remove a field | "Remove Price (€)?" | "3 items have a value in Price (€). The values are removed with the field." | "Cancel", "Remove field" |
| Discard template changes | "Discard changes to “Candidate, compact”?" | "Your layout changes won't be saved. Frontend hiring, Q4 keeps the current layout." | "Keep editing", "Discard changes" |
| Discard a new template (import) | "Discard this new template?" | "It hasn't been saved. The list keeps the template selected in the finish step." | "Keep editing", "Discard template" |
| Delete template (in use) | "Delete “Guest with table side”?" | "Wedding guests uses this template. Its cards switch to the template you choose, for every member of the list." (solo list: without ", for every member of the list"; several lists: "3 lists use this template. Their cards switch to the template you choose.") Select label "Card template for Wedding guests", value "Person", helper "Person is the template it was based on." | "Cancel", "Delete template" |
| Delete template (unused) | "Delete “Candidate, compact”?" | "No list uses it right now." | "Cancel", "Delete template" |
| Discard item edits | "Discard changes to Gökhan Doğan?" | "Your edits won't be saved. The item keeps its current values." | "Keep editing", "Discard changes" |
| Revert edited field | "Revert City to the original?" | "City goes back to “İstanbul”, the value from Contacts. Your edit “Ankara” is removed." (edited by another member: "Mert's edit “Ankara” is removed for everyone.") | "Cancel", "Revert" |
| Delete note | "Delete your note?" | "“Flying in from Berlin. Ask about dates first.” will be deleted from this item." (long notes: first 80 characters + "…") | "Cancel", "Delete note" |
| Reset invite link | "Reset the invite link?" | "The current link stops working right away. Members who already joined stay. Share the new link with anyone who hasn't joined yet." | "Cancel", "Reset link" |
| Change conflict rule | "Switch to Majority decides?" | "8 of 15 conflicts get a final decision right away. Members are notified." Panel: "8 become final now" + "Reject 1", "Maybe 1", "Accept 6"; "7 stay open" / "They wait for the last member to decide. Ties go to Mert." Other rules: exact strings in S35 §6. | "Cancel", "Switch to Majority" |
| Disconnect Google | "Disconnect Google?" | "You'll sign in with deniz.yilmaz@example.com and your password instead. Your lists aren't affected." | "Cancel", "Disconnect" |
| Disconnect blocked | "Add a password first" | "Google is your only way to sign in. Add a password so you can still sign in after disconnecting Google." | "Cancel", "Add a password" |
| Sign out | "Sign out?" | "Your lists are backed up to deniz.yilmaz@example.com. They'll be removed from this phone until you sign in again." | "Cancel", "Sign out" |
| Sign out, unsynced | "Sign out without backing up?" | "12 changes haven't been backed up because you're offline. Signing out now removes them from this phone, and they can't be recovered." | "Cancel", "Sign out anyway" |
| Delete account | "Delete your account?" | "This can't be undone. “Wedding guests” moves to Mert Aydın. Your other 5 lists (2 of them archived), your decisions and your notes are deleted." (archived lists are counted; without archived lists the parenthesis is left out) (delete for everyone: "Wedding guests is deleted for all 3 members.") | "Cancel", "Delete account" |
| iOS remove member | "Remove Selin from “Wedding guests”?" | "Selin can't open the list anymore. Kept decisions still count toward Agreed, Pending and Conflict." | "Remove and keep Selin's decisions", "Remove and discard Selin's decisions", "Cancel" |
| Progress verbs | — | "Deleting…", "Removing…", "Archiving…", "Leaving…", "Resetting…", "Ending Round 1…", "Signing out…" | — |
| Request failed (inline in dialog) | — | "Couldn't delete the list. Check your connection and try again." (verb per action: archive, leave, remove Selin, reset the link, end Round 1, change the rule) | — |

### 6.2 Snackbars (results of the dialogs and the catalog examples)

| After | String | Action |
| --- | --- | --- |
| Delete list / delete forever | "List deleted" | "Undo" |
| Archive | "List archived" | "Undo" |
| Leave | "You left “Wedding guests”" | — |
| Remove member | "Removed Selin" | "Undo" (6 s) |
| Transfer | "Mert is now the Owner" | — |
| End round | — (S27 opens) | — |
| Discard import / items / changes | — (screen closes) | — |
| Replace text | — | — |
| Remove field | "Removed Price (€)" | "Undo" |
| Delete template | "Template deleted" | "Undo" |
| Revert | "City reverted to İstanbul" | "Undo" |
| Delete note | "Note deleted" | "Undo" |
| Reset link | "Invite link reset" | — |
| Change rule | "Switched to Majority decides. 8 conflicts are now final." | "Undo" |
| Disconnect | "Google disconnected" | — |
| Duplicate | "Duplicated as “Desk setup (copy)”" (shown on the original list) | "Open" |
| Error example | "Couldn't archive “Wedding guests”. Check your connection and try again." | "Try again" |
| Error pattern | "Couldn't {verb} {object}. {How to fix}." | "Try again" |
| Web after deploy | "SwipeSort was updated." | "Reload" |
| Sorting example | "Mert chose Maybe on Mia Andersson. This is now a conflict." | "View" |

### 6.3 Offline banner

Pattern: "You're offline." + what is saved + (optional) what needs a connection. One or two sentences.

| Screen | String |
| --- | --- |
| Default (any screen) | "You're offline. Changes are saved on this phone." |
| Sorting (S25), conflicts (S36: "Resolutions…") | "You're offline. Decisions are saved on this phone." |
| List overview (S09, shared) | "You're offline. Decisions are saved on this phone. Inviting needs a connection." |
| Feature needs a connection | "You're offline. {Feature} needs a connection." e.g. "Changing the rule needs a connection.", "Changes to members need a connection.", "Starting a round for everyone needs a connection.", "Signing in needs a connection." |
| Web | "…saved in this browser." instead of "…saved on this phone." |
| iOS | "…on this iPhone." |
| Disabled controls offline | helper "Needs a connection" |
| Update postponed | "Update SwipeSort to sync your changes." + "Update" |

### 6.4 Sync notice

| State | String | Screen reader |
| --- | --- | --- |
| Offline | "Saved on this phone" (web "Saved in this browser"); compact in S25 / S36: "4 not synced" | "Saved on this phone, 4 changes not synced yet" |
| Syncing | "Syncing 12 decisions…"; mixed changes "Syncing 12 changes…"; one "Syncing 1 decision…" | announced once, politely |
| Synced | "Synced" | "All changes synced" |
| Failed | "Couldn't sync 12 decisions. They're safe on this phone." + "Try again" | `role="alert"` |

### 6.5 Error and not-found screens

| Frame | Title | Body | Actions |
| --- | --- | --- | --- |
| `S40-error` | "{Screen object} couldn't be loaded" (e.g. "Wedding guests couldn't be loaded", "Members couldn't be loaded") | "SwipeSort didn't respond. Check your connection and try again." + "Your decisions are saved on this phone." | "Try again", "Back to lists" |
| `S40-error-unknown` | "This screen couldn't be opened" | "Your lists and decisions are safe. Try again. If it keeps happening, restart SwipeSort or send us a report." | "Try again", "Send a report" (→ S06 Help and feedback, prefilled with technical details) |
| `S40-not-found` | "This list isn't available" | "It may have been deleted, or it's shared with a different account. You're signed in as deniz.yilmaz@example.com." (signed out: "Sign in with the account it was shared with.") | "Back to lists", "Switch account" (signed out: "Sign in") |
| `S40-not-found-deleted` | "This list was deleted" | "Deniz deleted “Wedding guests” for everyone today. Its items, decisions and notes were deleted with it." | "Back to lists" |
| `S40-not-found-removed` | "You're no longer on Wedding guests" | "Deniz removed you from the list, so you can't open it anymore. To join again, ask Deniz for a new invite." (left by yourself: "You left this list. To join again, ask Deniz for a new invite.") | "Back to lists" |
| `S40-item-gone` | "This item isn't in the list anymore" | "Mert removed it from Wedding guests. Its decisions and notes were removed with it." (unknown remover: "It was removed from Wedding guests. Its decisions and notes were removed with it.") | "Open Wedding guests" (from Results: "Back to results") |
| `S40-update-required` | "Update SwipeSort to keep syncing" | "This version can't sync with your account anymore. Your lists and decisions are saved on this phone and sync after you update." + "Until then you can keep sorting. Shared lists and backup wait for the update." | "Update on Google Play" (iOS "Update on the App Store"), "Not now" |
| `S40-web-not-found` | "This page doesn't exist" | "Check the address, or go to your lists." | "Go to your lists" |

### 6.6 Desktop and web

| Element | String |
| --- | --- |
| Toast | "15 conflicts in Wedding guests" / "Mert decides them." (event `newConflicts`, conflict icon instead of an avatar; opens S36); "Dismiss" (label). Any S38 event uses the same layout with its own title and detail |
| Tab title with unread events | "(3) SwipeSort" |
| Keyboard hints (S25 only) | "← Reject", "↑ Maybe", "→ Accept", "Z Undo", "N Note" |

## 7. Accessibility

- Dialogs: `role="alertdialog"`, `aria-modal`, `aria-labelledby` = title, `aria-describedby` = body. Focus
  moves to the dialog and lands on the **dismiss** button (the safe choice); focus is trapped; Esc / Android
  back = dismiss; on close, focus returns to the opener. Embedded RadioGroup has `aria-label` ("Selin's
  decisions") and arrow-key navigation.
- Action sheets and alerts on iOS use the native components (VoiceOver reads title, message, then buttons).
- Snackbars: `role="status"` (polite); errors `role="alert"`. Never under 10 s with a screen reader. The
  action is reachable by focus (TalkBack: actions menu). Undo results are announced ("List restored").
- Offline banner: `role="status"`, announced once when it appears. Sync notice: announced when syncing starts
  and when it fails (`role="alert"`); "Synced" is announced once.
- Error and not-found screens: the title is the screen's heading (`h1`) and is read first; the icon is
  decorative.
- Contrast: all text ≥ 4.5:1 in both themes (token pairs in contrast.md); the snackbar action uses
  `primary-inverse` on `foreground`. Focus ring `ring` ≥ 3:1 against `background` and `popover`.
- Touch targets ≥ 48 for every action, including snackbar actions and the toast's Dismiss.
- Large text: every text style scales, including buttons (label-lg 16 → about 32, buttons grow to 64 high) and snackbar actions; dialogs stack actions at ≥ 150% (`S40-dialog-large-text`, drawn at 200%); snackbars move the action under the
  text (`S40-snackbar-large-text`); the offline banner wraps to more lines.
- Reduced motion: dialogs, snackbars, banners and toasts fade 150 ms; sync icon static.

## 8. iOS and web differences

- **iOS**: action sheets for destructive choices made in context, alerts for read-before-deciding and
  non-destructive confirmations (§3.2); Cancel is a separate bottom button in action sheets; "this iPhone";
  snackbars use the same custom component (iOS has no native one), placed above the tab bar or the decision
  bar; update screen says "Update on the App Store".
- **Web, mobile**: same as Android; dialogs are the Android AlertDialog; "saved in this browser"; no update
  screen (reload snackbar); new events show the S38 in-app banner at the top.
- **Web, desktop**: everything in the centered 412 column (§3.6); dialogs centered over a full-viewport
  scrim; focus ring on keyboard focus; Esc and Enter; in-app toast bottom-right of the column instead of push;
  unknown routes show `S40-web-not-found`.

## 9. Edge cases

- **Long names** in titles (list, template or item names over ~40 characters): the title wraps (up to 3
  lines), never truncates; the object stays in quotes. Body text wraps freely.
- **Text expansion (+40%)**: dialog actions stack when they don't fit on one row; snackbar text wraps to 2
  lines, then the action moves below.
- **Counts of 1**: "1 item", "1 decision", "Syncing 1 decision…", "1 of 2 conflicts". Zero decisions on remove
  member hides the choice (§6.1).
- **Offline during a confirmation** that needs a connection: the opening control is already disabled with
  "Needs a connection" (A-88); if the connection drops after confirming, the dialog stays open with the
  inline failure line and Try again in place of the confirm label.
- **Several snackbars** in a row (fast undo/redo): the newest replaces the previous; a replaced Undo commits.
- **Snackbar + FAB / toast**: the FAB and the web toast move up above the snackbar; a snackbar taller than two
  lines hides the FAB until it closes.
- **Dialog opened while another member changes the same thing** (e.g. Selin leaves while the remove dialog is
  open): on confirm, the dialog closes and a snackbar explains ("Selin already left the list").
- **List deleted while open on another device**: the open screen is replaced by `S40-not-found-deleted`;
  unsynced local decisions on it are discarded (they can't be synced) and the screen says so: "Your changes
  on this list since 9:24 couldn't be saved." (only when there were unsynced changes).
- **Very long offline periods**: the banner stays; the sync notice count grows ("Saved on this phone, 1,204
  not synced" with thousands separators).
- **Sync failing for one list only**: the failed alert appears on that list (S09) and on Home as
  "Couldn't sync Wedding guests. Your changes are safe on this phone." + "Try again".
- **Desktop window narrower than 412**: behaves like mobile web (the column fills the width).
- **Very short desktop windows (< 568)**: the column keeps 568 high and the page scrolls (§3.6).

<!-- Proposed components: StateScreen (ErrorState/NotFound full-screen variant with app bar), WebToast
(InAppBanner variant from S38), UpdateRequiredScreen. Proposed tokens: none. -->
