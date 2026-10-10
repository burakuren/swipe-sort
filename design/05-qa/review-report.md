# QA review report (Phase 4, round 1)

Independent QA of the complete design (S01–S40, 813 frames, foundations, architecture, prototype).
Reviewer: QA lead (did not design anything). Date: 2026-10-10.

## Summary

**Verdict: not ready.** 5 Blocking, 22 Major and 101 Minor findings are open
(128 in total). The Blocking findings are two traceability gaps, two decision-model contradictions
and one forbidden domain word in UI copy. All five can be fixed in copy or spec text; none needs a redesign.
The foundations, coverage and flow structure are strong. Every screen ID exists with its brief-named
states, all link targets resolve, and all five prototype tests pass in both themes.

| Severity | Count |
| --- | --- |
| Blocking | 5 |
| Major | 22 |
| Minor | 101 |

| Area | Blocking | Major | Minor |
| --- | --- | --- | --- |
| a11y | 0 | 0 | 1 |
| consistency | 0 | 3 | 1 |
| copy | 0 | 10 | 4 |
| coverage | 0 | 0 | 2 |
| decision model | 2 | 3 | 1 |
| flow | 0 | 0 | 1 |
| platform | 0 | 1 | 1 |
| prototype | 0 | 1 | 0 |
| terminology | 1 | 0 | 2 |
| traceability | 2 | 0 | 2 |
| visual | 0 | 4 | 86 |

### Tool results

| Check | Result |
| --- | --- |
| `npm run lint` | 0 errors, 296 touch-target warnings (judged below and in QA-035 touch-target findings) |
| `npm run a11y` | 47 files × 2 themes, **0 violations** (no serious or critical) |
| `npm run flows` (light) | **5 passed, 0 failed** |
| `npm run flows -- --theme=dark` | **5 passed, 0 failed** |
| `node tools/qa/traceability.mjs` | 301 requirements; **2 unmapped (PLT-20, VIS-07)**; 51 mapped to documents only (foundation/process IDs) |
| `node tools/qa/refs.mjs` | All frame IDs cited in specs, navigation-map, components.md, assumptions, README and HANDOFF exist; 0 broken in-frame links; all navigation-map §5 frames and §6 `data-action`s exist. S02, S05 and S32 have no `Sxx-default` frame (QA-033) |
| `node tools/qa/terms.mjs` | No guest/invitee/wedding/RSVP/attendee/bride/groom in UI copy outside sample data and template names. "products" in S09-sample (Blocking) and S02-welcome (Minor); "records"/"entries" in S20 (Minor) |
| `node tools/qa/geometry.mjs` | Dialog centring, hitSlop reach of small targets and overflow candidates (used as evidence below) |
| Visual review | 1,626 PNGs (813 frames × light/dark), split across four reviewers by screen group, merged here |

### Prototype flow tests (`tools/flows/`)

| Test | Result | Notes |
| --- | --- | --- |
| `01-first-launch.flow.mjs` | Pass (light, dark) | S01-default → S02-welcome → S02-demo → S02-demo-done → S08-first-run → S11-default → S12-contacts → S13-select-default → S19-contacts → S20-default → S22-import-pick → S25-coach-1…4 → live sort in `swipe-demo.html?deck=wedding&count=6` (drag right, drag left, drag up, then ←/→/↑ keys) → S27-default. **SUC-04: 12 interactions from the empty home to the first decision (11 taps + 1 swipe), 16 from cold start, no account.** 4 of the 11 taps are coach marks (skippable). |
| `02-resort-maybe.flow.mjs` | Pass | S09-solo-round-done → S24-maybe → swipe demo `desk-maybe` (6 items, decided with the visible buttons) → S27-desk-round-2 → S28-default → S39-default → S39-google-destination → S39-google-confirm → S39-success-google. Counts are consistent (9/6/5 → 11/1/8). |
| `03-invite-web.flow.mjs` | Pass | S09-guest-wedding → S05-share → S05-moving → S05-moved → S31-default → S31-link-copied → S32-web-desktop → S03-web-desktop → S33-web-desktop → S25-web-desktop → S27-shared → S36-default → S37-confirm → S37-summary → S39-shared → S39-shared-google-destination → S39-shared-google-confirm → S39-success-shared (17 taps). Asserts desktop frames and keyboard hints. The S05-moving and S25-web-desktop steps only continue through visually hidden links (QA-019). |
| `04-csv-template.flow.mjs` | Pass | S08-default → S11-default → S14-default → S14-csv-preview → S19-csv → S20-none → S22-import-pick-csv → S23-default → S23-save → S22-import-pick-custom → S25-candidate (10 taps). |
| `05-swipe-demo.flow.mjs` | Pass | Mouse drags right, left and up, checked through `window.__swipeDemo.state()`. While dragging it checks the tilt, the armed tint and the "Accept" stamp. Also covered: a short slow drag snaps back, a down drag never decides, Undo by button (snackbar "Undid Maybe on …") and by Z, arrow-key decisions, and `?reduced=1` (no tilt or scale, decisions still commit). The test fails on any `console.error`, page error or failed local request. |

Each test asserts the URL hash at every step, that only the target frame is visible (prototype mode), and that
clicks are scoped to `[data-frame="<id>"] [data-action="…"]`. Shared helpers: `tools/qa/flow-helpers.mjs`.

### Success criteria (brief <success_criteria>)

| Criterion | Status | Evidence |
| --- | --- | --- |
| SUC-01 coverage.md shows every screen Done | **Not met** | coverage.md lists 39 screens "Designed, pending QA"; the lead updates it after fixes |
| SUC-02 traceability maps every requirement, no gaps | **Not met** | PLT-20 and VIS-07 are claimed by no spec §1 (QA-001, QA-002) |
| SUC-03 no open blocking issues; a11y clean; flows pass | **Not met** | 5 Blocking open. a11y 0 violations and 5/5 flows pass both met |
| SUC-04 import and first decision in under a minute, no account | Met | Flow 1: 12 interactions, guest throughout. The list size changes along the way (QA-006) |
| SUC-05 invited partner joins and sorts on the web without installing | Partly met | S32/S03/S33/S25 desktop frames exist and flow 3 passes. The web sorting step is a static frame (QA-019) |
| SUC-06 product shortlist without wedding wording | **Not met** | The sample product list says "20 desk products" and "Sample products" (QA-005). Otherwise clean |
| SUC-07 "X / Y decided" and counts visible whenever sorting | Met | Every S25 sorting frame has progress and per-button counts. Only S25-loading, -error, -resume and -nothing-left lack them, by design. S25-drag-maybe covers the progress (Minor) |
| SUC-08 every gesture has a visible, accessible button equivalent | Met | S25/S36 decision bar + Undo; S25-screen-reader actions; swipe-demo buttons and keys; iOS row swipe actions have menu equivalents (A-109) |
| SUC-09 new source = one more tile | Met | S11-new-source, A-55 data-driven Source definition |
| SUC-10 a coding agent can implement any screen from the docs | Met with exceptions | Specs have all 9 sections. The contradictions in QA-003, QA-004 and QA-006 and the S40 mismatches must be fixed first |

### Coverage (check 1)

Every screen S01–S40 exists, and so does every frame ID that navigation-map §5 requires. Each screen has the
states the brief names: the S08 first-run sample, the not-backed-up indicator, solo and shared S09, every
S10 operation, web-unavailable S11 tiles, the denied states in S12, all five import errors (S14/S15), coach
marks, note, undo, offline and web keyboard in S25, and success, failure and Google write confirmation in S39.
S38 shows all six event types and S06 every sub-page. Generic states (default, empty, loading, error, offline,
web) exist wherever they apply. Gaps are minor: three files have no `Sxx-default` frame, and S15 and S18 have
no large-text frame. No missing state is Blocking.

### Platform coverage (check 4)

- Each web-unavailable feature is handled everywhere it appears. Contacts: S11-web, S11-web-unavailable,
  S21-web. Photo gallery: S11-web "Upload photos", S18-web. Haptics: S06-web. Push: S06-notifications-web,
  S12-notifications-web, S38-web. The only inconsistency is QA-032 (S11-web has no visible "Get the app"
  link).
- Keyboard hints (`<kbd>`) appear only in desktop web frames. Every desktop S02/S25/S36 frame has them; no
  Android, iOS or mobile-web frame does (scripted check).
- iOS variants exist for every screen with different behavior. S32 documents its iOS behavior in §8
  (Universal Link identical; Safari uses the Smart App Banner), which is acceptable. One gap: S10-ios-action-sheet
  leads to the Android dialog instead of the iOS one (QA-011).

### Touch targets (check 7, lint warnings judged)

`tools/qa/geometry.mjs` measured all 394 controls smaller than 48 × 48 that are not inside a larger tappable
row or label. 328 can reach 48 × 48 with `hitSlop` without overlapping a neighbor. That covers the 40-high
SegmentedControl segments in a 48 track, 36-high FilterChips in 48 rows (components.md), the S06-feedback and
S24 segments, and the S26-add-note switch row. The 1 × 1 targets are visually hidden prototype shortcuts, not
UI. The remaining 66 are listed in QA-035. They are the S03 inline legal links (WCAG 2.5.8 inline exception;
acceptable), the S20 "Review merge" text link, the S28 Filter/Sort chips (36 high, room for 46) and the
S29-value-picker chips (room for 44). Recommendation: state `hitSlop` explicitly in components.md for
FilterChip and SegmentedControl, and add 4–8 dp row spacing where the reach is below 48.

### S40 mismatches reported by the S40 designer (check 9): verified

| Reported mismatch | Verified | Finding |
| --- | --- | --- |
| S06-sign-out confirm should be destructive | Yes: "Sign out" is `bg-primary` | QA-007 |
| S26-revert-confirm "Revert" should be destructive | Yes: primary | QA-008 |
| S10-delete-shared has an icon | Yes: `triangle-alert` in a 48 circle | QA-009 |
| S22-delete, S23-discard, S23-delete not vertically centred | Yes: rendered centre offset −48, −32 and −60 px (S13-close-confirm −32 too) | QA-010 |
| S10-delete / -large-text photos wording | Yes: "Your photos stay in your gallery; nothing on your phone is deleted." vs S40 "The photos in your gallery aren't changed." | QA-012 |
| S10-archive-shared button "Archive list" | Yes: "Archive" | QA-013 |
| S34-transfer-dialog missing sentence | Yes: lacks "Only Mert can make you the Owner again." | QA-014 |
| S21 discard dialog wording (spec) | Yes: spec "Nothing is added to Wedding guests." / "Keep going" vs S40 "Your choices for mert-family.csv will be lost…" / "Keep adding" | QA-015 |
| S17/S26 discard-edits wording | Yes: specs say "Discard changes?" with different bodies | QA-016 |
| S23-discard wording new vs existing template | Yes: frame and spec use "Discard changes to this template?"; S40 names the template | QA-017 |
| S17 remove-field wording + Undo snackbar | Yes: spec "Remove Price?" / "It will be removed from them."; no "Removed Price (€)" snackbar | QA-018 |
| S16/S17 specs link `#S40-default` for Discard import | Yes: S16 §2 line 30, S17 §2 line 28 | QA-028 |
| S24 spec cites S40-end-round for the solo new round | Yes: S24 spec line 204 | QA-029 |
| S32/S33 offline banners should say what needs a connection | **Already compliant**: "Joining a list needs a connection…" / "Joining needs a connection. Connect and try again." | none |
| S08/S27 offline banners wording | Yes: longer variants ("…and sync when you're back online", "4 decisions are saved…") | QA-030 |
| S10-ios-action-sheet Delete → S40-ios-delete-list | Yes: links to `S10-delete` (Android dialog) | QA-011 |
| S10-duplicated snackbar could add "Open" | Yes: no action | QA-031 |

### Reviewer suggestions not accepted

The visual reviewers suggested wider desktop layouts for S25/S26/S36/S38/S39 web-desktop frames. The
brief rules these out (PLT-04, PLT-12: "show the phone layout centered; do not design wide layouts"), so
they are not findings. One reviewer flagged S33-web/S33-web-desktop showing Mert joining as Collaborator.
That matches A-74 (Deniz makes him Decision Maker later in S34), so it is folded into QA-039 (the flow 3
story skips that step).

## Findings

Owner groups: A S01–S07 · B S08–S10 · C1 S11–S15 · C2 S16–S21 · D S22–S23 · E S24/S26/S27 · Lead S25 and
foundations/architecture/prototype · F S28–S30 · G1 S31–S34 · G2 S35–S38 · H S39 · I S40.

| ID | Severity | Area | Screens / frames | Evidence | Recommended fix | Owner | Status | Resolution |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QA-001 | Blocking | traceability | S06 (spec §1) | PLT-20 "Copy is English only" is claimed by no spec §1 (traceability.md gap). S06-language shows "English" as the only language, but the spec does not list PLT-20. | Add PLT-20 to S06-settings.md §1 (Language sub-page). Re-run `node tools/qa/traceability.mjs`. | A | Open | |
| QA-002 | Blocking | traceability | All specs; S25 at least | VIS-07 "No decorative gradients" is claimed by no spec §1. The visual review found no gradients, so this is a citation gap, not a design gap. | Add VIS-07 to the §1 list of S25 (and ideally every spec that cites VIS-01–VIS-06), then re-run the script. | Lead | Open | |
| QA-003 | Blocking | decision model | S27-shared, S36-default, S37-confirm, S37-summary (flow 3) | S27-shared ("Your Round 1 is done") shows Mert at 100 / 100 decided (58/15/27, A-72). The next flow steps (S36 → S37-confirm/summary, A-96) then say "You decided 12 of them… 3 stay open: You haven't decided these items" (c012, c034, c056). A member who decided all 100 items cannot have 3 undecided conflicts. S27-shared also keeps the list status at 32/15/53, although Mert's 15 extra decisions would change it. | Make the flow 3 summary consistent with A-38/A-96. Option 1: Mert ends at 97 / 100 with the 3 open conflicts undecided ("3 items left" summary, list status recomputed). Option 2: Mert stays at 85 and flow 3 goes from S25-web-desktop to S09-shared-decision-maker / S36. Update A-72, S27 spec and navigation-map §6 to match. | E, Lead | Open | |
| QA-004 | Blocking | decision model | S28-shared-change; S28-results.md §4/§6 | Copy: "Changing your decision updates the list status for everyone. Choosing Reject makes this item Agreed." The item is Isabella Rossi: Deniz Accept, Mert Reject, Selin Accept. If Deniz chooses Reject, Selin's Accept still differs, so the item stays a Conflict (DM-04/DM-05). The same string is in the spec. | Use an item where one change really creates agreement (e.g. Sophie Laurent: Deniz and Mert Accept, Selin Maybe, from Selin's view), or change the copy to "Choosing Reject keeps this item in Conflict: Selin chose Accept." Fix the HTML and the spec. | F | Open | |
| QA-005 | Blocking | terminology | S09-sample (both themes); S09-list-overview.md §6 | UI copy uses "product" as the word for items: "20 desk products to practise on…" and the source row "Sample products". This is the product-shortlist case of SUC-06, and design-principles §10 forbids "product" outside template names. | "20 sample items to practise on…" and source "Sample items" (or "Desk setup sample"). Keep the template value "Product". Also use US spelling "practice" (the rest of the copy is US English). | B | Open | |
| QA-006 | Major | decision model | S20-default, S22-import-pick, S22-import-pick-importing, S25-coach-1…4, S27-default (flow 1) | Item counts change during flow 1. The import finishes with "85 items from Contacts. 3 duplicate pairs merged.", while S20-default shows only 1 merge chosen and 2 groups unreviewed ("imported as separate items"). Sorting then starts at "0 / 100 decided" and the summary says "100 / 100 decided in 38 min" (62/14/24). | Use one number through flow 1: the coach frames and the flow 1 summary should use the imported count (85), with a dedicated S27 frame for this first round (or note in navigation-map §6 that S27-default is a later, full-list moment). Align S20-default's choices with "3 duplicate pairs merged". | Lead (S25), D, E, C2 | Open | |
| QA-007 | Major | copy | S06-sign-out | "Sign out" confirm is `bg-primary`; S40-sign-out uses destructive (A-112: sign out = destructive). | Use the destructive variant as in S40-sign-out. | A | Open | |
| QA-008 | Major | copy | S26-revert-confirm | "Revert" confirm is primary; S40-revert-field uses destructive (the edit is discarded). | Destructive variant; spec §6 to match S40. | E | Open | |
| QA-009 | Major | consistency | S10-delete-shared | The dialog shows a `triangle-alert` icon in a 48 circle above the title (geometry.mjs; S10 HTML ~line 401). A-112 says dialogs have no icon, and S40-delete-list-shared has none. | Remove the icon block. | B | Open | |
| QA-010 | Major | visual | S22-delete, S23-delete, S23-discard (also S13-close-confirm) | The rendered dialog centre is offset from the screen centre by −48, −60 and −32 px (S13-close-confirm −32). A-112 says dialogs are vertically centred. | Use the S40 dialog wrapper (`items-center`) in these frames. | D, C1 | Open | |
| QA-011 | Major | platform | S10-ios-action-sheet | The "Delete list" action links to `S10-delete`, the Android Material dialog. The iOS confirmation is S40-ios-delete-list (A-113). | Link to `S40-global-patterns.html#S40-ios-delete-list` and mention the iOS alert in S10 spec §8. | B | Open | |
| QA-012 | Major | copy | S10-delete, S10-delete-large-text (S10 spec) | Body: "Your photos stay in your gallery; nothing on your phone is deleted." S40-default (wins, A-112): "The photos in your gallery aren't changed." | Use the S40 sentence in both frames and the spec. | B | Open | |
| QA-013 | Major | copy | S10-archive-shared | The confirm button reads "Archive"; S40-archive-shared says "Archive list" (buttons name the object). | Rename to "Archive list". | B | Open | |
| QA-014 | Major | copy | S34-transfer-dialog | The body lacks the S40 sentence "Only Mert can make you the Owner again." | Copy the S40-transfer-ownership body. | G1 | Open | |
| QA-015 | Major | copy | S21-add-items.md §6 | The spec's discard dialog says "Nothing is added to Wedding guests." / "Keep going" / "Discard". S40-discard-add-items says "Your choices for mert-family.csv will be lost. Nothing has been added…" / "Keep adding" / "Discard". | Copy the S40 strings into the S21 spec. | C2 | Open | |
| QA-016 | Major | copy | S17-manual-entry.md §6, S26-item-detail.md §6 | The discard-edits dialog is specced as "Discard changes?" with different bodies ("Your changes to this item aren't saved." / "Your edits to Gökhan Doğan won't be saved."). S40-discard-edits: "Discard changes to Gökhan Doğan?" / "Your edits won't be saved. The item keeps its current values." / "Keep editing", "Discard changes". | Use the S40 strings (with the item name) in both specs. | C2, E | Open | |
| QA-017 | Major | copy | S23-discard, S23-template-editor.md §6 | Frame and spec use "Discard changes to this template?" for every case. S40-discard-template names the template ("Discard changes to “Candidate, compact”?"), and the body for an existing template differs. | Spec both variants: new template (unnamed, current S23-discard copy) and existing template (S40 copy). Point to S40-discard-template. | D | Open | |
| QA-018 | Major | copy | S17-manual-entry.md §5/§6 (S17-fields) | Spec: "Remove Price?" / "3 items have a value in Price. It will be removed from them." S40-remove-field: "Remove Price (€)?" / "…The values are removed with the field." The S40 "Removed Price (€)" snackbar with Undo is missing from S17. | Copy the S40 dialog strings, use the full field name, and add the Undo snackbar to the spec. | C2 | Open | |
| QA-019 | Major | prototype | S25-web-desktop, S05-moving, S02-demo (flows 1 and 3) | In flow 3 the partner's web sort is a static frame. The index says "Mert sorts with the keyboard", but arrow keys do nothing, and the only way on is a visually hidden link (flows test activates it with Tab + Enter). S05-moving and S02-demo (both auto-advance in the app) also continue only through sr-only links. A founder clicking with a mouse is stuck on these frames. | Link S25-web-desktop's decision bar (or the whole card) to `swipe-demo.html?deck=wedding&next=S27-shared` so web sorting is live. Make the S05-moving/S02-demo shortcuts visible in prototype mode (e.g. a small "Continue (prototype)" link in the canvas label), or note them in 04-prototype/index.html. | Lead | Open | |
| QA-020 | Major | visual | S40-snackbar, S40-snackbar-undo, S40-snackbar-success-action | The snackbars contradict the screen behind them. "You left “Wedding guests”" shows Wedding guests still in Lists, and Deniz is its Owner, who cannot leave (S40-leave-owner). "List deleted" + Undo shows all lists still present. "Duplicated as “Desk setup (copy)”" shows no copy. | Update the host screens (row removed or copy added), and use an action Deniz can take. | I | Open | |
| QA-021 | Major | decision model | S25-shared-menu | The frame and S25 spec promise the "Show others' decisions" switch (SRT-12), but the shared menu shows only Card template / Show the tutorial again / Open item details / End round. Nothing reaches S25-shared-others. The menu item "End round (Owner)" also leaks a role note into UI copy. | Add the "Show others' decisions" row with a switch (off by default) at the top of the menu, and label the item "End round". | Lead | Open | |
| QA-022 | Major | visual | S25-shared-others | The others'-decision avatars are 24 px with oversized decision badges that overlap the next avatar. Mert's Maybe badge covers half his face, and Selin's initials are cut by her dashed badge, so the decisions are hard to read. They are also not legible as text (color/icon only at tiny size). | Remove the negative overlap or use 32 px avatars with smaller badges, and add text ("Mert: Maybe, Selin: not decided") or a tap target that reveals it. | Lead | Open | |
| QA-023 | Major | decision model | S27-shared, S27-shared-owner, S27-offline, S27-web-desktop, S30-in-progress, S30-shared-detail | The list-status bar uses the darkest fill for Agreed (32 %) and mid-grey for Conflict, while the chips use the inverted dark chip for Conflict and an outline chip for Agreed. Readers map the dark chip to the dark segment and read "32 conflicts". The S30 bars have no legend. | Fill the segments with the chip tokens (Conflict = `bg-conflict`, Agreed light/outline, Pending `muted`) or put a swatch under each segment; add a legend in S30. | E, F | Open | |
| QA-024 | Major | consistency | S30-default, S30-ios, S30-large-text, S30-round-detail, S30-round-2-detail, S30-shared-detail | Decision split bars and legends run Accept → Maybe → Reject (green left). That reverses the same rounds in S27 and the "always Reject · Maybe · Accept" rule (design-principles §5). Only the Results segments are a documented exception (A-107). | Reorder to Reject, Maybe, Accept (or document a second exception and align S27). | F | Open | |
| QA-025 | Major | copy | S31-pending | Members shows Mert as Decision Maker, but the "Decision Maker" invite option still says "There's one Decision Maker, so the role moves from you to them." | "…so the role moves from Mert to them." (or disable the option with that reason). | G1 | Open | |
| QA-026 | Major | visual | S22-import-pick-custom (flow 4) | The "Template saved" snackbar covers the template tile row and hides the name of the just-saved, selected template, which is the point of this state. | Move the snackbar above the bottom bar with the selected tile visible, or name the template in the snackbar ("Saved “Candidate, short”"). | D | Open | |
| QA-027 | Major | consistency | All desktop web frames with `<kbd>`: S02-web-desktop, S23-web-desktop, S24-web-desktop, S25-web-desktop, S26-web-desktop, S27–S29 web-desktop, S36-web-desktop, S40 web frames; components.md Kbd | Keyboard hint chips render in the browser's monospace font ("Z", "N", "Alt", "Esc" visibly mono), because Tailwind preflight sets `kbd { font-family: ui-monospace }` and the chips have no `font-sans`. This is template tell §15.8 in the key web sorting frame. | Set `kbd { font-family: inherit }` in the foundations base layer (input.css) or add `font-sans` to the Kbd component. Re-run build:css. | Lead | Open | |
| QA-028 | Minor | copy | S16-plain-text.md §2 (line 30), S17-manual-entry.md §2 (line 28) | Close → "Discard import?" links to `S40-global-patterns.html#S40-default`, which is the delete-list dialog. | Link to `#S40-discard-import`. | C2 | Open | |
| QA-029 | Minor | copy | S24-start-round.md (line 204), S24-end-round-dialog | The spec cites S40-end-round for the solo "start a new round while one is open" case; the matching pattern is S40-new-round. The S24-end-round-dialog title "End Round 1 for everyone?" is paired with the button "End Round 1 and start", and S40 has no shared new-round variant. | Cite S40-new-round. Add a shared variant to S40 (title "End Round 1 for everyone and start Round 2?") or align the S24 title and button. | E, I | Open | |
| QA-030 | Minor | copy | S08-offline, S27-offline | The offline banners say "You're offline. Changes are saved on this phone and sync when you're back online." and "…4 decisions are saved on this phone and will sync later." S40 pattern: "You're offline. Changes are saved on this phone." | Use the S40 wording (plus what needs a connection where relevant). | B, E | Open | |
| QA-031 | Minor | copy | S10-duplicated | The snackbar "Duplicated as “March photos clean-up (copy)”" has no action, so the new list is hard to find. | Add an "Open" action (S40 snackbar-success-action pattern). | B | Open | |
| QA-032 | Minor | platform | S11-web, S11-web-desktop | The web-unavailable Contacts tile shows the reason but no visible "Get the app" link (design-principles §13, PLT-11). It only appears in the sheet after tapping (S11-web-unavailable). S21-web shows the link in its footer, so the two pickers disagree. | Add the S21-web footer line ("Contacts import needs the Android or iOS app. Get the app") to S11-web and S11-web-desktop. | C1 | Open | |
| QA-033 | Minor | coverage | S02-onboarding.html, S05-sign-in-prompt.html, S32-invite-link.html | No `Sxx-default` frame, which navigation-map §5 requires ("Every screen file must contain a Sxx-default frame"). | Rename the main frame (S02-welcome → also id S02-default, etc.) or relax the rule in navigation-map §5. | A, G1 | Open | |
| QA-034 | Minor | coverage | S15, S18 | No large-text frame (most import screens have one; PLT-16 is not claimed by S15/S18). | Add a 200% frame for the S15 tab picker and the S18 grid, or note in the spec how they reflow. | C1, C2 | Open | |
| QA-035 | Minor | a11y | S03 (11 frames: Terms of Service, Privacy Policy), S20-default/-reviewed-all/-ios ("Review merge"), S28 (14–15 frames: Filter, Recently decided, Price high to low), S29-value-picker, S29-applied, S29-ios, S29-web-desktop (value chips) | These targets cannot reach 48 × 48 even with hitSlop, because neighbours leave too little room (geometry.mjs: reach 43–46 high; S29 value chips 44). The S03 legal links are inline text (WCAG 2.5.8 inline exception), so they are acceptable. The other 328 small controls can reach 48 with hitSlop. | Add 4–8 dp vertical spacing around the S28 chip row and the S29 value chips. Make "Review merge" a 48-high ghost button. In components.md, state `hitSlop` for FilterChip (36) and SegmentedControl segments (40). | C2, F, Lead | Open | |
| QA-036 | Minor | terminology | S20-default, S20-merge, S20-large (S20 spec) | Glossary drift: "Merge 2 records", "Photo from the first record", "Your contacts have many repeated entries". | Use "items": "Merge 2 items", "Photo from the first item", "…many repeated items". | C2 | Open | |
| QA-037 | Minor | terminology | S02-welcome, S02-welcome-ios, S02-welcome-large-text, S02-web | "Works for people, products, photos and ideas." lists kinds of lists rather than naming items, so it is borderline under §10. | Optional: "Works for people, photos, things to buy and ideas." | A | Open | |
| QA-038 | Minor | decision model | S25-shared-conflict | After Deniz rejects Mia Andersson, the Undo label still reads "Undo last decision (Accept on Ayşe Demir)", and the next card behind the top card is the same item (Anna-Katharina Rosenthal-Brückner twice). | Undo label "Undo last decision (Reject on Mia Andersson)" and show the next item behind. | Lead | Open | |
| QA-039 | Minor | flow | S33-web-desktop → S25-web-desktop → S27-shared → S36-default (flow 3) | The flow 3 story skips steps. Mert joins as Collaborator (A-74), is at 85 / 100 in the very next frame, and is Decision Maker by S36. The role change in S34 is not part of the flow or the prototype index. | Add a one-line note in 04-prototype/index.html and navigation-map §6 ("later: Deniz makes Mert Decision Maker, S34-dm-changed"), or insert that step. | Lead | Open | |
| QA-040 | Minor | traceability | S07-profile.md §1, S21-add-items.md §1 | S07 claims DM-15 (rounds are started by the Owner) for the ownership hand-over; COL-11 is the right ID. S21 claims SRC-23 (Google connection failure) but shows only the offline Google tile. | Fix the citations (S21: add a Google failure state or drop SRC-23). | A, C2 | Open | |
| QA-041 | Minor | traceability | requirements SCR-00 | No spec claims SCR-00 (all applicable states). traceability.md maps it to coverage.md and this report. | Optional: cite SCR-00 in every spec §4. | Lead | Open | |
| QA-042 | Minor | consistency | 05-qa/screenshots | The foundations (DS-*, C-*) screenshots are deleted from the working tree (git status), so DEL-17 ("light and dark PNG of every frame") is incomplete for 01-foundations and 04-explorations. | Re-run `npm run shots -- --dir=01-foundations` and `--dir=04-explorations`. | Lead | Open | |
| QA-043 | Minor | visual | S10-ios-archived | The swiped row shows only "3 accepted"; the list name is off-screen, so the row no longer says which list the actions apply to. | Keep the title visible (truncated) or narrow the actions. | B | Open | |
| QA-044 | Minor | visual | S02-welcome-large-text | Only the headline scales to 200%; the body stays normal size (~380 px of empty canvas) and "No account needed" is dropped. | Scale the body copy and keep the note. | A | Open | |
| QA-045 | Minor | visual | S02-demo-large-text | With the image hidden the card keeps full height, leaving ~400 px of blank card between title and price. | Shrink the card to its content or show more fields. | A | Open | |
| QA-046 | Minor | visual | S02-demo-snap-back | The hint snackbar overlaps the card's bottom edge; a sliver of the "Desk" chip peeks out. | Place the hint below the card. | A | Open | |
| QA-047 | Minor | visual | S03-offline, S03-email-offline, S04-offline, S04-new-password-offline, S06-offline, S06-feedback-error, S07-offline, S09-offline | The offline banner sits flush against the next element (no top gap). | Add the section gap below the banner. | A, B | Open | |
| QA-048 | Minor | visual | S03-google-cancelled | The snackbar covers the Terms/Privacy footer; the underline of "Privacy Policy" peeks out below it. | Lift the snackbar above the footer. | A | Open | |
| QA-049 | Minor | visual | S03-ios, S03-ios-context-share | "Continue with Apple" uses the Lucide `apple` fruit icon instead of the Apple logo required by HIG. | State in the spec that the native Sign in with Apple button is used (A-51 stand-in). | A | Open | |
| QA-050 | Minor | visual | S03-error-locked | Sign-in is "paused for 15 minutes" but the filled "Sign in" stays enabled; "Forgot password?" duplicates the notice's "Reset password". | Disable Sign in while locked; drop the duplicate link. | A | Open | |
| QA-051 | Minor | visual | S03-error-uses-google | The primary action stays "Sign in" (password); the real fix, "Continue with Google", is a secondary button in the notice. | Promote "Continue with Google" to the main action. | A | Open | |
| QA-052 | Minor | visual | S04-sent, S04-resent, S04-large-text (dark) | "Send again in 0:42" is disabled-primary text: dim indigo on near-black, hard to read in dark. | Use `text-muted-foreground` for the countdown. | A | Open | |
| QA-053 | Minor | visual | S05-* sheets, S07-change-photo, S07-delete-transfer, S07-reauth, S07-web-change-photo, S09-source-details, S10-archived-menu, S10-row-sheet | Bottom sheets stop above the gesture bar, leaving an un-scrimmed strip; the status-bar strip is not covered by the scrim either. | Extend the sheet and scrim under the system bars. | A, B | Open | |
| QA-054 | Minor | visual | S05-moved, S05-moved-backup, S05-moved-merge | The success sheet says lists moved to the account, but the screen behind still says "Lists are on this phone only" with "Back up". | Update the host screen to the backed-up state. | A | Open | |
| QA-055 | Minor | visual | S06-default, S06-guest, S06-offline, S06-web… (bottom navigation) | At scale 1 the active "Settings" label renders as "Setting s" (QA crop confirmed). Likely glyph hinting of `text-caption font-semibold` at 1×, but visible in the review screenshots. | Check at scale 2; if it persists, adjust letter-spacing/weight for the active label. | Lead | Open | |
| QA-056 | Minor | visual | S06-large-text, S07-large-text, S09-large-text | Content stops early with 150–180 px of blank canvas; S06 drops the Activity badge, S07 omits the Delete account row, S09 ends after "Start a new round". | Continue rows to the frame edge or the nav; keep the badge. | A, B | Open | |
| QA-057 | Minor | visual | S06-*, S08-*, S10-archived-snackbar, S10-deleted-snackbar (Activity unread badge) | The unread badge uses `bg-destructive`, which §4 reserves for delete/remove/errors. | Use `primary` (or inverse foreground) for count badges; update components.md. | Lead | Open | |
| QA-058 | Minor | visual | S07-default, S07-google-*, S07-no-photo, S07-offline, S07-password-changed, S07-photo-uploading, S07-ios | The Google row text starts ~4 px further right than other rows (wider bordered "G" badge). | Give the badge a 20 px slot. | A | Open | |
| QA-059 | Minor | visual | S07-photo-uploading (dark) | The spinner is dark indigo on a light-washed avatar, nearly invisible; light uses a dark scrim with a white spinner. | Use the same treatment in both themes. | A | Open | |
| QA-060 | Minor | visual | S07-add-password, S07-change-password* | Rule "A number or a symbol" vs "A number or symbol" in S03/S04. | Use one wording. | A | Open | |
| QA-061 | Minor | visual | S08-large-text | The extended "New list" FAB covers the Desk setup summary, cutting it to "1 mayb". | Collapse the FAB to icon-only at large text or add bottom padding. | B | Open | |
| QA-062 | Minor | visual | S08-web-desktop | The FAB sits ~8 px below the Archived lists group. | Add bottom padding to the list. | B | Open | |
| QA-063 | Minor | visual | S09-new-list, S10-duplicated (dark) | The dark-mode hairline border narrows the group so "Card template" and "Copied from March photos clean-up" wrap only in dark. | `min-w-0 truncate` on values, `shrink-0` on labels. | B | Open | |
| QA-064 | Minor | visual | S09-shared-collaborator | The "Collaborator" role has no icon while Owner (crown) and Decision Maker (gavel) do. | Give every role an icon or none. | B | Open | |
| QA-065 | Minor | visual | S10-web-desktop | The dialog scrim covers only the app column; the desktop margins stay bright. | Extend the scrim to the viewport (match S40-web-dialog). | B | Open | |
| QA-066 | Minor | visual | S10-duplicated, S10-renamed | The snackbar overlaps the Sources group with fragments of rows peeking out. | Add bottom padding or change the scroll position. | B | Open | |
| QA-067 | Minor | visual | S13-ios-limited, S14-partial | The "Share more contacts" / "Show skipped rows" ghost links sit ~8 px right of the notice text (conflicting `px-5` and `px-3 -ml-3`). | Drop the duplicate `px-5`. | C1 | Open | |
| QA-068 | Minor | visual | S13-large-text, S19-large-text | The scrolling list stops early (4 contacts / 2 fields) with 100–160 px of empty canvas above the bottom bar. | Add rows so the list runs under the bottom bar. | C1, C2 | Open | |
| QA-069 | Minor | visual | S14-csv-preview, S14-no-header | The preview table ends exactly at a column edge, so the horizontal scroll (6 more columns) is not signalled (S14-excel-sheets does show a cut column). | Let the next column peek in. | C1 | Open | |
| QA-070 | Minor | visual | S16-large-text | The "Open a .txt file" button label is visibly smaller and lighter than the other scaled labels. | Use the scaled button label style. | C2 | Open | |
| QA-071 | Minor | visual | S17-add-item, S17-add-another, S17-edit-item, S17-field-sheet, S17-validation | The sheet header title is top-aligned while the close X is centred, ~12 px lower. | `items-center` on single-line sheet headers. | C2 | Open | |
| QA-072 | Minor | visual | S17-default, S17-deleted | Item names (main information) are hard-truncated ("27-inch 4K USB-C m…") by two trailing icon buttons; the price shows "389, Nordhaus" without the € unit. | Let titles wrap to 2 lines; format "€389". | C2 | Open | |
| QA-073 | Minor | visual | S18-default | Every day group holds exactly 2 photos, so the right half of each 4-column row is empty; the main frame looks sparse. | Vary the photos per day (4–7 for recent days). | C2 | Open | |
| QA-074 | Minor | visual | S18-loading | The "All photos" pill runs past the 20 px right gutter. | Reserve the trailing slot or add `pr-gutter`. | C2 | Open | |
| QA-075 | Minor | visual | S18-web-uploading | The compact drop zone wraps "Drop more photos here" next to a large button; looks cramped. | Shorten the text or stack. | C2 | Open | |
| QA-076 | Minor | visual | S19-web-desktop | The type popover opens upward and covers the stepper, the field count and the name of the field being edited. | Open below the chip or keep the field name visible. | C2 | Open | |
| QA-077 | Minor | visual | S20-large, S20-summary | Item names in duplicate rows are truncated ("Can Öztürk and Can Ozt…") by the status select; names are the main information. | Wrap titles to 2 lines or show the shared name once. | C2 | Open | |
| QA-078 | Minor | visual | S20-reviewed-all, S20-scrolled | The phone comparison wraps the label in one column but not the other; the right column runs into the card edge. | Same label layout in both columns. | C2 | Open | |
| QA-079 | Minor | visual | S21-ios | "From your Google Drive" wraps in the narrower iOS tile and misaligns the tile titles (S11 uses "From Google Drive"). | Use S11's copy. | C2 | Open | |
| QA-080 | Minor | visual | S21-offline, S22-change-offline | The offline banner butts against the next element; its placement differs from S11-offline. | Place it under the app bar as in S11-offline, with section spacing. | C2, D | Open | |
| QA-081 | Minor | visual | S22-change, S22-change-applied, S22-change-shared, S22-change-offline, S22-import-pick* | Template tile captions do not line up: two-line names push the status label down, and the Person tile in S22-change-applied has no status line. | Bottom-align the status line; give built-ins a status. | D | Open | |
| QA-082 | Minor | visual | S22-import-pick-partial | The summary says "30 items from Photos." while the notice and button say 28 are ready. | "28 of 30 photos copied". | D | Open | |
| QA-083 | Minor | visual | S22-renamed, S22-duplicated, S23-duplicated, S24-collaborator-asked | The snackbar half-covers the "New template" button or the first field row. | Scroll the content or pad by the snackbar height. | D | Open | |
| QA-084 | Minor | visual | S23-field-picker | The sheet is near full height but its content ends at ~70 %, leaving ~220 px empty. | Let the sheet hug its content. | D | Open | |
| QA-085 | Minor | visual | S23-ios | The preview card touches the two-line nav title; "Years of experience" wraps because of three icon buttons. | Add 12–16 px top spacing; tighten the controls. | D | Open | |
| QA-086 | Minor | visual | S23-default, S23-duplicated, S23-edit-saved, S23-ios, S23-preview-full, S22-import-pick-custom, S22-import-pick-text, S25-candidate | The compact sample template leaves 55–65 % of the hero card blank; the editor preview looks unfinished. | Use a sample with 3–4 field rows, or define in the card spec how sparse cards distribute space. | D, Lead | Open | |
| QA-087 | Minor | visual | S25-drag-maybe | The card dragged up covers the "76 / 100 decided" row and clips "Round 1". | Cap the drag offset below the progress row. | Lead | Open | |
| QA-088 | Minor | visual | S25-coach-3 | The raised demo card clips the descenders of "0 / 100 decided". | Lower the card a few px. | Lead | Open | |
| QA-089 | Minor | visual | S25-large-text | ~300 px of the card is empty while Email is hidden behind "2 more fields in details". | Show Email in the free space or shrink the card. | Lead | Open | |
| QA-090 | Minor | visual | S25-long-text | The name is clamped to "…von Hohenberg-…", losing the surname. | Allow a 4th line or step the size down. | Lead | Open | |
| QA-091 | Minor | visual | S25-resume, S32-already-member, S32-expired, S32-list-deleted, S32-reset | Centred text leaves widows ("1.", "join.", "link.") and splits names ("Wedding / guests", "Deniz / Yılmaz"). | `text-wrap: balance` and non-breaking spaces in names. | Lead, G1 | Open | |
| QA-092 | Minor | visual | S26-default, S26-edit, S26-edit-date and other S26 sheets | Text edges step: "Item details"/"My decision" sit on the gutter, "Fields"/"Notes"/footnotes 4 px further in (`px-1`). | One text edge. | E | Open | |
| QA-093 | Minor | visual | S26-decision-changed and S26 product frames | `object-cover` crops the product image (monitor bezel and stand cut). | `object-contain` on a neutral background for product images. | E | Open | |
| QA-094 | Minor | visual | S26-web-desktop | The keyboard hint row wraps, leaving "→ Accept" alone on a second line. | Fit the hints on one row. | E | Open | |
| QA-095 | Minor | visual | S26-ios-edit | The underlying "Wedding guests" title is sliced by the sheet edge. | Hide it or move the sheet top. | E | Open | |
| QA-096 | Minor | visual | S26-saved, S31-link-copied, S31-reset-done, S25-undo, S33-joined, S34-removed, S34-transferred | The snackbar half-covers a text row. | Pad the content or scroll the frame. | E, G1, Lead | Open | |
| QA-097 | Minor | visual | S28-changed, S28-empty-segment | S28-changed shows "Maybe 0" next to "Search 1 item in Maybe"; S28-empty-segment shows a live "Search 0 items" field above the empty state. | Keep the placeholder in sync; hide search on empty segments. | F | Open | |
| QA-098 | Minor | visual | S25-error, S34-error, S28-error | The full-screen errors differ (secondary centred vs filled primary in the upper third). | One treatment (S40-error). | Lead, F, G1 | Open | |
| QA-099 | Minor | visual | S28-large-list | The fast-scroll "M" bubble covers a status chip ("Agre…"). | Move the bubble clear of the status column. | F | Open | |
| QA-100 | Minor | visual | S28-large-text, S28-large-text-menu, S31-large-text, S33-large-text, S34-large-text | At 200 % text, badges, section labels, "Reset link" and role lines stay ~12 px. | Scale them with the font scale. | F, G1 | Open | |
| QA-101 | Minor | visual | S28-shared-resolved | The wide "Resolved by Mert" chip wraps every row's meta onto two lines. | Shorten to icon + "Resolved". | F | Open | |
| QA-102 | Minor | visual | S29-default, S29-no-results and other S29 sheets | The dimmed Results backdrop is a broken copy of S28 (back arrow ~6 px from the edge, Export loses its style) because `display: contents` spans replace the buttons. | Reuse the S28 app-bar markup, inert. | F | Open | |
| QA-103 | Minor | visual | S30-round-detail, S30-round-2-detail | Item names are truncated to ~13 characters. | Wrap to 2 lines or use compact badges. | F | Open | |
| QA-104 | Minor | visual | S32-get-app (dark) | The QR code is inverted in dark mode (cameras often fail on inverted codes), and it is a stylized glyph rather than a real QR code. | Keep the QR tile light in both themes; use a real QR for swipesort.app/get. | G1 | Open | |
| QA-105 | Minor | visual | S33-no-round | The role card still says "All 100 items of Round 1 / Everyone sorts every item of the round" with no round in progress. | Use next-round copy ("You'll sort every item when Deniz starts Round 2"). | G1 | Open | |
| QA-106 | Minor | visual | S33-decision-maker | Comma splice: "Under the current rule, Decision Maker decides, your choice on a conflict is final."; Deniz's member row uses a different layout. | "Under the current rule (Decision Maker decides), your choice on a conflict is final." | G1 | Open | |
| QA-107 | Minor | visual | S34 frames (content wrapper `px-4`) | The groups sit on a 16 px margin instead of the 20 px `px-gutter` used by S28/S31/S33. | Use `px-gutter`. | G1 | Open | |
| QA-108 | Minor | visual | S34-default, S34-dm-changed, S34-dm-confirm, S34-dm-off-confirm | An exclusive role is set with three independent switches (DM-10 says "a single switch"); S34-dm-confirm shows two switched on behind the dialog. | Keep the switches (brief DM-10) but show exactly one on behind the dialog, and state the exclusivity in the group footer (already partly there). | G1 | Open | |
| QA-109 | Minor | visual | S34-ios, S34-ios-actions, S34-transferred, S34-empty | On rows with long roles "85 / 100 decided" wraps under the role, so the rows have different heights. | nowrap or a fixed count column. | G1 | Open | |
| QA-110 | Minor | visual | S35-dm-none | The Decision Maker rule example says "Mert chooses the final decision." although nobody holds the role in this state. | "The Decision Maker chooses the final decision." | G2 | Open | |
| QA-111 | Minor | visual | S35-offline | Only the radio circles are dimmed; titles and the selected border stay full strength, so the options look tappable. | Dim the option tiles as unavailable (keep the reason readable). | G2 | Open | |
| QA-112 | Minor | visual | S36-majority | The "Waiting for 1 member" chip uses the Conflict chip (inverted, git-compare-arrows) with Pending wording. | Conflict chip + waiting text below it, or the Pending clock chip. | G2 | Open | |
| QA-113 | Minor | visual | S36-everyone-agreed | The "Agreed" chip stands alone; §5 puts the final decision badge next to it. | Add the "Accepted" badge. | G2 | Open | |
| QA-114 | Minor | visual | S36-remaining | At 0 / 3 left (all items Mert never decided), "Resolve all" stays active although it would skip all of them. | Disable or hide Resolve all in this state. | G2 | Open | |
| QA-115 | Minor | visual | S36-resolved | Same Gülşen Aydın card as S36-dm-undecided without the "You haven't decided this item. Resolve all skips it" notice. | Show the notice. | G2 | Open | |
| QA-116 | Minor | visual | S36-list | Rows show member decisions only as avatar badges (no visible text); the badge half covers Selin's initials. | Add a text line per row; offset the badge. | G2 | Open | |
| QA-117 | Minor | visual | S37-confirm, S37-ios, S37-large-text, S37-offline, S37-resolving, S37-nothing (light) | The "12 will be resolved" / "3 stay open" groups have no visible container in light (white on white); in dark they are bordered. | Tint or hairline in light, matching dark. | G2 | Open | |
| QA-118 | Minor | visual | S37-confirm, S37-ios, S37-large-text, S37-offline, S37-resolving | The title "Resolve 15 conflicts with your decisions?" while the button resolves 12. | "Resolve 12 conflicts with your decisions?" (body keeps "3 stay open"). | G2 | Open | |
| QA-119 | Minor | visual | S37-resolving | "Resolving 12 conflicts…" above the button and "Resolving…" inside it. | Keep one. | G2 | Open | |
| QA-120 | Minor | visual | S37-undo, S40-transfer-ownership | "Undo Resolve all" (discards 12 final decisions) and "Make Mert Owner" (Deniz loses Owner rights) use primary; A-112 lists "removes access" and discarding as destructive. | Decide and document in A-112 / S40 spec; apply consistently. | G2, I | Open | |
| QA-121 | Minor | visual | S38-web-desktop | The web toast repeats the unread top row of the open Activity feed and covers a row mid-text. | No toast for events already visible in the open feed. | G2 | Open | |
| QA-122 | Minor | visual | S38-in-app-banner | The banner says "Mert resolved 12 conflicts… 3 are still open" over an S35 screen that still says "Mert has 15 conflicts to resolve". | Use a host screen without conflict counts or update them. | G2 | Open | |
| QA-123 | Minor | visual | S39-google-destination, S39-apartments-destination | The account row says "Google account, read-only" on the step that writes; the shared variant uses different wording. | One sublabel that does not contradict writing (e.g. "Signed in with Google"). | H | Open | |
| QA-124 | Minor | visual | S39-ios-share | The native share sheet is drawn as grey placeholder shapes with a large empty area. | Tighten the sheet or note it as system UI (out of scope). | H | Open | |
| QA-125 | Minor | visual | S40-end-round | Labelled solo but drawn on the shared Wedding guests list; 88 / 100 with 20/13/55 matches no sample member. | Use a solo list (March photos clean-up). | I | Open | |
| QA-126 | Minor | visual | S40-desktop-frame, S40-web-toast | Lists shows "Apartment viewings, Archived" as a row although archived lists are a separate group; S40-desktop-frame drops the progress bars S40-desktop-short shows. | Keep the Lists content consistent across frames. | I | Open | |
| QA-127 | Minor | visual | S40-snackbar-large-text | The New list FAB overlaps the lists group by ~10 px. | Move the FAB up or hide it while the snackbar shows. | I | Open | |
| QA-128 | Minor | visual | S40-web-dialog | Cancel and Delete list are ~4 px apart (12–16 px in mobile dialogs). | Use the mobile gap. | I | Open | |
