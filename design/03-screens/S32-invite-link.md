# S32 Opening an invite link

Frames: `S32-invite-link.html`. Generator: `tools/generators/S31-S34-collaboration.py`. Related: S31 (sender),
S33 (join), S03 (web sign-in), S09 (list), navigation-map §4 (deep links).

## 1. Purpose and requirements

Turn `https://swipesort.app/join/<token>` into the shortest path to sorting: open the app when it is
installed; otherwise open the web app, where the person sees who invited them, the list, their role and
the members, signs in and joins without installing anything. Every way a link can fail has a clear,
non-technical page.

Covers: COL-03, COL-04, COL-05, COL-06 (preview part), PLT-03, PLT-04, PLT-11 (get the app pattern),
PLT-13–PLT-16, PLT-21, PLT-23, ACC-03, ACC-06/ACC-07 (via S03), DM-16 (join copy), GOAL-04, VIS-13,
SCR-32, SUC-05, DEL-24 (flow 3).

## 2. Entry points and exits

| From | How |
| --- | --- |
| Invite link tapped on Android with the app installed, not signed in | Android App Link → app → `S32-default` (in-app invite preview) |
| Invite link tapped on Android with the app installed | Android App Link → app → `S32-app` |
| Invite link on iPhone with the app installed | Universal Link → app → `S32-app` (same screen) |
| Link opened in a mobile browser without the app | `S32-web` |
| Link opened in a desktop browser | `S32-web-desktop` (prototype flow 3, Mert on his laptop) |
| Prototype | `S31-link-copied` [`partner-opens-link`] |

| To | How |
| --- | --- |
| S03 `S03-web-desktop` | "Sign in to join" (`data-action="sign-in-to-join"` in `S32-web-desktop`). After sign-in, S03 returns to S33 `S33-web-desktop` with the token kept |
| S33 | App: automatically after `S32-app`. Web, already signed in: automatically after `S32-web-signed-in` |
| `S32-get-app` dialog (desktop) / app store (mobile) | "Get the app" |
| S09 `S09-shared` | "Open list" (already a member) |
| S08 `S08-default` | "Open SwipeSort" on dead links, close in the app |

## 3. Layout and components

**Web invite preview** (`S32-web-desktop`, `S32-web`, `S32-role-changed`): a public page in the phone
layout (centered 412 dp column on desktop, PLT-04).

1. Brand header (64): logo mark + "SwipeSort" (`text-title-3`); right slot for the account chip when signed
   in. Hidden on mobile web when the app banner is shown (the banner already names the app).
2. Hero: inviter Avatar 56 + "{Name} invited you to sort a list together" (`text-body-lg`); list name
   `text-title-1` (`h1`); "100 items, Round 1" (`text-body muted`).
3. Role card (`rounded-group bg-card`): icon in a `secondary` circle, "You'll join as {Role}" and one
   sentence on what it means. Role-changed variant adds an info Alert inside the card.
4. Members ListGroup: avatar 32, name, role words. No progress or decisions are shown before sign-in.
5. Primary "Sign in to join" (lg 56) + "No download needed. Sort right here in your browser."
6. Desktop only: divider + "Prefer the app? …" + outline "Get the app".

**AppBanner** (Proposed, mobile web): 56 high strip at the top: close (48), app icon 40, "SwipeSort" /
"Sort with swipes in the app", outline "Get the app". On iOS Safari the native Smart App Banner
(`apple-itunes-app` meta tag) replaces it.

**Get the app dialog** (desktop): AlertDialog-styled Dialog with a real QR code (version 2-L, 160 dp,
encodes `https://swipesort.app/get`, which redirects to the right store), the URL as text, and "Close".
The QR tile stays dark-on-light in both themes (`bg-card text-foreground`, dark: `bg-foreground
text-background`) because cameras often fail on inverted codes.

**App opening** (`S32-app`): centered logo mark 64, spinner + "Opening {list}…", "Invite from {name}".

**Status pages** (expired, reset, invalid, deleted, offline, already a member): EmptyState pattern: 56
icon circle, `text-title-2` title, one sentence, one action.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S32-default` | App installed, nobody signed in (new install or guest): the invite preview inside the app with "Sign in to join" → S03 `S03-default` → S33. Note: "Lists on this phone move to your account when you sign in." |
| `S32-web-desktop` | Valid link, desktop browser, not signed in (flow 3) |
| `S32-web` | Valid link, mobile browser without the app, not signed in |
| `S32-get-app` | "Get the app" on desktop |
| `S32-web-signed-in` | Valid link, browser already signed in: < 1 s "Opening Wedding guests…" with the account chip, then S33 web (sign-in is skipped) |
| `S32-loading` | Web page waiting for the invite details (skeleton) |
| `S32-app` | App installed: link opens the app; the invite is checked, then S33 replaces this screen |
| `S32-already-member` | The signed-in person is already a member (here Mert, Decision Maker) |
| `S32-offline` | App opened from a link without a connection |
| `S32-expired` | Token older than 14 days |
| `S32-reset` | Token revoked by "Reset link" or "Turn off" |
| `S32-invalid` | Token unknown or malformed (incomplete copy) |
| `S32-list-deleted` | The list was deleted by its Owner |
| `S32-list-archived` | The list is archived (read-only until restored) |
| `S32-role-changed` | The link was a Decision Maker link but the role is already taken (someone joined with it first, or the Owner gave the role to someone else): the person joins as Collaborator |

When the app opens from a link and the person is not signed in (guest), S03 opens first with the same
"Sign in to join" context and returns to S33 (the app equivalent of the web flow). A guest's device lists
move to the account at that point (S05 moving step, ACC-05).

## 5. Interactions, gestures and transitions

- **Link resolution order**: (1) app installed → App Link / Universal Link opens the app; (2) otherwise the
  web app renders the preview; (3) signed-in browser → S33 directly after `S32-web-signed-in`.
- **Sign in to join**: navigates to S03 web with `?next=/join/<token>`; after Google or email sign-in the
  web app opens S33 (`S33-web-desktop`), never the home screen.
- **Get the app**: desktop opens the dialog; mobile web opens the store for the platform (Google Play on
  Android, App Store on iOS). The token is passed through the store install (deferred deep link) when
  available; otherwise the person opens the link again after installing.
- **Banner close**: hides the banner for this browser session.
- **Open list** (already a member): replaces S32 with S09 shared.
- **Try again** (offline): retries the token check; success → S33.
- **Open SwipeSort** on dead links: web → home (S08, or sign-in when signed out); app → S08.
- Prototype: in `S32-app` and `S32-web-signed-in` the whole loading area is a link to S33 (the app moves on by
  itself; the link only stands in for that).
- Transitions: app loading → S33 cross-fade 150 ms (no slide, it is a replacement). Web page loads show
  the skeleton for at most a short moment; no spinners on the web preview.
- Reduced motion: spinner becomes a static `loader-circle` icon with the same text; skeleton is static.

## 6. Copy

| Element | String |
| --- | --- |
| Brand | "SwipeSort" |
| Hero | "Deniz Yılmaz invited you to sort a list together" ("{inviter} invited you to sort a list together") |
| List | "Wedding guests"; "100 items, Round 1" (no round: "100 items") |
| Role card, Collaborator | "You'll join as Collaborator" / "You sort every item on your own. Your decisions count toward each item's final decision." |
| Role card, Decision Maker | "You'll join as Decision Maker" / "You sort every item and resolve conflicts. Under the current rule, your choice on a conflict is final." |
| Role changed note | "This invite was for the Decision Maker role. Mert Aydın joined in that role first, so you'll join as Collaborator." Owner-changed variant: "Deniz changed this invite to Collaborator, so you'll join as Collaborator." |
| Members | "Members (1)"; role words "Owner, Decision Maker" / "Owner" / "Decision Maker" / "Collaborator" |
| Primary | "Sign in to join" |
| Reassurance | "No download needed. Sort right here in your browser."; in-app (`S32-default`): "Lists on this phone move to your account when you sign in." |
| Desktop app prompt | "Prefer the app? It works the same, with haptics and push notifications." / "Get the app" |
| App banner | "SwipeSort" / "Sort with swipes in the app" / "Get the app"; close label "Close banner" |
| Get the app dialog | "Get SwipeSort on your phone" / "Scan the code with your phone's camera, or search for SwipeSort in Google Play or the App Store. Your invite works in the app too." / "swipesort.app/get" / "Close"; QR label "QR code for swipesort.app/get" |
| Signed in | "Opening Wedding guests…" / "Signed in as Mert Aydın"; account chip label "Account: Mert Aydın" |
| App opening | "Opening Wedding guests…" / "Invite from Deniz Yılmaz" |
| Already a member | App bar "Invite"; "You're already in Wedding guests" / "You joined on Sep 28. You're the Decision Maker." (Collaborator: "You joined on Oct 2 as Collaborator.") / "Open list" |
| Offline | Banner "You're offline."; "Connect to open this invite" / "Joining a list needs a connection. The link keeps working until it expires, so you can try again later." / "Try again" |
| Expired | "This invite link expired" / "Invite links work for 14 days. Ask Deniz Yılmaz to send you a new one." / "Open SwipeSort" |
| Reset | "This invite link was reset" / "Deniz Yılmaz made a new link, so this one stopped working. Ask Deniz for the new link." / "Open SwipeSort" |
| Turned off by the Owner | Same page as reset: "This invite link was turned off" / "Ask Selin Yılmaz or the list's Owner for a new link." |
| Invalid | "This invite link doesn't work" / "Check that you copied the whole link, or ask the person who sent it for a new one." / "Open SwipeSort" |
| Deleted | "This list was deleted" / "Its Owner deleted it, so there's nothing to join." / "Open SwipeSort" |
| Archived | "This list is archived" / "Its Owner archived it, so it can't take new members right now. Ask Deniz Yılmaz to restore it." / "Open SwipeSort" |
| Loading (screen reader) | "Loading invite" |
| Link preview (Open Graph, for chat apps) | Title "Join Wedding guests on SwipeSort"; description "Deniz Yılmaz invited you to sort 100 items together." |

## 7. Accessibility

- The list name is the page's `h1`; the inviter sentence precedes it in reading order so screen readers
  hear "Deniz Yılmaz invited you to sort a list together. Wedding guests, heading level 1".
- Focus order (web): banner close, Get the app (banner), brand, role card (static text), members, Sign in
  to join, Get the app (desktop).
- The QR code has a text alternative and the URL is printed below it, so nobody depends on the camera.
- Skeleton and app loading are `role="status"` with `aria-busy`; status pages use a heading and a single
  action.
- Avatars next to names are decorative (`alt=""`); the inviter's name is in the text.
- Centered status text uses `text-wrap: balance`, and names ("Wedding guests", "Deniz Yılmaz") never break
  across lines.
- Contrast: all text on `background`/`card` uses foreground or muted-foreground tokens (AA in both themes).
- Large text: the preview is a single column; titles wrap; buttons grow in height. The desktop column keeps
  412 dp and scrolls.
- Reduced motion: no animation besides the spinner, which becomes static.

## 8. iOS and web differences

- **iOS app**: identical to `S32-app` (Universal Link). No separate frame: nothing differs visually; Sign in
  with Apple is available in the S03 step that follows for signed-out people (ACC-08).
- **iOS Safari without the app**: the native Smart App Banner replaces the in-page AppBanner (system UI,
  out of scope); the page is otherwise `S32-web`.
- **Android browser without the app**: in-page AppBanner (`S32-web`), "Get the app" opens Google Play.
- **Desktop web** (`S32-web-desktop`, `S32-get-app`, `S32-web-signed-in`): the phone layout centered;
  "Get the app" opens the QR dialog instead of a store.
- Web is fully functional: sign in, join and sort without installing (SUC-05). Push and haptics are the
  only differences after joining (handled in S25/S38 as web-unavailable features).

## 9. Edge cases

- **Signed in with a different account than intended**: S33 shows "Joining as {name}" with "Switch account"
  (web) so the person can change accounts before joining.
- **Owner opens their own link**: treated as already a member ("You're already in Wedding guests").
- **Removed member opens an old link**: if the link is still valid they can join again (the Owner removed
  them, but links are the Owner's control: reset the link to prevent it). Their old decisions return only
  if they were kept (DM-17).
- **Long list or inviter names**: wrap; the list name wraps to three lines max in the preview.
- **Lists with many members**: the preview shows up to 5 members and "+3 more".
- **List is archived** (`S32-list-archived`): "This list is archived" / "Its Owner archived it, so it
  can't take new members right now. Ask Deniz Yılmaz to restore it." with "Open SwipeSort".
- **Token for a list at its member limit**: no member limit in this version (any number of people,
  COL-01).
- **Offline on web**: the browser's own offline page appears (out of scope); a cached web app shows
  `S32-offline` copy inside the web layout.
- **Privacy**: the public preview shows names and roles of members, never items, decisions, notes or
  progress. Dead links never show list content.
