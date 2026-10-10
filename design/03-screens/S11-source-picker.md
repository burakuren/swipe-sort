# S11 Source picker

Frames: `S11-source-picker.html`. Generator: `tools/generators/S11-S15-import.py` (builds S11–S15 with one
shared import chrome). Components: `01-foundations/components.md` › SourceTile, AppBar (modal), ImportStepper,
BottomSheet, Snackbar, OfflineBanner.

## 1. Purpose and requirements

Step 1 of every import: choose where the items come from. The picker is a data-driven grid of SourceTiles;
each tile renders one **Source definition** (`domain-model.md › Source`), so a new source is one more tile
that reuses the same steps (Select items → Map fields → Review duplicates → Finish).

Covers: SRC-01, SRC-02, SRC-03, SRC-04, SRC-18, SRC-19 (entry), PLT-03, PLT-04, PLT-07, PLT-08, PLT-11,
PLT-14, PLT-16, PLT-21, PLT-23, GOAL-02, GOAL-03, GOAL-05, SUC-09, SCR-11.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S08 Home | "Import a list" (first run, `S08-first-run`) or the New list FAB (`S08-default`) |
| S21 Add items | "Add items" on S09 opens S11 in list context (`S11-existing-list`) |
| S12, S13, S14, S15 | "Choose another source" / "Not now" return here |

| To | Trigger |
| --- | --- |
| `S12-permissions.html#S12-contacts` | Contacts tile (`data-action="source-contacts"`) when contacts access has never been asked |
| `S13-contacts-import.html#S13-default` | Contacts tile when access is already granted (skips S12) |
| `S12-permissions.html#S12-contacts-denied` | Contacts tile when access is permanently denied (goes straight to recovery) |
| `S14-file-import.html#S14-default` | CSV or Excel tile (`source-csv`) |
| `S15-google-sheets.html#S15-default` | Google Sheets tile (`source-google`); when Google Sheets is already connected, straight to `S15-spreadsheets` |
| `S16-plain-text.html#S16-default` | Plain text tile (`source-text`) |
| `S17-manual-entry.html#S17-default` | Manual entry tile (`source-manual`) |
| `S12-permissions.html#S12-photos` | Photos tile (`source-photos`) when gallery access was never asked; granted → `S18-photos-import.html#S18-default` |
| `S18-photos-import.html#S18-default` | Web: "Upload photos" tile (file upload, no permission) |
| `S11-web-unavailable` sheet | Web: Contacts tile |
| Snackbar (`S11-offline-tapped`) | Offline: Google Sheets tile |
| `S08-home.html#S08-default` | Close (`x`), new list context. Nothing has been imported yet, so closing never asks |
| `S09-list-overview.html#S09-shared` | Close in the add-items context |

## 3. Layout and components

Full-screen modal (Android), page sheet (iOS), same column on web. Top to bottom:

1. **AppBar (modal)**: close IconButton (`x`, label "Close import"), title "Import" (`text-title-3`), the same
   on every import step (S11–S21). In the S21 context the title is "Add items" and the heading names the list.
2. **ImportStepper**: "Choose source", "Step 1 of 5", 5 segments (first filled). The total is provisional
   at this step: it is 5 for sources with field mapping and becomes 4 once a source without mapping
   (photos, manual entry) is chosen.
3. **Heading**: "Where are your items?" (`text-title-2`) + one line (`text-body muted`).
4. **SourceTile grid**: 2 columns, gap 12, equal row heights (`auto-rows-fr`), tiles `rounded-tile border
   bg-card p-4 min-h-28`, icon 24 `text-primary`, name `text-label-lg`, one-line description
   `text-caption muted`. Order follows the brief: Contacts, CSV or Excel, Google Sheets, Plain text, Manual
   entry, Photos. Grid order = `Source.order`; an odd count leaves the last cell empty.
5. **Data-safety note** pinned to the bottom of the content: `shield-check` 16 + one line.
6. List context only: section "Already in {list name}" (ListGroup with one row per existing Source: icon,
   label, "88 items, added Sep 27") and a `combine` hint about combining sources (SRC-18).

No bottom action bar: a tile tap is the action. No loading state: the source list is static and local (a
remote source list is not planned; if one is added later, render the static tiles immediately and append).

**Source definition → tile** (what a coding agent implements once):

| Definition field | Tile |
| --- | --- |
| `name` | Tile title |
| `icon` (Lucide) | 24 icon |
| `description` (per platform: iOS photos "From your photo library") | Caption |
| `availableOn` | When the current platform is missing: web-unavailable tile variant |
| `needsConnection` (Google Sheets) | Offline: offline tile variant |
| `needsPermission` (`contacts`, `photos`) | Routes through S12 when the permission is undecided or denied |
| `selectStep` | Route opened on tap |
| `hasFieldMapping` | Stepper total 5 (true) or 4 (false) |
| `webReplacement` (photos → "Upload photos") | Swaps name, icon (`image-up`), description and route on web |

`S11-new-source` shows a hypothetical "Calendar" source added with nothing but a new definition.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S11-default` | New list, Android, online |
| `S11-existing-list` | Opened from S21 / S09 "Add items" for Wedding guests (l-wedding: 88 from contacts, 12 from mert-family.csv); app bar "Add items", heading "Add items to Wedding guests" |
| `S11-offline` | No connection: OfflineBanner under the app bar; Google Sheets tile becomes the offline variant (dashed border, `wifi-off` 16, "Needs a connection"); other sources work offline |
| `S11-offline-tapped` | Offline tile tapped: snackbar, no navigation |
| `S11-large-text` | Font scale ≥ 150%: one tile per row, icon left, title and description wrap; the grid scrolls |
| `S11-new-source` | Annotation: a seventh tile from a new Source definition |
| `S11-web` | Web (mobile browser): Contacts tile is the web-unavailable variant; Photos becomes "Upload photos" |
| `S11-web-unavailable` | Web: Contacts tile tapped → bottom sheet with reason, "Get the app" and "Import a CSV instead" |
| `S11-web-desktop` | Desktop browser: same column centered (PLT-04) |
| `S11-ios` | iOS page sheet: `x` top-left (first step), centered "Import"; Photos description "From your photo library" |

Not applicable: empty (there is always at least one source), loading (static), error (nothing is fetched).

## 5. Interactions and transitions

- Tile tap: pressed `bg-accent` (100 ms), then push the source's first screen (M3 shared axis X, 300 ms;
  iOS native push inside the sheet; reduced motion: 150 ms fade).
- Unavailable tiles (web, offline) remain focusable and tappable; they never navigate. Web opens the sheet
  (300 ms emphasized decelerate; reduced motion: fade 150 ms). Offline shows the snackbar for 4 s and
  re-enables the tile automatically when the connection returns (banner disappears, tile animates its
  border from dashed to solid with a 150 ms fade).
- Close: closes the import modal (Android: slide down 300 ms; iOS: sheet dismiss). iOS swipe-down to dismiss
  is allowed on S11 because nothing is selected yet.
- Android system back = close on S11 (it is the first step).
- The last-used source is not reordered to the top: a stable grid builds muscle memory.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; list context "Add items" |
| Close label | "Close import"; list context "Close, back to Wedding guests" |
| Stepper | "Choose source", "Step 1 of 5" |
| Heading | "Where are your items?"; list context "Add items to Wedding guests" (`Add items to {list name}`) |
| Sub line | "Choose a source. You can add items from other sources later."; list context "Choose where the new items come from. They join the current round." |
| Tiles | "Contacts" / "From this phone"; "CSV or Excel" / "A .csv or .xlsx file"; "Google Sheets" / "From Google Drive"; "Plain text" / "Paste a list or a .txt file"; "Manual entry" / "Type items one by one"; "Photos" / "From your gallery" (iOS: "From your photo library") |
| Web photos tile | "Upload photos" / "Image files from this device" |
| Web-unavailable tile | "Contacts" / "Needs the Android or iOS app" |
| Offline tile | "Google Sheets" / "Needs a connection" |
| Offline banner | "You're offline. Google Sheets needs a connection; other sources work." |
| Offline snackbar | "Google Sheets needs a connection. Try again when you're online." |
| Safety note | "SwipeSort imports a copy. Your contacts, files and sheets are never changed." |
| List context group | "Already in Wedding guests"; rows "Contacts" / "88 items, added Sep 27", "mert-family.csv" / "12 items, added Sep 28" |
| Combine hint | "A list can combine any sources. New items are checked for duplicates before they're added." |
| Web sheet title | "Contacts import needs the app" |
| Web sheet body | "Browsers can't read your phone's contacts. Get SwipeSort for Android or iOS to import them, or export your contacts as a CSV file and import that here." |
| Web sheet actions | "Get the app" (primary), "Import a CSV instead" (ghost, below) |
| Example future tile | "Calendar" / "Events from your calendar" (annotation only, not shipped) |

## 7. Accessibility

- Focus order: Close, title, stepper, heading, tiles in reading order (row by row), safety note.
- The stepper is a `progressbar` labeled "Step 1 of 5, Choose source".
- Tiles are links with the name and description as their accessible name ("Contacts, From this phone").
  Unavailable tiles announce the reason as part of the name ("Contacts, Needs the Android or iOS app") and
  `aria-haspopup="dialog"` (web) so users know a sheet opens.
- The unavailable reason is full-contrast `muted-foreground` text, never dimmed with opacity.
- The offline snackbar uses `role="status"`; the offline banner is `role="status"` and announced once.
- Large text: tiles switch to a single column at ≥ 150% font scale; text wraps, nothing truncates except
  the app bar title (the list name, also announced in full).
- Touch targets: tiles are ≥ 112 dp tall; close is 48.

## 8. iOS and web differences

- **iOS** (`S11-ios`): import opens as a page sheet (`presentation: 'pageSheet'`) with a 44 pt bar: `x` at the
  left on this first step and a centered title; later steps show a "Back" chevron at the left (edge-swipe
  back) and `x` at the right (same bar as S16–S21). Swipe-down dismisses on S11; later steps set
  `isModalInPresentation` once something is selected, and `x` asks "Discard import?" as an action sheet.
- **Web, mobile** (`S11-web`): contacts import is unavailable (PLT-07): the tile stays visible with the
  dashed unavailable treatment, a `monitor-smartphone` marker and the reason; tapping opens
  `S11-web-unavailable`. Photos use "Upload photos" (browser file input, `accept="image/*"`, multiple) and
  go to S18's web upload (PLT-08).
- **Web, desktop** (`S11-web-desktop`): the same column centered; tiles get a hover state (`bg-accent`).
- "Get the app" opens `https://swipesort.app/get`, which redirects to Google Play or the App Store by user
  agent and shows both store links with QR codes on desktop (lead to unify with S32/S40).

## 9. Edge cases

- **Contacts permission already granted**: the contacts tile skips S12 and opens S13 directly. Permanently
  denied: opens `S12-contacts-denied` directly (no pointless explainer).
- **Google Sheets already connected**: skips S15's explainer and opens `S15-spreadsheets`.
- **Offline**: only Google Sheets is affected; contacts, files, text, manual entry and photos work offline.
  Coming back online re-enables the tile without reloading.
- **Combining sources** (SRC-18): any number of sources per list; in list context the new items join the
  current round (`Item.addedInRoundId`) and duplicates against existing items are reviewed in S20.
- **Long list names** in the add-items context truncate in the app bar; the heading's sub line uses the
  full name and wraps.
- **Text expansion** (+40%): descriptions may wrap to two lines; rows keep equal heights via
  `auto-rows-fr`; at large text the single-column layout takes over.
- **New sources**: more than 8 tiles still fit the scrolling grid; group headers are not needed until
  more than 12 sources exist (then: "On this phone", "Files", "Online").
