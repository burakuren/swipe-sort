# Component specs

Visual reference: `components.html` (copy markup from there). Tokens: `tokens.json`. Motion: `motion.md`.
"RNR" = React Native Reusables (`@rn-primitives` + NativeWind). Components marked **Custom** do not exist in
RNR and are designed in the same style; build them in `components/ui/` next to the RNR ones with the same
API conventions (`className` passthrough, `variant`, `size`, `cva`).

General rules for every component:
- Minimum touch target 48×48 dp (`hitSlop` where the visual is smaller).
- Every interactive element has `accessibilityRole` and an `accessibilityLabel` when it has no text.
- States: default, pressed (`bg-accent` or `opacity-90` on fills), focused (web/keyboard: `ring-2 ring-ring
  ring-offset-2`), disabled (`opacity-50`, not focusable), loading (spinner + progress verb).
- Text uses the named type scale; colors use tokens only.

## Index

| Component | RNR | Where |
| --- | --- | --- |
| Button | `Button` | everywhere |
| IconButton | `Button size="icon"` | app bars, rows |
| ExtendedFab | Custom (M3) | S08 Android |
| DecisionButton, UndoButton, DecisionBar | Custom | S25, S36, S02 |
| SwipeCard, CardStack, DecisionStamp | Custom | S25, S02, S23 preview, S36 |
| DecisionBadge, StatusBadge, Badge | `Badge` | results, rows, cards |
| MemberDecisions | Custom | S26, S28, S36, cards (opt-in) |
| Progress, SegmentedProgress | `Progress` + Custom | S25, S08, S09, S34 |
| Input, Label, Textarea, SearchField | `Input`, `Label`, `Textarea` | forms, search |
| Switch, Checkbox, RadioGroup | `Switch`, `Checkbox`, `RadioGroup` | settings, import |
| SegmentedControl | `ToggleGroup` (single) | theme, final/my toggle, card order |
| FilterChip | `Toggle` | S29, S24 |
| DecisionSegments | `Tabs` styled as chips | S28 |
| Select | `Select` | S24 sort field, S19 type |
| ListGroup, Row variants | Custom on `View`/`Pressable` (+ `Separator`) | settings, members, fields |
| ItemRow, SelectableRow, ListRow, MemberRow | Custom | S28, S13, S08, S34 |
| AppBar (small, large, modal, iOS) | Custom (expo-router `Stack.Screen` header replaced) | every screen |
| BottomNav | expo-router `Tabs` with custom `tabBar` | tabs |
| ImportStepper | Custom (uses `Progress` semantics) | S12–S22 import |
| Tabs | `Tabs` | S38 |
| BottomSheet | Custom on `@gorhom/bottom-sheet` | notes, filters, menus |
| AlertDialog | `AlertDialog` | S40 confirmations |
| Dialog | `Dialog` | rename, save template |
| Snackbar | Custom (or `sonner-native`) | feedback |
| DropdownMenu | `DropdownMenu` | overflow menus (Android), iOS uses action sheet |
| Alert / Banner | `Alert` | notices, errors, web-unavailable |
| OfflineBanner, SyncNotice, BackupIndicator | Custom | S25, S08, S09 |
| EmptyState, ErrorState | Custom | many |
| Skeleton, Spinner | `Skeleton` + `ActivityIndicator` | loading |
| SourceTile | Custom | S11 |
| TemplateTile | Custom | S22 |
| Avatar, AvatarStack | `Avatar` | members, items |
| CoachMark | Custom | S25 first run |
| Kbd | Custom (web only) | S25 web |

---

## Button

**Anatomy**: container (radius `control` 12), optional leading icon (20), label (`text-label-lg`), optional
spinner. **Variants**: `default` (primary fill), `secondary`, `outline` (border-input, card fill), `ghost`,
`destructive`, `link`. **Sizes**: `lg` 56 (bottom actions), `default` 48, `sm` 40 (only with a 48 hit
area), `icon` 48 round. **Props**: `variant`, `size`, `loading`, `loadingText`, `leftIcon`, `disabled`,
`onPress`. **Rules**: one `default` per view; label is a verb phrase; width hugs content or `w-full` at the
bottom; label wraps instead of truncating. **A11y**: role button; loading sets `accessibilityState.busy` and
announces the loading text.

## IconButton

48 round, icon 24 (app bar) or 20 (rows). `variant`: ghost (default), secondary, outline. Always
`accessibilityLabel` ("Back", "More options", "Add note").

## ExtendedFab (Android only)

Radius `tile` 16, `shadow-overlay`, height 56, icon + "New list". Bottom-right above bottom navigation,
16 from edges. Collapses to a 56 icon FAB when the list scrolls. iOS: "+" icon button in the large-title
bar instead.

## DecisionButton · UndoButton · DecisionBar (Custom)

**DecisionButton**: circle 64 (`size-16`), icon 28, label + count below (`text-caption`, count
`tabular-nums text-muted-foreground`). Props: `decision: 'accept'|'reject'|'maybe'`, `count`, `progress`
(0–1 from the active drag), `armed`, `disabled`, `onPress`.

| State | Look |
| --- | --- |
| rest | `bg-{d}-soft text-{d}-soft-foreground` |
| dragging (progress p) | soft fill, icon scales 1 + 0.1p |
| armed | `bg-{d} text-{d}-foreground ring-4 ring-{d}/25` |
| pressed | solid fill, scale 0.94 (spring `press`) |
| disabled | opacity 40% (end of round, read-only lists) |

**UndoButton**: circle 48, outline, `undo-2` icon, label "Undo". Disabled when the undo stack is empty.

**DecisionBar**: row `Undo · Reject · Maybe · Accept · Note`, evenly spaced, 16 bottom padding above the
system bar. Order never changes. **A11y**: labels "Reject, 17 rejected", "Maybe, 11 maybe", "Accept, 48
accepted", "Undo last decision (Accept on Ayşe Demir)"; disabled undo "Nothing to undo".

## SwipeCard · CardStack · DecisionStamp (Custom)

**CardStack**: the top card plus the next card behind it (scale 0.95, translateY 14, no shadow; slightly
`opacity-100` but its content hidden behind the top card). When there is no next card, nothing renders
behind. Last card: the stack area shows the round-complete transition (S27).

**SwipeCard** (`rounded-hero` 28, `bg-card`, `shadow-hero`; dragging `shadow-hero-drag`): content from the
list's card template.

| Template | Layout |
| --- | --- |
| Person | Image area top (photo, cover-cropped, 46% of height); without a photo, a 96 initials avatar on `bg-muted` above the title (no empty image block); title `text-card-title` (max 3 lines); subtitle `text-body-lg muted`; up to 4 field rows (label 64 wide `muted`, value; multi-value shows first + "+2"); tags as secondary chips pinned to the bottom |
| Product | Image area top (50%), title, subtitle (store), price `text-title-1 tabular-nums`, rating with `star` icon and review count, tags |
| Photo | Image fills the card; caption panel at the bottom on `bg-card` with the title and subtitle fields (e.g. place and country in "Trip ideas", A-130/A-131); no overlays on the image. For sources with an image link per row (CSV, Google Sheets) |
| Candidate / Task / Generic | No image (or avatar); title, subtitle, rows, tags; rows can go up to 6 |

Sparse cards (image area None): title, subtitle and rows form one block vertically centered above the pinned tags (`my-auto`); templates with up to 3 rows use `text-title-2` values with `space-y-5`, 4–6 rows `text-title-3` with `space-y-3`; title-only cards use `text-display`. The template's row count decides, never the item's values.

Missing values: rows with no value are omitted; missing image → initials (person) or `image-off`
placeholder (product, photo). Long text: title clamps at 3 lines, rows at 1 line with ellipsis. Edited
fields show a 14 `pencil-line` after the value. A note on the card shows a `sticky-note` line at the
bottom (first line of my note; private notes with `lock`). Optional "others' decisions" row
(MemberDecisions compact) at the top-right when the member turned it on (shared lists only).

**DecisionStamp**: pill (`rounded-full`, h 44, px 16, `text-label-lg`, icon 24) in the solid decision
color, rotated −8° (Accept, top-left), +8° (Reject, top-right), 0° (Maybe, bottom-center). Opacity/scale
per `motion.md` §2.4. Tint overlay: full card, `bg-{d}` at 0–24% opacity.

**A11y**: the card is one accessible element: label = title + subtitle + visible fields; hint "Swipe right
to accept, left to reject, up for maybe. Actions available."; `accessibilityActions` Accept, Reject, Maybe,
Undo, Add note, Open details. Tap opens S26.

## DecisionBadge · StatusBadge · Badge

`h-7`, `rounded-full`, `px-2.5`, icon 16 + `text-caption`. DecisionBadge: Accepted / Rejected / Maybe /
Not decided (soft colors). StatusBadge: Agreed (outline, `check-check`), Pending (muted, `clock`), Conflict
(`bg-conflict`, `git-compare-arrows`), Resolved by {name} (outline, `gavel`). Badge (neutral, secondary):
Shared, Edited, Archived, Owner, Decision Maker (primary-soft), Only you (dashed, lock), Not backed up
(text only, `cloud-off`).

## MemberDecisions (Custom)

Compact: overlapping avatars (32 or 40, `ring-2 ring-card`) each with a 20 decision dot (solid decision
color + 12 icon; undecided = `circle-dashed` on card). Expanded: rows `avatar · name · DecisionBadge`, me
first with "(you)", plus their notes underneath when present. A11y: compact variant is one image with
label "Deniz: Accept. Mert: Reject. Selin: not decided."

## Progress · SegmentedProgress

Sorting progress: label "76 / 100 decided" (`text-label tabular-nums`) + bar `h-1.5 bg-muted`, fill
`bg-primary`. Decision split: stacked `bg-accept | bg-maybe | bg-reject` on `bg-muted`, each segment
separated by 2 dp gaps, always accompanied by icon + count legend. List status: `bg-foreground` (agreed),
`bg-foreground/50` (conflict), `bg-muted` (pending) + legend with icons. A11y: `progressbar` with value
text, or `img` with full text label.

## Input · Label · Textarea · SearchField

Input 48 high, `rounded-control`, `border-input`, `bg-card`, text `text-body`, placeholder `muted`.
Focus: `border-primary ring-2 ring-ring/30`. Error: `border-2 border-destructive` + helper with
`circle-alert` icon, `aria-invalid`. Disabled: `bg-muted`. Edited (working copy): helper "Edited.
Original: …" with `pencil-line`, plus "Revert" link in S26. Suffix slot (currency, unit). Textarea:
same border, min 3 lines, counter "45 / 1,000". SearchField: `rounded-full bg-secondary`, `search` icon,
clear button (48) when filled.

## Switch · Checkbox · RadioGroup

Switch 52×32 (`w-13 h-8`) M3 style: on `bg-primary` with 24 thumb; off `border-2 border-input bg-muted`
with 20 thumb. Checkbox 24 `rounded-sm`, checked `bg-primary` + check; indeterminate shows `minus`.
Radio 24 circle. All live inside a row whose whole area is the target. Labels are the row text.

## SegmentedControl · FilterChip · DecisionSegments · Select

SegmentedControl: `rounded-full bg-secondary p-1`, segments 40 high (`hitSlop` 4 so each reaches 48), selected `bg-card shadow-raised`.
Use for 2–3 mutually exclusive options (theme, final/my decisions, card order). FilterChip: 36 high
(`h-9`) in a 48 row with `hitSlop` 6 (keep ≥ 6 dp free above and below the chip row), selected `border-primary bg-primary-soft` with leading check. DecisionSegments
(Results): chip tabs with icon + label + count; selected `bg-foreground text-background`. Select: trigger
like Input with `chevron-down`; opens a bottom sheet list on Android/iOS and a popover on web.

## ListGroup and rows (Custom)

ListGroup: `rounded-group bg-card`, no shadow, `divide-y` hairlines, optional section header above
(`text-label text-muted-foreground`, sentence case, `px-1 pb-2`) and footer text below
(`text-body-sm muted`). Rows (min 56, `px-4 py-3`, gap 16): leading icon (20, muted) or avatar, text
(title `text-body`, description `text-body-sm muted` wraps), trailing (chevron, value, switch, badge,
icon button). Pressed `bg-accent`. Destructive row: `text-destructive` icon and label. Unavailable
(web): title in `muted-foreground`, control at `opacity-50`, reason + "Get the app" link at full contrast.

**ItemRow** (results, conflicts): avatar/thumbnail 40, title (1 line), meta (1 line: subtitle field, or
note preview with `sticky-note`, or "Deniz accepted, Mert rejected" on shared lists), trailing badge.
Long-press / overflow opens "Change decision" sheet. **SelectableRow**: leading checkbox. **ListRow**
(home): name `text-title-3`, meta line with icon (Shared with 2 / On this phone only / Archived),
progress bar + "76 / 100". **MemberRow**: avatar, name, progress, role badge, overflow button.

## AppBar (Custom)

Small: 64 high, back/close icon button, `text-title-3` title (1 line, truncates), up to 2 trailing
actions. Large: small bar + `text-title-1` title below (top-level tabs). Modal: `x` close + title + text
action. Sorting bar: close, list name + round, overflow (see S25). iOS: 44 pt bar, `chevron-left` + previous
title in `text-primary`, centered title, large titles collapse on scroll (native). A11y: title is a header;
back button label "Back to {previous}".

## BottomNav

expo-router Tabs with a custom bar: 80 high, `bg-card border-t`, 3 items Lists (`list-checks`), Activity
(`activity`), Settings (`settings`). Active: `primary-soft` pill 64×32 behind the icon and semibold label.
Activity badge: unread count on `bg-primary text-primary-foreground` (`text-caption`); `destructive` is reserved for delete, remove and errors. iOS: standard tab bar height, active tint
only. Hidden inside list stacks, sorting and modals.

## ImportStepper (Custom)

Under the modal app bar on import steps: current step name (`text-label`), "Step 3 of 5" (`text-caption
muted`), segmented bar (one segment per step, `bg-primary` done/current, `bg-muted` next). Steps: Choose
source, Select items, Map fields, Review duplicates, Finish. Sources without mapping (manual entry)
drop that step; "Review duplicates" is removed when none are found.

## BottomSheet (Custom on @gorhom/bottom-sheet)

`bg-popover rounded-t-sheet shadow-sheet`, handle 32×4, title row (`text-title-3` + close icon button),
content, bottom actions (full-width). Scrim `bg-scrim/50`. Snap points by content; keyboard-aware for
notes. Back/escape closes. iOS: native page sheet (`presentation: 'formSheet'`) with grabber. A11y:
focus moves into the sheet; title is announced.

## AlertDialog · Dialog

`bg-popover rounded-dialog shadow-dialog p-6`, max width 360 within a 24 margin. Title `text-title-3`
(names the object), description `text-body muted`, actions right-aligned (Android) as ghost "Cancel" +
specific verb (destructive variant for destructive actions). Dialog (non-alert) for rename/save
template: title, input, Cancel + Save. iOS: destructive confirmations use the native action sheet / alert
with the same copy. Web: same as Android.

## Snackbar (Custom)

Inverse: `bg-foreground text-background rounded-control shadow-overlay`, min 48, `text-body-sm`,
optional single action in `text-primary-inverse`. Placement: 12 above the bottom navigation or decision
bar. Durations in motion.md. A11y: `role=status` (or `alert` for failures) announced politely.

## DropdownMenu

`bg-popover rounded-control shadow-overlay`, items 48 with icon + label, separator before destructive
items. iOS uses an action sheet / UIMenu with the same items.

## Alert / Banner · OfflineBanner · SyncNotice · BackupIndicator

Alert variants: `info` (primary-soft fill), `error` (card + destructive border + icon), `neutral` (card +
border, used for web-unavailable with `monitor-smartphone` and "Get the app"). OfflineBanner: slim
`bg-muted` strip under the app bar, `wifi-off` + "You're offline. Decisions are saved on this phone."
SyncNotice: inline text with `refresh-cw` (spinning) "Syncing 12 decisions…" → `cloud-check` "Synced".
BackupIndicator (guest): `cloud-off` + "Lists are on this phone only" + "Back up" link → S05 (web copy per D-08, S08 spec).
Per-list label (signed in, list kept on this phone only, D-33/A-137): `cloud-off` 16 + "On this phone only"
(`text-body-sm muted`) in the row meta (S08) and header meta (S09); web "On this browser only".

## EmptyState · ErrorState · Skeleton · Spinner

Centered column: optional 32 Lucide icon in `muted-foreground`, title `text-title-3`, one sentence
`text-body muted` (max-w-xs), primary action, optional ghost secondary. Error state uses the error copy
pattern ("This file can't be read. Save it as .csv or .xlsx and try again."). Skeleton: `bg-muted`
blocks with pulse. Spinner: `loader-circle` spin in `text-primary` + progress verb text.

## SourceTile (Custom)

Grid 2 columns, gap 12, `rounded-tile border bg-card p-4 min-h-28`. Icon 24 `text-primary` top-left; name
`text-label-lg`; one-line description `text-caption muted`. Pressed `bg-accent`. Unavailable on web:
dashed border, transparent fill, icon and name in `muted-foreground` (no opacity), `monitor-smartphone` 16 top-right, description "Needs the Android or iOS
app"; tapping opens a sheet explaining it with "Get the app". Data-driven: each tile is a Source definition
(see domain-model.md) — adding a source adds a tile.

## TemplateTile (Custom)

`rounded-tile border bg-card p-3`, a miniature schematic of the layout (image area, title bar, rows) on
`bg-muted`, name below, selected = `border-2 border-primary` + `circle-check`. "Custom" badge for user
templates. Long-press/overflow: Rename, Duplicate, Delete.

## Avatar · AvatarStack

Sizes 24, 32, 40, 56, 96. Photo `rounded-full`; fallback initials (first letters of first and last word)
on `bg-muted text-muted-foreground`. Stack: −8 overlap, `ring-2 ring-background`, "+3" overflow
counter. A11y: names as labels; decorative when the name is next to it.

## CoachMark (Custom)

First sort only (per user, per device). 4 steps: Swipe right to accept → Swipe left to reject → Swipe up for
maybe → "Tap the card for details. Undo is always here." Each step: scrim `bg-scrim/60` except the card,
the card animates the gesture (motion.md §3), bubble with icon, title, one line, step dots, Skip + Next
(Done on the last). Reduced motion: static arrow illustration. A11y: each step is a dialog; screen-reader
users get a single dialog explaining actions instead of gesture steps.

## Kbd (web only)

`h-6 min-w-6 rounded-sm border border-b-2 bg-card text-caption`. Shown in the S25 desktop frame under the
decision bar: ← Reject, ↑ Maybe, → Accept, Z Undo. Hidden on touch devices.

---

## Components promoted from the screens (Phase 3)

Designed inside screen files during Phase 3 and promoted here. Each entry names the reference frame(s) that
show it in every variant; build it once in `components/ui/` and reuse it. All use existing tokens only.

| Component | Built from | Anatomy and rules | Reference frames |
| --- | --- | --- | --- |
| **FullHeightSheet** | BottomSheet | Full-height sheet on `bg-background`, sticky footer for the primary action | `S31-default` |
| **PermissionExplainer** | Custom | 56 icon circle, title, lead, then 3 promise points / steps / event list / thumbnails, bottom actions. Also the no-permission intro before a system picker (D-17, D-18) | `S12-contacts`, `S12-notifications`, `S13-picker-intro`, `S15-default` |
| **SourceTile (offline variant)** | SourceTile | Dashed tile, `wifi-off`, "Needs a connection" | `S11-offline` |
| **FileRow / FileCard** | Row | File icon, name, meta (size, rows), "Change" | `S14-csv-preview`, `S39-file-ready` |
| **FilePreviewTable** | Custom | Horizontally scrolling table in a group, row numbers, "—" for empty cells, focusable scroll region; record view at ≥150% text | `S14-csv-preview`, `S14-csv-preview-large-text` |
| **FastScrollIndex** | Custom | Letter strip + letter bubble for lists > 200 | `S13-large` |
| **FieldMappingRow** | Row | Field name + rename, sample values, type chip (Select), several-values chip, "Show on cards" switch | `S19-contacts`, `S19-type-sheet`, `S19-multi-value` |
| **DuplicateGroup** | Custom | Reason line, two columns, Same/Similar markers (icon + word), Merge / Keep both / Skip radiogroup, outcome line; compact variant for long lists | `S20-default`, `S20-merge`, `S20-large` |
| **ColumnMatchRow** | Row + Select | File column and samples left, list field select right, "New" badge | `S21-mapping` |
| **SelectableTile** | Checkbox | Image tile as `role=checkbox` with a check badge. Only used by the retired Photos source (S18, out of scope, D-32); kept for a future image source | `S18-default` |
| **UploadFileRow + DropZone** | Custom | Upload progress per file, retry; drop zone on desktop only. Only used by the retired S18 (D-32); kept for future file sources | `S18-web`, `S18-web-uploading` |
| **PasswordRules** | Custom | Live rule list with `circle` / `circle-check` / `circle-alert` | `S03-sign-up`, `S04-new-password` |
| **ListMoveRow** | Row | List icon tile, name, count, neutral status icon + label (Moved, Moving…, Waiting, Not moved, and "On this phone only" with `cloud-off` muted for a list kept out of the move, A-143) | `S05-moving`, `S05-move-partial`, `S05-moving-some-kept` |
| **SelectableRow, locked** | Checkbox row | Checked and disabled with a reason line and `lock` icon ("Needed to share") | `S05-choose-lists` |
| **GestureChecklist** | Badge | Reject / Maybe / Accept chips; dashed when untried, soft + check when tried | `S02-demo` |
| **SignInCard** | Group | Icon, text, primary button; shown when not signed in | `S06-guest` |
| **SettingsStatusBlock** | Group | Backup state icon + label + detail + action | `S06-backup`, `S06-backup-failed` |
| **ProviderRow** | Row | Sign-in method with a trailing text action (Connect / Disconnect) | `S07-default` |
| **OwnershipChoice** | RadioGroup | Per owned shared list: transfer to a member or delete for everyone | `S07-delete-transfer` |
| **ResumeButton** | Button (pill) | Trailing pill on a list row, opens S25 at the next undecided item | `S08-default` |
| **DecisionCountChips** | Badge | Decision badges with counts in Reject, Maybe, Accept order | `S09-default` |
| **ListStatusLegend** | Group | Agreed / Conflict / Pending rows with meaning and count | `S09-shared` |
| **DecisionMakerCallout** | Alert | Resolve card at the top for the Decision Maker | `S09-shared-decision-maker` |
| **MembersLink** | AvatarStack + Row | Avatar stack + names, opens S34 | `S09-shared` |
| **SourceRow** | Row | Type icon, source label, count + date, "New" badge; opens a details sheet | `S09-shared-added`, `S09-source-details` |
| **SearchAppBar** | AppBar + SearchField | Search field replaces the title | `S08-search` |
| **SwipeActions (iOS)** | Custom | Row swipe actions on iOS | `S10-ios-archived`, `S28` iOS frames |
| **CountChip** | Badge | Pile count with decision icon on its soft color | `S24-default` |
| **DecisionPicker** | RadioGroup | Three equal buttons; selected = solid decision fill + icon + label | `S26-decision-changed` |
| **DecideBar** | DecisionButton | Three soft pill buttons pinned under the S26 sheet | `S26-default` |
| **FieldRow (detail)** | Row | 96 label column, wrapping value, edited block (badge, original value, Revert) | `S26-edited`, `S26-revert-confirm` |
| **NoteCard** | Card (flat) | Shared (muted fill), private (dashed, lock, "Only you"), solo; Edit / Delete | `S26-default`, `S26-private-note` |
| **FilterRow** | Row + chips | Field, operator, value chips; AND across rows | `S24-custom`, `S29-default` |
| **SummaryCounts** | Custom | Three decision columns with a split bar (S27 only) | `S27-default` |
| **TemplateTile (pick variant)** | TemplateTile | 128 wide, caption Recommended / Custom / Current, horizontal radio carousel | `S22-import-pick` |
| **CardPreview** | SwipeCard | Scaled SwipeCard (`aspect-card`, 50%) with previous/next and expand | `S22-import-pick`, `S23-default` |
| **ReorderRow** | Row | Drag handle + move up / move down / remove; lifted state while dragging | `S23-reorder` |
| **InfoRow** | Row | Non-interactive icon, title, description | `S33-default` |
| **AppBanner (web)** | Alert | "Get the app" strip on mobile web | `S32-web` |
| **GetAppDialog** | Dialog | QR code + store links on desktop | `S32-get-app` |
| **ConflictCard** | SwipeCard | SwipeCard + expanded MemberDecisions + notes; stamp "Final: Accept" for the Decision Maker | `S36-default`, `S36-drag-accept`, `S36-everyone-drag` |
| **RuleCard** | RadioGroup item | Tile with description, example and consequence | `S35-default` |
| **ActivityRow** | Row | Avatar with event badge, two lines, time, unread dot | `S38-default` |
| **InAppBanner / WebToast** | Snackbar | Top banner in app; toast on web (push unavailable) | `S38-in-app-banner`, `S38-web` |
| **ColumnPreview** | Badge | Your fields as outline chips, added columns as primary-soft chips with `plus` | `S39-google-destination` |
| **WriteConfirmation** | Group | Label/value rows: Creates / Writes / Doesn't change | `S39-google-confirm` |

| **AppliedFilterChip** | Toggle | Removable input chip (label + `x`) | `S28-filtered` |
| **ChangeDecisionSheet** | BottomSheet + DecisionPicker | Change my decision from a row; applies on tap | `S28-change-decision` |
| **MemberDecisionsText** | Text + icons | "You and Selin accepted" / "Mert rejected" with decision icons | `S28-shared` |
| **RoundRow** | Row | Round summary: name, date, split bar + legend, info button | `S30-default` |
| **DecisionSegments (extended)** | Tabs | Adds Conflicts, Pending and Not decided tabs | `S28-shared`, `S28-shared-mine` |

Token added for these: `aspect-card` (3 / 5, the Android sort-card shape).
