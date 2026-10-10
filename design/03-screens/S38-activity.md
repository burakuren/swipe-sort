# S38 Activity and notifications

Frames: `S38-activity.html`. Generator: `tools/generators/S35-S38-collaboration.py` (events from
`02-data/sample-data.json › activity`, ev1–ev6). Related: S06 (notification preferences
`S06-notifications`, `S06-notifications-denied`, `S06-notifications-web`), S12 (push pre-permission
`S12-notifications`), S34, S36, S09, S28, S25.

## 1. Purpose and requirements

One place to see what happened on shared lists, newest first, grouped by day, with unread state, a filter and
a direct way to the screen each event is about. The same events reach the phone as push notifications (per
the preferences in Settings), appear as an in-app banner while SwipeSort is open, and on the web as in-app
notifications only.

Covers: COL-17, COL-18, COL-19, COL-20, COL-21, COL-22, COL-23 (entry to preferences), COL-24 (entry to the
pre-permission), PLT-10, PLT-11, PLT-02, PLT-03, PLT-04, PLT-13–PLT-16, DM-20, GOAL-04, STK-06, STK-07,
A-21 (tab), A-52 (preferences), SCR-38.

## 2. Entry points and exits

| From | How |
| --- | --- |
| Bottom navigation | Tab "Activity" (badge = unread count) |
| Push notification / in-app banner / web toast | Opens the event's target directly; the event is marked read |

| To | How |
| --- | --- |
| S34 `S34-default` | memberJoined, roleChanged (`/l/<id>/members`) |
| S09 `S09-shared` | memberFinished (`/l/<id>`) |
| S36 `S36-default` (Decision Maker) / `S36-non-dm` (others) | newConflicts (`/l/<id>/conflicts`) |
| S28 `S28-shared` | conflictsResolved |
| S25 `S25-shared` | roundStarted (`/l/<id>/sort`) |
| S06 `S06-notifications` (web: `S06-notifications-web`) | App bar "Notification settings" (`data-action="notification-settings"`) |
| S12 `S12-notifications` | "Turn on notifications" on the permission prompt |
| S06 `S06-notifications-denied` | "Turn on in Settings" when notifications are off |
| S08 `S08-default` | Empty state "Go to your lists"; tab Lists |
| `https://swipesort.app/get` | "Get the app" (web) |

Route: `(tabs)/activity`. Feed covers every shared list the user is a member of (newest first).

## 3. Layout and components

1. **AppBar (large title)**: "Activity" (`text-title-1`), IconButtons "Mark all as read" (`check-check`,
   disabled when nothing is unread) and "Notification settings" (`settings-2`).
2. **Tabs (underline)** from components.html: All, Conflicts, Members (filter, decided): Conflicts =
   newConflicts + conflictsResolved (+ rule changes); Members = memberJoined + memberFinished + roleChanged;
   roundStarted shows only under All.
3. Optional top block (one at a time, inside a 16 inset): permission prompt (Group with `bell-ring`, two
   actions), "Notifications are off" neutral Alert, web "Push notifications need the app" neutral Alert, or
   OfflineBanner (strip under the tabs).
4. **Feed**: sections per day ("Today", "Yesterday", then "Oct 3", "Oct 2", "Sep 28"; with a year when not
   the current one). Rows are full-bleed (Row surface, hairline dividers), not cards:
   - Leading: actor Avatar 40 with a 20 event badge bottom-right (`bg-secondary`, event icon 12:
     `user-plus` joined, `flag` finished, `check-check` resolved, `play` round, `user-cog` role); events
     without an actor (new conflicts) use a 40 `bg-conflict` circle with `git-compare-arrows`.
   - Text: event sentence with actor, verb and list name `text-body` (unread: semibold); optional second
     line with the detail ("100 / 100 decided", "Mert decides them.") in `text-body-sm muted`.
   - Trailing: time (`text-caption muted`: "11 min ago" today, otherwise clock time; the section gives the
     day) and the unread dot (10, `bg-primary`). Unread rows also get `bg-primary-soft/40`.
   - Decision Maker rows for conflicts that need them carry an inline text Button "Review".
5. **BottomNav** (Lists, Activity, Settings) with the unread badge on Activity (`bg-destructive`).
6. Overlays: Snackbar above the bottom navigation; in-app banner (Proposed **InAppBanner**: `bg-popover
   rounded-control shadow-overlay`, actor avatar + event badge, title, detail, "now"); web toast (same
   component, bottom-right of the column, with Dismiss).

<!-- Proposed components: ActivityRow (avatar + event badge, two lines, time + unread dot) and InAppBanner / web toast. -->

## 4. States

| Frame | Trigger |
| --- | --- |
| `S38-default` | Today (Oct 10). Deniz (Owner), 2 unread (ev6 "15 conflicts in Wedding guests", Oct 3; ev5 "Selin joined Wedding guests", Oct 2), badge 2. No "finished sorting" or "conflicts resolved" event exists yet: Selin is at 43 / 100 and all 15 conflicts are open |
| `S38-all-read` | "Mark all as read": unread styling and badge gone, snackbar |
| `S38-filter` | Tab Conflicts |
| `S38-filter-members` | Tab Members |
| `S38-member-finished` | Later state, Oct 20 (the only frame with these two events): Selin finished sorting today (100 / 100), Mert resolved 12 conflicts yesterday (3 open, after S37); 2 unread; the older days (Oct 3, Oct 2, Sep 28) stay below |
| `S38-decision-maker` | Mert's feed: "15 conflicts need your decision" with "Review"; "Deniz made you the Decision Maker" |
| `S38-empty` | No shared lists yet (or nothing happened yet) |
| `S38-loading` | First load: skeleton rows |
| `S38-error` | Feed couldn't be loaded |
| `S38-offline` | No connection: last synced feed with time |
| `S38-permission-prompt` | Push permission not asked yet (Android 13+/iOS) and the user is on a shared list |
| `S38-notifications-off` | Permission denied, or the master switch in S06 is off |
| `S38-push-content` | Annotation: title and body of every push, per event (system UI not designed) |
| `S38-in-app-banner` | Moment of Mert's Resolve all (S37): Selin is on another screen (her read-only S35) and gets the banner "Mert resolved 12 conflicts in Wedding guests" |
| `S38-web` | Web, mobile: push unavailable, in-app only, Get the app |
| `S38-web-desktop` | Same moment, web desktop: Deniz reviews conflicts (S36 member view, now 12 / 15 resolved by Mert, card c012) and the toast appears in the browser viewport's top-right corner, outside the phone column, so it covers nothing. No toast while the Activity feed is on screen |
| `S38-large-text` | 200% font scale |
| `S38-ios` | iOS large title and tab bar |

Sample events ev1–ev6, generated from `sample-data.json › activity` (texts adapted to the viewer, times and days from `at`; Sep 28: Round 1 started 7:05 PM with 88 items, Mert joined 9:15 PM, made Decision Maker 9:20 PM). ev4 (memberFinished) is an illustrative future event and appears only in the later-dated `S38-member-finished`; conflictsResolved appears only in frames set after S37 ("Mert resolved 12 conflicts"). ev2/ev5 render as "Mert joined Wedding guests" / "Selin joined Wedding guests"; joining through a Decision Maker invite link renders "Mert joined Wedding guests as Decision Maker" (G1, S33). Push bodies keep the short form because the push title is the list name; the push annotation describes "finishes sorting" and "conflicts resolved" generically ("{Name} finished sorting…").

## 5. Interactions, gestures and transitions

- **Tap a row**: opens its target (push, M3 shared axis X) and marks the event read. Back returns to the feed
  at the same scroll position.
- **Unread**: an event is unread until its row (or its push / banner / toast) is opened, or "Mark all as
  read" is used. Opening the tab does **not** clear unread (decided: unread means "not looked at yet"; the
  badge always equals the number of unread rows). Snackbar "Marked 2 as read" (no undo needed; harmless).
- **Filter tabs**: switch instantly (cross-fade 150 ms); the chosen tab is remembered per device. Empty tab:
  "No conflict activity yet." / "No member activity yet."
- **Pull to refresh** (Android/iOS); live updates otherwise: new events slide in at the top (250 ms) with
  the "Today" section created if needed.
- **Grouping and batching**: events of the same type, list and actor within 10 minutes merge into one row
  ("15 new conflicts"); push notifications for new conflicts are sent at most once per list per hour, with
  the count so far.
- **Permission prompt** (`S38-permission-prompt`): "Turn on notifications" opens S12 explainer → system
  prompt; "Not now" hides the prompt for 30 days. Not shown on web or when permission is decided.
- **Notifications off** (`S38-notifications-off`): "Turn on in Settings" opens S06 notifications (denied
  state links to the system settings). Dismissible; reappears after 30 days.
- **Push** (Android channels / iOS): one channel per event type, named like the S06 switches ("Someone
  joins a list", "Someone finishes sorting", "New conflicts", "Conflicts resolved", "A new round starts",
  "Your role changes"). Tapping a push deep-links (navigation-map §4). Own actions never notify yourself.
- **In-app banner** (app open, any screen except sorting S25 and S36 cards, where it would interrupt): slides
  down below the app bar (250 ms), stays 4 s, swipe up to dismiss, tap opens the target. While sorting, only
  the badge updates.
- **Web**: no push. New events appear in the feed live, raise the badge and show a toast for 6 s
  (top-right of the browser viewport on desktop, top of the column on mobile web) while the tab is open, but only when the Activity feed is not on screen; the browser tab title gets the count
  ("(3) SwipeSort").
- Reduced motion: banners and toasts fade (150 ms); new rows appear without sliding; skeleton is static.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Activity"; "Mark all as read"; "Notification settings" |
| Tabs | "All", "Conflicts", "Members"; group label "Filter activity" |
| Day headers | "Today", "Yesterday", "Oct 3", "Oct 2", "Sep 28" |
| Events (Owner, Oct 10) | "15 conflicts in Wedding guests" / "Mert decides them."; "Selin joined Wedding guests"; "You started Round 1 in Wedding guests" / "88 items"; "You made Mert the Decision Maker" / "Wedding guests"; "Mert joined Wedding guests" |
| Events (Decision Maker, Oct 10, 2 unread) | "15 conflicts in Wedding guests need your decision" / "You're the Decision Maker." + "Review"; "Deniz started Round 1 in Wedding guests" / "88 items"; "Deniz made you the Decision Maker" / "Wedding guests"; "You joined Wedding guests" |
| Other event texts | Main line = actor + verb + list name (domain-model ActivityEvent); role events name the list on the second line. "Mert joined Wedding guests as Decision Maker"; "Deniz made Selin the Decision Maker"; "Nobody is the Decision Maker now"; "Deniz changed the conflict rule to Majority decides"; "Mert resolved 12 conflicts in Wedding guests" / "3 are still open."; "Deniz started Round 2 with 11 items"; "Selin left the list"; new conflicts under Everyone must agree: "3 new conflicts" / "Wedding guests. Members need to match." |
| Times | "now", "11 min ago", clock times from `activity[].at` ("11:45 AM", "5:40 PM", "9:20 PM", "9:15 PM", "7:05 PM") |
| Unread (screen reader) | "Unread." prefix |
| Snackbar | "Marked 2 as read" |
| Permission prompt | "Get notified about shared lists" / "Know when someone finishes sorting or a conflict needs a decision, without opening SwipeSort." / "Not now", "Turn on notifications" |
| Notifications off | "Notifications are off" / "SwipeSort can't send push notifications on this phone. New events still appear here." / "Turn on in Settings" |
| Push (title = list name) | "Selin joined the list."; "Mert joined as Decision Maker."; "Selin finished sorting. 100 / 100 decided."; "3 new conflicts. Mert decides them."; "3 new conflicts need your decision."; "Mert resolved 12 conflicts. 3 are still open."; "Deniz started Round 2 with 6 items."; "Deniz made you the Decision Maker." |
| In-app banner | "Mert resolved 12 conflicts in Wedding guests" / "3 are still open." / "now" (any event uses the same pattern) |
| Web alert | "Push notifications need the app" / "In the browser, new events show up here and as a badge while SwipeSort is open. To get notified on your phone, get SwipeSort for Android or iOS." / "Get the app" |
| Web toast | "Mert resolved 12 conflicts in Wedding guests" / "3 are still open."; "Dismiss" |
| Later state (S38-member-finished) | "Selin finished sorting Wedding guests" / "100 / 100 decided"; "Mert resolved 12 conflicts in Wedding guests" / "3 are still open." |
| Empty | "No activity yet" / "When you share a list, you'll see here when people join, finish sorting or disagree." / "Go to your lists"; filtered: "No conflict activity yet.", "No member activity yet." |
| Loading | (skeleton) screen reader "Loading activity" |
| Error (S40-error treatment) | "Activity couldn't be loaded" / "SwipeSort didn't respond. Check your connection and try again." / "Your lists and decisions are saved on this phone." / "Try again" |
| Offline | "You're offline. Showing activity from your last sync, Oct 10 at 9:30 AM." |
| Bottom nav | "Lists", "Activity", "Settings"; badge label "Activity, 2 unread" |

## 7. Accessibility

- Focus order: title, Mark all as read, Notification settings, tabs (`tablist`), top block, rows (each one
  link: "Unread. 15 conflicts in Wedding guests. Mert decides them. Oct 3, 11:45 AM."), bottom
  navigation. Day headers are headings (`h2`) for quick navigation.
- The event badge and avatar are decorative (the sentence names the actor and event).
- New events while the screen is open are announced politely ("New: Mert resolved 12 conflicts"); the
  in-app banner and toast use `role="status"`.
- Large text (`S38-large-text`): rows grow, the time moves under the text, tabs grow to 56 high; nothing
  truncates.
- Unread is not color-only: semibold text, dot and the "Unread" prefix for screen readers.
- Touch targets: rows ≥ 64; icon buttons 48; "Review" 48.

## 8. iOS and web differences

- **iOS** (`S38-ios`): large title "Activity" (collapses on scroll), trailing bar buttons in `primary`,
  standard tab bar with a red badge; push permission explainer `S12-notifications-ios`; notification
  banners are system UI with the same text; Notification Summary may group them (system).
- **Web, mobile** (`S38-web`): push unavailable (PLT-10) — the alert explains and links "Get the app";
  preferences open `S06-notifications-web` (they control the badge only).
- **Web, desktop** (`S38-web-desktop`): phone layout centered; toasts appear in the top-right corner of the browser viewport (outside the phone column; on mobile web at the top of the column); no permission prompt.
- **Android**: channels per event type; Android 12 and lower have no permission step (notifications on).

## 9. Edge cases

- **Many events**: the feed loads 50 at a time (infinite scroll); events older than 90 days are dropped.
- **Several lists**: the second line always names the list; merging never crosses lists.
- **Left or removed from a list**: its events stay but rows open S40 not-found ("You're no longer on
  Wedding guests").
- **Long list names / names**: wrap to two lines; the time column keeps its width.
- **Actor without a photo**: initials avatar (Selin "SY").
- **Signed out (no account)**: Activity shows the empty state; sharing requires an account (S05).
- **Offline**: last synced feed; Mark all as read works locally and syncs later.
- **Notification preferences off for an event type**: the event still appears in Activity (unread),
  without push.
