# S18 Photos import (retired)

> **Out of scope (D-32) — kept for reference; not part of the current design.** The Photos source was removed
> until its outcome is designed (`docs/build-decisions.md` D-32; `design/00-brief/assumptions.md` A-129). No
> screen links here (the S11 and S21 tiles, the S12 photos explainer, denied and limited-access states are gone)
> and no flow passes through these frames. When photos return, they use the system photo picker and never
> `READ_MEDIA_IMAGES` (D-27). Contact photos and image fields are unaffected. Everything below describes the
> design as it stood before D-32; its references to `S12-photos` and the S11 Photos tile no longer resolve.

Frames: `S18-photos-import.html`. Generator: `tools/generators/S18-photos-import.py`. Components: ImportStepper,
AppBar (modal), SelectableTile (proposed), BottomSheet, Alert, Snackbar (`01-foundations/components.md`).

## 1. Purpose and requirements

Step 2 of the photos import ("Select items"). On Android and iOS the person picks photos from the gallery in
SwipeSort's own selection grid; on the web, where the gallery picker is not available, they upload photo files.
Each photo becomes one item. Photos have fixed fields (Photo, Taken, Location, File name), so field mapping is
skipped, and duplicate review is skipped (two photos are never merged). The result becomes a list like
the former sample list "March photos clean-up" (sample `photos` ph01–ph30; replaced by "Trip ideas", A-130).

Covers: SRC-01 (photos source), SRC-02, SRC-07 (select photos), SRC-24 (partial import: upload), PLT-02,
PLT-03, PLT-04, PLT-08, PLT-11, PLT-13, PLT-14, PLT-15, PLT-16 (large text, described in §7), PLT-21, PLT-23, GOAL-02, GOAL-05, VIS-13, VIS-14,
SMP-05, SCR-18.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S12 photos explainer (`S12-permissions.html#S12-photos`) | Access granted in the system prompt (full or limited on iOS) |
| S11 source picker (`S11-source-picker.html#S11-default`) | Photos tile when access was already granted |
| S11 on web (`S11-web`) | Photos tile reads "Upload photos" and opens `S18-web` directly (no permission step) |
| S21 add items | Photos tile in list context (same step, app bar title "Add items", stepper of S21) |

| To | How |
| --- | --- |
| S22 finish (`S22-template-library.html#S22-import-pick`) | Continue (`data-action="continue"`); Photo card template is preselected there |
| S11 source picker | Empty gallery: "Choose another source"; iOS: Back |
| S08 home (`S08-home.html#S08-default`) | Close (`x`); with photos selected the "Discard import?" dialog (S40) asks first |
| System settings / iOS limited picker | iOS limited access links (system UI, out of scope) |
| Permission denied | Never reaches S18: handled in S12 (denied recovery state) |

## 3. Layout and components

Full-screen modal, no bottom navigation. Top to bottom:

1. **AppBar (modal)**: close IconButton (`x`, "Close import"), title "Import". iOS: 44 pt bar, back chevron
   "Back" (to Choose source), centered title, close at the right.
2. **ImportStepper**: "Select items", "Step 2 of 3" (Choose source, Select items, Finish).
3. **Selection toolbar** (gallery): count ("30 selected" / "Select photos" / "Loading photos…", `text-label
   tabular-nums`, live region), album select chip ("All photos", `images` icon, opens the album sheet), text
   button "Clear" / "Select all". Hairline border below.
4. **Grid** (gallery): sections per day, newest first; days with fewer than 4 photos merge into their week
   (Monday to Sunday) so rows stay full ("Mar 9 to 15"). Header (56 high): "Sunday, Mar 15" or "Mar 9 to 15" (`text-label`,
   heading) + locations in that group (`text-caption muted`, "No location" when none) + day checkbox button
   (48, checked / mixed / unchecked). Tiles: 4 columns, edge to edge, 2 dp gaps, square, `object-cover`.
   - **SelectableTile** (Proposed component): button `role="checkbox"`. Selected: 2 dp `ring-primary` inset
     ring + 24 check badge top-right (`bg-primary` + `check` icon, `ring-2 ring-card`). Unselected: 24 empty
     circle (`border-2 border-card` on `bg-scrim/30`). The check icon, not the color, carries the state.
5. **Bottom action**: note "Each photo becomes one item." + primary "Continue" (h-14, full width).
6. Web: **upload zone** (dashed `border-input`, `rounded-tile`, `bg-card`): `upload` icon, "Upload photos from
   this device", formats caption, outline button "Choose photos" (`image-plus`). Desktop while uploading: compact
   zone "Drop to add more" + ghost "Add photos". **File list** (ListGroup): 48 thumbnail (`rounded-sm`;
   `image-off` placeholder for non-images), file name + size on line 1, status on line 2 (Uploaded / Uploading…
   64% with a 80-wide bar / Waiting / Paused / error in `text-destructive` with `circle-alert`), remove icon
   button on errors. Overall status line + progress bar above the list.
7. Overlays: album BottomSheet, limit Snackbar, web-unavailable Alert (neutral, `monitor-smartphone`), large
   selection Alert (info), iOS limited-access Alert (neutral, `lock`).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S18-default` | Android, access granted, all 30 photos (ph01–ph30) selected; "30 selected" + Clear |
| `S18-none-selected` | First open: nothing selected; count reads "Select photos", "Select all"; Continue disabled |
| `S18-loading` | Gallery is being read: spinner + "Loading photos…", first day loaded, other tiles skeleton; Continue disabled; tiles not focusable until loaded |
| `S18-empty` | Gallery has no photos: empty state with "Choose another source" |
| `S18-albums` | Album chip tapped: sheet with All photos 30, Camera 26, Lisbon 8, Downloads 4 |
| `S18-large` | 1,000 or more selected (1,248): info alert, Continue stays enabled |
| `S18-limit` | Trying to select beyond 5,000: selection stops at 5,000, snackbar explains; the day with the boundary is mixed |
| `S18-ios-limited` | iOS limited photo access: only the 12 shared photos (ph19–ph30) show; banner with "Select more photos" and "Allow access to all photos in Settings" |
| `S18-web` | Web (mobile browser): gallery unavailable notice + upload zone; Continue disabled until a photo is uploaded |
| `S18-web-uploading` | Web desktop: 32 files chosen, 30 valid uploading ("Uploading 18 of 30 photos…"), 1 video and 1 file over 25 MB rejected before upload; Continue disabled |
| `S18-web-partial` | Upload finished with failures: "Uploaded 30 of 32 photos"; failed files listed with reasons; "Continue with 30 photos" |
| `S18-web-offline` | Connection lost during upload: offline banner, files "Paused", "Uploaded 12 of 30 photos. Paused."; resumes automatically |

Not separate frames (same layout): iOS with full access = `S18-default` with the iOS bar from `S18-ios-limited`;
web desktop before choosing = `S18-web` inside the desktop frame with the zone reading "Drop photos here".

## 5. Interactions, gestures and transitions

- **Tap a tile**: toggles selection. Check badge scales in 0.8 → 1 with a 150 ms fade (`short3`, standard);
  ring appears at once. Reduced motion: instant.
- **Long-press a tile**: opens a full-screen preview (system-like viewer, out of scope for frames) with the
  date, location and file name, and a "Select" toggle. Swipe left/right in the preview moves between photos.
- **Drag-select** (Android, iOS): after a long-press on the check badge area, dragging across tiles selects the
  range (standard gallery pattern). Optional for the first build; tapping is always enough.
- **Day checkbox**: selects or clears every photo of that day; mixed when some are selected.
- **Clear / Select all**: Clear deselects everything (no confirmation; selection is cheap to redo). Select all
  selects the album, up to 5,000.
- **Album chip**: opens the album sheet (M3 bottom sheet, 300 ms enter). Switching album keeps the selection.
- **Limit**: selecting past 5,000 is ignored; snackbar (4 s) explains. Selecting 1,000+ shows the info alert
  above the grid (not blocking).
- **Continue**: goes to S22 finish (pick mode, Photo template preselected). Photos are copied into SwipeSort's
  working copy at "Start sorting" in S22 ("Importing 30 items…").
- **Scrolling**: the toolbar stays pinned under the stepper; day headers scroll with content.
- **iOS limited**: "Select more photos" opens the system limited-library picker; on return the grid refreshes
  and newly shared photos are added selected. "Allow access to all photos in Settings" opens iOS Settings.
- **Web upload**: "Choose photos" opens the browser file picker (`accept="image/jpeg,image/png,image/heic,
  image/webp"`, multiple). Desktop also accepts drag and drop on the zone and anywhere over the column (the zone
  highlights with `border-primary` while dragging over). Files are checked for type and size before upload;
  rejected files appear at once with the reason. Uploads run 3 at a time; progress per file and overall.
  Remove (`x`) on a failed file removes it from the list. When every upload settles, the screen shows the result
  (`S18-web-partial` if anything failed, otherwise Continue enables and the status reads "Uploaded 30 photos").
- **Offline (web)**: uploads pause; resume automatically when the connection returns. The Android/iOS gallery
  works offline (local files).
- **Back**: Android system back / iOS edge swipe returns to Choose source (selection is kept for this session).
- **Haptics**: none on selection (selection is frequent; feedback is visual).

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; close label "Close import"; iOS back "Back" (label "Back to Choose source") |
| Stepper | "Select items", "Step 2 of 3" (label "Step 2 of 3, Select items") |
| Toolbar count | "30 selected"; "Select photos" (none selected); "Loading photos…"; "1,248 selected"; "5,000 selected"; "12 selected" |
| Toolbar actions | "Clear"; "Select all" |
| Album chip | "All photos" (label "Album: All photos. Change album") |
| Album sheet | Title "Album"; subtitle "Selected photos stay selected when you switch albums."; rows "All photos" "30 photos", "Camera" "26 photos", "Lisbon" "8 photos", "Downloads" "4 photos"; close label "Close" |
| Day header | "{Weekday}, {Mon} {d}" e.g. "Sunday, Mar 15"; locations "Cihangir, İstanbul"; "No location" |
| Day checkbox label | "Select all photos from Mar 15" |
| Tile label | "Photo taken Mar 15, 15:16, Cihangir, İstanbul" (location omitted when missing) |
| Bottom | Note "Each photo becomes one item."; "Continue" |
| Empty | "No photos on this phone" / "Photos you take or save show up here. You can import from another source instead." / "Choose another source" |
| Large selection | "1,248 photos make a long round" / "You can import them all and sort in several sittings. Progress saves as you go." |
| Limit snackbar | "Up to 5,000 photos can be imported at once. Unselect some to add others." |
| iOS limited | "SwipeSort can see 12 photos you chose" / "Select more photos" / "Allow access to all photos in Settings" |
| Web unavailable | "Picking from your phone's gallery needs the Android or iOS app" / "You can upload photo files here instead." / "Get the app" |
| Upload zone (mobile web) | "Upload photos from this device" / "JPG, PNG, HEIC or WebP, up to 25 MB each." / "Choose photos" |
| Upload zone (desktop) | "Drop photos here" / "or" / "Choose photos" / formats caption; while uploading "Drop to add more" + "Add photos" |
| Upload status | "Uploading 18 of 30 photos…"; "2 can't be added"; "Uploaded 30 photos" (all done); "Uploaded 12 of 30 photos. Paused." |
| File states | "Uploaded"; "Uploading… 64%"; "Waiting"; "Paused" |
| File errors | "Videos can't be imported."; "Too large. The limit is 25 MB."; other formats: "This file type can't be imported. Use JPG, PNG, HEIC or WebP."; unreadable: "This file can't be read. Choose it again." |
| Remove button label | "Remove {file name}" |
| Bottom note (web, uploading) | "You can continue when the upload finishes." |
| Partial result | "Uploaded 30 of 32 photos" / "2 files couldn't be added. Save them as JPG, PNG, HEIC or WebP under 25 MB and choose them again, or continue without them." / section "Couldn't be added (2)" / section "Ready to import (30)" / "And 22 more" / "Continue with 30 photos" / "Choose more photos" |
| Offline (web) | "You're offline. Uploads continue when you're back online." |
| Screen reader | Selection changes announce "30 selected"; upload completion announces "Uploaded 30 of 32 photos" |

## 7. Accessibility

- Focus order: Close, (iOS Back), stepper, toolbar count, album chip, Clear/Select all, then per day: day
  checkbox, tiles left to right, then Continue.
- Tiles are `role="checkbox"` buttons with `aria-checked` and a label made of date, time and location (no file
  name; it is not meaningful to most people). Day checkboxes support `mixed`.
- Selection state is shown by the check icon and the ring, never by tint alone; the empty circle shows
  selectability.
- The count is a live region (polite), so selection and loading changes are announced.
- Touch targets: tiles ~101 dp; day checkbox, chips, text buttons and remove buttons 48.
- Upload rows: progress bars are `progressbar` with value and name; errors pair `circle-alert` with text.
- Large text: the grid is not text-dense, so no separate frame. At 200% the toolbar wraps to two lines (count
  above, album chip and Clear below), day headers grow (location wraps), tiles keep 4 columns (3 below 360 dp
  width), file rows wrap the status line. The bottom note wraps above Continue.
- Reduced motion: no badge scale, skeleton pulse becomes static, sheets fade (150 ms).

## 8. iOS and web differences

- **iOS full access**: identical grid with the iOS bar (back chevron + centered title + close at right; edge
  swipe goes back to Choose source). No separate frame.
- **iOS limited access** (`S18-ios-limited`): only shared photos appear, preselected; the banner offers
  "Select more photos" (system limited picker) and Settings. The banner stays while access is limited.
- **iOS sheets**: the album picker is an iOS page sheet with a grabber and "Done"; content the same as
  `S18-albums`.
- **Web** (PLT-08, PLT-11): no gallery picker. The step shows the neutral "needs the app" notice with
  "Get the app" (links to the app store page chooser, `https://swipesort.app/get`) and the upload zone. On mobile
  browsers "Choose photos" opens the browser picker, which on phones includes the photo library and camera;
  the zone does not mention dragging there. Desktop adds drag and drop.
- **Web offline**: uploads pause and resume; no Continue until finished.
- Android is the reference (M3 bottom sheet, snackbar above the bottom action).

## 9. Edge cases

- **Very large libraries** (10,000+ photos): the grid virtualizes rows; thumbnails load progressively
  (skeleton tiles); Select all selects the first 5,000 newest and shows the limit snackbar.
- **Over 5,000**: hard limit per import (same as plain text); more can be added later with S21 Add items.
- **1,000 to 5,000**: info alert only, never blocks.
- **Photos without date** (rare, e.g. downloaded images): grouped under "No date" at the end; Taken field empty.
- **Photos without location**: header shows "No location"; Location field empty on the card (row hidden).
- **Live Photos / bursts / videos**: only still images are listed in the gallery grid; on the web, videos are
  rejected with "Videos can't be imported."
- **HEIC on web**: accepted and converted for display; if a browser cannot decode it, "This file can't be read.
  Choose it again." with remove.
- **Duplicates**: the same photo cannot be selected twice in the gallery; on the web, choosing the same file
  name and size again is ignored silently.
- **Permission revoked while open**: the grid empties and S12 denied recovery opens.
- **Leaving with a selection**: Close asks "Discard import?" (S40); Android back steps back and keeps it.
- **Offline (app)**: gallery selection works; the import itself is local.
- **Long album names / Turkish**: chip truncates at 160 dp with the full name in the sheet; toolbar wraps at
  large text.
