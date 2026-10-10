# S05 Sign-in prompt and moving lists

Frames: `S05-sign-in-prompt.html`. Generator: `tools/generators/S05-sign-in-prompt.py`.

## 1. Purpose and requirements

When someone without an account tries to share or back up, explain in one sheet why an account is needed,
let them sign in without leaving the screen, move every list on this device into the account safely, and
then continue exactly what they were doing.

Covers: SCR-05, ACC-01, ACC-02, ACC-03, ACC-04, ACC-05, ACC-06, ACC-07, ACC-08, COL-01 (gate before
inviting), GOAL-03, PLT-02, PLT-03, PLT-13, PLT-14, PLT-16, PLT-21, PLT-23, STK-06, STK-07, VIS-12,
VIS-13, SUC-05, DEL-24 (flow 3).

## 2. Entry points and exits

| From | How | Frame |
| --- | --- | --- |
| S09 list overview (`S09-guest-wedding`) | Share / Invite | `S05-share` |
| S10 list management | Share | `S05-share` |
| S06 Settings › Backup (`S06-backup-guest`), sign-in card | "Sign in" / "Sign in to back up" | `S05-default` (backup prompt over Settings) |
| S08 not-backed-up indicator (`S08-guest`) | "Back up" | `S05-backup` |

| To | How |
| --- | --- |
| Origin, unchanged | "Not now", scrim tap, system back, drag down |
| Google / Apple native sheet (out of scope) | "Continue with Google" (`data-action="continue-google"`), "Continue with Apple" |
| S03 `S03-context-share` / `S03-context-backup` | "Continue with email"; after sign-in S03 returns to `S05-moving` |
| `S05-moving` → `S05-moved` | Automatic after sign-in (prototype: clicking the progress area has `data-action="next"`) |
| S31 `S31-default` | "Share list" on `S05-moved` (`data-action="continue"`) |
| S06 `S06-backup` | "Done" on `S05-moved-backup` |

## 3. Layout and components

- **Background**: the origin screen stays in place under a `bg-scrim/50` scrim that also covers the status and
  navigation bars (frames use inert copies of S09-guest-wedding, S08-guest and S06-guest, generated from their
  generators). The sheet runs under the gesture bar with extra bottom padding (24 Android, 34 iOS). After
  the move, the host already shows the backed-up state.
- **BottomSheet** (M3; `bg-popover rounded-t-sheet shadow-sheet`, handle): status icon (48 circle,
  `primary-soft`), `text-title-2` title, `text-body` reason, a short **reason list** (2 rows, icon 20 +
  text) explaining what happens to the lists, then the button stack: iOS Apple, Google (outline), email
  (outline), ghost "Not now".
- **Moving** (`S05-moving`): "Signed in as" row (avatar 32 + email), title, one sentence, Progress
  ("2 of 4 moved" + bar), **ListMoveRow** list (Proposed: list icon tile 40 on `secondary`, name, item count,
  trailing status with icon + label: Moved `circle-check`, Moving… spinner in `primary`, Waiting `clock`,
  Not moved `circle-alert` destructive). Statuses are neutral, never decision colors.
- **Result** (`S05-moved…`, failures): status icon, title, sentence, the same list rows, actions.
- The sheet grows with its content up to 90% of the screen; with large text it becomes full height and
  scrolls.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S05-default` | Back up from Settings while not signed in (host: S06-guest). Entry frame for links from other files |
| `S05-share` | Share or Invite on a list while not signed in |
| `S05-backup` | Back up while not signed in |
| `S05-signing-in` | Returned from the Google chooser; exchanging the token |
| `S05-offline` | Prompt opened while offline: reason shown, sign-in buttons disabled, "Not now" enabled |
| `S05-moving` | Signed in; device lists are being moved (one at a time) |
| `S05-moved` | All lists moved; origin was Share. The host screen already shows the backed-up state (no not-backed-up indicator; "Backed up" on the list) |
| `S05-moved-backup` | All lists moved; origin was Back up |
| `S05-moved-merge` | The account already had lists; device lists were added next to them |
| `S05-move-partial` | Some lists moved, at least one failed |
| `S05-move-failed` | Connection dropped before any list moved |
| `S05-share-large-text` | Font scale ≥ 150% |
| `S05-ios`, `S05-ios-backup` | iOS |
| `S05-web`, `S05-web-backup`, `S05-web-moving` | Web (lists live in this browser) |

## 5. Interactions, gestures and transitions

- Sheet enter: translateY 100% → 0, 300 ms emphasized decelerate; scrim fades to 50%. Exit 200 ms.
  Reduced motion: fade 150 ms. Drag down past 30% or 800 dp/s dismisses (only on the prompt step; the moving
  step can't be dismissed while a list is mid-transfer, the handle hides).
- After sign-in the sheet content cross-fades (150 ms) to the moving step; height animates 250 ms.
- Moving: lists upload one at a time, the list the person is sharing first, then by most recent activity.
  A list is marked Moved only after the server confirms it; until then the local copy is the source of
  truth and remains fully usable (sorting continues in the background). Each list's `backedUp` becomes
  true as it is confirmed.
- If the app goes to the background, moving continues when it returns; the sheet reappears on the origin.
- Done: success haptic; the result sheet stays until the person taps the action.
- "Share list" opens S31 for “Wedding guests” (the origin action, same name as the Share entry).
- Partial failure: "Try again" retries only the failed lists; "Continue to share" is offered when the shared
  list itself moved. The failed list keeps showing "On this phone only" and appears in S06 › Backup as
  "Backup paused" with Try again.
- Full failure: retries automatically when back online (S40 sync notice); "Later" closes the sheet; the
  person is signed in.
- Prototype: Google goes straight to `S05-moving`; the app shows the native chooser first.

## 6. Copy

| Element | String |
| --- | --- |
| Share title | "Sign in to share this list" |
| Share body | "Sharing needs an account, so members can sort “Wedding guests” on their own devices and see where you agree." |
| Share reasons | "Your 4 lists on this phone move to your account and are backed up."; "Sorting keeps working offline, like now." |
| Backup title | "Sign in to back up your lists" |
| Backup body | "Your lists are saved on this phone only. If you lose it or remove the app, they're gone. An account keeps them safe and on every device." |
| Backup reasons | "Your 4 lists on this phone move to your account."; "Open them on other phones and in the browser." |
| Buttons | "Continue with Apple" (iOS), "Continue with Google", "Continue with email", "Not now" |
| Busy | "Signing in…" |
| Offline | "You're offline. Signing in needs a connection. Your lists stay on this phone." |
| Signed in as | "Signed in as deniz.yilmaz@example.com" |
| Moving title | "Moving your lists to your account" |
| Moving body | "Keep SwipeSort open. Each list stays on this phone until it's safely in your account." |
| Progress | "2 of 4 moved" (screen reader "2 of 4 lists moved") |
| Row statuses | "Moved", "Moving…", "Waiting", "Not moved"; item count "100 items" |
| Moved title | "4 lists moved to your account" |
| Moved body (share) | "They're backed up to deniz.yilmaz@example.com and stay on this phone too. Now you can share “Wedding guests”." |
| Moved body (backup) | "They're backed up to deniz.yilmaz@example.com and stay on this phone too. Changes back up automatically from now on." |
| Moved actions | "Share list" (share); "Done" (backup) |
| Merge title | "4 lists added to your account" |
| Merge body | "Your account now has 6 lists: the 4 from this phone and the 2 that were already there. Nothing was replaced. Now you can share “Wedding guests”." |
| Partial title | "3 of 4 lists moved" |
| Partial body | "“March photos clean-up” didn't move. It's still on this phone and nothing is lost. Try again now, or later from Settings › Backup." |
| Partial actions | "Try again", "Continue to share" |
| Failed title | "Your lists didn't move" |
| Failed body | "The connection dropped. You're signed in, and all 4 lists are safe on this phone. They move automatically when you're back online, or try again now." |
| Failed actions | "Try again", "Later" |
| Web wording | "On this browser only"; "Lists are in this browser only"; "Your 4 lists in this browser move to your account and are backed up."; backup body "Your lists are saved in this browser only. If you clear its data, they're gone. An account keeps them safe and on every device."; moving body "Keep SwipeSort open. Each list stays on this browser until it's safely in your account." |
| Singular forms | "1 list moved to your account"; "Your list on this phone moves to your account." |
| Prototype-only link | Progress-area overlay labelled "Finish moving (prototype: click the progress; the sheet moves on by itself)" |

## 7. Accessibility

- The sheet is a modal dialog labelled by its title; focus moves to the title; background is inert.
- Focus order: title, body, reasons, Apple, Google, email, Not now.
- Moving progress is a `progressbar` with a text value; each status change of a row is announced politely
  ("Desk setup moved"). The final title is announced as a status.
- Row statuses use icon + label (never color alone); failure rows use destructive icon and text.
- Large text: reason list hidden (the body already says it), buttons wrap to 64+, sheet full height,
  scrolls.
- Buttons ≥ 48 (56 for the stack).

## 8. iOS and web differences

- **iOS** (`S05-ios`): sheet with grabber at the medium detent (content height), Sign in with Apple first
  as the system button, then Google, email; swipe down dismisses (prompt step only).
- **Web** (`S05-web`): lists created without an account live in this browser's storage, so every string
  says "this browser" instead of "this phone" ("On this browser only"); Apple is not offered. Desktop web
  uses the same sheet in the phone column.
- **Android**: system back closes the sheet on the prompt step; on the moving step, back is ignored until
  the current list finishes, then closes the sheet (moving continues in the background).

## 9. Edge cases

- **No lists on the device**: no moving step; sign-in completes and the origin action continues directly.
- **Account already has lists** (`S05-moved-merge`): device lists are added; nothing is merged or
  overwritten. A device list with the same name as an account list gets " (2)" appended.
- **Very large lists** (5,000+ items, photos): progress per list shows "Moving… 1,204 / 5,000 items" in the
  row; photos upload originals in the background after the list itself is confirmed (cards show
  thumbnails until then).
- **Signed in with a different account on the web earlier**: the web prompt moves only this browser's lists.
- **App killed during moving**: unconfirmed lists stay local and the move resumes on next launch; nothing
  is duplicated (lists carry a client ID).
- **Person signs out later**: lists are already in the account; sign-out removes local copies (S06).
- **Long list names**: truncate in rows; full names in the partial-failure sentence wrap.
- **Offline**: the prompt explains and disables sign-in; local use is never blocked.
