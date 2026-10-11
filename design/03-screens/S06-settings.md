# S06 Settings

Frames: `S06-settings.html` (generator `tools/generators/S06-settings.py`). Profile and account deletion
are S07. Components: `01-foundations/components.md` (ListGroup and rows, Switch, RadioGroup,
SegmentedControl, AlertDialog, BottomSheet, Alert, Snackbar, OfflineBanner, BottomNav, AppBar).

## 1. Purpose and requirements

One calm place for the account, backup, app preferences and support. Everything a person needs to feel
safe about their data (backup status, lists kept on this phone only, sign-out consequences, privacy in plain
words, the anonymous usage data switch) is one tap away.

Covers: ACC-10, SET-13, SET-01 (entry to profile), SET-02 (entry to connected accounts via S07), SET-03, SET-04, SET-05,
SET-06, SET-07, SET-08, SET-09, SET-10, SET-11, SET-12 (entry: Privacy › Delete account → S07),
COL-23, ACC-01, ACC-02, ACC-03, ACC-04 (backup prompt entry), PLT-09, PLT-10, PLT-11, PLT-14, PLT-16,
PLT-20 (Language sub-page: English is the only language for now), PLT-21, PLT-23, STK-06, STK-07, GOAL-03, VIS-11, VIS-12, VIS-13, TERM-02, SCR-06.

## 2. Entry points and exits

| From | How |
| --- | --- |
| Bottom navigation | Settings tab (`settings` route, tab stack) |
| S38 Activity | Notification preferences link → `S06-notifications` |
| S01 error | "Send a report" → `S06-feedback` |
| S07 Profile | back returns to `S06-default` |

| To | How |
| --- | --- |
| S07 Profile (`S07-profile.html#S07-default`) | Profile row (signed in); Backup › Account row; Privacy › Delete account |
| S05 backup prompt (`S05-sign-in-prompt.html#S05-default`, the backup prompt over Settings) | Not signed in: "Sign in" card on the root; Backup › "Sign in to back up" |
| S22 Template library, manage mode (`S22-template-library.html#S22-default`) | Card templates row |
| S12 notifications explainer (`S12-permissions.html#S12-notifications`) | Notifications › "Turn on notifications" (permission never asked) |
| Android/iOS system settings | Notifications › "Open phone settings" (permission denied) |
| S02 Onboarding (`S02-onboarding.html#S02-default`, the replay entry with Close instead of Skip) | Help › Replay the introduction |
| S08 Home first run (`S08-home.html#S08-first-run`) | After Sign out |
| In-app browser (external) | Help center, Privacy policy, Terms of service, Email support (mail app), Rate SwipeSort (store) |
| App stores | Web: "Get the app" sheet |

Sub-pages push inside the Settings tab stack (bottom navigation stays visible on the root only; sub-pages
hide it, matching the list stacks). Android back and the app-bar back arrow return to the root.

## 3. Layout and components

**Root** (`S06-default`): large-title AppBar "Settings"; scrolling column of ListGroups (`px-4`, 24 dp
between groups, section headers `text-label muted`); BottomNav (Settings active).

1. Profile group: one row, Avatar 56, name `text-title-3`, email `text-body-sm muted`, chevron → S07.
   Not signed in: replaced by the sign-in card (group surface, cloud-off icon, title, one sentence, primary
   "Sign in" button 48 high).
2. **Lists**: Backup (status in the description, icon follows status: `cloud-check` backed up,
   `cloud-off` not backed up or offline; when signed in with lists on this phone only the description adds
   the count: "Backed up. 1 list on this phone only"), Card templates.
3. **Preferences**: Appearance (value = current theme), Haptics (inline Switch row, no sub-page),
   Notifications (value On / Off / In-app only), Language (value English).
4. **Support**: Privacy, Help and feedback, About (value = version).
5. Sign out (button row, neutral color: signing out loses nothing that is backed up). Hidden when not
   signed in.
6. Footer caption "SwipeSort 1.0.0 (142)".

**Sub-pages**: small AppBar (back arrow, title), content `px-4 pt-2`, groups as on the root.
- Appearance: RadioGroup (System, Light, Dark) in a group; footer note.
- Notifications: master "Push notifications" Switch row, then "Notify me when" group of six Switch rows
  (one per ActivityEvent type, `notificationPreferences` in sample data), footer.
- Language: RadioGroup with English only, then an info Alert (primary-soft).
- Backup: centered status block (56 icon circle, `text-title-2` title, one sentence), a group with
  Account, Backed-up lists, Changes waiting (value rows, not tappable except Account → S07), and a secondary
  button "Back up now" / "Try again". Below it, when signed in with lists on this phone only (D-33, A-132,
  A-138): a group headed **"On this phone only"**, one row per list (list icon, name, item count, trailing
  text button "Back up", 48 high) and the footer "Lists on this phone only don't move to a new phone. Back
  them up first." The group is hidden when there are none. Not signed in: status block, primary "Sign in to
  back up", group of lists on this phone (the sample list is not listed: it never moves, D-10).
- Privacy: first a group with the Switch row **"Share anonymous usage data"** (on by default, D-28) and a
  footer saying where it applies; then five short headed paragraphs (`text-title-3` + `text-body muted`,
  max 64ch): What SwipeSort keeps, Contacts, Lists on this phone only, Shared lists, Your original files;
  then a group of links (external-link icon) and "Delete account" (destructive row → S07).
- Help and feedback: two groups (help; "Contact us").
- Send feedback: SegmentedControl "Type" (Idea, Problem, Other; "Report a problem" preselects Problem),
  Textarea "Message" (counter, max 2,000), Switch row "Include device details", reply-to note, bottom
  primary "Send feedback".
- About: mark 64 + "SwipeSort" + version, links group, rate group.
- Open-source licenses: intro sentence and one row per library (name + license); a row opens the full
  license text in a plain scrolling page (platform-default text view, not designed).

**Overlays**: Sign out AlertDialog (Android, web) / action sheet (iOS), with a variant that names lists on
this phone only (A-136); "Get the app" BottomSheet (web); Snackbars "Feedback sent…" and "“{name}” is backed
up".

## 4. States

| Frame | Trigger |
| --- | --- |
| `S06-default` | Signed in (Deniz Yılmaz), online, backed up; "Frontend hiring, Q4" is on this phone only (A-139) |
| `S06-default-end` | Root scrolled to the end: Support group, Sign out, version |
| `S06-guest` | Not signed in (no account): sign-in card, Backup "Not backed up", no Sign out |
| `S06-offline` | No connection: offline banner; Backup "Paused while offline"; everything else works |
| `S06-sign-out` | Sign out tapped, all changes backed up, no list on this phone only |
| `S06-sign-out-device-only` | Sign out tapped with a list on this phone only: the dialog names it (A-136) |
| `S06-sign-out-unsynced` | Sign out tapped while changes are not backed up (offline or backup failing) |
| `S06-appearance` | Appearance row |
| `S06-language` | Language row |
| `S06-notifications` | Notifications row, push permission granted |
| `S06-notifications-not-asked` | Push permission never requested on this device |
| `S06-notifications-denied` | Permission denied in system settings: switches disabled, link to system settings |
| `S06-notifications-web` | Web: in-app only explanation; switches control the Activity badge |
| `S06-backup` | Backed up, nothing waiting; "On this phone only" group with "Frontend hiring, Q4" and Back up |
| `S06-backup-list-backing-up` | "Back up" tapped on a list on this phone only: the row shows "Backing up…" |
| `S06-backup-list-backed-up` | That list is backed up: the group is gone (none left), Backed-up lists 4, snackbar |
| `S06-backup-syncing` | Changes uploading |
| `S06-backup-failed` | Server unreachable or upload failed (also shown while offline, with the offline banner) |
| `S06-backup-guest` | Not signed in |
| `S06-privacy` | Privacy row: usage data switch on top |
| `S06-privacy-end` | Privacy scrolled to the end: paragraphs and links |
| `S06-help` | Help and feedback row |
| `S06-feedback` | Send feedback / Report a problem |
| `S06-feedback-sent` | Sent: back on Help with a snackbar |
| `S06-feedback-error` | Send failed because offline; message kept |
| `S06-about` | About row |
| `S06-licenses` | About › Open-source licenses |
| `S06-large-text` | 200% font scale |
| `S06-ios`, `S06-ios-notifications`, `S06-ios-sign-out`, `S06-ios-sign-out-device-only` | iOS variants |
| `S06-web`, `S06-web-get-app`, `S06-web-desktop` | Web mobile, Get the app sheet, desktop browser |

No loading state: every value on these pages is local (preferences, cached profile, last backup time).
Backup counts refresh in place.

## 5. Interactions, gestures and transitions

- Rows push sub-pages (M3 shared axis X, 300 ms; iOS native push; reduced motion: 150 ms fade).
- Switches and radios apply immediately and persist locally (per device for Appearance, Haptics and Share
  anonymous usage data; per account for notification preferences, synced). No Save buttons.
- **Share anonymous usage data** (D-28): on by default, also without an account. Off stops sending analytics
  events from this device at once (nothing queued is sent later). It is **per device**, not per account: the
  events carry no user or account ID (D-28), people without an account need the same switch, and signing in
  or out must never flip it. The footer says so ("Applies on this phone.").
- **Appearance**: switching theme cross-fades the app (150 ms). "System" follows the OS and updates live.
- **Haptics** switch: when turned on, plays one `selectionAsync()` as confirmation. Off disables every
  haptic in `motion.md §5`.
- **Notifications**: master switch off disables (`aria-disabled`) the event switches but keeps their
  values. "Turn on notifications" opens S12 notifications explainer, then the system prompt; granted →
  `S06-notifications`, denied → `S06-notifications-denied`. "Open phone settings" opens the app's
  system notification settings (`Linking.openSettings()`); on return the page re-checks permission.
- **Back up a list on this phone only** (S06 › Backup): "Back up" needs no confirmation (nothing is lost,
  A-132); the row shows "Backing up…", the list moves to the account like at sign-in, then the row leaves the
  group and the snackbar says "“Frontend hiring, Q4” is backed up" (4 s). Offline it queues: the row says
  "Backs up when you're online" (A-139). Turning backup off is done in S09 (A-134), not here.
- **Backup**: automatic whenever online; "Back up now" starts an upload immediately (button turns into
  "Backing up…", busy) and ends in `S06-backup`. Failure → `S06-backup-failed`; "Try again" retries; the
  app also retries with backoff.
- **Sign out**: dialog with a destructive "Sign out" button (as S40-sign-out; it removes data from this phone). If every change is backed up → "Sign out" signs out, removes backed-up lists from
  this phone and opens `S08-first-run`. Lists on this phone only stay on the phone, **hidden** until the same
  account signs in here again (A-136); the dialog names them (`S06-sign-out-device-only`; two or more: "2
  lists on this phone only stay here, hidden until you sign in again."). Another account or no account never
  sees them. The sample list stays visible (A-139). If changes are waiting → the unsynced dialog: "Sign out anyway"
  (destructive) discards them. Cancel returns to Settings.
- **Send feedback**: Send is disabled until the message has at least 1 non-space character. On success
  the page pops to Help with the snackbar (4 s). On failure the message and choices stay and the inline
  error appears; the button becomes "Try again".
- **Web Get the app**: tapping "Get the app" in an unavailable row opens the sheet; on a phone browser
  only the matching store button is shown (both on desktop).

## 6. Copy

| Element | String |
| --- | --- |
| Root title | "Settings" |
| Profile row | "Deniz Yılmaz", "deniz.yilmaz@example.com"; label "Deniz Yılmaz, deniz.yilmaz@example.com. Profile and account" |
| Sign-in card (not signed in) | "Sign in to back up and share" / "Your 4 lists are on this phone only. With an account they're backed up, and you can decide together with others." / "Sign in" |
| Section headers | "Lists", "Preferences", "Support" |
| Backup row | "Backup"; "Backed up. 1 list on this phone only" (signed in with lists on this phone only; plural "2 lists") / "Backed up today at 09:12" (none, and on web) / "Not backed up. Lists are on this phone only." / "Paused while offline" |
| Card templates row | "Card templates", "Built-in and your own" |
| Appearance row | "Appearance", value "System" / "Light" / "Dark" |
| Haptics row | "Haptics", "Vibrate when you decide"; web: "Haptics need the Android or iOS app." + "Get the app" |
| Notifications row | "Notifications", value "On" / "Off" / "In-app only" |
| Language row | "Language", value "English" |
| Support rows | "Privacy", "Help and feedback", "About" (value "1.0.0") |
| Sign out row | "Sign out" |
| Footer | "SwipeSort 1.0.0 (142)" |
| Offline banner | "You're offline. Changes are saved on this phone." |
| Sign out dialog | "Sign out?" / "Your lists are backed up to deniz.yilmaz@example.com. They'll be removed from this phone until you sign in again." / "Cancel" / "Sign out" |
| Unsynced dialog | "Sign out without backing up?" / "12 changes haven't been backed up because you're offline. Signing out now removes them from this phone, and they can't be recovered." / "Cancel" / "Sign out anyway" |
| Sign out, list on this phone only | "Sign out?" / "Your lists backed up to deniz.yilmaz@example.com leave this phone and come back when you sign in. “Frontend hiring, Q4” stays on this phone, hidden until you sign in again." / "Cancel" / "Sign out" (web: "this browser") |
| iOS action sheet | "Your lists are backed up to deniz.yilmaz@example.com. They'll be removed from this iPhone until you sign in again." / "Sign out" / "Cancel"; with a list on this phone only: "Your lists backed up to deniz.yilmaz@example.com leave this iPhone and come back when you sign in. “Frontend hiring, Q4” stays on this iPhone, hidden until you sign in again." |
| Appearance | "Appearance"; "System", "Match your phone's light or dark setting"; "Light"; "Dark"; "Applies right away on this device." |
| Language | "Language"; "English"; "English only for now" / "More languages are coming, starting with Turkish. SwipeSort will switch automatically when your phone's language is available." |
| Notifications | "Notifications"; "Push notifications", "On this phone" (iOS "On this iPhone"); header "Notify me when"; "Someone joins a list", "Someone finishes sorting", "New conflicts", "Conflicts resolved", "A new round starts", "Your role changes"; footer "Activity always shows every event, whatever you choose here." |
| Not asked | "Turn on push notifications" / "Hear when someone joins, finishes sorting or a conflict needs you. Choose which events below." / "Turn on notifications"; footer "These apply once push notifications are on. Activity always shows every event." |
| Denied | "Notifications are off in your phone's settings" / "Turn them on for SwipeSort in Android settings to get push notifications. Activity still shows every event." (iOS: "in iPhone Settings") / "Open phone settings" |
| Web notifications | "Push notifications need the app" / "In the browser, new events appear in Activity and as a badge while SwipeSort is open." / "Get the app"; header "Show in Activity with a badge"; footer "Events you turn off still appear in Activity, without a badge." |
| Backup, backed up | "Backed up" / "Last backup today at 09:12. Backed-up lists update automatically whenever you're online."; rows "Account" + email, "Backed-up lists" "3", "Changes waiting" "None"; "Back up now" |
| Backup, on this phone only | Header "On this phone only"; row "Frontend hiring, Q4" / "12 items" / "Back up" (accessible name "Back up Frontend hiring, Q4"); progress "Backing up…"; offline "Backs up when you're online"; footer "Lists on this phone only don't move to a new phone. Back them up first."; snackbar "“Frontend hiring, Q4” is backed up" |
| Backup, syncing | "Backing up…" / "Backing up 12 changes. You can keep using SwipeSort."; "Changes waiting" "12"; button "Backing up…" |
| Backup, paused | "Backup paused" / "SwipeSort couldn't reach its servers. Your 12 changes are saved on this phone and back up automatically when the connection works again."; "Last backup" "Yesterday"; "Try again" |
| Backup, not signed in | "Not backed up" / "Your 4 lists are saved on this phone only. Sign in to back them up and open them on other devices." / "Sign in to back up"; header "On this phone only"; rows list name + "100 items" etc. |
| Privacy, usage data | Switch "Share anonymous usage data" (on); description "Events like finishing a round, with no ID that follows you. Never list contents, names or anything you type."; footer "Applies on this phone. The privacy policy lists every event." (web: "Applies in this browser.") |
| Privacy | "What SwipeSort keeps" / "The lists you make: items, fields, decisions and notes. If you sign in, also your name, email and photo."; "Contacts" / "SwipeSort reads only the contacts you choose to import and keeps only the fields you map. On newer phones you choose them in your phone's own contact picker, so SwipeSort sees only the ones you pick." (D-32: photos removed; D-18: system picker); "Lists on this phone only" / "A list you keep on this phone only never leaves it. It isn't backed up, so it can't be recovered if you lose the phone."; "Shared lists" / "Members of a shared list see its items, everyone's decisions and notes. Notes marked private are visible only to you."; "Your original files" / "Imported files and Google Sheets are never changed unless you confirm an export to them."; "Privacy policy", "Terms of service", "Delete account" / "From your profile" |
| Help and feedback | "Replay the introduction" / "See the gesture demo again"; "Help center" / "Guides and answers"; header "Contact us"; "Send feedback" / "Ideas and suggestions"; "Report a problem" / "Something isn't working"; "Email support" / "support@swipesort.app" |
| Send feedback | Title "Send feedback" (from Report a problem: "Report a problem"); "Type": "Idea", "Problem", "Other"; "Message", placeholder "What would make SwipeSort better?" (Problem: "What happened, and what did you expect?"); counter "100 / 2,000"; "Include device details" / "App version, phone model and system version. No lists or contacts."; "We reply to deniz.yilmaz@example.com." (not signed in: field "Email for a reply (optional)"); "Send feedback" |
| Feedback sent | Snackbar "Feedback sent. Thanks for helping improve SwipeSort." |
| Feedback error | Banner "You're offline. Your message stays here; sending needs a connection."; "Couldn't send your feedback" / "You're offline. Your message stays here; send it when you're back online."; "Try again". Server error variant: "Couldn't send your feedback" / "Something went wrong on our side. Your message stays here; try again in a moment." |
| About | "SwipeSort", "Version 1.0.0 (142)", "Terms of service", "Privacy policy", "Open-source licenses", "Rate SwipeSort" / "On Google Play" (iOS "On the App Store") |
| Licenses | "Open-source licenses"; "SwipeSort is built with these open-source projects. Tap one to read its license."; rows "Expo" MIT, "React Native" MIT, "React Native Reusables" MIT, "NativeWind" MIT, "react-native-gesture-handler" MIT, "react-native-reanimated" MIT, "expo-haptics" MIT, "Inter typeface" "SIL Open Font License 1.1", "Lucide icons" ISC |
| Get the app sheet (web) | "Get SwipeSort for your phone" / "Haptics, push notifications and importing phone contacts need the app. Your lists come with you when you sign in." / "Get it on Google Play" / "Download on the App Store" |
| Back buttons (labels) | "Back to Settings", "Back to Help and feedback", "Back to About"; iOS "Settings" |
| Bottom navigation | "Lists", "Activity" ("Activity, 3 unread"; no badge when not signed in, since there is no shared activity), "Settings" |

## 7. Accessibility

- Root focus order: title, profile row (or sign-in card), Lists group, Preferences, Support, Sign out,
  bottom navigation. Section headers are headings (`h2`) so screen-reader users can jump between groups.
- Each row is one target (≥ 56 high) whose label includes its value ("Appearance, System"); switch rows
  expose `role=switch` with the row title as name and the description as hint. Radios use a radiogroup
  named after the page.
- Disabled switches (`S06-notifications-denied`, web Haptics) use `aria-disabled`; their explanation is
  never dimmed and is read as the hint. The "Get the app" link is a separate focus stop.
- Backup status blocks are `role=status`; changes (syncing → backed up) are announced politely. Each "Back
  up" button in the "On this phone only" group names its list; "Backing up…" is a polite status.
- The usage data switch is `role=switch` named "Share anonymous usage data", with its description as the
  hint; the footer is read after it.
- Dialogs trap focus; initial focus on "Cancel" (the safe action), especially for "Sign out anyway".
- The SegmentedControl segments are 40 high inside a 48 high track; the whole track half is the target
  (lint warning reviewed and accepted).
- Large text (`S06-large-text`): rows grow to two lines, values move under the title, only the email
  truncates; bottom navigation labels grow to `text-label`.
- Reduced motion: page pushes and the theme switch use a 150 ms fade; the backup spinner becomes a static
  `refresh-cw` icon with "Backing up…".
- Contrast: every pair from tokens (`contrast.md`); external-link and chevron icons are decorative.

## 8. iOS and web differences

- **iOS** (`S06-ios`, `S06-ios-notifications`, `S06-ios-sign-out`): inset grouped lists (radius 12),
  large title that collapses on scroll, iOS tab bar (tint only, no pill), sub-pages pushed with a back
  chevron labelled "Settings" and the edge-swipe back gesture, native UISwitch. Sign out confirms with an
  action sheet (destructive "Sign out" + "Cancel"); with a list on this phone only the message names it
  (`S06-ios-sign-out-device-only`). Denied notifications link to iPhone Settings. Rate
  opens the App Store review sheet (`StoreReview.requestReview()` first, store page as fallback).
- **Web, mobile** (`S06-web`): same layout without system bars. Haptics row unavailable (muted title,
  switch at 50% opacity, reason + "Get the app" at full contrast). Notifications value "In-app only" and
  its page (`S06-notifications-web`) explains push needs the app; the switches then control the Activity
  badge. "Get the app" opens `S06-web-get-app`. Rate SwipeSort is hidden on web.
- **Web, desktop** (`S06-web-desktop`): the phone layout centered; same content as web mobile.
- **Web, lists kept in this browser only**: device-only lists are per device, so the web Backup row shows
  "Backed up today at 09:12" in the sample world (Deniz's "Frontend hiring, Q4" is on her phone, not in this
  browser). When a browser has such lists, Backup's group reads "On this browser only" with the footer
  "Lists on this browser only don't move to other devices, and browsers can clear lists you haven't opened
  for a while. Back them up first." (D-08). The usage data footer reads "Applies in this browser" there.
- **Android** is the reference. Rate opens the Google Play in-app review flow.

## 9. Edge cases

- **Not signed in**: no profile or Sign out; Backup row and page explain lists are on this phone only; all
  preferences work. Notification preferences still save (they matter once lists are shared). The usage data
  switch works the same.
- **Sample list** ("Desk setup (sample)", D-10, A-139): never counted or listed in Backup (not signed in or
  signed in), never moved at sign-in, never removed at sign-out; it has no Back up button.
- **Lists on this phone only and a new phone**: they are not in the account, so a new phone never receives
  them (footer, A-138). Deleting the account keeps them on this phone without an account (S07).
- **Several lists on this phone only**: one row each, ordered by latest activity; the root row counts them
  ("Backed up. 2 lists on this phone only").
- **Device-only lists and unsynced changes**: they never have changes waiting (they don't sync), so the
  unsynced sign-out dialog counts only backed-up lists' changes.
- **Offline**: Backup shows paused; Send feedback fails gracefully and keeps the text; signing out while
  changes wait shows the unsynced dialog. Everything else works offline.
- **Backup failing for days**: "Last backup" shows the date ("Oct 2"); the root row reads "Backup paused"
  and Home shows the not-backed-up indicator (S08).
- **Long names and emails**: the profile name wraps to 2 lines; the email truncates in the middle on the
  root and wraps in S07.
- **Text expansion (+40%)**: row values ("In-app only" → "Yalnızca uygulama içi") wrap under the title
  when they would collide with the title; group headers wrap.
- **Permission changed outside the app** (granted or revoked in system settings): Notifications re-reads
  the permission on every focus and switches between `S06-notifications` and `-denied`.
- **Theme "System" at night**: the app follows OS changes live without a restart.
- **Sign out with a sort in progress**: progress is saved and backed up first (if online); offline goes
  through the unsynced dialog.
- **Account deleted on another device**: the next sync signs the user out and opens S08 first run with a
  snackbar "You were signed out because this account was deleted."
