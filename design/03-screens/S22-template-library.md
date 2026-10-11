# S22 Template library

Frames: `S22-template-library.html` (generator `tools/generators/S22-S23-templates.py`). Editor: `S23-template-editor.md`.
Components: `01-foundations/components.md` (TemplateTile, SwipeCard, ListGroup, BottomSheet, AlertDialog, Dialog,
Snackbar, ImportStepper, Input, Select, Switch, BackupSwitchRow). Data: `templates`, `contacts` c001, `candidates` k01,
`products` p01/p03, `trips` tr01, `books`, `me.signedIn.email` in `02-data/sample-data.json`.

## 1. Purpose and requirements

One screen with three modes, all built on the same pieces (live card preview + template choice):

- **Manage** (Settings › Card templates): see the six built-in templates and your own, with the lists that use
  them; open, rename, duplicate, delete; create a new template.
- **Pick** (the import finish step, A-22): name the new list, choose its card template with a live preview of
  the first imported item, start sorting. The recommended template is preselected. Signed in, the step also
  holds the "Back up this list" switch (on by default), so a private list never has to reach the server
  (D-33, A-132, A-168).
- **Change** (a list's Card template, from S09 or the S25 menu): switch the template of an existing list at any
  time; it applies immediately with Undo.

Covers: TPL-01, TPL-04 (no font or color options anywhere), TPL-05 (preview uses the list's own items),
TPL-08 (pick mode shows the just-saved template), TPL-09, TPL-10, TPL-11, TPL-12 (any template on any list;
"Used by" per template), TPL-13, SRC-16, SRC-17, SRC-24 (partial copy at import), SRC-03/GOAL-05 (one finish
step for every source), ACC-10 (backup per list at creation, D-33), DM-02 (template change on shared lists applies to every member), GOAL-02, GOAL-03,
VIS-01–VIS-06, VIS-11–VIS-14, TERM-01–TERM-03, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23, SUC-04, SUC-06,
SCR-22.

## 2. Entry points and exits

| From | How | Mode |
| --- | --- | --- |
| S06 Settings | "Card templates" row (`S22-default`) | manage |
| S19 / S20 / S17 | "Continue" on the last step before Finish (`S22-import-pick`) | pick |
| S09 list overview | "Card template" row | change |
| S25 sorting menu | "Card template" (returns to S25 on back) | change |
| S23 editor | "Save" in the save dialog (`S22-import-pick-custom`), back | pick / manage |

| To | How |
| --- | --- |
| S25 sorting | Pick: "Start sorting" (`data-action="start-sorting"`). Contacts → `S25-coach-1` (first sort shows coach marks); CSV with the custom template → `S25-candidate`; Trip ideas → `S25-photo` |
| S23 editor | Pick/change: "Customize" (`data-action="customize-template"`) opens a copy of the selected built-in, or "Edit template" for a custom one. Manage: tap a template; "New template" sheet → Continue; actions sheet → Edit |
| S06 / S09 / S25 | Back (manage, change) |
| S20 / S19 / S17 | Back from pick mode (previous import step, every choice kept) |
| S08 | Close (`x`) in pick mode: S40 "Discard import?" dialog first |

## 3. Layout and components

### Manage mode (`S22-default`)
1. **AppBar** small: back (`arrow-left`, "Back to Settings"), title "Card templates". Bottom navigation is hidden
   (pushed in the Settings stack).
2. Intro (`text-body-sm muted`), one sentence.
3. **Built-in**: section header (`text-label muted`), 2-column grid of **TemplateTile** (library variant):
   `rounded-tile border bg-card p-3`, layout schematic (`h-12`, `bg-muted rounded-sm`, bars at `muted-foreground/25–40`),
   name (`text-label-lg`), one-line description (`text-caption muted`, wraps to 2 lines). Order: Person, Product,
   Photo, Task, Candidate, Generic. Schematic per image area: avatar = circle + title bar; cover = block on top;
   full = block filling the box; none = bars only.
4. **Your templates**: ListGroup rows (min 72): 56-wide schematic, name (`text-body`), "Used by {list}" / "Used by
   2 lists" / "Not used by any list" (`text-body-sm muted`), overflow IconButton ("More options for {name}").
   Order: newest first. Row tap → S23 (`S23-edit-saved`). Built-in tiles tap → S23 read-only (`S23-built-in`).
5. Button `outline` full width "New template" (`plus`).
6. Overlays: actions BottomSheet, rename Dialog, delete AlertDialog, New template BottomSheet, Snackbar.

### Pick mode (`S22-import-pick`)
1. **AppBar (modal)**: close `x` ("Close import"), title "Import" ("New list" for manual entry, as in S17).
2. **ImportStepper** (same markup as C2, `px-gutter pb-3 pt-1`): "Finish", "Step 5 of 5" (contacts, CSV, Excel,
   Google Sheets), "Step 4 of 4" (plain text, manual entry). A skipped duplicate step (A-23) still counts as
   done, so the total never changes mid-flow.
3. **List name** Input (label above, 48 high), prefilled from the source and fully selected on arrival so typing
   replaces it (`S22-import-pick-prefilled`). Prefill: contacts "Contacts"; CSV/Excel file name without
   extension ("candidates-q4"); Google Sheets spreadsheet name; plain text the file name or "Pasted list";
   manual entry "New list". 1–80 characters.
4. **Import summary** line (`text-body-sm muted`, 16 icon): item count and source, plus the duplicate outcome:
   "3 duplicate pairs merged." after S20, "No duplicates found." when the step was skipped.
4a. **Backup** (signed in only, D-33, A-132, A-168): a BackupSwitchRow 12 below the summary, the same row as
   S09's Backup group but standing alone (`rounded-group bg-card`, min 64): `cloud-check` / `cloud-off` 20
   muted, "Back up this list" (`text-body`), one line under it (`text-body-sm muted`, `aria-live="polite"`)
   and the Switch (`data-action="toggle-backup"`), **on by default**. Not shown without an account (flow 1
   frames have none), and never for the sample list (it is not imported). When the row is present the preview
   stage shrinks to 224 high at 36% (as on iOS) so the template row stays in view above the bottom action.
5. **Card template** header (`text-title-3`) with a text button "Customize" (`pencil`, primary, 48 high).
6. **Live preview**: the real **SwipeCard** (identical markup to S25: `rounded-hero bg-card shadow-hero`, same
   content rules) on a 372 × 620 card box (the Android sort card, `aspect-[3/5]`), drawn at 46%
   (`origin-top scale-[.46]`, iOS 36% because the screen is shorter) and centered in a 288-high stage (iOS 224), so
   the whole template row stays visible above the bottom action. The item is the first imported item (c001 Ayşe
   Demir for contacts, k01 Lena Hoffmann for the CSV, p01, tr01 Kaş, Antalya for Trip ideas, the first book). It updates instantly when a
   tile is chosen (150 ms cross-fade).
7. **Template carousel** (horizontal scroll, `role="radiogroup"`, gap 12, `px-gutter`): TemplateTile pick variant
   (128 wide): schematic, name (`text-label`, wraps), caption "Recommended" / "Current" / "Custom" / "Built-in", bottom-aligned so captions line up when names wrap;
   selected = `border-2 border-primary` + `circle-check`. Order: the recommended template, then your templates
   (newest first), then the remaining built-ins. The order does not change while the screen is open.
8. **Bottom action**: Button lg (h-14) full width "Start sorting" on `bg-background` with a top hairline.

### Change mode (`S22-change`)
AppBar small: back ("Back to {list}"), title "Card template", list name as caption. On shared lists an info
Alert (`users`): "Shared list" / "A new template changes the cards for all 3 members." Then the live preview
(first item of the list, or the current item when opened from S25), a header row "Templates" + "Customize"
(built-in current) or "Edit template" (custom current), the carousel with "Current" on the list's template,
and a footer line explaining that decisions, notes and fields are untouched. No bottom button: choosing a tile
applies it. Offline on a shared list the change is **queued, not blocked** (D-05): the offline banner sits under
the app bar and the shared notice says the template applies on this phone now and members see it once it's
synced (`S22-change-offline`).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S22-default` | Manage mode, signed in or guest: 6 built-ins, 2 custom templates (Candidate, compact used by Frontend hiring, Q4; Guest with table side used by Wedding guests) |
| `S22-actions` | Overflow on a custom template: Edit, Rename, Duplicate, Delete template |
| `S22-actions-built-in` | Long-press on a built-in tile: View layout, Duplicate, and why it can't be edited |
| `S22-rename`, `S22-renamed` | Rename dialog (prefilled, focused, all selected) → snackbar "Template renamed" |
| `S22-rename-error` | Name already used by another of your templates (case-insensitive) |
| `S22-duplicated` | Duplicate → "Candidate, compact (copy)" appears first (newest first), snackbar with "Edit"; content shown scrolled so the snackbar covers nothing |
| `S22-delete` | Delete a template in use: the dialog asks for the replacement template of each list using it (default: the built-in it was based on) |
| `S22-deleted` | Snackbar "Template deleted" + Undo (restores the template and every list's choice) |
| `S22-new` | "New template" sheet: which list's fields to use (default: the most recently opened list) and which built-in to start from → S23 |
| `S22-empty` | No templates of your own yet (empty state with "New template") |
| `S22-loading` | First open after sign-in while synced templates load (skeleton tiles); local templates show immediately |
| `S22-import-pick` | Pick mode, contacts (flow 1): 88 contacts selected, 3 duplicate pairs merged and 1 pair kept, so 85 items; "Wedding guests" typed, Person recommended, Ayşe Demir preview; Start sorting → `S25-coach-1` (0 / 85) |
| `S22-import-pick-prefilled` | Arrival: name "Contacts" prefilled, focused and selected, helper explains it |
| `S22-import-pick-csv` | CSV (flow 4 in the app), signed in: "Frontend hiring, Q4", Candidate recommended, "No duplicates found." Role is hidden (S19), so the built-in's subtitle is left out. "Back up this list" on (the default on arrival) |
| `S22-import-pick-device-only` | Same, after the person turned "Back up this list" off: `cloud-off`, "It stays on this phone only. You can back it up later." (A-139: in the signed-in sample world this list is on this phone only) |
| `S22-import-pick-custom` | Back from S23 after "Save": the screen returns scrolled so the carousel sits above the snackbar; "Candidate, compact" selected (2nd tile), preview Lena Hoffmann compact, snackbar "Template saved"; the backup switch keeps the person's choice (off) |
| `S22-import-pick-text` | Plain text, Step 4 of 4: one field, Generic recommended; the card is the title only |
| `S22-import-pick-manual` | Manual entry (title "New list"), Step 4 of 4: Product recommended; p01 has no rating, so the rating is left out |
| `S22-import-pick-trips` | CSV with an image link per row (trip-ideas.csv, signed in, backup on): Image field + 4 other fields, Photo recommended; preview tr01 Kaş, Antalya (replaces `S22-import-pick-photos`, D-32) |
| `S22-import-pick-error` | Name cleared and "Start sorting" pressed: inline error, focus moves to the field |
| `S22-import-pick-importing` | "Start sorting" pressed: button busy "Importing 85 items…" (copy into the working copy), then S25 |
| `S22-import-pick-partial` | After "Start sorting": 2 of the 30 image links didn't open an image. Every item is in the list; the summary says "28 of 30 images downloaded.", a neutral Alert (`image-off`, `role=status`) names the rows, "Start sorting" continues (those 2 cards show the `image-off` placeholder) |
| `S22-change` | Change mode, solo list (Desk setup): Product marked Current |
| `S22-change-shared` | Change mode on a shared list: notice that it applies to every member |
| `S22-change-applied` | Tapped "Guest with table side": applied at once, snackbar "Card template changed to Guest with table side" + Undo; header action becomes "Edit template" |
| `S22-change-offline` | Same on a shared list while offline (D-05): queued, not blocked. Applied on this phone at once; the shared notice says members see it once it's synced; snackbar "Card template changed. Saved on this phone until it syncs." + Undo |
| `S22-ios`, `S22-ios-actions`, `S22-import-pick-ios` | iOS variants |
| `S22-web-desktop` | Desktop browser: template actions as a menu |
| `S22-import-pick-web-device-only` | Web (mobile), signed in, backup off: "It stays in this browser only. Browsers can clear lists you haven't opened for a while." (D-08, A-137) |
| `S22-large-text` | 200% text in pick mode |
| `S22-import-pick-device-only-large-text` | 200% text, signed in: the switch sits on the row with "Back up this list"; the line wraps below at full width |

Not applicable: web-unavailable (templates use no device features). Error: template data is local; a failed
sync shows the global sync notice (S40), not a state of this screen.

### Recommendation rules (pick mode)
Evaluated on the list's fields after mapping, first match wins:
1. Source is contacts, or the fields include a phone or email plus a name → **Person**.
2. An image field plus a number field named like price/cost → **Product**.
3. An image field, the title and at most three other fields → **Photo** (A-131, read as "besides the title", so
   its own example qualifies: Trip ideas has Photo, Place (title), Country, Best time, Budget). Hidden fields
   don't count. Contact photos never trigger it (rule 1 comes first).
4. Text fields named like role/position plus experience or salary → **Candidate**.
5. A date field named like due/deadline plus owner/assignee → **Task**.
6. Otherwise → **Generic**.
If one of your templates was saved from a list with the same field names, it is recommended instead (TPL-12).

### How templates fit other lists (TPL-12)
Built-ins are role-based: each slot takes the matching field; when the list has no match, the slot takes the
next unused field in list order (like Generic). Custom templates store field names; on another list, slots
whose field doesn't exist are left out and the editor marks them "Not in this list". The preview always shows
the real result before anything is applied.

## 5. Interactions, gestures and transitions

- **Tile tap (pick)**: selects; preview cross-fades (150 ms, reduced motion: instant). Nothing is saved until
  "Start sorting".
- **Tile tap (change)**: applies immediately: preview cross-fades, the "Current" caption moves, snackbar with
  Undo (6 s; Undo restores the previous template). The list's cards change for every member on shared lists
  (any member may change it: domain-model permissions). An activity event is not created (cosmetic change).
- **Carousel**: horizontal scroll with snap to tiles; the selected tile is scrolled into view on open.
- **Customize**: pick/change with a built-in selected → S23 on an unsaved copy ("Copy of {name}"); with a custom
  template selected → S23 editing that template.
- **Start sorting**: validates the name; creates the list, copies items into the working copy ("Importing 85
  items…"), applies the template, closes the import modal and opens S25 (coach marks on the very first sort).
  Image links (CSV, Google Sheets) are downloaded in the same step; when some links don't open an image, every
  item is still created, the step stays open once with `S22-import-pick-partial`, and "Start sorting" continues.
- **Back up this list** (signed in): the switch only sets the new list's storage mode (`backedUp` or
  `deviceOnly`, domain-model › List); nothing is sent before "Start sorting". On: the list is created in the
  account (uploads queue when offline). Off: the list is created on this phone only and never reaches the
  server; it can be backed up later from S09 (A-132) or S06 › Backup. No confirmation either way (nothing exists
  yet to lose). The choice survives Back, Customize and the editor (`S22-import-pick-custom`), and is
  forgotten when the import is discarded.
- **Manage**: tile/row tap → S23; overflow (or long-press) → actions sheet (Android), action sheet (iOS),
  menu (web). Rename: Dialog with the name selected; Enter = Rename. Duplicate: copy named "{name} (copy)" (then
  "(copy 2)"…, as S40/S10), not used by any list. Delete: AlertDialog; when lists use the template, a Select per list chooses
  its replacement (default: the built-in it was based on, else Generic).
- **Back**: system back / edge swipe closes the topmost sheet or dialog first. In pick mode back returns to the
  previous import step with everything kept.
- Sheets 300 ms emphasized decelerate; dialogs 250 ms; snackbars per motion.md §3. Reduced motion: fades only.

## 6. Copy

| Element | Text |
| --- | --- |
| App bar (manage) | "Card templates"; back "Back to Settings" |
| Intro | "Templates decide which fields show on a list's cards. Any list can switch templates at any time." |
| Section headers | "Built-in", "Your templates" |
| Built-in descriptions | Person "Photo, name and contact details"; Product "Image, price and rating"; Photo "The image fills the card"; Task "Title, due date and owner"; Candidate "Role, experience and salary"; Generic "The first fields of any list" |
| Custom row meta | "Used by {list name}", "Used by 2 lists", "Not used by any list" |
| Row overflow | a11y "More options for {template}" |
| New template button | "New template" |
| Actions sheet (custom) | title "{template}", subtitle "Used by …"; "Edit", "Rename", "Duplicate", "Delete template" |
| Actions sheet (built-in) | "{template}", "Built-in template"; "View layout", "Duplicate"; "Built-in templates can't be changed or deleted. Duplicate one to make your own version." |
| Rename dialog | "Rename template"; label "Template name"; "Cancel", "Rename"; success "Template renamed" |
| Rename errors | "Enter a name for the template." / "You already have a template with this name. Choose another name." |
| Duplicate | copy named "{name} (copy)", then "(copy 2)"; snackbar "Duplicated as “{name} (copy)”", action "Edit" |
| Delete dialog (in use) | "Delete “{template}”?"; "{List} uses this template. Its cards switch to the template you choose, for every member of the list." (solo list: without ", for every member of the list"); 2+ lists: "2 lists use this template. Choose a template for each."; Select label "Card template for {list}"; helper "{Built-in} is the template it was based on."; "Cancel", "Delete template" |
| Delete dialog (unused) | "Delete “{template}”?"; "No list uses it."; "Cancel", "Delete template" |
| Deleted | "Template deleted", action "Undo" |
| New template sheet | "New template"; "Use fields from"; helper "The preview shows this list's items. You can use the template on any list."; "Start from"; built-in names; "Continue" |
| Empty | "No templates of your own yet" / "Duplicate a built-in template or start a new one to choose your own fields." / "New template" |
| Loading | a11y "Loading templates" |
| Pick: app bar, stepper | "Import" or "New list"; "Close import"; "Finish"; "Step 5 of 5" / "Step 4 of 4" |
| Pick: name | label "List name"; helper on arrival "Prefilled from the source. Type to rename it."; placeholder when empty "e.g. Desk setup"; error "Enter a name for the list."; over 80 characters "Use 80 characters or fewer." |
| Pick: summary | "85 items from Contacts. 3 duplicate pairs merged, 1 pair kept as separate items." / "{n} items from Contacts. No duplicates found." / "12 items from candidates-q4.csv. No duplicates found." / "12 items from pasted text." / "3 items you added." / "30 items from trip-ideas.csv. No duplicates found." / "8 items from Flat hunt 2026." |
| Pick: backup (signed in) | "Back up this list"; on "Backed up to deniz.yilmaz@example.com"; off "It stays on this phone only. You can back it up later."; web off "It stays in this browser only. Browsers can clear lists you haven't opened for a while." (web on: same as mobile) |
| Pick: template | "Card template"; "Customize"; tile captions "Recommended", "Current", "Custom", "Built-in" |
| Pick: action | "Start sorting"; busy "Importing 85 items…"; after save "Template saved" |
| Partial import | image links: summary "30 items from trip-ideas.csv. 28 of 30 images downloaded."; Alert "2 images couldn't be downloaded" / "The image links in rows 14 and 27 don't open an image. Those 2 cards show without one. You can change a link in item details."; "Start sorting" (one link: "1 image couldn't be downloaded" / "The image link in row 14 doesn't open an image. That card shows without one. …"); files: "2 rows couldn't be read" / "Rows 14 and 52 are empty in every column. The other 86 are ready." |
| Import failed | "The list couldn't be created. Your phone is out of storage. Free up space and try again." / "Try again" |
| Change mode | "Card template"; caption "{list}"; "Templates"; "Customize" / "Edit template"; caption "Current"; footer "Choosing a template changes the cards right away. Decisions, notes and fields stay as they are." |
| Shared notice | "Shared list" / "A new template changes the cards for all 3 members."; offline "The new template applies on this phone now. All 3 members see it once it's synced." |
| Applied | "Card template changed to {template}", "Undo"; offline (shared list) "Card template changed. Saved on this phone until it syncs." + "Undo" (solo lists offline use the online string: nothing waits for others) |
| Offline banner | "You're offline. Changes are saved on this phone." |
| Large text | "See card preview" |

## 7. Accessibility

- Preview: one element `role="img"` labelled "Card preview: {title}, {subtitle}. {Field} {value}. … Tag {tag}."
  (the same text the S25 card announces). Large-text users and screen-reader users get "See card preview",
  which opens the full-size preview (S23-preview-full) with previous/next.
- Carousel: `radiogroup` "Card template" (change mode: "Card template for {list}"); tiles are `radio` with
  name + caption as the label; arrow keys move between tiles on web. Selection is announced; in change mode the
  snackbar is announced politely and Undo is reachable (snackbar stays 10 s with a screen reader).
- Library tiles: label "{name}, built-in. {description}". Overflow buttons: "More options for {template}".
- Backup row (signed in): the Switch is `role="switch"` named "Back up this list"; its state line is
  `aria-live="polite"`, so turning it off announces "It stays on this phone only. You can back it up later."
  The icon (`cloud-check` / `cloud-off`) and the text carry the state, not the track color alone.
- Focus order (pick): close, list name, backup switch (signed in), Customize, preview, tiles, Start sorting. On error, focus moves to the
  name field and the error is announced (`aria-invalid` + described by the message).
- Dialogs follow S40 (A-112): vertically centered, max width 384, no icon; confirm is destructive when something is
  deleted or discarded, primary otherwise (Rename, Save). Initial focus: the input (rename) or the dismiss button
  (delete). Background is inert while a sheet or dialog is open.
- Touch targets ≥ 48 (tiles 128 × ~140, overflow 48, text buttons 48 high). Selected tile = 2 dp primary border
  + check icon (not color alone).
- Large text (`S22-large-text`, `S22-import-pick-device-only-large-text`): the backup row keeps the switch on the
  title line and lets the state line wrap below at full width; stepper and labels scale; the preview becomes a button; the carousel becomes a
  vertical radio list with captions; buttons grow to 64 high.

## 8. iOS and web differences

- **iOS** (`S22-ios`, `S22-ios-actions`, `S22-import-pick-ios`): navigation bar with back chevron + previous
  title ("Settings", "Back" in the import stack) and centered title; template actions use an action sheet
  (Cancel separate, destructive in red); rename/delete use native alerts with the same copy; the New template
  sheet is a page sheet with Cancel / Continue in its bar; edge-swipe back. In the import stack the close `x`
  moves to the right (as in C2).
- **Web mobile**: same as Android; browser back = app back. The backup switch is offered on the web too
  (`S22-import-pick-web-device-only`): off means "on this browser only", with the D-08 line that browsers can
  clear lists not opened for a while (A-137, A-168). Same rule as S09's web switch; hiding it on the web would
  make the same account behave differently per platform.
- **iOS**: the backup row is the same row with a UISwitch; no separate frame (layout identical).
- **Web desktop** (`S22-web-desktop`): phone column centered; overflow opens a DropdownMenu anchored to the
  button: right-aligned with it and opening upward, its bottom edge 4 px above the button, when there is no room below; Escape closes it; carousel tiles are reachable with Tab and
  the arrow keys; Enter on a tile selects (pick) or applies (change).

## 9. Edge cases

- **Long names**: template names up to 40 characters; tiles wrap to 2 lines then truncate with "…" (full
  name in the label); list names wrap in the input's helper-free layout.
- **Missing values** in the preview item: left out, exactly as on the sort card (rows hidden, initials or
  `image-off` for missing images). If the first item has no title value, the preview uses the first item that
  has one.
- **Very large lists**: the preview uses the first item; counts use grouping ("1,240 items from …").
- **Template used by many lists**: delete dialog lists each list with its own Select (scrolls inside the
  dialog after 3).
- **Deleting the template the current list uses** from change mode is not possible (no delete there).
- **Offline**: banner under the app bar with 12 dp before the content (as S11-offline). Manage and change work offline (local first, synced later); pick mode works offline for every
  source already read. Changing the template of a **shared** list offline is queued, not blocked (D-05,
  A-169): it applies on this phone at once, Undo works locally, and members see it after the change syncs. If
  another member changed the template meanwhile, the change that reaches the server last wins (D-09 per-field
  rule); there is no outcome message, because the cards show the result right away (D-S22-7).
- **Image links offline** (pick mode): items are created at once; images download when a connection returns
  (cards show the `image-off` placeholder until then). Only links that fail while online produce the partial
  state.
- **Backup switch offline** (pick mode): both positions work. On queues the upload until a connection returns
  (A-139); the S09 sync notice shows "Saved on this phone" meanwhile.
- **Backup switch hidden**: without an account, and never in change or manage mode. A list created on this
  phone only can be shared later; Share then asks to back it up first (A-133).
- **Guest user**: templates are stored on the device and move to the account with the lists (A-46). No backup
  switch in pick mode: every list is on this phone (A-35/A-137).
- **Shared lists**: anyone on the list can change the template (domain-model permissions); members see the new
  template the next time a card renders. A custom template applied to a shared list is copied to the list so
  members without that template see the same cards; editing it from their side creates their own copy.
- **Built-in templates** cannot be renamed, edited or deleted; Duplicate is always available.

### Decisions
- **D-S22-1** Pick mode shows one live preview of the first item; cycling items is in the editor and in the
  full-size preview, to keep the finish step short (SUC-04).
- **D-S22-2** Template order in pick and change mode: recommended or current first, then your templates, then the
  other built-ins; order is stable while the screen is open.
- **D-S22-3** The preview is the real SwipeCard at 46% in pick mode (50% in change mode and S23) on the Android card box (372 × 620); the app renders the
  same component with a scale transform.
- **D-S22-4** The ImportStepper keeps its total when the duplicate step is skipped (A-23): the skipped step
  counts as done and the summary line says "No duplicates found."
- **D-S22-5** Sample data marks "Guest with table side" as used by Wedding guests, while S25 shows that list with
  Person. The frames tell it as a sequence: `S22-change-shared` (Person current) → `S22-change-applied`
  (switched), and manage mode shows the state after the switch.
- **D-S22-6** `S22-import-pick` is the contacts finish step (flow 1). Flow 4 reaches it from `S20-none` because
  S20 links every Continue there; the faithful CSV state is `S22-import-pick-csv`. Both "Customize" links open
  `S23-default`.
- **D-S22-7** Template changes are cosmetic and do not create an activity event or a notification.
- **D-S22-8** The backup switch sits under the import summary (a property of the list being created, next to
  its name), not in the bottom action area: the action stays one button, and the row is read before "Start
  sorting". The preview shrinks to 36% when the row is shown so the template row stays visible.
- **D-S22-9** `S22-import-pick-photos` became `S22-import-pick-trips` (D-32): a CSV with an image link per row is
  now the Photo template's example. No flow or link used the old ID.
