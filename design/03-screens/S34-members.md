# S34 Members and roles

Frames: `S34-members.html`. Generator: `tools/generators/S31-S34-collaboration.py`. Related: S31 (invite),
S35 (conflict rule, group G2), S36/S37 (conflicts, G2), S38 (activity), S09 (list overview), S40 (dialog
patterns).

## 1. Purpose and requirements

One place to see who is on a shared list and how far each member is, and to manage membership: invite,
assign the Decision Maker with a single switch, change roles, remove a member (keeping or discarding their
decisions), transfer ownership and leave.

Covers: COL-07, COL-08, COL-09, COL-10, COL-11, COL-12, COL-01 (invite entry), COL-13 (entry to S35),
COL-22 (role changes notify), DM-06 (rule entry), DM-08/DM-09 (Decision Maker meaning), DM-10, DM-17,
DM-20, GOAL-03, GOAL-04, PLT-02, PLT-03, PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, STK-06, STK-07, SCR-34.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S09 `S09-shared` | "Members" row / member avatars |
| S38 activity | "Selin joined Wedding guests", "Deniz made you the Decision Maker" (deep link `/l/<id>/members`) |
| S31 | Close returns here when S31 was opened from S34 |

| To | How |
| --- | --- |
| S31 `S31-default` | App bar `user-plus`, "Invite people" row (Owner); `S31-collaborator` for others |
| S31 `S31-pending` | "Invite links" row (Owner) |
| S35 `S35-default` | "Conflict rule" row (`data-action="conflict-rule"`) |
| S36 `S36-default` | "Review 15 conflicts" (Decision Maker view) |
| Member options sheet / menu / action sheet | Options button on a member row (Owner) |
| Dialogs in S34 | Decision Maker change, remove, transfer, leave |
| S08 `S08-default` | After leaving (snackbar "You left Wedding guests") |
| S09 `S09-shared` | Back |

## 3. Layout and components

Stack screen inside `list/[listId]`, no bottom navigation. AppBar (small): back, "Members" with the list
name as subtitle, trailing `user-plus` "Invite people". Content in the 16 dp inset, sections 24 apart:

1. **{n} members** ListGroup:
   - MemberRow per member: Avatar 40, name ("(you)" for the viewer), role text with icon (`crown` Owner,
     `gavel` Decision Maker, plain "Collaborator") and the count "85 / 100 decided" on one line, Progress
     bar (`h-1.5`) below, options IconButton (`ellipsis-vertical`, 48) for the Owner on other members' rows.
     Finished members show `circle-check` "Finished" after the name.
   - Owner: "Invite links" row (`link-2`, "2 active, Collaborator", chevron) → S31 pending.
   - "Invite people" row (`user-plus`, primary text).
2. **Resolving conflicts** ListGroup: "Conflict rule" row with the current rule as description → S35.
   Decision Maker view adds "Review 15 conflicts" → S36.
3. **Decision Maker** ListGroup (Owner): one row per member (Avatar 32, name, Switch). Footer: "Resolves
   conflicts and breaks ties. One member at a time." Others see a single read-only row naming the Decision
   Maker and "Only Deniz, the Owner, can change roles."
4. Owner: "Transfer ownership" (`crown`) and "Leave list" (`log-out`, destructive). Others: "Leave list".

**Decision Maker assignment (DM-10), decided design**: the Decision Maker group is the single place the
Owner assigns the role; each member has one Switch and at most one is on. Turning a switch on is one
interaction; when it moves the role away from someone else, a confirmation names who loses it and what the
new Decision Maker will resolve. The same switch is repeated in the member options sheet (same state, same
behavior) for people who start from a member. The member row label updates everywhere ("Decision Maker"
moves to the new holder). Roles stay: **Owner** (exactly one) and **Collaborator**, plus the independent
**Decision Maker** flag (domain-model.md); "role change Collaborator ↔ Decision Maker" is this switch.

**Member options** (Owner): BottomSheet with avatar 56, name, email, "Collaborator, joined Oct 2", progress,
then rows: Decision Maker (Switch), Make Owner, Remove from list (destructive). iOS: action sheet. Web
desktop: DropdownMenu anchored to the options button.

Dialogs: AlertDialog (S40 pattern). Remove uses a RadioGroup inside the dialog (keep / discard).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S34-default` | Owner (Deniz) on Wedding guests: Mert is Decision Maker; progress Deniz 76, Mert 85, Selin 43 |
| `S34-scrolled` | Same, scrolled to Transfer ownership and Leave list |
| `S34-finished` | A member decided every item of the round (Selin 100 / 100) |
| `S34-empty` | Just shared, nobody joined yet: Owner is the only member and Decision Maker (A-26); invite empty state |
| `S34-dm-confirm` | Owner turns on Selin's switch while Mert holds the role |
| `S34-dm-changed` | Confirmed: Selin on, Mert off, snackbar |
| `S34-dm-self-confirm` | Owner turns on their own switch (DM-10 "including themselves") |
| `S34-dm-off-confirm` | Owner turns off the only Decision Maker |
| `S34-member-sheet` | Options for Selin (role change sheet) |
| `S34-remove-dialog` | "Remove from list": keep (default) or discard Selin's decisions (DM-17) |
| `S34-removed` | Removed: Selin gone, snackbar with Undo |
| `S34-transfer-dialog` | "Make Owner" on Mert |
| `S34-transferred` | Confirmed: Mert is Owner and Decision Maker; Deniz now sees the Collaborator view |
| `S34-leave-owner` | Owner taps Leave list: must choose a new Owner first |
| `S34-transfer-pick` | "Choose new Owner" or "Transfer ownership": pick a member, then transfer and leave, or transfer and stay |
| `S34-leave-dialog` | A Collaborator (Selin) leaves |
| `S34-collaborator` | Selin's read-only view |
| `S34-decision-maker` | Mert's view: "You're the Decision Maker", "Review 15 conflicts" |
| `S34-loading` | First load: skeleton |
| `S34-error` | Members couldn't be loaded |
| `S34-offline` | No connection: last synced progress, every change disabled with the reason |
| `S34-large-text` | 200% font scale |
| `S34-ios`, `S34-ios-actions` | iOS: large title, iOS switches, action sheet for member options |
| `S34-web-desktop` | Desktop browser: member options as a menu |

## 5. Interactions, gestures and transitions

- **Decision Maker switch** (Owner):
  - Nobody holds the role → on immediately; snackbar "Selin is now the Decision Maker".
  - Someone else holds it → the tapped switch shows on, the dialog asks; Cancel turns it back off;
    "Change Decision Maker" turns the previous holder's switch off (200 ms), updates the row labels and
    shows the snackbar. Notifies both members (S38 roleChanged: "Deniz made you the Decision Maker",
    "Deniz made Selin the Decision Maker").
  - Owner's own switch → "Become the Decision Maker?" dialog when someone else holds it.
  - Turning off the current holder → "Turn off the Decision Maker?" dialog; copy depends on the rule (see
    §6). Under "Everyone must agree" no dialog is needed (the role has no effect) and it turns off directly.
  - Open conflicts are not reassigned to a person: whoever is Decision Maker when resolving resolves them.
- **Options button / row tap** (Owner, other members): opens the member options sheet (300 ms). Back or
  scrim tap closes.
- **Make Owner** → transfer dialog → "Make Mert Owner": Mert becomes Owner (keeps his Decision Maker flag),
  Deniz becomes Collaborator, the screen re-renders in the Collaborator view, snackbar "Mert is now the
  Owner". Irreversible by Deniz (only the new Owner can transfer back), so it always confirms.
- **Remove from list** → remove dialog with Keep preselected → "Remove Selin": the row collapses (200 ms),
  counts update ("2 members"), snackbar "Removed Selin" with Undo (6 s; Undo restores membership and
  decisions exactly). Discarded decisions recompute list statuses after the snackbar times out. Removing
  the Decision Maker leaves nobody in the role (the dialog adds a sentence, §6).
- **Leave list**: Collaborator/Decision Maker → leave dialog → back to S08 with "You left Wedding guests".
  Owner → "Choose a new Owner first" → transfer picker sheet → "Make Mert Owner and leave" (S08, snackbar
  "You left Wedding guests") or "Make Mert Owner and stay" (`S34-transferred`).
- **Invite links / Invite people / Conflict rule**: navigate (S31 sheet over S34; S35 push).
- **Live updates**: progress bars animate to new values (250 ms standard) as members sort; new members
  appear at the end of the group with a fade.
- **Pull to refresh**: refreshes progress (Android/iOS); web uses live updates only.
- Reduced motion: sheet/dialog fade 150 ms; progress jumps; rows appear/disappear instantly.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Members"; subtitle "Wedding guests"; back label "Back to Wedding guests"; action "Invite people" |
| Members header | "3 members" ("1 member") |
| Member row | "Deniz Yılmaz (you)"; "Owner"; "Decision Maker"; "Collaborator"; "76 / 100 decided"; "Finished"; options label "Options for Mert Aydın" |
| Invite rows | "Invite links" / "2 active, Collaborator"; "Invite people"; non-owner: "Invite people" / "As Collaborator" |
| Empty | "1 member"; "Only you so far" / "Invite people to sort Wedding guests with you. Everyone decides on their own." / "Invite people"; DM footer "You're the Decision Maker until you give the role to someone who joins." |
| Conflicts section | "Resolving conflicts"; "Conflict rule" / "Decision Maker decides" ("Majority decides", "Everyone must agree"); DM view: "Review 15 conflicts" / "You resolve them as Decision Maker" |
| Decision Maker section | "Decision Maker"; switch labels "Decision Maker: Selin Yılmaz"; footer "Resolves conflicts and breaks ties. One member at a time." |
| Read-only | "Mert Aydın" / "Resolves conflicts and breaks ties."; "You're the Decision Maker" / "You resolve conflicts and break ties."; "Only Deniz, the Owner, can change roles." |
| Ownership | "Transfer ownership" / "Make another member the Owner"; "Leave list" |
| Move dialog | "Make Selin the Decision Maker?" / "Mert stops being the Decision Maker. Selin will resolve the 15 open conflicts and any new ones." / "Cancel", "Change Decision Maker" (rule Majority: "Selin will break ties from now on.") |
| Self dialog | "Become the Decision Maker?" / "Mert stops being the Decision Maker. You'll resolve the 15 open conflicts and any new ones." / "Cancel", "Become Decision Maker" |
| Off dialog | "Turn off the Decision Maker?" / "Under the rule Decision Maker decides, conflicts need a Decision Maker. Without one, they stay open until members change their decisions to match. You can turn it on again at any time." / "Cancel", "Turn off". Rule Majority: "Under the rule Majority decides, ties will stay as conflicts until members change their decisions. You can turn it on again at any time." |
| Snackbars | "Selin is now the Decision Maker"; "Nobody is the Decision Maker now"; "Removed Selin" + "Undo"; "Mert is now the Owner"; "You left Wedding guests"; "Couldn't save the change. Check your connection and try again." |
| Member sheet | "Selin Yılmaz"; "selin.yilmaz@example.com"; "Collaborator, joined Oct 2"; "Decision Maker" / "Resolves conflicts and breaks ties. Mert has this role now." (when nobody: "Resolves conflicts and breaks ties."); "Make Owner" / "Hand the list over. You become a Collaborator."; "Remove from list" |
| Remove dialog | "Remove Selin from Wedding guests?" / "Selin can't open the list anymore. Choose what happens to Selin's 43 decisions." / "Keep Selin's decisions" — "They still count toward Agreed, Pending and Conflict." / "Discard Selin's decisions" — "Item statuses are recalculated without them." / "Cancel", "Remove Selin". Removing the Decision Maker adds: "Mert is the Decision Maker, so nobody will have this role." |
| Transfer dialog | "Make Mert the Owner?" / "Mert will manage members, rounds and the conflict rule, and can rename or delete the list. You'll stay on the list as a Collaborator." / "Cancel", "Make Mert Owner" |
| Owner leave | "Choose a new Owner first" / "Wedding guests needs an Owner. Make another member the Owner, then you can leave. To remove the list for everyone, delete it instead." / "Cancel", "Choose new Owner" |
| Transfer picker | "Choose the new Owner"; "Mert Aydın" / "Decision Maker"; "Selin Yılmaz" / "Collaborator"; "Mert will manage members, rounds and the conflict rule. You'll leave Wedding guests; your 76 decisions stay and still count." / "Make Mert Owner and leave", "Make Mert Owner and stay" |
| Leave dialog | "Leave Wedding guests?" / "You won't see this list anymore. Your 43 decisions stay and still count toward the list status. To come back, ask Deniz for a new invite." / "Cancel", "Leave list" |
| Loading | (skeleton) screen reader "Loading members" |
| Error | "Members couldn't be loaded" / "SwipeSort didn't respond. Check your connection and try again." / "Try again" |
| Offline | Banner "You're offline. Changes to members need a connection."; DM footer "Changes to members need a connection." |
| iOS action sheet | "Selin Yılmaz, Collaborator"; "Make Decision Maker" (or "Remove as Decision Maker"); "Make Owner"; "Remove from list"; "Cancel" |
| Web menu | "Decision Maker" (switch item), "Make Owner", "Remove from list" |

## 7. Accessibility

- Focus order: Back, title, Invite people, member rows (each reads "Mert Aydın, Decision Maker, 85 of
  100 decided" then its options button "Options for Mert Aydın"), Invite links, Invite people, Conflict
  rule, Decision Maker switches, Transfer ownership, Leave list.
- Switches are `role="switch"` with labels "Decision Maker: {name}" and announce their state; the group
  label is announced once ("Decision Maker, one member at a time"). Because they behave as a single choice,
  the screen reader announces the result after a change: "Selin is now the Decision Maker. Mert is no
  longer the Decision Maker."
- Progress bars: `progressbar` with "{first name}: 85 of 100 decided".
- Dialogs: `alertdialog`, focus on the title, Cancel is the default focused action for destructive
  dialogs; the remove dialog's radio group is labelled "Selin's decisions".
- Touch targets: rows ≥ 56, switches have a 52×48 target, options buttons 48.
- Large text (`S34-large-text`): names and role text wrap, counts move below the bars, rows grow; switch
  rows grow with the name.
- Color is never the only signal: role labels have text and icons; the destructive actions have text.
- Reduced motion: no progress animation, dialogs and sheets fade.

## 8. iOS and web differences

- **iOS** (`S34-ios`): back chevron with "Wedding guests", large title "Members" (collapses on scroll),
  "Invite people" as a `user-plus` bar button; inset grouped sections; iOS-style switches (thumb inside
  the track, `primary` tint kept for brand consistency); edge-swipe back.
- **iOS member options** (`S34-ios-actions`): an action sheet with "Make Decision Maker" (or "Remove as
  Decision Maker"), "Make Owner", "Remove from list" (destructive) and "Cancel". The Decision Maker switch
  group on the screen stays the primary way (DM-10). Dialogs use native alerts with the same copy.
- **Web, mobile**: same as Android without system bars; options open the bottom sheet.
- **Web, desktop** (`S34-web-desktop`): phone layout centered; options open a DropdownMenu next to the
  button with "Decision Maker" as a switch menu item, "Make Owner" and "Remove from list"; Escape closes.
  No pull to refresh.

## 9. Edge cases

- **Owner is also the Decision Maker**: row shows both labels ("Owner" and "Decision Maker").
- **Only the Owner**: `S34-empty`; Transfer ownership and Leave list are hidden (nobody to transfer to);
  "Delete list" lives in S10.
- **Removing the Decision Maker**: the dialog adds the extra sentence; afterwards nobody holds the role and
  the Decision Maker group shows all switches off.
- **Discarding decisions** of a member with no decisions: the radio group is hidden and the body says
  "Selin hasn't decided any items yet."
- **Member left while the sheet is open**: the sheet closes with snackbar "Selin left the list".
- **Owner transfer while offline**: disabled (offline state).
- **Two Owners editing**: impossible (exactly one Owner); concurrent Decision Maker changes from another
  device resolve last-write-wins and the screen updates live.
- **Many members** (10+): the group lists all members (the screen scrolls); the Decision Maker group lists
  everyone too; a search field is not needed at this size.
- **Long names**: wrap to two lines; the count wraps under the role text.
- **Progress after a new round**: bars reset to the new round's totals ("0 / 11 decided").
- **Members screen on a solo list**: not reachable (S09 solo has no Members row).
