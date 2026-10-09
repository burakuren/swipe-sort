# Navigation map

How every screen connects. Route names follow expo-router conventions so the coding agent can map them
directly. Screen files live in `03-screens/`; each screen's main frame is `Sxx-default` unless noted.

## 1. Structure

```
Root stack
├── S01 Splash (cold start only, replaced by next route)
├── S02 Onboarding (first launch only; can be replayed from Settings › Help)
├── (tabs)                                  bottom navigation: Lists · Activity · Settings
│   ├── index        → S08 Home (lists)
│   ├── activity     → S38 Activity (feed; badge = unread)
│   └── settings     → S06 Settings (+ sub-pages pushed in the same tab stack, S07 Profile)
├── list/[listId]    (stack, pushed over tabs; bottom navigation hidden)
│   ├── index        → S09 List overview (solo | shared)
│   ├── results      → S28 Results          (S29 Filter and sort = bottom sheet)
│   ├── rounds       → S30 Round history
│   ├── members      → S34 Members and roles (S31 Invite = full-height sheet)
│   ├── conflict-rule→ S35 Conflict rule settings
│   ├── conflicts    → S36 Conflicts: one-by-one resolution
│   ├── template     → S22 Template library (mode: change list template) → S23 Template editor
│   ├── export       → S39 Export flow (stack inside a full-screen modal)
│   └── item/[itemId]→ S26 Item detail (also opened as a sheet from S25)
├── sort/[listId]    (full-screen modal, no tabs) → S25 Sorting → S27 Round summary (replace)
├── round/new        (full-screen modal)          → S24 Start a round
├── import           (full-screen modal stack; one stepper for every source)
│   ├── index        → S11 Source picker
│   ├── permission   → S12 Pre-permission (contacts | photos) and denied recovery
│   ├── contacts     → S13   file → S14   google → S15   text → S16   manual → S17   photos → S18
│   ├── fields       → S19 Field mapping
│   ├── duplicates   → S20 Duplicate review (skipped automatically when none are found)
│   └── finish       → S22 in "pick" mode: choose card template + name the list → Start sorting
├── list/[listId]/add→ S21 Add items to an existing list (reuses import steps; ends with "Add to list")
├── auth             (modal stack)
│   ├── sign-in      → S03 Sign up / sign in
│   ├── forgot       → S04 Forgot password
│   └── prompt       → S05 Sign-in prompt (bottom sheet from share/backup) + moving lists
├── join/[token]     → S32 Opening an invite link → S33 Join a list
└── Global overlays (S40): dialogs, snackbars, offline banner, sync notice, error and not-found screens
```

Back behavior: Android system back and iOS edge swipe close the topmost sheet or dialog first, then pop the
stack. Modals (import, sort, round/new, export, auth) close with an `x` button top-left; leaving import with
unsaved progress asks "Discard import?" (S40). Sorting never asks: progress is saved continuously.

## 2. Canonical files

| ID | File | Group |
| --- | --- | --- |
| S01 | `S01-splash.html` | A |
| S02 | `S02-onboarding.html` | A |
| S03 | `S03-sign-in.html` | A |
| S04 | `S04-forgot-password.html` | A |
| S05 | `S05-sign-in-prompt.html` | A |
| S06 | `S06-settings.html` | A |
| S07 | `S07-profile.html` | A |
| S08 | `S08-home.html` | B |
| S09 | `S09-list-overview.html` | B |
| S10 | `S10-list-management.html` | B |
| S11 | `S11-source-picker.html` | C1 |
| S12 | `S12-permissions.html` | C1 |
| S13 | `S13-contacts-import.html` | C1 |
| S14 | `S14-file-import.html` | C1 |
| S15 | `S15-google-sheets.html` | C1 |
| S16 | `S16-plain-text.html` | C2 |
| S17 | `S17-manual-entry.html` | C2 |
| S18 | `S18-photos-import.html` | C2 |
| S19 | `S19-field-mapping.html` | C2 |
| S20 | `S20-duplicate-review.html` | C2 |
| S21 | `S21-add-items.html` | C2 |
| S22 | `S22-template-library.html` | D |
| S23 | `S23-template-editor.html` | D |
| S24 | `S24-start-round.html` | E |
| S25 | `S25-sorting.html` | reference (lead) |
| S26 | `S26-item-detail.html` | E |
| S27 | `S27-round-summary.html` | E |
| S28 | `S28-results.html` | F |
| S29 | `S29-filter-sort.html` | F |
| S30 | `S30-round-history.html` | F |
| S31 | `S31-invite.html` | G1 |
| S32 | `S32-invite-link.html` | G1 |
| S33 | `S33-join-list.html` | G1 |
| S34 | `S34-members.html` | G1 |
| S35 | `S35-conflict-rule.html` | G2 |
| S36 | `S36-conflicts.html` | G2 |
| S37 | `S37-bulk-resolve.html` | G2 |
| S38 | `S38-activity.html` | G2 |
| S39 | `S39-export.html` | H |
| S40 | `S40-global-patterns.html` | I |

## 3. Screen connections

| ID | Entry points | Exits |
| --- | --- | --- |
| S01 | App cold start | S02 (first launch), S08 (returning), S32 (opened via invite link) |
| S02 | S01 first launch; Settings › Help › "Replay the introduction" | S08 first-run (Get started); S03 ("I have an account") |
| S03 | S02; S05 (Continue with email); S06 (Sign in row, guest); S32 web (sign in to join) | Back to origin; S04; S05 moving-lists step (when guest lists exist) |
| S04 | S03 "Forgot password?" | S03 (after reset link sent / Back to sign in) |
| S05 | S09/S10 Share or Invite while guest; S06 Backup "Back up lists" while guest; S08 not-backed-up indicator | S03 (email); Google/Apple native sheet (out of scope) → moving lists → origin action continues (S31 or backup on) |
| S06 | Tab Settings | Sub-pages (theme, haptics, notifications, language, privacy, help, about, backup, card templates → S22); S07; S03 (guest sign in); sign out dialog (S40) |
| S07 | S06 profile row | Connected accounts; delete account flow → S08 signed-out home |
| S08 | Tab Lists; S02; after delete/leave list | S09 (list row); S11 (Import a list / New list FAB); sample list → S09 sample; S05 (indicator); S10 archived lists; S25 (Resume chip on a list in progress) |
| S09 | S08; deep links from notifications | S25 (Continue sorting / Start sorting); S24 (Start new round); S28; S30; S34; S35; S36 (Review conflicts); S39 (Export); S21 (Add items); S22 (Card template); S10 (overflow menu); S31 (Invite / Share) or S05 if guest |
| S10 | S09 overflow menu; S08 row long-press; S08 › Archived lists | Rename dialog; Duplicate → new S09; Archive → S08 with snackbar; Delete dialog → S08; Leave dialog → S08; Archived lists screen → S09 (read-only) / Restore |
| S11 | S08 (Import a list / +); S21 (Add from another source) | S12 (contacts, photos without permission); S13–S18; web-unavailable tile → "Get the app" |
| S12 | S11 contacts or photos tile; S38 / S06 notifications toggle (notifications explainer) | System permission prompt (out of scope) → S13 / S18; denied → recovery state → system settings or another source (S11) |
| S13 | S12 granted; S11 when permission already granted | S19 |
| S14 | S11 CSV / Excel tile | System file picker (out of scope) → preview → S19; errors → retry / choose another file |
| S15 | S11 Google Sheets tile | Google account chooser (out of scope) → spreadsheet → tab → S19 |
| S16 | S11 Plain text tile | S19 (single field "Text": rename and type only), then S20 / S22 pick |
| S17 | S11 Manual entry tile | S22 pick (manual entry defines fields inline, no S19) |
| S18 | S12 granted; S11 on web (file upload) | S22 pick (photos have fixed fields; S19 skipped) |
| S19 | S13, S14, S15, S16 | S20 (duplicates found) or S22 pick |
| S20 | S19 | S22 pick (import) or S21 confirm (add items) |
| S21 | S09 "Add items" | S11 (choose source, list context) → … → S20 → "Add to list" → S09 with snackbar |
| S22 | Import finish (pick mode); S09 Card template (change mode); S06 › Card templates (manage mode) | S23 (Customize / New template); S25 (Start sorting, pick mode); S09 (template applied) |
| S23 | S22 | S22 (Save template), discard dialog (S40) |
| S24 | S09 Start new round; S27 "Start a new round" / "Re-sort Maybe" (preselected) | S25 (Start round) |
| S25 | S22 pick (Start sorting); S09; S24; S08 resume chip; S33 Start sorting | S26 (tap card; sheet); note sheet; S27 (last card decided); S09 (close, progress saved) |
| S26 | S25 card tap (sheet); S28 row; S36 card | Back to origin; revert field dialog |
| S27 | S25 last decision | S28 (Review results); S24 (Re-sort Maybe / Start a new round); S39 (Export); S36 (Review conflicts, shared) ; S09 (Done) |
| S28 | S09; S27 | S29 sheet; S26 row; change decision (row menu); S39 export |
| S29 | S28 | S28 (Apply / Reset) |
| S30 | S09 Rounds | S28 filtered to that round |
| S31 | S09 Share/Invite; S34 Invite | System share sheet (out of scope); S34 |
| S32 | Invite link opened (app installed: Android App Link / iOS Universal Link; not installed: mobile web; desktop web) | S33; S03 (web sign-in); app stores |
| S33 | S32 | S25 (Start sorting); S09 shared |
| S34 | S09 Members | S31; role sheet; remove dialog (keep/discard decisions); transfer ownership dialog; leave dialog; S35 |
| S35 | S09 shared settings; S34 | S09 |
| S36 | S09 Review conflicts; S27 shared; S38 conflict notification | S37 (Resolve all); S26; S09 |
| S37 | S36 "Resolve all"; S09 conflicts row (Decision Maker only) | S37 summary → S36 (remaining) or S09 |
| S38 | Tab Activity; push / in-app notification | S09, S36, S34 per event; S12 notification explainer; notification preferences (S06 sub-page) |
| S39 | S09 Export; S27 Export; S28 Export | Format → scope → options → destination (Google) → write confirmation → success/failure; system share sheet for files and plain text |
| S40 | Global | — |

## 4. Deep links

| Link | Behavior |
| --- | --- |
| `https://swipesort.app/join/<token>` | Invite link. Android App Link / iOS Universal Link opens the app (S32 app-opening → S33). Not installed: opens the web app in the browser (S32 web, with "Get the app" banner) → sign in (S03 web) → S33 → S25 web. Expired or revoked token → S32 invalid-link state. |
| `https://swipesort.app/l/<listId>` | Opens S09 (members only; others get S40 not-found). |
| `https://swipesort.app/l/<listId>/conflicts` | Opens S36 (from "New conflicts" notification). |
| `https://swipesort.app/l/<listId>/members` | Opens S34 (from "Someone joined" / "Role changed"). |
| `https://swipesort.app/l/<listId>/sort` | Opens S25 (from "New round started"). |
| `swipesort://` | Custom scheme fallback for the same paths. |

## 5. Cross-file link targets

Agents link to these exact frame IDs (prototype mode shows `file.html#frame-id`). Every screen file must
contain a `Sxx-default` frame plus the IDs listed for it here.

| Frame ID | What it shows |
| --- | --- |
| `S01-default` | Splash |
| `S02-welcome`, `S02-demo`, `S02-demo-done` | Onboarding steps |
| `S03-default` | Sign in (Android), `S03-ios`, `S03-web-desktop` |
| `S05-share` | Sign-in prompt for sharing; `S05-backup`, `S05-moving`, `S05-moved` |
| `S06-default` | Settings root (signed in); `S06-guest` |
| `S08-first-run` | Empty home with Try a sample list; `S08-default` (lists); `S08-guest` |
| `S09-solo` = `S09-default`; `S09-solo-round-done` (Desk setup after round 1); `S09-shared` (Wedding guests); `S09-guest-wedding` (wedding list before sharing, guest) | List overview |
| `S11-default` | Source picker (Android); `S11-web` |
| `S12-contacts` | Contacts explainer; `S12-photos`, `S12-notifications`, `S12-contacts-denied` |
| `S13-select-default` | Contacts selection (88 selected) |
| `S14-default` | File import start; `S14-csv-preview` (candidates-q4.csv loaded) |
| `S19-contacts` | Field mapping for contacts; `S19-csv` (candidates) |
| `S20-default` | Duplicate review (4 groups) ; `S20-none` |
| `S22-import-pick` | Finish import: template + list name; `S22-import-pick-custom` (custom template selected) |
| `S23-default` | Template editor; `S23-save` |
| `S24-maybe` | Start round with Maybe pile preselected; `S24-default` |
| `S25-default` | Sorting (solo); `S25-shared`, `S25-web-desktop`, `S25-candidate`, `S25-coach-1` |
| `S27-default` | Round summary (solo, Wedding guests round 1 complete); `S27-desk-round-2` (Maybe pile re-sorted); `S27-shared` |
| `S28-default` | Results |
| `S31-default` | Invite; `S31-link-copied` |
| `S32-web-desktop` | Invite link opened in desktop browser; `S32-app` |
| `S33-default` | Join (app); `S33-web-desktop` |
| `S36-default` | One-by-one conflicts |
| `S37-confirm` | Bulk resolve confirmation; `S37-summary` |
| `S39-default` | Export: choose format; `S39-google-destination`, `S39-google-confirm`, `S39-success-google`, `S39-shared` |

## 6. Prototype flows

`data-action` values are stable selectors for flow tests. Each step is a link inside the named frame.

**Flow 1: first launch → first decision → round summary (guest)**
`S01-default` (auto) → `S02-welcome` [`data-action="next"`] → `S02-demo` [`next`] → `S02-demo-done`
[`get-started`] → `S08-first-run` [`import-list`] → `S11-default` [`source-contacts`] → `S12-contacts`
[`continue`] → `S13-select-default` [`continue`] → `S19-contacts` [`continue`] → `S20-default`
[`continue`] → `S22-import-pick` [`start-sorting`] → `S25-coach-1` [`next`…`done`] → live sort in
`04-prototype/swipe-demo.html?deck=wedding&count=6` → `S27-default`.

**Flow 2: re-sort Maybe → results → Google Sheets**
`S09-solo-round-done` [`resort-maybe`] → `S24-maybe` [`start-round`] → `swipe-demo.html?deck=desk-maybe`
→ `S27-desk-round-2` [`review-results`] → `S28-default` [`export`] → `S39-default` [`format-google`] →
`S39-google-destination` [`continue`] → `S39-google-confirm` [`confirm-write`] → `S39-success-google`.

**Flow 3: invite partner → web join → conflicts → bulk resolve → export**
`S09-guest-wedding` [`share`] → `S05-share` [`continue-google`] → `S05-moving` → `S05-moved`
[`continue`] → `S31-default` [`copy-link`] → `S31-link-copied` [`partner-opens-link`] →
`S32-web-desktop` [`sign-in-to-join`] → `S03-web-desktop` [`continue-google`] → `S33-web-desktop`
[`start-sorting`] → `S25-web-desktop` (keyboard sorting) [`finish`] → `S27-shared`
[`review-conflicts`] → `S36-default` [`resolve-all`] → `S37-confirm` [`confirm-resolve`] →
`S37-summary` [`export`] → `S39-shared` → `S39-success-google` (via the Google steps).

**Flow 4: list from CSV with a custom template**
`S08-default` [`new-list`] → `S11-default` [`source-csv`] → `S14-default` [`choose-file`] →
`S14-csv-preview` [`continue`] → `S19-csv` [`continue`] → `S20-none` [`continue`] → `S22-import-pick`
[`customize-template`] → `S23-default` [`save-template`] → `S23-save` [`confirm-save`] →
`S22-import-pick-custom` [`start-sorting`] → `S25-candidate`.
