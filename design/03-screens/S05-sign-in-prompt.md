# S05 Sign-in prompt and moving lists

Frames: `S05-sign-in-prompt.html`. Generator: `tools/generators/S05-sign-in-prompt.py`.

## 1. Purpose and requirements

When someone without an account tries to share or back up, explain in one sheet why an account is needed,
let them sign in without leaving the screen, move the lists on this device into the account safely (all of
them by default; "Choose lists" keeps some on this phone only, D-33, A-135), and then continue exactly what
they were doing.

Covers: ACC-10, ACC-11, SCR-05, ACC-01, ACC-02, ACC-03, ACC-04, ACC-05, ACC-06, ACC-07, ACC-08 (Changed by D-13: Apple on
every platform), COL-01 (gate before
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
| Google chooser / Apple sign-in (out of scope) | "Continue with Google" (`data-action="continue-google"`), "Continue with Apple" (`continue-apple`; iOS native sheet, Android and web Apple's sign-in page in the browser, D-13) |
| `S05-choose-lists` (share), `S05-backup-choose-lists` (backup), `S05-ios-choose-lists`, `S05-web-choose-lists` | "Choose lists" under the first reason (`data-action="choose-lists"`) |
| Prompt (`S05-share-chosen` after a change) | Choose lists › "Done" (`done`); back arrow / iOS "Back" returns without changes |
| `S05-moving-some-kept` → `S05-moved-some-kept` | Sign-in after unchecking lists; "Share list" (`continue`) opens S31 |
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
  text) explaining what happens to the lists; the first reason ends with a text link **"Choose lists"**
  (48 high). Then the button stack in platform order (A-140): iOS Apple (system button), Google, email;
  Android and web Google, Apple (Apple's outline style; white in dark mode), email; ghost "Not now" last.
- **Choose lists** (`S05-choose-lists`, same sheet, content cross-fades): back arrow + `text-title-2`
  "Choose lists to move", one `text-body` sentence, a checklist of every list on this phone (SelectableRow:
  Checkbox 24 leading, list icon tile 40 on `secondary`, name, item count; min height 64), a live summary
  ("3 of 4 lists move", `text-body-sm muted`, `tabular-nums`) and primary "Done". The list being shared is
  checked, disabled (checkbox at 50%) and says "Needed to share" with a `lock` 16 icon (full contrast). The
  sample list is never listed. iOS: navigation row inside the sheet ("Back", "Choose lists", bold "Done") and
  round iOS checkmarks.
- **Moving** (`S05-moving`): "Signed in as" row (avatar 32 + email), title, one sentence, Progress
  ("2 of 4 moved" + bar), **ListMoveRow** list (Proposed: list icon tile 40 on `secondary`, name, item count,
  trailing status with icon + label: Moved `circle-check`, Moving… spinner in `primary`, Waiting `clock`,
  Not moved `circle-alert` destructive, and **On this phone only** `cloud-off` muted for a list left
  unchecked; web "On this browser only"). Statuses are neutral, never decision colors.
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
| `S05-choose-lists` | "Choose lists" on the share prompt: every list checked at first, "Wedding guests" locked on ("Needed to share"); the frame shows "Frontend hiring, Q4" unchecked |
| `S05-share-chosen` | Back on the prompt after Done: the first reason counts what moves and what stays |
| `S05-backup-choose-lists` | "Choose lists" on a backup prompt: nothing is locked |
| `S05-choose-lists-large-text` | Choose lists at 200%: text scrolls above the pinned summary and Done |
| `S05-moving` | Signed in; device lists are being moved (one at a time) |
| `S05-moved` | All lists moved; origin was Share. The host screen already shows the backed-up state (no not-backed-up indicator; "Backed up" on the list) |
| `S05-moved-backup` | All lists moved; origin was Back up |
| `S05-moved-merge` | The account already had lists; device lists were added next to them |
| `S05-moving-some-kept` | Moving after Choose lists: "2 of 3 moved"; the unchecked list shows "On this phone only" |
| `S05-moved-some-kept` | Done: "3 lists moved to your account", 1 stays on this phone only |
| `S05-move-partial` | Some lists moved, at least one failed. The host shows the shared list as backed up |
| `S05-move-failed` | Connection dropped before any list moved |
| `S05-share-large-text` | Font scale ≥ 150%: full-height sheet, reasons kept, text scrolls, actions pinned |
| `S05-ios`, `S05-ios-backup`, `S05-ios-choose-lists` | iOS |
| `S05-web`, `S05-web-backup`, `S05-web-choose-lists`, `S05-web-moving` | Web (lists live in this browser; D-08 copy) |

## 5. Interactions, gestures and transitions

- Sheet enter: translateY 100% → 0, 300 ms emphasized decelerate; scrim fades to 50%. Exit 200 ms.
  Reduced motion: fade 150 ms. Drag down past 30% or 800 dp/s dismisses (only on the prompt step; the moving
  step can't be dismissed while a list is mid-transfer, the handle hides).
- After sign-in the sheet content cross-fades (150 ms) to the moving step; height animates 250 ms.
- **Choose lists** (D-33, A-135): the link swaps the sheet content to the checklist (cross-fade 150 ms, height
  250 ms; reduced motion: instant). Every list starts checked. Tapping a row toggles it; the summary updates
  ("3 of 4 lists move"). The list being shared can't be unchecked ("Needed to share"; tapping it does
  nothing). "Done" returns to the prompt, whose first reason now reads "3 of your 4 lists on this phone move
  to your account. 1 stays on this phone only."; back or system back returns without changes. The choice
  lives until the sheet closes ("Not now" forgets it). Choosing doesn't sign in; the provider buttons do.
- Lists left unchecked stay on this phone only and, once signed in, **belong to the account** as
  device-only lists: they show "On this phone only" on Home and S09 (A-137), appear in S06 › Backup with "Back
  up", and are hidden after sign-out until the same account signs in again (A-136).
- Moving: checked lists upload one at a time, the list the person is sharing first, then by most recent
  activity. Unchecked lists are shown in the list with "On this phone only" and never upload.
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
| Choose lists link | "Choose lists" |
| Reason after choosing | "3 of your 4 lists on this phone move to your account. 1 stays on this phone only." (web: "in this browser" / "in this browser only") |
| Choose lists step | Title "Choose lists to move" (iOS nav title "Choose lists"); "Checked lists move to your account and are backed up. The others stay on this phone only. You can back them up later in Settings › Backup."; locked row "Needed to share"; summary "3 of 4 lists move" (singular "1 of 4 lists moves"; none: "No lists move"); "Done"; back label "Back" |
| Choose lists, web | "Checked lists move to your account and are backed up. The others stay in this browser only. Browsers can clear lists you haven't opened for a while. You can back them up later in Settings › Backup." |
| Buttons | "Continue with Google", "Continue with Apple", "Continue with email", "Not now" (iOS order: Apple, Google, email) |
| Busy | "Signing in…" |
| Offline | "You're offline. Signing in needs a connection. Your lists stay on this phone." |
| Signed in as | "Signed in as deniz.yilmaz@example.com" |
| Moving title | "Moving your lists to your account" |
| Moving body | "Keep SwipeSort open. Each list stays on this phone until it's safely in your account." |
| Progress | "2 of 4 moved" (screen reader "2 of 4 lists moved") |
| Row statuses | "Moved", "Moving…", "Waiting", "Not moved", "On this phone only" (web "On this browser only"); item count "100 items" |
| Progress after choosing | "2 of 3 moved" |
| Moved, some kept | Title "3 lists moved to your account"; body "1 stays on this phone only. You can back it up anytime in Settings › Backup. Now you can share “Wedding guests”." (backup origin ends "Changes back up automatically from now on."); "Share list" / "Done" |
| Moved title | "4 lists moved to your account" |
| Moved body (share) | "They're backed up to deniz.yilmaz@example.com and stay on this phone too. Now you can share “Wedding guests”." |
| Moved body (backup) | "They're backed up to deniz.yilmaz@example.com and stay on this phone too. Changes back up automatically from now on." |
| Moved actions | "Share list" (share); "Done" (backup) |
| Merge title | "4 lists added to your account" |
| Merge body | "Your account now has 6 lists: the 4 from this phone and the 2 that were already there. Nothing was replaced. Now you can share “Wedding guests”." |
| Partial title | "3 of 4 lists moved" |
| Partial body | "“Trip ideas” didn't move. It's still on this phone and nothing is lost. Try again now, or later from Settings › Backup." |
| Partial actions | "Try again", "Continue to share" |
| Failed title | "Your lists didn't move" |
| Failed body | "The connection dropped. You're signed in, and all 4 lists are safe on this phone. They move automatically when you're back online, or try again now." |
| Failed actions | "Try again", "Later" |
| Web wording | "On this browser only"; "Your 4 lists in this browser move to your account and are backed up."; backup body (D-08) "Your lists are saved in this browser only. Browsers can clear lists you haven't opened for a while. Signing in keeps them safe and on every device."; moving body "Keep SwipeSort open. Each list stays on this browser until it's safely in your account." |
| Singular forms | "1 list moved to your account"; "Your list on this phone moves to your account." |
| Prototype-only link | Progress-area overlay labelled "Finish moving (prototype: click the progress; the sheet moves on by itself)" |

## 7. Accessibility

- The sheet is a modal dialog labelled by its title; focus moves to the title; background is inert.
- Focus order: title, body, reasons, Choose lists, provider buttons in their platform order (iOS Apple,
  Google, email; Android and web Google, Apple, email), Not now.
- Choose lists: focus moves to the step title; each row is one `role=checkbox` target ≥ 64 high named by the
  list ("Desk setup, 20 items"). The locked row is `aria-disabled="true"` with "Needed to share" as its
  description (never dimmed below AA; only the checkbox is at 50%). The summary is a polite live region.
  Done returns focus to "Choose lists" on the prompt.
- Moving progress is a `progressbar` with a text value; each status change of a row is announced politely
  ("Desk setup moved"). The final title is announced as a status.
- Row statuses use icon + label (never color alone); failure rows use destructive icon and text.
- Large text: the sheet grows to full height when needed; title, body and both reasons scroll above a pinned action area
  (buttons wrap to 64+, separated by a hairline).
- Buttons ≥ 48 (56 for the stack).

## 8. iOS and web differences

Sign in with Apple is offered on every platform (D-13; it was iOS-only in the brief).

- **iOS** (`S05-ios`, `S05-ios-choose-lists`): sheet with grabber at the medium detent (content height), Sign
  in with Apple first as the system button, then Google, email; swipe down dismisses (prompt step only).
  Choose lists uses a navigation row inside the sheet ("Back", "Choose lists", bold "Done") and round
  checkmarks (iOS multi-select), with the same rules.
- **Android**: Google, Apple, email (A-140). Apple uses Apple's "white with outline" style (white in dark
  mode) and opens Apple's sign-in page in a Custom Tab; the app returns by deep link to the moving step. The
  browser page is out of scope to draw. System back closes the sheet on the prompt step, returns from Choose
  lists to the prompt, and on the moving step is ignored until the current list finishes, then closes the
  sheet (moving continues in the background).
- **Web** (`S05-web`, `S05-web-backup`, `S05-web-choose-lists`): lists created without an account live in
  this browser's storage, so every string says "this browser" instead of "this phone" ("On this browser
  only"). The copy names the risk (D-08): browsers can clear lists not opened for a while; signing in keeps
  them (backup body and Choose lists). Apple is offered (same order and style as Android) through Apple's
  sign-in page: a popup on desktop, a redirect on phones. Desktop web uses the same sheet in the phone column.

## 9. Edge cases

- **No lists on the device**: no moving step and no "Choose lists"; sign-in completes and the origin action
  continues directly.
- **Sample list** ("Desk setup (sample)", D-10, A-139): it stays on the device and is never moved or backed
  up. It is not in the Choose lists checklist, the counts ("Your 4 lists" excludes it), the moving list or
  the result, and it stays visible on Home after sign-in (and after sign-out). If it is the only list on the
  device, there is no moving step.
- **Every list unchecked** (backup origin; on share the shared list is always checked): the reason reads "None
  of your 4 lists move. They stay on this phone only." and sign-in has no moving step; the backup origin
  returns to S06 › Backup, which lists them with "Back up".
- **Unchecked lists later**: they can be backed up one by one from S06 › Backup or the S09 switch "Back up
  this list" (A-132); sharing one asks to back it up first (A-133).
- **Account already has lists** (`S05-moved-merge`): device lists are added; nothing is merged or
  overwritten. A device list with the same name as an account list gets " (2)" appended.
- **Very large lists** (5,000+ items, or many images such as contact photos and image fields): progress per
  list shows "Moving… 1,204 / 5,000 items" in the row; image files upload in the background after the list
  itself is confirmed (D-10 attachments queue; cards show thumbnails until then).
- **Signed in with a different account on the web earlier**: the web prompt moves only this browser's lists.
- **App killed during moving**: unconfirmed lists stay local and the move resumes on next launch; nothing
  is duplicated (lists carry a client ID).
- **Person signs out later**: moved lists are in the account; sign-out removes their local copies (S06).
  Lists kept on this phone only stay, hidden until the same account signs in again (A-136).
- **Long list names**: truncate in rows; full names in the partial-failure sentence wrap.
- **Offline**: the prompt explains and disables sign-in; local use is never blocked.
