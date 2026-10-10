# S12 Pre-permission explainers and permission-denied recovery

Frames: `S12-permissions.html`. Generator: `tools/generators/S11-S15-import.py`.

## 1. Purpose and requirements

Before any system permission prompt (contacts, photos, push notifications), explain why access is needed
and how the data is used, so the user can say yes with confidence. When access was denied, explain how to
recover and always offer a working alternative. One layout for every permission (**PermissionExplainer**,
proposed component) so the pattern scales to future sources.

Covers: SRC-05, SRC-06, SRC-02, COL-24, PLT-02, PLT-07, PLT-08, PLT-10, PLT-11, PLT-16, GOAL-03, SAFE-01,
OUT-01, SCR-12.

## 2. Entry points and exits

| From | When |
| --- | --- |
| S11 Contacts tile | Contacts permission never asked (`S12-contacts`) or permanently denied (`S12-contacts-denied`) |
| S11 Photos tile | Photos permission never asked (`S12-photos`) or denied (`S12-photos-denied`) |
| S31 Invite (first share) / S33 Join | Once, right after a list is first shared or joined, if notification permission is undecided (`S12-notifications`) |
| S38 Activity banner "Turn on notifications" / S06 Notifications switch | Permission undecided → `S12-notifications`; denied → `S12-notifications-denied` |

| To | Trigger |
| --- | --- |
| System permission prompt (out of scope) | "Continue" / "Turn on notifications" / "Allow access" |
| `S13-contacts-import.html#S13-select-default` | Contacts granted (prototype goes to the 88-selected frame; the real first arrival is `S13-default`) |
| `S13-contacts-import.html#S13-ios-limited` | iOS 18 contacts limited to a selection |
| `S18-photos-import.html#S18-default` | Photos granted (full or limited, after `S12-photos-limited-ios`) or "Pick photos with the photo picker" |
| `S14-file-import.html#S14-default` | "Import a CSV instead" |
| `S11-source-picker.html#S11-default` | "Not now" (import explainers) |
| System app settings | "Open settings" (Android `ACTION_APPLICATION_DETAILS_SETTINGS`; iOS `openSettingsURLString`) |
| Origin screen (S09, S38, S06) | Notifications "Not now", close, or after the prompt |

Returning from system settings: the app re-checks the permission on `AppState` "active". Granted →
continue automatically to S13 / S18 (or back to the origin for notifications) with no extra tap. Still
denied → stay on the recovery state.

## 3. Layout and components

Import permissions sit inside the import modal: **AppBar (modal)** "Import" + **ImportStepper** ("Select
items": contacts Step 2 of 5; photos Step 2 of 3 because photos skip field mapping and duplicate review; A-62). Notifications are a
standalone full-screen modal (close only, no stepper).

**PermissionExplainer** (proposed, built from existing tokens):
1. Icon in a 56 circle: `bg-primary-soft text-primary-soft-foreground` for the ask; `bg-muted
   text-muted-foreground` for recovery states (calm, not alarming).
2. Title `text-title-2`, lead `text-body-lg muted` (max 64ch).
3. Either **promise points** (3 rows: icon 24 muted, title `text-label-lg`, one line `text-body-sm muted`),
   a **steps list** (numbered 1–3 in `bg-secondary` circles; a real sequence), an **events group**
   (notifications: ListGroup of 6 rows) or a **thumbnail grid** (limited photos).
4. Bottom actions (shared import pattern, identical to S16–S21): top hairline, optional note
   (`text-body-sm muted`) naming the next system step, primary `h-14` full width, ghost secondary below it.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S12-default` | Same as `S12-contacts` (every screen file has a default frame) |
| `S12-contacts` | Contacts permission not determined (Android) |
| `S12-contacts-denied-once` | Android: the user tapped "Don't allow" once; Android can still show the prompt again, so the primary is "Allow access" |
| `S12-contacts-denied` | Android "don't ask again" state (second denial, `shouldShowRequestPermissionRationale` false after a denial): only Settings can grant it |
| `S12-photos` | Gallery permission not determined (Android) |
| `S12-photos-denied` | Gallery denied: Settings, or the system photo picker (no permission needed) |
| `S12-photos-limited-ios` | iOS "Limit access…" (and Android 14 "Allow limited access", same layout in an Android frame): 24 photos allowed |
| `S12-notifications` | Push permission not determined (Android 13+ `POST_NOTIFICATIONS`) |
| `S12-notifications-denied` | Push denied (Android won't ask again) |
| `S12-notifications-web` | Web: push is unavailable; sheet over Activity explains in-app notifications |
| `S12-contacts-ios` | iOS contacts explainer |
| `S12-contacts-denied-ios` | iOS contacts denied (iOS asks once) |
| `S12-notifications-ios` | iOS push explainer |
| `S12-contacts-large-text` | 200% font scale |

Web contacts: never reaches S12. The S11 contacts tile is the unavailable variant and opens
`S11-web-unavailable` (reason + "Get the app" + "Import a CSV instead"). Web photos use file upload (no
permission). Web notifications: `S12-notifications-web`.

## 5. Interactions and transitions

- "Continue" / "Turn on notifications" / "Allow access" call the platform request (expo-contacts
  `requestPermissionsAsync`, expo-media-library `requestPermissionsAsync`, expo-notifications
  `requestPermissionsAsync`). While the system prompt is up the screen stays as is.
- Result handling: granted → push the next step (shared axis X 300 ms; reduced motion 150 ms fade);
  limited → limited state (photos) or S13 limited (contacts); denied → replace this screen with the
  matching recovery state (cross-fade 150 ms). No error haptic for a denial: it is the user's choice, not
  an error.
- "Not now" returns to S11 (import) or closes the modal (notifications). The notifications explainer is
  shown automatically **once**; after "Not now" it only appears again from the Activity banner or the
  Settings switch.
- "Select more photos" (iOS limited) opens `presentLimitedLibraryPicker`; the count updates on return.
- "Share more contacts" on iOS 18 opens the system contact access picker (handled in S13).

## 6. Copy

| Element | String |
| --- | --- |
| Stepper | "Select items", "Step 2 of 5" (contacts); "Step 2 of 3" (photos) |
| Contacts title | "Allow access to your contacts" |
| Contacts lead | "SwipeSort reads your contacts so you can pick the ones to sort. Here's how they're handled." (large text: "SwipeSort reads your contacts so you can pick the ones to sort.") |
| Contacts points | "Only the contacts you pick" / "You choose on the next screen. Nothing else is imported."; "Kept on this phone" / "Imported contacts stay on this phone until you share or back up the list."; "Your address book isn't changed" / "SwipeSort never edits, adds or deletes contacts. Decisions only change SwipeSort's copy." |
| Contacts note | Android "Next, Android asks you to allow access."; iOS "Next, iOS asks once. Allow full access, or choose contacts to share." |
| Contacts buttons | "Not now", "Continue" |
| Denied once | "SwipeSort can't see your contacts" / "You chose Don't allow. To pick contacts, allow access. Or use a CSV file: most contacts apps can export one." / note "Access only lets SwipeSort read contacts. It never changes your address book." / "Import a CSV instead", "Allow access" |
| Denied (Android) | "Contacts access is off" / "Android won't ask again, so access has to be turned on in Settings. When you come back, your contacts are ready to choose." / steps "Tap Open settings", "Tap Permissions, then Contacts", "Choose Allow" / "Import a CSV instead", "Open settings" |
| Denied (iOS) | "Contacts access is off" / "iOS asks only once, so access has to be turned on in Settings. When you come back, your contacts are ready to choose." / steps "Tap Open Settings", "Tap Contacts", "Choose Full Access" / "Import a CSV instead", "Open Settings" |
| Photos title | "Allow access to your photos" |
| Photos lead | "SwipeSort shows your gallery so you can pick photos to sort. Each photo becomes one card." |
| Photos points | "Only the photos you pick" / "Choose photos or whole albums on the next screen."; "Kept on this phone" / "Photos stay on this phone until you share or back up the list."; "Nothing is deleted" / "Rejecting a photo doesn't delete it. Your gallery isn't changed." |
| Photos note | "Next, Android asks you to allow access to all photos or only some." |
| Photos buttons | "Not now", "Continue" |
| Photos denied | "Photo access is off" / "To browse your gallery in SwipeSort, turn access on in Settings. Or pick photos with Android's photo picker, which needs no access." / steps "Tap Open settings", "Tap Permissions, then Photos and videos", "Choose Allow all" / "Pick photos with the photo picker", "Open settings" |
| Limited photos | "SwipeSort can see 24 photos" / "You allowed access to selected photos only. Sort these, select more, or allow all photos in Settings." / link "Allow all photos in Settings" / "Select more photos", "Continue with 24 photos"; thumbnail overflow "+17" |
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
- The "+17" thumbnail is part of an image group labeled "24 photos allowed, 7 shown".
- Large text (`S12-contacts-large-text`): the content scrolls; the bottom actions stay pinned and grow;
  button labels wrap instead of truncating.
- Notifications sheet on web: `role="dialog"`, focus moves to the sheet title, Escape closes.

## 8. iOS and web differences

- **iOS asks once** per permission. After a denial the app can't show the prompt again, so iOS recovery
  states never offer "Allow access"; only "Open Settings" plus the alternative (`S12-contacts-denied-ios`).
- **iOS 18 contacts** can be limited to selected contacts; S13 then shows only those
  (`S13-ios-limited`). The explainer's note says so ("Allow full access, or choose contacts to share").
- **Limited photos** on iOS (and Android 14+) → `S12-photos-limited-ios`; the user can sort the allowed
  photos immediately.
- **iOS navigation**: import explainers sit in the import page sheet ("Back" chevron to Choose source at the
  left, `x` at the right); the notifications explainer has "Not now" top-left. Settings is written
  "Settings" with a capital S, as on iOS.
- **Android 12 and lower** have no notification permission: `S12-notifications` is skipped (notifications
  are on by default) and the Settings switch controls the channel.
- **Web**: contacts and push are unavailable (PLT-07, PLT-10) and never trigger S12; see §4. Photos use file
  upload. The web notifications sheet (`S12-notifications-web`) appears where a mobile user would see
  `S12-notifications`.

## 9. Edge cases

- **Permission revoked while importing** (user turns it off in Settings mid-flow): S13/S18 detect it on
  resume and replace themselves with the recovery state; nothing already selected is lost until the user
  leaves.
- **Managed devices / parental controls** (iOS `restricted`): show the iOS denied state with the lead "Access
  to contacts is restricted on this device." and only the CSV alternative.
- **Returning from Settings still denied**: the recovery state stays; no message spam.
- **Very old Android without runtime permissions**: no explainer needed; tile goes straight to S13.
- **Text expansion**: steps wrap to two lines; the Settings path names follow the platform's own wording
  in each language.
- **Offline**: irrelevant; permissions are local.
