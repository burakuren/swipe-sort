# S31 Invite (sender side)

Frames: `S31-invite.html`. Generator: `tools/generators/S31-S34-collaboration.py`. Related: S32 (what the
invited person sees), S33 (join), S34 (members), S05 (sign-in prompt), S40 (dialog pattern).

## 1. Purpose and requirements

Share a list by link: choose the role the link grants, then copy it or hand it to the system share sheet.
The sheet also shows who is already on the list, when the link expires, and lets the person reset it.

Covers: ACC-10, COL-01, COL-02, ACC-03, ACC-04 (routing to S05), DM-10 (Decision Maker invite moves the role),
DM-16 (intro copy: everyone sorts every item), GOAL-04, PLT-02, PLT-03, PLT-04, PLT-14, PLT-15, PLT-16,
PLT-21, PLT-23, OUT-01 (system share sheet not designed), VIS-11–VIS-13, SCR-31, DEL-24 (flow 3 start).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S09 list overview (shared or about to be shared) | "Invite" / "Share" action. A guest is routed to S05 `S05-share` first; after sign-in and moving lists (`S05-moved`), S31 opens (prototype flow 3) |
| S10 `S10-share-backup` (signed in, list on this phone only) | "Back up and share": the list backs up first (D-33, A-133, A-177); S31 opens with the snackbar "“{name}” is backed up" (4 s, S40 rules). Not drawn as its own frame: same layout as `S31-default` |
| S34 members | App bar `user-plus` "Invite people", "Invite people" row (→ `S31-default`), "Invite links" row (→ `S31-pending`) |
| S34 collaborator / Decision Maker view | "Invite people" (→ `S31-collaborator`) |

| To | How |
| --- | --- |
| System share sheet (out of scope) | "Share…" (Android `Intent.ACTION_SEND`, iOS `UIActivityViewController`, web `navigator.share`) |
| Clipboard | "Copy link" → snackbar "Invite link copied" |
| Reset dialog (in S31; same pattern as S40) | "Reset link" |
| S05 `S05-share` | "Sign in" in the signed-out state |
| Origin (S09 or S34) | Close (`x`), system back, swipe down on the sheet; iOS "Done" |
| Prototype only | `S31-link-copied` [`partner-opens-link`] → `S32-invite-link.html#S32-web-desktop` |

Prototype flow 3: `S05-moved` → `S31-default` [`copy-link`] → `S31-link-copied` [`partner-opens-link`] →
`S32-web-desktop`.

## 3. Layout and components

Full-height BottomSheet (Proposed variant **FullHeightSheet**, see below) over the origin screen: scrim
`bg-scrim/50`, sheet `top-4` (16 dp below the status bar), `rounded-t-sheet`, `shadow-sheet`, surface
`bg-background` so the grouped lists inside read like a page. Top to bottom:

1. Handle (32×4) and title row: "Invite to {list name}" (`text-title-2`) + close IconButton.
2. Intro (`text-body-sm muted`): what invited people do.
3. **Invite as** (section label + ListGroup, `role="radiogroup"`): two radio rows with one-line
   explanations. Collaborator is preselected. Decision Maker only appears for the Owner.
4. **Invite link**: label + read-only Input (`link-2` icon, `swipesort.app/join/<token>`), the role line
   ("Anyone with the link can join as Collaborator."), expiry with `clock` icon, "Reset link" text button
   (48 target) on the right.
5. Optional **Active invite links** group (`S31-pending`).
6. **Members ({n})** ListGroup: avatar 32, name ("(you)" for the viewer), role words. Footer when alone:
   "Nobody else has joined yet…".
7. Sticky footer (`border-t bg-background`): "Copy link" (primary, lg 56, `copy` icon) and "Share…"
   (secondary, 48, `share-2` icon; iOS uses `share`). Content scrolls under the footer.

Overlays: Snackbar in a slot directly above the sticky footer (the scroll area ends above it, so it never covers a row), AlertDialog (reset), loading spinner text.

**Link model** (refines A-36): every member who can invite has their **own** link (so S32 can say who
invited you). The Owner's link can be switched to Decision Maker; a Decision Maker link works for one
person and then invites as Collaborator again. Links expire 14 days after they are created or reset.
Each person can reset their own link; the Owner can turn off anyone's link (`S31-pending`).

Sample data: list `l-wedding` (100 items, Round 1), Owner `u-deniz` (default Decision Maker when first
shared, A-26), `u-mert`, `u-selin`. Tokens: `k4Rm9Tq2` (Deniz), `Pz83vLwe` (after reset), `Dm6xW3nB`
(Decision Maker link), `s7Lw2Qe9` (Selin).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S31-default` | First invite for Wedding guests (flow 3). Nobody has joined; Deniz is Owner and Decision Maker; Collaborator selected; link created |
| `S31-link-copied` | "Copy link" pressed: link on the clipboard, snackbar "Invite link copied". Prototype control "Mert opens the link" |
| `S31-role-dm` | Owner selects Decision Maker: the sheet shows the Decision Maker link and its one-person rule |
| `S31-pending` | Opened from S34 "Invite links" on the steady-state list: the active links (pending invites) with Turn off, then members |
| `S31-reset-confirm` | "Reset link" pressed |
| `S31-reset-done` | Reset confirmed: new token, new 14-day expiry, snackbar "Invite link reset" |
| `S31-loading` | Sheet opened and the link is being created (first open, or after reset): skeleton field, "Creating link…", actions disabled |
| `S31-offline` | No connection when the sheet opens or on Copy/Share: inline notice "Invites need a connection", role choice and actions disabled |
| `S31-error` | Server did not answer when creating the link |
| `S31-expired` | The viewer's link passed its 14 days: struck-through link, "Create new link" |
| `S31-signed-out` | Session ended (signed out elsewhere or token expired) while the list is shared: "Sign in to invite people" → S05 |
| `S31-collaborator` | Selin (Collaborator) invites: no role choice, info note, her own link |
| `S31-large-text` | 200% font scale |
| `S31-ios` | iOS page sheet |
| `S31-web` | Mobile browser (Web Share API available) |
| `S31-web-desktop` | Desktop browser: Copy link only |

Guests (no account) never see S31: Invite/Share routes to S05 `S05-share` (ACC-04).

## 5. Interactions, gestures and transitions

- **Open**: bottom sheet enter, 300 ms emphasizedDecelerate; scrim 0 → 50% (motion.md §3). Reduced motion:
  150 ms fade.
- **Role choice**: tapping a radio row selects it and swaps the link shown (Collaborator link ↔ Decision
  Maker link) in place, with a 150 ms cross-fade of the link field and the role line. The Decision Maker
  link is created on first selection (`S31-loading` style for < 1 s). Selecting a role never changes
  anyone's current role; the role moves only when someone joins with the Decision Maker link.
- **Copy link**: writes `https://swipesort.app/join/<token>` to the clipboard, snackbar "Invite link copied"
  (4 s). Shown on every platform for consistency (Android 13+ may also show its own clipboard overlay).
- **Share…**: opens the system share sheet with the text "Join “Wedding guests” on SwipeSort to sort it
  with me: https://swipesort.app/join/k4Rm9Tq2" (the list name is the only dynamic part).
- **Reset link**: AlertDialog (scale 0.96 → 1, 250 ms). "Reset link" revokes the old token, creates a new
  one, resets the expiry to 14 days and shows "Invite link reset". Cancel closes the dialog.
- **Turn off** (Owner, `S31-pending`): revokes that member's link immediately (no dialog; the member can
  create a new one); the row disappears with a 200 ms collapse and snackbar "Selin's link turned off".
- **Create new link** (`S31-expired`): creates a fresh link for the viewer, same as reset without a dialog.
- **Try again** (offline/error): retries creating or fetching the link; on success the default content
  replaces the notice.
- **Close**: close button, system back, drag down past 30% or fling 800 dp/s. Closing never asks.
- **Members** list updates live while the sheet is open (someone joining appears at the end of the group
  with a 250 ms fade-in; the footer note disappears).

## 6. Copy

| Element | String |
| --- | --- |
| Title | "Invite to Wedding guests" ("Invite to {list name}") |
| Intro | "People you invite sort the same 100 items on their own. The list then shows where you agree." |
| Role section | "Invite as" |
| Collaborator | "Collaborator" / "Sorts every item and adds notes. Can invite others as Collaborator." |
| Decision Maker (Owner is the Decision Maker) | "Decision Maker" / "Also resolves conflicts. There's one Decision Maker, so the role moves from you to them." |
| Decision Maker (someone else is, e.g. `S31-pending`) | "Also resolves conflicts. There's one Decision Maker, so the role moves from Mert to them." |
| Decision Maker (nobody is) | "Also resolves conflicts." |
| Link label | "Invite link" |
| Role line | "Anyone with the link can join as Collaborator." / Decision Maker: "The first person to join with this link becomes the Decision Maker. After that, the link invites as Collaborator." |
| Expiry | "Expires Oct 24, in 14 days" ("Expires {date}, in {n} days"; last day: "Expires today") |
| Reset | "Reset link" |
| Members | "Members (1)"; "Deniz Yılmaz (you)"; role words "Owner, Decision Maker", "Decision Maker", "Collaborator" |
| Alone | "Nobody else has joined yet. People show up here as soon as they join." |
| Active links | "Active invite links (2)"; "Your link" / "Collaborator, expires Oct 24. 2 people joined."; "Selin's link" / "Collaborator, expires Oct 21. Nobody joined yet."; "Turn off"; footer "A link stops working when it expires, is reset or is turned off. Members who joined stay." |
| Buttons | "Copy link", "Share…" |
| Snackbars | "Invite link copied"; "Invite link reset"; "Selin's link turned off" |
| Reset dialog | "Reset the invite link?" / "The current link stops working right away. Members who already joined stay. Share the new link with anyone who hasn't joined yet." / "Cancel", "Reset link" |
| Loading | "Creating link…" |
| Offline | "Invites need a connection" / "Connect to the internet to create or copy the invite link. Your lists and decisions are safe on this phone." / "Try again" |
| Error | "Couldn't create the invite link" / "SwipeSort didn't respond. Check your connection and try again." / "Try again" |
| Expired | "This link expired on Oct 8. Create a new one to invite more people." / "Create new link" |
| Signed out | "Sign in to invite people" / "Sharing needs an account, so everyone sorts the same list. Your lists stay on this phone and move to your account when you sign in." / "Sign in" |
| Collaborator note | "You can invite people as Collaborator. Only Deniz, the Owner, can invite a Decision Maker." |
| Web desktop footer | "Paste the link into an email or a chat to invite people." |
| iOS | Sheet title "Invite", "Done"; Decision Maker description "Also resolves conflicts. The role moves from you to them."; Collaborator "Sorts every item and adds notes." |
| Share text | "Join “Wedding guests” on SwipeSort to sort it with me: https://swipesort.app/join/k4Rm9Tq2" |
| Accessibility labels | Close: "Close"; link input label "Invite link"; Turn off: "Turn off Selin's link" |

## 7. Accessibility

- The sheet is a modal dialog labelled by its title; focus moves to the title on open and returns to the
  invoking control on close.
- Focus order: Close, role radios (Collaborator, Decision Maker), invite link field (read-only, selectable),
  Reset link, members, Copy link, Share….
- Radio group: arrow keys move the selection on web; TalkBack/VoiceOver read "Collaborator, radio button,
  selected, 1 of 2" plus the description.
- The link input is read-only but focusable so screen-reader users can hear and copy it.
- Snackbars are `role="status"` (polite); errors are `role="alert"`.
- Disabled actions use the real `disabled` attribute; the offline/error explanation stays at full contrast.
- Large text (`S31-large-text`): title wraps to two lines, descriptions wrap, the link wraps (`break-all`)
  instead of truncating, the footer buttons grow to fit and stay pinned.
- Touch targets: radio rows ≥ 56, Reset link 48 high, footer buttons 56 and 48.
- Reduced motion: sheet and dialog fade (150 ms), link swap is instant.

## 8. iOS and web differences

- **iOS** (`S31-ios`): an iOS page sheet (`presentation: 'pageSheet'`) with grabber; the parent screen
  shows scaled behind; a centered nav title "Invite" and "Done" on the right instead of the close icon;
  the role choice is a checkmark list (iOS selection pattern) instead of radio circles; the share icon is
  `share` (box with arrow). Swipe down dismisses.
- **Web, mobile** (`S31-web`): same layout as Android without system bars. "Share…" uses the Web Share API
  and is shown only when `navigator.share` exists; otherwise only "Copy link".
- **Web, desktop** (`S31-web-desktop`): the sheet sits in the centered phone column; "Copy link" only, with
  the hint to paste the link into an email or chat (desktop browsers mostly lack Web Share). Escape closes
  the sheet.
- No web-unavailable features on this screen.

## 9. Edge cases

- **Long list names**: the title wraps to two lines, then truncates with an ellipsis; the share text and
  the link preview use the full name.
- **Many members**: the members group shows the first 5 and "Show all {n} members" (opens S34).
- **Decision Maker link already used**: the Owner's link shows the Collaborator role line again and the
  radio returns to Collaborator; a one-time note appears above the link: "Mert joined as Decision Maker. Your
  link invites as Collaborator again."
- **Owner gives the Decision Maker role to someone else in S34 while a Decision Maker link is active**: the
  link falls back to Collaborator (S32 `S32-role-changed` explains this to the invited person).
- **Link expires while the sheet is open**: the field switches to `S31-expired` at the expiry time.
- **Offline after copying**: copying works offline once the link exists (it is cached); creating, resetting
  and turning off need a connection.
- **Text expansion**: buttons and labels wrap; the expiry row stacks "Reset link" below the date when it no
  longer fits on one line.
- **Proposed component**: FullHeightSheet (BottomSheet variant at full height with a sticky footer and a
  `background` surface). Built in this screen; see the lead's component review.
