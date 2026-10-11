# S12 Pre-permission explainers and permission-denied recovery

Frames: `S12-permissions.html`. Generator: `tools/generators/S11-S15-import.py`.

## 1. Purpose and requirements

Before any system permission prompt, explain why access is needed and how the data is used, so the user can
say yes with confidence. When access was denied, explain how to recover and always offer a working
alternative. One layout for every permission (**PermissionExplainer**, proposed component) so the pattern
scales to future sources.

Since the build decisions, S12 covers only the permissions SwipeSort still asks for (least privilege, D-17
rule, ADR-0005):

- **Contacts on Android 16 and lower** (`READ_CONTACTS` with `maxSdkVersion="36"`, D-18). Android 17 and later
  and iOS pick contacts in the system contact picker, which needs no permission, so they never see S12 (S13
  picker path).
- **Push notifications** (Android 13+, iOS).
- The **photos** explainer, denied and limited-access states are gone with the Photos source (D-32, A-129).
- The **iOS contacts** explainer and denied state stay as labeled fallback frames, used only if SwipeSort ever
  asks iOS for full contacts access (D-18, A-156).

Covers: SRC-05 (changed by D-18 and D-32), SRC-06, SRC-02, COL-24, PLT-02, PLT-07, PLT-10, PLT-11, PLT-16,
GOAL-03, SAFE-01, OUT-01, SCR-12 (changed by D-18 and D-32).

## 2. Entry points and exits

| From | When |
| --- | --- |
| S11 / S21 Contacts tile, **Android 16 and lower** | Contacts permission never asked (`S12-contacts`) or permanently denied (`S12-contacts-denied`) |
| S31 Invite (first share) / S33 Join | Once, right after a list is first shared or joined, if notification permission is undecided (`S12-notifications`) |
| S38 Activity banner "Turn on notifications" / S06 Notifications switch | Permission undecided → `S12-notifications`; denied → `S12-notifications-denied` |

| To | Trigger |
| --- | --- |
| System permission prompt (out of scope) | "Continue" / "Turn on notifications" / "Allow access" |
| `S13-contacts-import.html#S13-select-default` | Contacts granted (prototype goes to the 88-selected frame; the real first arrival is `S13-default`) |
| `S14-file-import.html#S14-default` | "Import a CSV instead" |
| `S11-source-picker.html#S11-default` | "Not now" (import explainers) |
| System app settings | "Open settings" (Android `ACTION_APPLICATION_DETAILS_SETTINGS`; iOS `openSettingsURLString`) |
| Origin screen (S09, S38, S06) | Notifications "Not now", close, or after the prompt |

Returning from system settings: the app re-checks the permission on `AppState` "active". Granted →
continue automatically to S13 (or back to the origin for notifications) with no extra tap. Still denied →
stay on the recovery state.

Removed exits: `S18-photos-import.html` (Photos, D-32) and `S13-ios-limited` (iOS limited contacts access is
now a fallback frame only, D-18).

## 3. Layout and components

Import permissions sit inside the import modal: **AppBar (modal)** "Import" + **ImportStepper** ("Select
items", Step 2 of 5). Notifications are a standalone full-screen modal (close only, no stepper).

**PermissionExplainer** (proposed, built from existing tokens):
1. Icon in a 56 circle: `bg-primary-soft text-primary-soft-foreground` for the ask; `bg-muted
   text-muted-foreground` for recovery states (calm, not alarming).
2. Title `text-title-2`, lead `text-body-lg muted` (max 64ch).
3. Either **promise points** (3 rows: icon 24 muted, title `text-label-lg`, one line `text-body-sm muted`),
   a **steps list** (numbered 1–3 in `bg-secondary` circles; a real sequence) or an **events group**
   (notifications: ListGroup of 6 rows). (The thumbnail grid variant left with the photos limited-access
   state, D-32.)
4. Bottom actions (shared import pattern, identical to S16–S21): top hairline, optional note
   (`text-body-sm muted`) naming the next system step, primary `h-14` full width, ghost secondary below it.

The same layout, without a permission, is reused as an intro before a system picker: `S13-picker-intro`
(contacts) and `S15-default` (Google's file picker).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S12-default` | Same as `S12-contacts` (every screen file has a default frame) |
| `S12-contacts` | Contacts permission not determined, **Android 16 and lower** |
| `S12-contacts-denied-once` | Android 16 and lower: the user tapped "Don't allow" once; Android can still show the prompt again, so the primary is "Allow access" |
| `S12-contacts-denied` | Android 16 and lower, "don't ask again" state (second denial, `shouldShowRequestPermissionRationale` false after a denial): only Settings can grant it |
| `S12-notifications` | Push permission not determined (Android 13+ `POST_NOTIFICATIONS`) |
| `S12-notifications-denied` | Push denied (Android won't ask again) |
| `S12-notifications-web` | Web: push is unavailable; sheet over Activity explains in-app notifications |
| `S12-notifications-ios` | iOS push explainer |
| `S12-contacts-large-text` | 200% font scale, contacts explainer (Android 16 and lower) |
| `S12-contacts-ios` | **Fallback only (D-18)**: iOS contacts explainer, if full contacts access is ever requested |
| `S12-contacts-denied-ios` | **Fallback only (D-18)**: iOS contacts denied (iOS asks once) |

Removed (D-32): `S12-photos`, `S12-photos-denied`, `S12-photos-limited-ios`.

Web contacts: never reaches S12. The S11 contacts tile is the unavailable variant and opens
`S11-web-unavailable` (reason + "Get the app" + "Import a CSV instead"). Web notifications:
`S12-notifications-web`.

## 5. Interactions and transitions

- "Continue" / "Turn on notifications" / "Allow access" call the platform request (expo-contacts
  `requestPermissionsAsync` on Android 16 and lower, expo-notifications `requestPermissionsAsync`). While the
  system prompt is up the screen stays as is.
- Result handling: granted → push the next step (shared axis X 300 ms; reduced motion 150 ms fade);
  denied → replace this screen with the matching recovery state (cross-fade 150 ms). No error haptic for a
  denial: it is the user's choice, not an error.
- "Not now" returns to S11 (import) or closes the modal (notifications). The notifications explainer is
  shown automatically **once**; after "Not now" it only appears again from the Activity banner or the
  Settings switch.
- Fallback only: "Share more contacts" on iOS 18 limited access opens the system contact access picker
  (S13 fallback frame).

## 6. Copy

| Element | String |
| --- | --- |
| Stepper | "Select items", "Step 2 of 5" |
| Contacts title | "Allow access to your contacts" |
| Contacts lead | "SwipeSort reads your contacts so you can pick the ones to sort. Here's how they're handled." (large text: "SwipeSort reads your contacts so you can pick the ones to sort.") |
| Contacts points | "Only the contacts you pick" / "You choose on the next screen. Nothing else is imported."; "Stays with your list" / "SwipeSort keeps only the contacts you import. They leave this phone only when the list is backed up or shared." (iOS fallback: "…leave this iPhone only…", A-137); "Your address book isn't changed" / "SwipeSort never edits, adds or deletes contacts. Decisions only change SwipeSort's copy." |
| Contacts note | Android 16 and lower "Next, Android asks you to allow access."; iOS fallback "Next, iOS asks once. Allow full access, or choose contacts to share." |
| Contacts buttons | "Not now", "Continue" |
| Denied once | "SwipeSort can't see your contacts" / "You chose Don't allow. To pick contacts, allow access. Or use a CSV file: most contacts apps can export one." / note "Access only lets SwipeSort read contacts. It never changes your address book." / "Import a CSV instead", "Allow access" |
| Denied (Android 16 and lower) | "Contacts access is off" / "Android won't ask again, so access has to be turned on in Settings. When you come back, your contacts are ready to choose." / steps "Tap Open settings", "Tap Permissions, then Contacts", "Choose Allow" / "Import a CSV instead", "Open settings" |
| Denied (iOS, fallback only) | "Contacts access is off" / "iOS asks only once, so access has to be turned on in Settings. When you come back, your contacts are ready to choose." / steps "Tap Open Settings", "Tap Contacts", "Choose Full Access" / "Import a CSV instead", "Open Settings" |
| Notifications title | "Get notified about shared lists" |
| Notifications lead | "Know when it's your turn or when a decision needs you, without opening the app." |
| Events header | "You'll hear when" |
| Events | "Someone joins a list", "A member finishes sorting", "New conflicts need a decision", "Conflicts are resolved", "A new round starts", "Your role changes" |
| Notifications note | Android "Choose which ones in Settings, under Notifications."; iOS "Next, iOS asks once. Change it later in Settings." |
| Notifications buttons | "Not now", "Turn on notifications"; close label "Not now" |
| Notifications denied | "Notifications are off" / "Android won't ask again. To get notified, turn them on in Settings. Activity always shows every update in the app." / steps "Tap Open settings", "Tap Notifications", "Turn on All SwipeSort notifications" / "Not now", "Open settings" |
| Web notifications sheet | "Push notifications need the app" / "In the browser, updates appear in Activity while SwipeSort is open. To get notified on your phone, get SwipeSort for Android or iOS." / "Not now", "Get the app" |

## 7. Accessibility

- Focus order: Back (iOS) or close, title, stepper, icon (decorative, hidden), heading, lead, points or steps,
  note, secondary, primary. Initial focus on the heading so the explanation is read before the buttons.
- The steps list is an ordered list labeled "Steps"; numbers are real sequence markers.
- Recovery states use muted icons, never red: denial is a choice, not an error.
- Large text (`S12-contacts-large-text`): the content scrolls; the bottom actions stay pinned and grow;
  button labels wrap instead of truncating.
- Notifications sheet on web: `role="dialog"`, focus moves to the sheet title, Escape closes.

## 8. Platform differences

- **Android 16 and lower** (reference frames): contacts explainer, denied-once and don't-ask-again recovery.
  This is the founder's Android 13 phone and today's majority (D-18).
- **Android 17 and later**: no contacts permission. The Contacts tile opens `S13-picker-intro`, then the
  system contact picker (`ACTION_PICK_CONTACTS`, multi-select, only the fields SwipeSort needs). If the
  Android 17 spike shows the picker can't select in bulk, D-18 keeps `READ_CONTACTS` on 17+ and these phones
  use the Android 16 frames unchanged.
- **iOS**: no contacts permission; the Contacts tile opens `S13-picker-intro-ios` (system contact picker).
  `S12-contacts-ios` and `S12-contacts-denied-ios` are kept as **fallback frames** for the case where full
  contacts access is ever requested (D-18): iOS asks once, so its recovery never offers "Allow access", only
  "Open Settings" plus the alternative; with full access requested, iOS 18 could also limit access to chosen
  contacts (`S13-ios-limited`, fallback). Notifications on iOS: `S12-notifications-ios`. Settings is written
  "Settings" with a capital S, as on iOS. Import explainers sit in the import page sheet ("Back" chevron to
  Choose source at the left, `x` at the right); the notifications explainer has "Not now" top-left.
- **Android 12 and lower** have no notification permission: `S12-notifications` is skipped (notifications
  are on by default) and the Settings switch controls the channel.
- **Web**: contacts and push are unavailable (PLT-07, PLT-10) and never trigger S12; see §4. The web
  notifications sheet (`S12-notifications-web`) appears where a mobile user would see `S12-notifications`.

## 9. Edge cases

- **Permission revoked while importing** (Android 16 and lower, user turns it off in Settings mid-flow): S13
  detects it on resume and replaces itself with the recovery state; nothing already selected is lost until the
  user leaves.
- **Phone updated from Android 16 to 17**: the next contacts import uses the picker path; a permission
  granted earlier is no longer used (the manifest limits it with `maxSdkVersion="36"`).
- **Managed devices / parental controls** (fallback only, iOS `restricted`): show the iOS denied state with the
  lead "Access to contacts is restricted on this device." and only the CSV alternative.
- **Returning from Settings still denied**: the recovery state stays; no message spam.
- **Very old Android without runtime permissions**: no explainer needed; tile goes straight to S13.
- **Text expansion**: steps wrap to two lines; the Settings path names follow the platform's own wording
  in each language.
- **Offline**: irrelevant; permissions are local.
