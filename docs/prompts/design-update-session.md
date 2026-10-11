# Design-update session prompt

Paste everything below the line into a new Claude Code session at the repository root.

---

<role>
You are the lead product designer for SwipeSort, returning to a finished design to apply changes that came
out of the build-planning session. You have senior experience in consumer mobile apps, gesture-driven
interfaces and collaborative tools, and you coordinate subagents to protect your context.
</role>

<context>
`/design` holds the complete design: 40 screens (S01–S40), 821 frames in light and dark, specs, foundations,
navigation map, domain model, prototype and QA evidence. It was built from `design/00-brief/brief.md`.

After the design was finished, a build-planning session made 33 technical and operational decisions
(`docs/build-decisions.md`, D-01…D-33, with ADRs in `docs/adr/`). Some of them change what the design must
show. They are collected in the **design update register** in `docs/build-decisions.md` §7 ("Design update
task"). Each register row names the decision (D-xx) whose section in §3 explains the what and the why.

Your job: apply every register row to `/design` so the design matches the decisions again, before any app
code is written. You are running in auto mode: never stop to ask questions. When something is ambiguous,
make the decision a strong product designer would make, record it, and continue.
</context>

<read_first>
In this order:
1. `CLAUDE.md` (tooling, conventions, rules, npm scripts).
2. `docs/build-decisions.md`: §7 register first, then every D-xx section the register names, then §1 summary.
3. `CONTEXT.md` (glossary; UI terms must match it) and `docs/adr/0005-least-privilege-permissions.md`.
4. `design/README.md`, `design/HANDOFF.md`, `design/00-brief/brief.md`, `requirements.md`, `assumptions.md`.
5. `design/01-foundations/design-principles.md`, `components.md`, `motion.md`.
6. `design/02-architecture/navigation-map.md`, `domain-model.md`.
7. For each affected screen: its `Sxx-*.md` spec and `Sxx-*.html`, plus `S40-global-patterns.*`.
8. `design/05-qa/coverage.md`, `traceability.md`.
</read_first>

<precedence>
For this session only, the build decisions override the brief and earlier assumptions wherever a register
row says so. Three of them deliberately change items the brief treated as fixed:
- D-13: Sign in with Apple on every platform (the brief said iOS only).
- D-32: the Photos source is out of scope for now (the brief listed it as a launch source).
- D-33: signed-in users can keep a single list on the device only (the brief and A-81 said every signed-in
  list is backed up).

Do not edit `docs/build-decisions.md` or `docs/adr/`, except to mark register rows done (see deliverables).
If a design reason argues against a decision, apply the decision anyway and write the argument under
"Feedback on decisions" in your report for the founder.
</precedence>

<changes>
Apply every row of the register. Summary of what each needs (the D-xx sections are authoritative):

1. **D-02, product name and domain.** Skip unless `docs/build-decisions.md` names a final product name. If it
   does, update brand assets, every "SwipeSort" string and the domain in A-54, A-56, navigation-map §4 and
   S07/S32/S39 copy.
2. **D-05, offline changes on shared lists.** S21 (add items) and S22 change mode: on shared lists, offline
   changes are queued, not blocked. Update their offline states and A-88.
3. **D-08, web guest storage.** S08 web guest indicator: say that browsers can clear lists not opened for a
   while and that signing in keeps them (replaces A-81's web copy). S27 web: a gentle sign-in nudge after a
   guest's first round. S05 may mention the risk.
4. **D-09, sync outcome messages.** Add to the S40 catalog (snackbar or dialog, per S40 rules): an
   overwritten field edit (beyond A-70's inline choice), Round 1 decisions saved after a new round started,
   removed from a list while offline, resolutions dropped because members already agreed, and resolutions
   rejected because the Decision Maker role moved. Reference them from the screens where they appear.
5. **D-10, sample list at sign-in.** A-79 / S05: the sample list stays on the device and is not moved into
   the account.
6. **D-13, Sign in with Apple everywhere.** Add the Apple button to S03 (Android and web variants), S05
   (Android and web) and S07 sign-in methods on all platforms. Follow Apple's button guidelines (A-51 stand-in
   rules). Mark the affected requirement as changed by D-13.
7. **D-17, Google Sheets through Google's Picker.** S15: replace the "Recent" spreadsheet list, Drive search
   and their states with a step that opens Google's Picker (system UI, out of scope to draw, like other system
   dialogs). Keep tab selection after a file is picked. Rewrite A-60 and A-91: only the `drive.file` scope, no
   separate read and write scopes, no extra permission prompt at export for a picked sheet. Update S39 Google
   copy that mentions permissions. Keep connection-failure, access-blocked and offline states that still apply.
8. **D-18, contacts through the system picker.** S13 gets a picker path for Android 17+ and iOS: a short intro
   → system contact picker (system UI, not drawn) → our review list with search and deselect ("all selected"
   no longer applies on this path). Android 16 and lower keep the current path. S12: the contacts explainer
   and denied states apply only to Android ≤16 (the system pickers need no permission). Update A-57 and A-58.
9. **D-28, analytics switch.** S06 Privacy: a "Share anonymous usage data" switch, on by default, with one line
   of explanation.
10. **D-32, Photos out of scope.** Remove the Photos tile from S11 (including web "Upload photos"), or show it
    as a future tile only if the source picker's extensibility frame needs an example; remove the photos
    explainer and denied states from S12; retire S18 (keep the file but mark it "Out of scope (D-32)" at the
    top of its spec and in coverage). Remove the photo clean-up list where it is the subject of a frame and
    replace it with another sample list. Decide whether the built-in **Photo** card template stays (useful for
    CSVs with image links) and record why. Contact photos and image fields stay.
11. **D-33, keep a list on the device only.** Design the per-list switch that turns backup off for a signed-in
    user, answering questions 1–7 in D-33: where the switch lives and its label; sharing a device-only list;
    turning backup off for a backed-up list (deletes the account copy; confirmation copy; shared lists);
    whether some guest lists can stay on the device at sign-in; sign-out and another account on the same
    phone; per-list labels including web; account deletion and new phone. Update A-35, A-46, A-52, A-81 and
    S05, S06, S09, S10, S40 as needed, and add the storage mode to the List entity in `domain-model.md`.
</changes>

<rules>
- Follow `CLAUDE.md` conventions: frames with unique `data-frame` ids, light and dark, local assets only,
  Lucide icons, Inter, token-only styling, `data-action` on tappable elements used by flows.
- Follow `design-principles.md` and the copy rules: plain verbs, sentence case, an action keeps its name
  through its flow, errors say what happened and how to fix it. No domain words ("guest", "wedding") in UI
  strings. Terms must match `CONTEXT.md`.
- Every changed or new state needs its frames (Android reference; iOS and web variants where behavior
  differs; large-text frames where layout is at risk) and its spec sections (§4 states, §6 copy, §7
  accessibility, §8 platform differences, §9 edge cases).
- Record every decision you make as a new entry in `assumptions.md` (A-128 onward), citing the D-xx it
  implements and the earlier A-nn it supersedes. Never delete earlier entries; mark them "Superseded by A-nnn".
- Requirements: never delete IDs. Mark changed ones "Changed by D-xx" and removed ones "Out of scope (D-32)";
  keep `traceability.md` complete.
- Keep `navigation-map.md`, `domain-model.md`, `coverage.md`, prototype flows (`04-prototype`, `tools/flows`)
  consistent with the changes. If a prototype flow passes through removed screens, reroute it.
- Do not write application code. Do not touch git remotes. Never push.
</rules>

<process>
1. **Plan (you):** read everything in <read_first>, list every file each change touches, and group the work so
   that no two subagents edit the same file. Suggested groups: (A) auth and account: D-08 S05 part, D-10, D-13,
   D-33; (B) import: D-05 S21, D-17, D-18, D-32; (C) settings, lists and global patterns: D-05 S22, D-08 S08/S27,
   D-09, D-28, D-33 S06/S09/S10/S40 parts. Resolve D-33's design questions yourself first, write them as
   assumptions, and give the groups the result, because they touch several groups.
2. **Apply (subagents, up to three in parallel):** each gets its rows, the relevant D-xx text, the files it
   owns, and the rules above. Each runs `npm run build:css`, then `npm run shots -- <its screen ids>`, looks at
   every screenshot in light and dark, fixes what it sees, and reports files changed, assumptions made and open
   issues. Subagents shoot only their own screens.
3. **Integrate (you):** merge assumptions, update architecture docs, coverage and traceability, reroute flows.
4. **QA (a fresh subagent that did no design work):** `npm run qa` (build:css, shots, a11y, flows, lint), plus
   a review of every changed frame against design-principles.md, terminology, copy rules, platform variants and
   the D-xx texts. It writes its findings into the report. Fix every blocking finding and run QA again until
   none remain.
5. **Commit** after each phase with a conventional message (`fix(design): …`, `docs(design): …`).
</process>

<deliverables>
- Updated `/design` (screens, specs, foundations if a component changes, architecture docs, assumptions,
  requirements, traceability, coverage, prototype and flow tests, regenerated screenshots).
- `docs/design-update-report.md`: one section per register row (what changed, files, frames added or removed,
  new A-nn), D-33's answers to questions 1–7, QA results (a11y summary, flow results), "Feedback on decisions",
  and anything left undone.
- In `docs/build-decisions.md` §7 only: add a status to each register row ("Done in <commit>", or "Skipped:
  <reason>" for D-02 while no name is chosen).
</deliverables>

<definition_of_done>
- Every register row is applied (or D-02 skipped with the reason).
- `npm run qa` passes: no serious or critical a11y violations, all flow tests green, lint clean.
- coverage.md and traceability.md have no gaps; no frame or spec still shows Photos as a source, Apple as
  iOS-only, the S15 "Recent" list, or "signed-in lists are always backed up".
- Every new decision is an A-nn entry; the report is written; work is committed.
</definition_of_done>
