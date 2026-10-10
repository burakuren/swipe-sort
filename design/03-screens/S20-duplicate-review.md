# S20 Duplicate review

Frames: `S20-duplicate-review.html`. Generator: `tools/generators/S20-duplicate-review.py`.

## 1. Purpose and requirements

Step 4 of the import. When items look alike (common when combining sources, and in phone contacts saved
twice), the user sees each pair side by side with the matching fields marked, and chooses Merge, Keep both or
Skip. Nothing is lost by default: anything not reviewed is kept as separate items (GOAL-03). The same screen
compares new rows with items already in a list when adding items (S21).

Covers: SRC-14, SRC-15, SRC-18, SRC-19 (via S21), SMP-03 (duplicates), GOAL-03, GOAL-05, VIS-09 (matches not by
color alone), VIS-12, VIS-13, VIS-14, PLT-01–PLT-03, PLT-13–PLT-16, PLT-21, PLT-23, STK-07, TERM-01, DEL-22
(flow 1), DEL-25 (flow 4, `S20-none`), SCR-20.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S19 Field mapping | "Continue" when duplicates were found (`S19-contacts` → `S20-default`) |
| S19-csv | prototype flow 4 shows `S20-none`; in the app the step is skipped when nothing is found (A-23) and S22 shows "No duplicates found" |
| S21 Add items | "Continue" on `S21-mapping` → `S20-existing` |
| Back from S22 pick / S21 confirm | system back or iOS back |

| To | How |
| --- | --- |
| S22 pick mode | "Continue" (`data-action="continue"`) from `S20-reviewed-all` (flow 1), `S20-default`, `S20-none`, `S20-summary` |
| `S20-reviewed-all` | "Review the other 2" (`data-action="review"`) on `S20-default` (flow 1) |
| S21 confirm | "Continue" from `S20-existing` |
| Merge detail | "Review merge" link under a merged group (sheet) |
| Previous step | system back / iOS back chevron (to Map fields) |
| Close | `x` → "Discard import?" (`S40-global-patterns.html#S40-discard-import`) |

## 3. Layout and components

1. **AppBar (modal)** "Import" ("Add items" in S21 context) + **ImportStepper** "Review duplicates", "Step 4 of 5".
2. **Header**: `text-title-2` count ("4 possible duplicates"), one-line explanation, reviewed counter (the bulk action hides once every group is reviewed)
   ("2 of 4 reviewed", `tabular-nums`) with the bulk action (outline Button "Merge all identical (1)"; in S21
   "Skip all identical (1)"), Progress bar.
3. **DuplicateGroup** (Proposed component) per pair, on a ListGroup surface (`rounded-group bg-card`, flat):
   - reason row: icon (`phone`, `mail`, `user`, `copy-check`) + reason ("Same phone number, similar name") +
     position ("1 of 4"); optional column labels ("In the list" / "In mert-family.csv");
   - two columns, each with avatar (photo or initials) and the name; in S21 the existing item shows its final
     decision (`check` "Accepted", decision language);
   - comparison rows (field label + value 1 + value 2). **Matching fields**: muted band + icon (`equal` "Same",
     `equal-approximately` "Similar") + the word; never color alone;
   - **choice**: 3 radio buttons in a row (`role="radiogroup"`): Merge (`merge`), Keep both (`copy`), Skip
     (`skip-forward`). Selected: 2 dp primary border, `primary-soft` fill, icon replaced by `check`;
   - outcome line under the choice (`role="status"`), e.g. "Both are imported as separate items.".
4. **Bottom**: note about unreviewed groups + full-width primary "Continue" (`h-14`).
5. **Merge detail**: tall BottomSheet "Merge 2 items": photo source, multi-value fields as checkboxes
   (combined by default), single-value conflicts as radios, a muted note listing fields that are the same;
   primary "Merge", ghost "Cancel".
6. **Many duplicates**: compact rows (avatar, names, reason, action select) + filter chips (All, Identical,
   Similar) + bulk buttons (secondary "Merge all identical (26)", outline "Keep both for the rest").

## 4. States

| Frame | Trigger |
| --- | --- |
| `S20-default` | 4 groups from sample `duplicates`: c001/c097 (Merge chosen), c093/c098 (Keep both chosen); 2 of 4 reviewed |
| `S20-scrolled` | Same screen scrolled: c005/c099 (same name) and c058/c100 (identical), not reviewed |
| `S20-reviewed-all` | Flow 1: "Review the other 2" on `S20-default`; c005/c099 and c058/c100 merged. All 4 reviewed: 3 merged (c001/c097, c005/c099, c058/c100), 1 kept both (c093/c098: different phone numbers, could be two people) → 85 of 88 contacts imported, matching S22-import-pick |
| `S20-merge` | "Review merge" on c005/c099: both phone numbers kept, choose an email |
| `S20-summary` | All 4 reviewed: list of outcomes with "Change"; 85 of 88 will be imported |
| `S20-none` | No duplicates (candidates-q4.csv, 12 items) |
| `S20-loading` | Detection running ("Looking for duplicates in 88 items…") |
| `S20-existing` | S21 context: mert-family.csv rows vs. items already in Wedding guests (c003 identical → Skip; c009 adds Address → Merge) |
| `S20-large` | 41 possible duplicates in a 1,204-contact import: filters, bulk actions, compact rows |
| `S20-large-text` | 200% font scale: values stacked, options full width |
| `S20-ios`, `S20-ios-merge` | iOS bar; merge detail as a page sheet with Cancel / Merge |

## 5. Interactions, gestures and transitions

- **Detection** (after mapping): pairs with the same normalized phone, the same email (case-insensitive), the
  same title (Turkish-aware folding: "Ayşe" ≈ "Ayse"), or identical values in every shown field. Similar names
  use accent folding plus edit distance ≤ 2. Groups of 3+ show all items in a horizontal scroll (rare).
- **Choose an option**: tap Merge, Keep both or Skip. The choice applies immediately and the counter updates
  (250 ms progress animation). Changing is always possible; there is no undo snackbar because nothing is
  written until Finish.
  - **Merge**: one item; matching values once; multi-value fields (phones, emails in contacts) combined; for
    other differing fields the first item's value is kept unless changed in the merge detail; photo from
    whichever item has one.
  - **Keep both**: both become items.
  - **Skip**: the second item is left out. In S21 context: the new row is not added; the existing item is
    unchanged.
- **Merge all identical** (bulk): sets Merge on every group whose shown fields are all the same; snackbar
  "Merged 1 identical pair" with Undo (restores previous choices). In S21: "Skip all identical".
- **Not reviewed**: Continue is always enabled; unreviewed groups are imported as separate items (S21: added as
  new items). The bottom note says how many.
- **Merge detail**: sheet; Merge saves the field choices and closes; Cancel or back closes without changes.
- **Summary**: "Change" scrolls back to that group with its options focused.
- **S21 merge semantics**: Merge fills empty fields and adds new field values (e.g. Address) to the existing
  item; it never overwrites a value the user edited (SAFE-02) and keeps decisions, notes and round membership.
- Motion: groups do not move when reviewed (no auto-scroll); sheets per motion.md §3. Reduced motion: fades.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import" / "Add items"; close "Close import" / "Close adding items" |
| Stepper | "Review duplicates"; "Step 4 of 5" |
| Header | "4 possible duplicates"; "These items look alike. Merge them, keep both, or skip one. Anything you don't review is kept."; "2 of 4 reviewed" |
| Bulk | "Merge all identical (1)"; snackbar "Merged 1 identical pair" + "Undo"; S21 "Skip all identical (1)" |
| Reasons | "Same phone number, similar name"; "Same email, similar name"; "Same name"; "Identical name, phone and email"; S21 "Same name and phone number" |
| Markers | "Same"; "Similar"; badge "Identical" |
| Options | "Merge"; "Keep both"; "Skip"; group a11y "What to do with Ayşe Demir and Ayse Demir" |
| Outcomes | "One item with values from both." + ghost button "Review merge" (48 high, `git-merge` icon); "Both are imported as separate items."; "Ayse Demir is left out."; "One item. Nothing differs, so there's nothing to choose." |
| Outcomes (S21) | "Zeynep Kaya stays as it is. The row isn't added."; "Oğuz Kılıç gets the Address from the file. Decisions and notes stay."; "Added as a new item." |
| Bottom note | "2 not reviewed yet. They'll be imported as separate items." + ghost button "Review the other 2"; "All 4 reviewed: 3 merged, 1 kept both. 85 of 88 contacts will be imported."; S21 "1 not reviewed yet. It will be added as a new item." |
| Merge sheet | "Merge 2 items"; "Choose which values to keep."; "Photo from the first item"; "Phone" / "Both numbers are kept. The first one shows on cards."; "Email" / "Choose one."; "Name, Side, Relationship and City are the same in both."; "Merge"; "Cancel" |
| Summary | "All 4 reviewed"; "85 of 88 contacts will be imported: 3 pairs merged into one item each, 1 pair kept as two items."; "Merged"; "Kept both"; "Skipped"; "Change" (a11y "Change what happens to {name}") |
| None | "No duplicates found"; "All 12 items are different, so there's nothing to merge." |
| Loading | "Looking for duplicates in 88 items…" |
| S21 header | "3 already in Wedding guests"; "These rows in mert-family.csv match items in the list. Skip leaves the list as it is; Merge fills in new values and keeps decisions and notes."; column labels "In the list", "In mert-family.csv"; "Empty" |
| Many | "41 possible duplicates"; "Your contacts have many repeated items. Merge the identical ones in one step, then check the rest."; chips "All 41", "Identical 26", "Similar 15"; "Merge all identical (26)"; "Keep both for the rest"; row state "Not reviewed" / "Merge" / "Keep both" / "Skip"; "40 not reviewed yet. They'll be imported as separate items." |
| Continue | "Continue" |

## 7. Accessibility

- Each group is a `section` labeled by its reason; the comparison reads row by row: "Phone, same:
  +90 500 000 97 62, +90 500 000 97 62".
- Options are a radiogroup named after the pair; the outcome line is a polite live region.
- Matches use icon + word + band; decisions on existing items use icon + label.
- Focus order: header, bulk action, each group (reason, values, options, outcome), Continue.
- Large text (`S20-large-text`): items no longer sit side by side; each field shows one value with "Same", or
  both values numbered "1." and "2."; options become full-width stacked buttons.
- Touch targets: options 56 high; compact rows 64; bulk buttons 48.

## 8. iOS and web differences

- **iOS** (`S20-ios`): 44 pt bar with "Back" (to Map fields) and close at the right; edge swipe back. The merge
  detail is a **page sheet** with Cancel / Merge in its bar (`S20-ios-merge`) instead of bottom buttons. Bulk
  undo uses the same snackbar-style toast.
- **Web**: same as Android. Desktop: centered column; options are reachable with Tab and arrow keys within
  the radiogroup. No separate frame (no behavior difference).

## 9. Edge cases

- **Groups of three or more** (same contact saved three times): columns scroll horizontally; Merge combines
  all; Skip keeps only the first.
- **Very long values** (emails, long names): wrap at "@" and spaces inside each column; at large text they
  stack.
- **Missing values**: shown as "Empty" in muted text; never counted as a match.
- **Hundreds of duplicates** (`S20-large`): compact list, filters, bulk; the full comparison opens on tap.
- **Edited items in S21**: merge never replaces a value the user edited in SwipeSort; it shows "Edited in
  SwipeSort, kept" in the merge detail.
- **Existing item already decided** (S21): decisions, notes and status stay; Keep both creates a new undecided
  item in the current round.
- **Offline**: detection is local; works offline.
- **Changing the mapping after review** (back to S19): choices are kept for pairs that are still detected;
  new pairs appear unreviewed.
