# S13 Contacts import

Frames: `S13-contacts-import.html`. Generator: `tools/generators/S11-S15-import.py`. Sample data: the 88
`contacts` with `source: "contacts"` (c001–c088) plus 8 service numbers that exist only in Deniz's address
book and are never imported (Apartman Yönetimi, Emlakçı Serdar, Kuaför Nilay, Moda Taksi Durağı, Patiler
Veteriner Kliniği, Su Siparişi, Tesisatçı Hüseyin, Kurye Mehmet) = 96 contacts.

## 1. Purpose and requirements

Import step 2 (Select items) for the Contacts source: search the address book and choose which contacts
become items. Everything starts selected: SwipeSort's sorting is where decisions happen, so this step only
removes contacts that clearly don't belong (services, shops) instead of making people tick hundreds of
boxes (the exact chore the product replaces).

Covers: SRC-07, SRC-13 (multi-value marked, handled in S19), SRC-04–SRC-08 flow, PLT-07 (web path in S11),
PLT-14, PLT-15, PLT-16, PLT-21, SMP-03, GOAL-01, GOAL-03, SUC-04, SCR-13.

## 2. Entry points and exits

| From | How |
| --- | --- |
| S12 contacts explainer | Permission granted (`S12-contacts` → Continue → system prompt → Allow) |
| S11 Contacts tile | Permission already granted |
| S12 iOS | Limited access → `S13-ios-limited` |

| To | Trigger |
| --- | --- |
| `S19-field-mapping.html#S19-contacts` | "Continue with 88 contacts" (`data-action="continue"` on `S13-select-default`) |
| `S14-file-import.html#S14-default` | "Import a CSV instead" (empty address book, read error) |
| `S11-source-picker.html#S11-default` | "Choose another source" (empty) |
| `S13-close-confirm` dialog → `S08-home.html#S08-default` | Close (`x`) or system back while contacts are selected |
| S12 recovery state | Permission revoked while the screen was in the background |

## 3. Layout and components

Import modal. Top to bottom:

1. **AppBar (modal)** "Import" (or "Add items" in the S21 context) + **ImportStepper** "Select
   items, Step 2 of 5".
2. **SearchField** (`rounded-full bg-secondary`, 48): placeholder "Search name or number"; clear button
   when filled.
3. **Select-all row** (full-bleed, 56, bottom hairline): tri-state checkbox (checked, mixed, unchecked) +
   "Select all" + count "88 of 96 selected" (`tabular-nums`). While searching it reads "Select all
   results" and acts on the results only.
4. **Hint** (first arrival only, `S13-default`): primary-soft strip "All contacts are selected. Uncheck the
   ones you don't want to sort." Disappears after the first change.
5. **Contact list**: full-bleed **SelectableRow**s (64 min height, checkbox 24, avatar 40 photo or
   initials, name `text-body` truncating, second line `text-body-sm muted`), grouped by first letter with
   sticky section headers (`text-label muted` on `background`). Second line: the single phone number; for
   several numbers `phone` icon + "2 phone numbers" (SRC-13 multi-value, resolved in S19); no phone → the
   email; neither → "No phone or email". Sorted by the device's collation (Turkish: Ç after C, İ after I,
   Ö after O, Ş after S, Ü after U).
6. **Fast-scroll index** (lists over 200 contacts): letters on the right edge (`text-caption muted`,
   current letter `text-primary` semibold), letter bubble (56, `bg-primary`) while scrubbing.
7. **Bottom bar** (top hairline, `bg-background`): primary "Continue with {n} contacts" (`h-14`, full
   width). Disabled with a note when nothing is selected.

## 4. States

| Frame | Trigger |
| --- | --- |
| `S13-default` | First arrival: all 96 selected, hint visible |
| `S13-select-default` | After unchecking the 8 service numbers (Apartman Yönetimi visible unchecked): 88 of 96, select-all mixed. Prototype target |
| `S13-search` | Query "oz": 8 matches, accent-insensitive (Çağrı Özbek, Dr. Hülya Öztürk (dentist), Duygu Özer, Hakan Özkan, İlker Bozkurt, Leyla Özdemir, Ozan Erbil, Özge Kara); matched text semibold |
| `S13-search-empty` | Query "Selim": no matches; "Select all results" disabled |
| `S13-none-selected` | Everything unchecked: Continue disabled, note above it |
| `S13-loading` | Reading the address book (large books take a moment): skeleton rows, "Reading contacts…", search and Continue disabled |
| `S13-empty` | Address book has no contacts |
| `S13-error` | The contacts API failed |
| `S13-close-confirm` | Close or back with a selection: AlertDialog vertically centred (S40 `S40-discard-import`, A-112) |
| `S13-large` | 2,140 contacts: sticky "M" header, fast-scroll index, letter bubble while scrubbing; the 43-character “Muhammed Abdurrahman Karaosmanoğlu Ertuğrul” truncates |
| `S13-large-text` | 200% font scale: avatars hidden, names wrap, count shortened to "88 of 96" |
| `S13-ios` | iOS page sheet, round selection marks |
| `S13-ios-limited` | iOS 18 limited contacts access: 40 shared contacts, "Share more contacts" |

**Offline**: not applicable. Contacts are read from the phone; the step behaves identically without a
connection, so there is no offline frame.

## 5. Interactions

- Tap anywhere on a row toggles it (checkbox animates 100 ms; selection haptic `selectionAsync` on
  Android/iOS). Long-press is not used.
- Select all: unchecked/mixed → checks all (in search: all results); checked → unchecks all. The count
  updates with a 250 ms tick (reduced motion: instant).
- Search filters as you type (debounce 150 ms), matching name, phone (digits only, so "0500" finds "+90 500
  …") and email; accents and case are ignored (ç=c, ğ=g, ı=i=İ, ö=o, ş=s, ü=u). Selection survives
  searching and clearing. Clear (`x`) restores the full list at the previous scroll position.
- Fast-scroll index: drag or tap on the strip to jump to a letter; the bubble shows the letter; light
  selection haptic per letter change.
- Continue: pushes S19 with the selected contacts (field mapping detects Name, Phone (multi), Email, Photo
  and any other contact fields present). Nothing is written to the list until Finish.
- Close with a selection → "Discard import?" dialog; with nothing selected, close immediately.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; close label "Close import"; iOS back "Back" (label "Back to Choose source") |
| Stepper | "Select items", "Step 2 of 5" |
| Search | label "Search contacts", placeholder "Search name or number", clear "Clear search" |
| Select all | "Select all"; searching "Select all results" |
| Count | "88 of 96 selected"; "96 of 96 selected"; "0 of 96 selected"; large text "88 of 96"; "2,140 of 2,140 selected"; iOS limited "40 of 40 selected" |
| Hint | "All contacts are selected. Uncheck the ones you don't want to sort." |
| Row second line | "+90 500 000 97 62"; "2 phone numbers"; email; "No phone or email" |
| Search result header | "8 contacts match “oz”. Accents are ignored."; one result "1 contact matches “oz”. Accents are ignored." |
| No results | "No contacts match “Selim”" / "Check the spelling, or search by phone number." / "Clear search" |
| Continue | "Continue with 88 contacts"; one "Continue with 1 contact"; none "Continue" (disabled) |
| None selected note | "Select at least one contact to continue." |
| Loading | "Reading contacts…" |
| Empty | "No contacts on this phone" / "Add contacts in your phone's Contacts app, or import them from a CSV file." / "Choose another source", "Import a CSV instead" |
| Error | "Contacts couldn't be read" / "Your phone didn't return the contacts. Try again, or import a CSV file instead." / "Import a CSV instead", "Try again" |
| Discard dialog | "Discard import?" / "Your selection of 88 contacts will be lost. Nothing has been added to SwipeSort yet." / "Keep importing", "Discard import" |
| iOS limited | "SwipeSort can see 40 contacts" / "You chose which contacts to share with SwipeSort." / "Share more contacts" |
| Screen reader, row | "Ahmet Ateş, 2 phone numbers, selected, checkbox" |
| Screen reader, after select all | "All 96 contacts selected" / "96 contacts unselected" |

## 7. Accessibility

- Focus order: Close, title, stepper, search, Select all, (hint), list (section headers are headings, so
  screen-reader users jump by letter with heading navigation), Continue.
- Each row is a single `checkbox` element with the name and second line as its label; the visual checkbox
  and avatar are hidden from assistive tech.
- Select all is a tri-state checkbox (`aria-checked="mixed"`).
- The count is in the Select all label and announced politely after each change ("88 of 96 selected").
- The fast-scroll index is hidden from screen readers (heading navigation replaces it) and has a 48-wide
  touch strip.
- Disabled Continue is a real disabled button; the explanation above it is full contrast.
- Large text: avatars hide at ≥ 150% so names get the width; names and numbers wrap; rows grow.

## 8. iOS and web differences

- **iOS** (`S13-ios`): page sheet with "Back" (to Choose source) and `x`; round selection marks (iOS convention) instead of square
  checkboxes; swipe-down to dismiss is disabled once anything is selected (`isModalInPresentation`), and
  `x` shows the discard confirmation as an action sheet. The fast-scroll index uses the native
  `SectionList` index on iOS.
- **iOS 18 limited access** (`S13-ios-limited`): only shared contacts appear; an info alert says how many
  and "Share more contacts" opens the system `ContactAccessPicker`; new ones are added selected.
- **Web**: contacts import is unavailable (PLT-07); S13 is never reached on web. See S11 web frames.

## 9. Edge cases

- **Long names** truncate in rows (full name in the accessible label and in S19/S26); in large text they
  wrap.
- **Contacts without name** (only a number): shown as the number in the name position, sorted under "#".
- **Missing phone and email** (c014, c032, c044, c059, c072 have no phone): second line shows the email,
  or "No phone or email".
- **Several phone numbers** (c002, c009, c012, c027, c046 with 3, c057, c080, c083): marked with "2 phone
  numbers"/"3 phone numbers"; all numbers import into the multi-value Phone field (S19 decides display).
- **Duplicates inside the address book** (same person twice): both appear here; S20 handles them.
- **Contacts already in the list** (S21 context): rows show a second-line suffix "Already in Wedding
  guests" and start unchecked; checking them adds them as duplicates for S20 to resolve.
- **Very large address books** (2,000+): virtualized list, index strip, search first. Up to 10,000
  contacts per import (same row limit as files); above that the count reads "10,000 of 12,480 selected"
  with the note "SwipeSort imports up to 10,000 contacts at a time."
- **Address book changes while open**: the list refreshes in place on resume; selections of deleted
  contacts are dropped.
- **Offline**: not relevant (local data).
