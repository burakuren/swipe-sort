# S35 Conflict rule settings

Frames: `S35-conflict-rule.html`. Generator: `tools/generators/S35-S38-collaboration.py` (reads
`02-data/sample-data.json`, so every count below is computed from the sample). Related: S34 (Decision Maker
switches, source of truth for the role), S36 (conflicts), S37 (bulk resolve), S38 (activity), S09.

## 1. Purpose and requirements

Lets the Owner choose how a conflict on a shared list gets its final decision, explains each rule in plain
words with one concrete example, and shows what switching does to the open conflicts before it happens.
Everyone else sees the current rule, who chose it and what it means for them.

Covers: COL-13, DM-05, DM-06, DM-07, DM-08, DM-09, DM-10 (link to the switch; inline switch when the rule
needs a Decision Maker), DM-20, GOAL-03 (undo, nothing changes without confirmation), GOAL-04, PLT-02,
PLT-03, PLT-13–PLT-16, PLT-17 (dialogs fade), STK-06, STK-07, SCR-35.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S34 `S34-default` | "Conflict rule" row (`data-action="conflict-rule"`) |
| S09 `S09-shared` | List settings › "Conflict rule" |
| S36 menu | "Conflict rule" (opens the read-only view for non-Owners) |

| To | How |
| --- | --- |
| S34 `S34-default` | Back; "Change" next to the Decision Maker (`data-action="change-decision-maker"`); "Assign a Decision Maker" |
| S36 `S36-default` | "Review 15 conflicts" (Decision Maker's read-only view) |
| Dialogs in S35 | Switching rule (`S35-confirm-majority`, `S35-confirm-everyone`, `S35-dm-none-confirm`) |

Route: `list/[listId]/conflict-rule`, a stack screen without bottom navigation.

## 3. Layout and components

AppBar (small): back ("Back to Members"), title "Conflict rule", subtitle list name. Content inset 16, 16
between blocks:

1. **Intro** (`text-body muted`): one sentence defining a conflict.
2. **Example** (bordered row, `rounded-control bg-card`): MemberDecisions compact (32 avatars with decision
   dots, `gap-1.5`) for item c002 Mehmet Yılmaz (Deniz Accept, Mert Reject, Selin Accept) and the sentence
   "Example: Deniz and Selin accept Mehmet Yılmaz, Mert rejects." The same item is the example in every rule,
   so the three results can be compared directly.
3. **RadioGroup as radio cards** (Tile surface: `rounded-tile border bg-card p-4`; selected
   `border-2 border-primary`). Each card: Radio 24, title `text-title-3`, rule icon (`users`, `vote`,
   `gavel`), description `text-body-sm muted`, example result line (`corner-down-right` icon), and below a
   hairline a **consequence line**:
   - Current rule: "Current rule. …" plus, on Decision Maker decides, the Decision Maker row (Avatar 32,
     "Mert Aydın", "Decision Maker", text button "Change" → S34).
   - Other rules: "If you switch: …" with the real recalculation on the open conflicts.
4. **Footer** (`text-body-sm muted`): what never changes when the rule changes.

Read-only view (non-Owner): "Current rule" section with a selected-style card (title, description,
"Chosen by Deniz, the Owner, on Sep 28", Decision Maker row), a "What it means for you" group (Decision
Maker adds the primary Button "Review 15 conflicts"), an "Other rules" ListGroup with the two other rules
explained, and the footer "Only Deniz, the Owner, can change the rule."

Dialogs: AlertDialog with a `bg-muted` summary block (counts by decision with icon + label + count, in the
order Reject, Maybe, Accept). Components: AppBar, RadioGroup (Proposed **RuleCard**, see report), Avatar,
MemberDecisions, Button, Switch, AlertDialog, Snackbar, Alert, OfflineBanner, Skeleton.

<!-- Proposed component: RuleCard — RadioGroup item rendered as a Tile with description, example and consequence slots. -->

## 4. States

| Frame | Trigger |
| --- | --- |
| `S35-default` | Owner (Deniz), rule Decision Maker decides (sample `l-wedding.conflictRule`), Mert is Decision Maker, 15 open conflicts |
| `S35-confirm-majority` | Owner taps Majority decides. Recalculation: 8 of 15 become final (1 Reject, 1 Maybe, 6 Accept), 7 stay open waiting for the last member |
| `S35-switched` | Confirmed: Majority selected, consequence line updated, snackbar with Undo (shown scrolled to the Majority card so the snackbar sits over empty space) |
| `S35-confirm-dm` | Rule is Majority decides and Mert is Decision Maker; the Owner taps Decision Maker decides: Mert takes the 7 open conflicts, the 8 already final stay final |
| `S35-confirm-everyone` | Owner taps Everyone must agree: all 15 stay open; Mert can no longer resolve them |
| `S35-majority-no-dm` | Rule Majority decides and nobody holds the Decision Maker role (after S34 "Turn off"): inline explanation of ties + "Assign a Decision Maker" |
| `S35-dm-none` | From that state the Owner taps Decision Maker decides: the card shows "Choose the Decision Maker first" with one Switch per member; the rule is not applied yet (Majority stays "Current rule"). With nobody in the role the example reads "The Decision Maker chooses the final decision." |
| `S35-dm-none-confirm` | A switch turned on (Mert): one dialog confirms role and rule together |
| `S35-collaborator` | Selin (Collaborator): read-only, what it means for her |
| `S35-decision-maker` | Mert (Decision Maker): read-only, "Review 15 conflicts" |
| `S35-loading` | First load: skeleton |
| `S35-offline` | No connection: rule visible; option tiles shown unavailable (dashed border, no fill, muted titles, dimmed radios, `aria-disabled`), "Change" disabled; the banner gives the reason at full contrast |
| `S35-error` | Switching failed: inline error alert at the top, rule unchanged, "Try again" |
| `S35-large-text` | 200% font scale |
| `S35-ios`, `S35-ios-confirm` | iOS pushed screen; native alert for the confirmation |

Recalculation numbers (from sample data, conflict IDs c002 c012 c015 c020 c029 c034 c037 c043 c049 c056 c059
c060 c064 c069 c071):
- **Majority decides**: final when all three decided and one decision has most votes: c002 Accept, c015
  Accept, c029 Accept, c037 Reject, c043 Maybe, c049 Accept, c059 Accept, c069 Accept (8: 6 Accept, 1 Reject,
  1 Maybe). Open, waiting for 1 member: c012, c034, c056 (Mert), c020, c060, c064, c071 (Selin). No current
  three-way ties.
- **Everyone must agree**: 0 become final; 15 stay open.
- **Decision Maker decides**: 0 become final automatically; all open conflicts go to the Decision Maker.

## 5. Interactions, gestures and transitions

- **Tapping a rule card** (Owner, not the current rule) opens the confirmation dialog (250 ms scale + fade).
  Nothing changes before confirming. Cancel closes and the previous radio stays selected.
- **Confirm** ("Switch to Majority", "Switch to Everyone must agree"): the rule is saved on the server
  (needs a connection), every open conflict is recalculated, the radio moves (150 ms), consequence lines
  re-render, snackbar "Switched to Majority decides. 8 conflicts are now final." with **Undo** (6 s). Undo
  restores the previous rule and the exact previous statuses. Members get an Activity entry (rule change,
  in-app only, no push; see S38).
- **Resolved items are never reopened** by a rule change; only open conflicts are recalculated. Members'
  own decisions never change.
- **Switching to Decision Maker decides with a Decision Maker**: no recalculation dialog is needed beyond
  "Switch to Decision Maker decides?" (`S35-confirm-dm`; copy in §6).
- **Switching to Decision Maker decides without one** (`S35-dm-none`): the card expands (200 ms) with the
  member switches (same control as S34 Decision Maker group, at most one on). Turning one on opens
  `S35-dm-none-confirm`; confirming sets both the role and the rule in one step. Cancel turns the switch off
  and collapses the card.
- **"Change" / "Assign a Decision Maker"** push S34 (M3 shared axis X, 300 ms). Back returns here with the
  updated Decision Maker.
- **Live updates**: if another device changes the rule, the screen updates and announces "Conflict rule
  changed to Majority decides by Deniz".
- Reduced motion: dialogs and the card expansion fade (150 ms); no radio animation.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Conflict rule"; subtitle "Wedding guests"; back label "Back to Members" |
| Intro | "When members decide an item differently, it's a conflict. Choose how conflicts get a final decision." |
| Example | "Example: Deniz and Selin accept Mehmet Yılmaz, Mert rejects." |
| Everyone must agree | Title "Everyone must agree"; "Final only when every member chooses the same. Members can change their decision to match."; "Example: Stays a conflict until all three match." |
| Majority decides | Title "Majority decides"; "Once everyone has decided, the most chosen decision is final. Ties go to the Decision Maker."; "Example: Accept is final, 2 of 3 chose it." |
| Decision Maker decides | Title "Decision Maker decides"; "The Decision Maker chooses the final decision for each conflict."; "Example: Mert chooses the final decision." (no Decision Maker: "Example: The Decision Maker chooses the final decision.") |
| Consequences | "Current rule. Mert has 15 conflicts to resolve."; "Current rule. 8 conflicts became final. 7 wait for the last member."; "Current rule. 15 conflicts wait for members to match."; "If you switch: all 15 conflicts stay open."; "If you switch: 8 of 15 conflicts become final now."; "If you switch: Mert resolves the 7 open conflicts." |
| Decision Maker row | "Mert Aydın"; "Decision Maker"; "Change" (label "Change Decision Maker") |
| Majority without Decision Maker | "No Decision Maker, so ties stay open" / "A tie is when no decision has the most votes. With 3 members, that's when all three choose differently. Ties stay conflicts until someone changes their decision." / "Assign a Decision Maker" |
| Decision Maker rule without one | Collapsed: "Needs a Decision Maker. Choose one when you pick this rule."; expanded: "Choose the Decision Maker first" / "This rule needs one member to resolve conflicts. Turn on one switch, then confirm the rule."; switch labels "Decision Maker: Mert Aydın"; Majority card: "Current rule. Ties stay open because nobody is the Decision Maker." |
| Footer | "Changing the rule never changes anyone's own decisions. Conflicts that are already resolved stay resolved." |
| Majority dialog | "Switch to Majority decides?" / "8 of 15 conflicts get a final decision right away. Members are notified." / "8 become final now" + "Reject 1", "Maybe 1", "Accept 6" / "7 stay open" — "They wait for the last member to decide. Ties go to Mert." / "Cancel", "Switch to Majority" |
| Everyone dialog | "Switch to Everyone must agree?" / "No conflict gets a final decision until members change their decisions to match. Members are notified." / "15 stay open" — "Mert can no longer resolve them. Each item is final only when Deniz, Mert and Selin choose the same." / "Cancel", "Switch to Everyone must agree" |
| Decision Maker dialog (with one) | "Switch to Decision Maker decides?" / "Mert resolves the 7 open conflicts and any new ones. The 8 conflicts that became final by majority stay final. Members are notified." / "Cancel", "Switch to Decision Maker decides" |
| Role + rule dialog | "Make Mert the Decision Maker?" / "The rule changes to Decision Maker decides. Mert resolves the 7 open conflicts and any new ones. Members are notified." / "Cancel", "Make Mert Decision Maker" |
| Snackbars | "Switched to Majority decides. 8 conflicts are now final." + "Undo"; "Switched to Everyone must agree"; "Switched to Decision Maker decides"; after Undo: "Conflict rule is Decision Maker decides again" |
| Read-only | "Current rule"; "Chosen by Deniz, the Owner, on Sep 28"; "What it means for you"; Collaborator: "Keep deciding on your own. When your decision differs from someone else's, the item becomes a conflict and Mert chooses its final decision. You can still change your own decision; if everyone ends up choosing the same, the item is Agreed."; Decision Maker: "You're the Decision Maker. When members decide an item differently, you choose its final decision. Members see "Resolved by Mert"." + "Review 15 conflicts"; "Other rules"; "Only Deniz, the Owner, can change the rule." |
| Read-only under other rules | Majority (Collaborator): "Keep deciding on your own. Once everyone has decided an item, the decision most members chose is final. Ties go to Mert."; Everyone (Collaborator): "An item is final only when everyone chooses the same. Open Conflicts to see where you differ and change your decision if you agree." |
| Offline | Banner "You're offline. Changing the rule needs a connection." |
| Error | "Couldn't change the rule" / "The rule is still Decision Maker decides. Check your connection and try again." / "Try again" |
| Loading | (skeleton) screen reader "Loading conflict rule" |
| Activity entry (in-app) | "Deniz changed the conflict rule to Majority decides" |

## 7. Accessibility

- Focus order: Back, title, intro, example, rule cards (each a `radio` in a `radiogroup` labelled "Conflict
  rule"), the "Change" button inside the current card, footer.
- Each radio's accessible name = title; description = description + example + consequence, read after the
  name. Selection does not apply on focus/arrow keys (confirmation required): arrow keys move focus, Space
  or Enter opens the dialog.
- The example MemberDecisions is one image: "Deniz: Accept. Mert: Reject. Selin: Accept."
- Dialogs: `alertdialog`, focus on the title, Cancel focused first; counts read as "Reject, 1. Maybe, 1.
  Accept, 6."
- After switching, the snackbar is announced politely; Undo is reachable for at least 10 s with a screen
  reader running (motion.md).
- Large text (`S35-large-text`): cards stay full width and grow; titles `text-title-1`; description and
  consequence wrap; nothing truncates.
- Color is never the only signal: selected card has the filled radio plus the 2 px border; decisions in the
  example and dialogs carry icons and labels.
- Touch targets: whole card is the target (≥ 120 high); "Change" 48 high.

## 8. iOS and web differences

- **iOS** (`S35-ios`): pushed screen with back chevron "Members" and centered title; edge-swipe back. Cards
  are the same (inset grouped style is not used because the cards carry explanations). The confirmation is a
  native alert (`S35-ios-confirm`) with the counts in one sentence ("8 of 15 conflicts get a final decision
  right away: 1 Reject, 1 Maybe, 6 Accept. 7 stay open until the last member decides. Members are
  notified."), actions "Switch to Majority" (bold) and "Cancel".
- **Web, mobile**: same as Android without system bars. **Web, desktop**: phone layout centered (no extra
  frame: behavior is identical; arrow keys move between radio cards, Enter opens the dialog, Escape closes it).

## 9. Edge cases

- **Two members**: every disagreement is a tie, so Majority decides behaves like Decision Maker decides (with
  one) or Everyone must agree (without one). The Majority card adds: "With 2 members, every disagreement is a
  tie."
- **Even number of members (4, 6…)**: 2–2 splits are ties; same tie rule.
- **Recalculation while members are sorting**: counts in the dialog are computed when it opens; if they
  change before confirming, the dialog updates in place.
- **Rule changed during a Decision Maker's one-by-one session** (S36): the Decision Maker sees a sheet
  "Deniz changed the rule to Majority decides" and the deck reloads.
- **Decision Maker leaves or is removed** under Decision Maker decides: the list keeps the rule; S35 shows the
  `S35-dm-none` prompt as an alert in the current card, and new conflicts stay open until one is assigned.
- **Solo list**: not reachable (no conflicts on solo lists).
- **Offline**: read-only (`S35-offline`), because recalculation must use everyone's latest decisions.
- **Long list names**: subtitle truncates in the app bar; the content never repeats the list name.
