# S33 Join a list

Frames: `S33-join-list.html`. Generator: `tools/generators/S31-S34-collaboration.py`. Related: S32 (link
opening), S25 (sorting), S09 (list overview), S34 (members).

## 1. Purpose and requirements

The signed-in invited person confirms they want in: who invited them, which list, their role and what it
means, who else is on the list and how far they are, and that they will sort every item of the current
round with others' decisions hidden. One tap joins and starts sorting.

Covers: COL-06, COL-04 (web join without installing), COL-05, DM-02, DM-09 (Decision Maker variant),
DM-10 (role moves on join), DM-16, SRT-12 (hidden by default note), PLT-02, PLT-03, PLT-04, PLT-13–PLT-16,
PLT-21, PLT-23, GOAL-04, VIS-12 (Join → Joining… → "You joined Wedding guests"), SCR-33, SUC-05, DEL-24.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S32 `S32-app` | App opened from the link, signed in |
| S03 `S03-web-desktop` | After sign-in from "Sign in to join" (flow 3) |
| S32 `S32-web-signed-in` | Browser already signed in |

| To | How |
| --- | --- |
| S25 `S25-shared` (app) / `S25-web-desktop` (web) | "Join and start sorting" (`data-action="start-sorting"` in `S33-web-desktop`, `join` in `S33-default`) |
| S09 `S09-shared` | "Join list" when no round is in progress |
| S08 `S08-default` | Close (`x`) / iOS "Cancel" without joining; "Back to my lists" after a join error |
| S03 `S03-web-desktop` | "Switch account" (web) |
| S32 `S32-get-app` | "Get the app" (web) |

## 3. Layout and components

Full-screen modal (app) or the web page (web). Top to bottom:

1. AppBar (modal): close + "Join a list". Web: brand header with "Get the app" (desktop) and the account
   chip. iOS: nav bar with "Cancel" and centered "Join a list".
2. Hero: inviter Avatar 40 + "{Name} invited you" (`text-body-lg`); list name `text-title-1`; "100 items,
   Round 1 in progress".
3. Optional Alerts: Decision Maker move note (info), link reset error (error), no-round note (info),
   offline banner under the app bar.
4. **Your role** ListGroup of three InfoRows (Proposed: non-interactive rows with icon, title and
   description):
   - role: `user-round` Collaborator / `gavel` Decision Maker, with what the role can do;
   - `list-checks` "All 100 items of Round 1" (DM-16);
   - `eye-off` "Others' decisions are hidden" (SRT-12 default).
5. **Members ({n})** ListGroup of MemberRows: avatar 40, name, role text with icon (`crown` Owner, `gavel`
   Decision Maker) and "76 / 100 decided" on one line, Progress bar below. Progress is shown, decisions
   are not.
6. Sticky footer: primary "Join and start sorting" (lg 56) + "Joining as {name}." (+ "Switch account" link
   on web).

The joined step (`S33-joined`) is S25 shared with a snackbar; it is shown here to complete the flow.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S33-default` | Selin (signed in, app) opens a valid Collaborator invite from Deniz while Round 1 is in progress. Members: Deniz (Owner, 76 / 100), Mert (Decision Maker, 85 / 100) |
| `S33-joining` | "Join and start sorting" pressed: button shows spinner and "Joining…", disabled |
| `S33-joined` | Joined: S25 shared opens at item 1 of Round 1, 0 / 100 decided, snackbar "You joined Wedding guests" |
| `S33-decision-maker` | Mert opens Deniz's Decision Maker link (variant): role row explains resolving conflicts; info note that the role moves from Deniz |
| `S33-web-desktop` | Flow 3: Mert after signing in on the desktop browser; joins as Collaborator; only Deniz is on the list |
| `S33-web` | Same on a mobile browser, with the app banner |
| `S33-loading` | Invite details loading: skeleton, button disabled |
| `S33-offline` | No connection: offline banner, button disabled with the reason above it |
| `S33-error-link-reset` | The link was reset (or turned off) between opening and pressing Join: error Alert, "Back to my lists" |
| `S33-no-round` | The list has no round in progress (Round 1 complete): "Join list" goes to the list overview |
| `S33-large-text` | 200% font scale |
| `S33-ios` | iOS |

Other errors on Join (server did not answer): snackbar "Couldn't join. Check your connection and try
again." with "Try again"; the button returns to its rest state.

## 5. Interactions, gestures and transitions

- **Join and start sorting**: creates the membership (role from the link), then replaces S33 with S25 for
  the current round (shared transition: S33 fades out, S25 slides up 300 ms emphasizedDecelerate;
  reduced motion: 150 ms cross-fade). The snackbar "You joined Wedding guests" shows on S25 for 4 s.
  First-time sorters see S25 coach marks first (`S25-coach-1`), then the snackbar.
- **Decision Maker link**: joining makes the person the Decision Maker and turns it off for the previous
  holder; an activity event "Deniz made Mert the Decision Maker" is not generated (it was the Owner's
  invite choice); instead "Mert joined as Decision Maker" (S38 memberJoined with role).
- **Activity**: every join creates "Selin joined Wedding guests" for the other members (COL-17).
- **Close / Cancel / system back**: leaves without joining; the link keeps working until it expires.
- **Switch account** (web): signs out and returns to S03 web with the same `next` token.
- **Offline**: the button is disabled; when the connection returns the banner disappears and the button
  enables without a reload.
- **Link reset while open**: detected on Join; the error replaces the role/round alerts at the top and the
  footer swaps to "Back to my lists".

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Join a list"; close label "Close"; iOS "Cancel" |
| Hero | "Deniz Yılmaz invited you"; "Wedding guests"; "100 items, Round 1 in progress" (no round: "100 items, no round in progress") |
| Section | "Your role" |
| Collaborator row | "Collaborator" / "You sort every item and add notes. You can invite others as Collaborator." |
| Decision Maker row | "Decision Maker" / "You sort every item and resolve conflicts. Under the current rule, Decision Maker decides, your choice on a conflict is final." (rule Majority: "…and break ties when the majority is split."; rule Everyone must agree: "…Conflicts stay open until everyone agrees; you can review them like everyone else.") |
| Round row | "All 100 items of Round 1" / "Everyone sorts every item of the round." |
| Hidden row | "Others' decisions are hidden" / "While you sort, so nobody sways you." |
| Decision Maker note | "Deniz is the Decision Maker now. The role moves to you when you join." |
| Members | "Members (2)"; "Owner", "Decision Maker", "Collaborator"; "76 / 100 decided" |
| Primary | "Join and start sorting"; busy "Joining…" |
| Identity | "Joining as Selin Yılmaz." / web: "Joining as Mert Aydın. Switch account" |
| Web header | "Get the app"; account chip "Mert" (label "Account: Mert Aydın") |
| Snackbar | "You joined Wedding guests" |
| Offline | Banner "You're offline."; above the button: "Joining needs a connection. Connect and try again." |
| Link reset error | "This invite link was reset" / "Deniz made a new link while you were here, so this one can't be used to join. Ask Deniz for the new link." / "Back to my lists" |
| Join failed | "Couldn't join. Check your connection and try again." / "Try again" |
| No round | "Round 1 is complete. You can see the results now. When Deniz starts the next round, you'll sort it with everyone." / "Join list" |
| Loading (screen reader) | "Loading invite" |

## 7. Accessibility

- Focus order: Close, inviter line, list name (heading), alerts, role rows (read as text), members (each
  row: "Deniz Yılmaz, Owner, 76 of 100 decided"), Join button, identity line, Switch account.
- Progress bars have labels ("Deniz: 76 of 100 decided").
- The Join button announces busy state ("Joining…") and the result snackbar politely.
- Error and offline notices are `role="alert"` / `role="status"`; the disabled reason stays at full
  contrast.
- Large text (`S33-large-text`): the hero title becomes `text-display`, rows wrap, member counts move under
  their bars, the footer keeps only the button (the identity line moves into the scroll area).
- Touch targets: button 56, Switch account ≥ 48 high, close 48.
- Reduced motion: transitions become cross-fades; no other animation except the busy spinner (static with
  reduced motion).

## 8. iOS and web differences

- **iOS** (`S33-ios`): presented as a full-screen modal with "Cancel" (text button, top-left) instead of the
  close icon and a centered title; edge-swipe back does not apply (modal); swipe-down dismiss is enabled.
- **Web, desktop** (`S33-web-desktop`): brand header with "Get the app" (opens the QR dialog) and the
  account chip; "Switch account" in the identity line; after joining, S25 web with keyboard hints
  (`S25-web-desktop`).
- **Web, mobile** (`S33-web`): app banner on top, same content; "Get the app" lives in the banner.
- Push notifications after joining: not on web (in-app activity only, PLT-10); no prompt is shown here.
  On Android/iOS the notification pre-permission (S12 `S12-notifications`) is offered later, after the
  first sorting session, not during joining (keeps the first decision fast).

## 9. Edge cases

- **Joining late**: the member starts at item 1 of the current round regardless of others' progress
  (DM-16); their progress starts at 0 / 100.
- **Round ends while on S33**: the screen switches to the no-round variant on Join.
- **Decision Maker link but the role was taken meanwhile**: the role row shows Collaborator and an info
  note "Mert joined as Decision Maker first, so you'll join as Collaborator." (same copy as
  `S32-role-changed`).
- **Already a member** (e.g. joined on another device): S32 `S32-already-member` instead of S33.
- **Many members**: the members group shows 5 and "Show all 8 members" (expands in place).
- **Long names**: names wrap; role text and counts wrap to a second line instead of truncating.
- **Very large lists**: counts use thousands separators ("All 1,204 items of Round 2").
- **Guest lists on the device**: if the person used the app as a guest before, signing in to join moves
  their lists to the account first (S05 moving step); the join continues afterwards.
