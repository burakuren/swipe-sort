# S16 Plain-text import

Frames: `S16-plain-text.html` (generator `tools/generators/S16-plain-text.py`). Components: `01-foundations/components.md`.
Next step: `S19-field-mapping.html#S19-text`.

## 1. Purpose and requirements

The "Select items" step for the Plain text source: paste a list or open a `.txt` file, one item per line. Every
non-blank line becomes one item with a single text field; S19 lets the user name that field (A-24). Sample:
`books` in `sample-data.json` (12 titles; the resulting list is "Book club picks", `l-books`).

Covers: SRC-01 (plain text: paste or .txt), SRC-03 (same flow structure as every source), SRC-04, SRC-07 (select
items), SRC-14 (duplicate lines handled in place), SRC-20 (unreadable file), SRC-21 (empty file), SRC-24 (limit:
only the first 5,000 lines are imported), GOAL-02, GOAL-03, GOAL-05, PLT-01–PLT-04, PLT-13–PLT-16, PLT-21, PLT-23,
VIS-11–VIS-14, TERM-01, SCR-16.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S11 source picker | Tile "Plain text" (`S11-source-picker.html#S11-default`) |
| S21 add items | Same tile in list context (title "Add items"; see S21 spec) |
| S19 (back) | System back / iOS back chevron returns here with the text kept |

| To | How |
| --- | --- |
| S19 field mapping, single field | "Continue" (`S19-field-mapping.html#S19-text`, `data-action="continue"`) |
| System file picker | "Open a .txt file" (Android Storage Access Framework, iOS Files app, browser file input); out of scope |
| S11 | System back / iOS back chevron "Back" |
| S08 home | Close (`x`). With text entered, the S40 "Discard import?" dialog asks first (`S40-global-patterns.html#S40-default`) |

## 3. Layout and components

Full-screen import modal. Top to bottom:

1. **AppBar (modal)**: close IconButton (`x`, "Close import"), title "Import" (`text-title-3`).
2. **ImportStepper**: "Select items", "Step 2 of 4" (Choose source, Select items, Map fields, Finish).
   Review duplicates is not part of this flow because duplicate lines are handled here (decision D-S16-1).
3. **Heading**: "Paste your list" (`text-title-2`) + one-line instruction (`text-body muted`).
4. **SegmentedControl** (ToggleGroup as tabs): "Text" / "Preview (12)". Segments are 48 high in a `p-1` track.
5. **Text tab**: Textarea (RNR `Textarea`, multiline, `rounded-control`, ~15 visible lines, grows to fill the
   space, scrolls inside), then a status row: live count "12 items" (`text-label tabular-nums`) left, "1 blank
   line skipped" (`text-caption muted`) right. Optional file chip above the box when a file was opened.
6. **Open a .txt file**: Button `outline`, full width, `file-up` icon.
7. **Preview tab**: ListGroup of parsed items, each row with its line-order number (muted, tabular) and the text.
8. **Alerts** (Alert component) above the box: `info` for duplicate lines, `error` for limits and file errors.
9. **Bottom action**: Button `lg` full width "Continue" (disabled while there are 0 items).

## 4. States

| Frame | Trigger |
| --- | --- |
| `S16-empty` | First open from S11. Empty box (focused, keyboard up), placeholder, "0 items", Continue disabled |
| `S16-default` | 12 lines pasted (with one blank line), count 12, Continue enabled |
| `S16-preview` | Preview tab: 12 parsed items in order |
| `S16-duplicates` | Two lines appear twice; info alert with "Remove duplicates"; count "14 items, 2 duplicates" |
| `S16-too-many` | More than 5,000 non-blank lines (6,214 pasted); error alert; button "Continue with 5,000 items" |
| `S16-file` | "Open a .txt file" succeeded: file chip "book-club.txt", text loaded into the box (editable) |
| `S16-loading` | Reading a large file (spinner + "Reading book-club.txt…"); Continue disabled |
| `S16-error-empty-file` | The chosen .txt file has no text (or only blank lines) |
| `S16-error-unreadable` | The chosen file is not plain text (e.g. .docx, binary) or not decodable |
| `S16-large-text` | 200% font scale |
| `S16-ios` | iOS variant |
| `S16-web-desktop` | Desktop browser: paste or drop a file |

Offline: not applicable (paste and local files work offline). Web-unavailable: not applicable (works on web).

## 5. Interactions, gestures and transitions

- **Parsing** runs on every change (debounced 150 ms): split on `\n` / `\r\n`, trim each line, drop empty lines.
  Count = non-blank lines. Leading and trailing whitespace is removed; inner text is kept exactly (case, accents,
  Turkish characters).
- **Count** updates in place (`tabular-nums`, no animation). Screen readers hear it via `role="status"`, at most
  once per second.
- **Tabs**: Text ↔ Preview swap content with a 150 ms cross-fade (reduced motion: instant). The preview is
  read-only; tapping a row switches to Text with the cursor on that line.
- **Duplicate lines** (exact match after trimming, case-insensitive): info alert lists up to 3 values
  ("and 4 more" beyond that). "Remove duplicates" keeps the first occurrence, removes later ones, updates the
  count and shows a snackbar "Removed 2 duplicate lines" with "Undo". Duplicates are kept unless removed.
- **Limit**: 5,000 items per import (same limit as photos, D-S16-2). Above it, the error alert shows and the
  primary button label states the outcome: "Continue with 5,000 items". Lines after 5,000 are not imported; the
  preview count shows "Preview (5,000)".
- **Open a .txt file**: opens the system picker filtered to `text/plain`. While reading: loading state. Success:
  file chip + content replaces the box text (if the box already had text, a dialog asks "Replace the text in the
  box?" with "Replace" / "Cancel"). "Clear" empties the box and removes the chip. Encoding: UTF-8, UTF-16 with BOM;
  Windows-1254 (Turkish) fallback when UTF-8 decoding fails.
- **Errors** keep the user on this step; "Choose another file" reopens the picker; the paste box stays usable.
- **Continue**: goes to S19 (`S19-text`) with one field "Text", standard push transition (M3 shared axis X 300 ms;
  reduced motion: fade 150 ms).
- **Close**: with any text, S40 dialog "Discard import?"; otherwise closes immediately.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; close label "Close import" |
| Stepper | "Select items", "Step 2 of 4" |
| Heading | "Paste your list" |
| Instruction | "One item per line. Blank lines are skipped." |
| Tabs | "Text", "Preview (12)" (count of items to import) |
| Textarea label (screen reader) | "Items, one per line" |
| Placeholder | "Type or paste, one item per line" |
| Count | "0 items", "1 item", "12 items", "14 items, 2 duplicates", "6,214 items, limit 5,000" |
| Blank lines | "1 blank line skipped", "3 blank lines skipped" |
| File button | "Open a .txt file"; after a file: "Open another file" |
| File chip | "book-club.txt"; "12 lines, editable below"; "Clear" (label "Clear book-club.txt") |
| Preview | "Each line becomes one item, in this order." |
| Duplicates alert | "2 lines appear twice: Piranesi, Station Eleven." / "Duplicates stay in the list unless you remove them." / "Remove duplicates" |
| Duplicates snackbar | "Removed 2 duplicate lines" + "Undo" |
| Limit alert | "6,214 lines" / "Up to 5,000 items can be imported at a time. Only the first 5,000 lines will be imported." |
| Limit button | "Continue with 5,000 items" |
| Loading | "Reading book-club.txt…" |
| Empty file | "reading-list.txt is empty" / "Choose another file or paste your list." |
| Unreadable file | "book-club.docx can’t be read" / "Save it as plain text (.txt) and try again." |
| Error action | "Choose another file" |
| Replace dialog | "Replace the text in the box?" / "The text you typed is replaced by book-club.txt." / "Cancel", "Replace" |
| Primary | "Continue" |
| Web drop zone | "Drop a .txt file here, or browse" / "Plain text, UTF-8, up to 5,000 lines" |
| Discard dialog (S40) | "Discard import?" (copy owned by S40) |

## 7. Accessibility

- Focus order: Close, step indicator, heading, tabs, (alert and its action), file chip and Clear, text box, count,
  Open a .txt file, Continue.
- Tabs use `role="tablist"`/`tab` with `aria-selected`; segments are 48 high.
- Text box has a programmatic label "Items, one per line"; the count and the blank-line note are a polite live
  region. Error alerts use `role="alert"` and move focus to the alert title after a failed file read; the haptic
  error pattern plays (motion.md §5).
- Disabled Continue uses the real `disabled` attribute; the reason is visible ("0 items").
- Preview rows: the line numbers are decorative (`aria-hidden`); the list is an `ol`, so screen readers announce
  positions.
- Large text (`S16-large-text`): heading, tabs and box text scale; the box keeps at least 6 visible lines and the
  page scrolls; long lines wrap inside the box (no horizontal scroll); step label and "Step 2 of 4" stack.
- Contrast: all text uses AA token pairs; the placeholder uses `muted-foreground`.

## 8. iOS and web differences

- **iOS** (`S16-ios`): 44 pt bar with a back chevron "Back" to the source picker (edge swipe back) and close `x`
  at the right; "Open a .txt file" opens the Files app document picker (`UIDocumentPicker`, type `public.plain-text`).
  Paste uses the iOS paste permission prompt (system, out of scope).
- **Web, mobile**: same layout as Android, no system bars; the file opens with the browser file input.
- **Web, desktop** (`S16-web-desktop`): phone layout centered; the outline button is replaced by a dashed drop
  zone "Drop a .txt file here, or browse" (dropping anywhere on the column also works; the zone highlights with
  `border-primary bg-primary-soft` while dragging). Ctrl/Cmd+V pastes into the box.

## 9. Edge cases

- **Very long lines**: kept in full (up to 1,000 characters; longer lines are cut at 1,000 with a note "2 lines
  were shortened to 1,000 characters"). Cards clamp titles to 3 lines anyway.
- **Only blank lines**: count "0 items", Continue disabled; for a file, the empty-file error.
- **Tabs or commas in lines**: kept as text (no column splitting; CSV is a separate source). If every line has
  the same number of tabs or commas (> 1), an info note suggests "This looks like a table. Import it as CSV
  instead?" with a link to S14.
- **Bullets and numbering** ("- ", "• ", "1. "): kept as typed in this version; the preview shows exactly what is
  imported.
- **Mixed line endings, BOM**: normalized silently.
- **Files over 5 MB**: read in the background with the loading state; above 5,000 lines the limit state applies.
- **Turkish text** (İnce Memed, Kürk Mantolu Madonna): preserved; duplicate checks use locale-aware case folding
  (İ/i, I/ı).
- **Adding to an existing list (S21)**: same screen with app bar "Add items"; the single field is matched to the
  list's title field in S21 mapping.

## Decisions

- **D-S16-1** Plain-text imports have 4 steps (Choose source, Select items, Map fields, Finish): duplicate lines
  are handled in place on S16, so the Review duplicates step is dropped. S19-text is "Step 3 of 4".
- **D-S16-2** Import limit: 5,000 items per import, shared with photos (S18). Extra lines are not imported and the
  primary button names the outcome.
- **D-S16-3** Duplicate lines are kept unless the user removes them (the user's text is never changed silently).
- **D-S16-4** Opening a file loads its text into the same editable box rather than a separate preview, so both
  paths share one screen.
