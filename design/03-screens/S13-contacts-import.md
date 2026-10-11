# S13 Contacts import

Frames: `S13-contacts-import.html`. Generator: `tools/generators/S11-S15-import.py`. Sample data: the 88
`contacts` with `source: "contacts"` (c001–c088) plus 8 service numbers that exist only in Deniz's address
book and are never imported (Apartman Yönetimi, Emlakçı Serdar, Kuaför Nilay, Moda Taksi Durağı, Patiler
Veteriner Kliniği, Su Siparişi, Tesisatçı Hüseyin, Kurye Mehmet) = 96 contacts.

## 1. Purpose and requirements

Import step 2 (Select items) for the Contacts source: choose which contacts become items. One "contact source"
with two selection modes (D-18):

- **Android 16 and lower: full address book.** After the contacts permission (S12), search the whole address
  book and choose. Everything starts selected: SwipeSort's sorting is where decisions happen, so this step
  only removes contacts that clearly don't belong (services, shops) instead of making people tick hundreds of
  boxes (the exact chore the product replaces).
- **Android 17 and later, iOS: system contact picker.** No permission. A short intro says what happens next,
  the system contact picker opens (not drawn), and the picked contacts come back to an in-app **review list**:
  all included, with search, uncheck and "Add more". "All selected" and Select all no longer apply: the person
  already chose in the picker. Duplicates are still handled later (S20).

Covers: SRC-07 (changed by D-18), SRC-26, SRC-13 (multi-value marked, handled in S19), SRC-04–SRC-08 flow,
PLT-07 (web path in S11), PLT-14, PLT-15, PLT-16, PLT-21, SMP-03, GOAL-01, GOAL-03, SUC-04, SCR-13 (changed by
D-18).

## 2. Entry points and exits

| From | How |
| --- | --- |
| S12 contacts explainer (Android 16 and lower) | Permission granted (`S12-contacts` → Continue → system prompt → Allow) |
| S11 / S21 Contacts tile (Android 16 and lower) | Permission already granted |
| S11 / S21 Contacts tile (Android 17 and later) | `S13-picker-intro` |
| S11 / S21 Contacts tile (iOS) | `S13-picker-intro-ios` |

| To | Trigger |
| --- | --- |
| `S19-field-mapping.html#S19-contacts` | "Continue with 88 contacts" (`data-action="continue"` on `S13-select-default` and `S13-picked`) |
| System contact picker (out of scope) | "Choose contacts" (`open-picker`) on the intro; "Add more" (`add-more`) on the review list |
| `S13-picked` / `S13-picked-ios` | The picker returns one or more contacts |
| Intro, unchanged | The picker is cancelled or returns nothing |
| `S14-file-import.html#S14-default` | "Import a CSV instead" (empty address book, read error) |
| `S11-source-picker.html#S11-default` | "Choose another source" (empty address book, picker intro) |
| `S13-close-confirm` dialog → `S08-home.html#S08-default` | Close (`x`) or system back while contacts are selected or picked |
| S12 recovery state | Android 16 and lower: permission revoked while the screen was in the background |

## 3. Layout and components

Import modal: **AppBar (modal)** "Import" (or "Add items" in the S21 context) + **ImportStepper** "Select
items, Step 2 of 5" on every frame of both paths.

**Android 16 and lower (full address book):**

1. **SearchField** (`rounded-full bg-secondary`, 48): placeholder "Search name or number"; clear button
   when filled.
2. **Select-all row** (full-bleed, 56, bottom hairline): tri-state checkbox (checked, mixed, unchecked) +
   "Select all" + count "88 of 96 selected" (`tabular-nums`). While searching it reads "Select all
   results" and acts on the results only.
3. **Hint** (first arrival only, `S13-default`): primary-soft strip "All contacts are selected. Uncheck the
   ones you don't want to sort." Disappears after the first change.
4. **Contact list**: full-bleed **SelectableRow**s (64 min height, checkbox 24, avatar 40 photo or
   initials, name `text-body` truncating, second line `text-body-sm muted`), grouped by first letter with
   sticky section headers (`text-label muted` on `background`). Second line: the single phone number; for
   several numbers `phone` icon + "2 phone numbers" (SRC-13 multi-value, resolved in S19); no phone → the
   email; neither → "No phone or email". Sorted by the device's collation (Turkish: Ç after C, İ after I,
   Ö after O, Ş after S, Ü after U).
5. **Fast-scroll index** (lists over 200 contacts): letters on the right edge (`text-caption muted`,
   current letter `text-primary` semibold), letter bubble (56, `bg-primary`) while scrubbing.
6. **Bottom bar** (top hairline, `bg-background`): primary "Continue with {n} contacts" (`h-14`, full
   width). Disabled with a note when nothing is selected.

**Android 17 and later, iOS (system picker):**

1. **Intro** (`S13-picker-intro`, `S13-picker-intro-ios`): the PermissionExplainer layout without a
   permission: 56 icon circle (`contact`), title "Choose contacts", lead, three promise points, note naming
   the next system step ("No permission needed…"), primary "Choose contacts", ghost "Choose another source".
2. **Review list** (`S13-picked`): SearchField ("Search picked contacts"); a **summary row** in place of
   Select all (56, bottom hairline): count text ("88 contacts picked", or "87 of 88 included" once something is
   unchecked; `role="status"`) and a text button "Add more" (`user-plus`, 48 high) that reopens the picker;
   first-arrival hint strip "These are the contacts you picked. Uncheck any you don't want to sort."; the same
   SelectableRows, letter headers and collation as above, all checked; fast-scroll index above 200 picked;
   bottom bar "Continue with {n} contacts".
3. **Missing-field note** (`S13-picked-missing`): when picked contacts lack a phone number, an info Alert
   ("5 contacts have no phone number") whose "Show them" filter lists only those, with "Show all" to return.

## 4. States

**Android 16 and lower (full address book)**

| Frame | Trigger |
| --- | --- |
| `S13-default` | First arrival: all 96 selected, hint visible |
| `S13-select-default` | After unchecking the 8 service numbers (Apartman Yönetimi visible unchecked): 88 of 96, select-all mixed. Prototype target (Flow 1) |
| `S13-search` | Query "oz": 8 matches, accent-insensitive (Çağrı Özbek, Dr. Hülya Öztürk (dentist), Duygu Özer, Hakan Özkan, İlker Bozkurt, Leyla Özdemir, Ozan Erbil, Özge Kara); matched text semibold |
| `S13-search-empty` | Query "Selim": no matches; "Select all results" disabled |
| `S13-none-selected` | Everything unchecked: Continue disabled, note above it |
| `S13-loading` | Reading the address book (large books take a moment): skeleton rows, "Reading contacts…", search and Continue disabled |
| `S13-empty` | Address book has no contacts |
| `S13-error` | The contacts API failed |
| `S13-close-confirm` | Close or back with a selection: AlertDialog vertically centred (S40 `S40-discard-import`, A-112). Same dialog on the picker path |
| `S13-large` | 2,140 contacts: sticky "M" header, fast-scroll index, letter bubble while scrubbing; the 43-character “Muhammed Abdurrahman Karaosmanoğlu Ertuğrul” truncates |
| `S13-large-text` | 200% font scale: avatars hidden, names wrap, count shortened to "88 of 96" |

**Android 17 and later, iOS (system contact picker)**

| Frame | Trigger |
| --- | --- |
| `S13-picker-intro` | Android 17 and later: Contacts tile. No permission; "Choose contacts" opens the system picker |
| (no frame) picker cancelled | Back on the intro (or on the review list after "Add more"), nothing changed, no message: cancelling is a choice, not an error |
| (no frame) nothing picked | The picker returns zero contacts (iOS "Done" with none selected): same as cancelled |
| `S13-picked` | 88 picked (Deniz's wedding contacts, c001–c088): all included, hint visible. Prototype target |
| `S13-picked-search` | Query "oz" inside the picked contacts; Dr. Hülya Öztürk (dentist) unchecked: "87 of 88 included" |
| `S13-picked-none` | Every picked contact unchecked: "0 of 88 included", Continue disabled with the note |
| `S13-picked-few` | A few picked (3: Elif Şahin, Kerem Acar, Zeynep Kaya) with the "Missed someone?" line under the list |
| `S13-picked-many` | Many picked (312): sticky "M" header and fast-scroll index (above 200, as A-58) |
| `S13-picked-missing` | Fields missing: 5 picked contacts have no phone number (c014, c032, c044, c059, c072); the note filters to them |
| `S13-picked-large-text` | 200% font scale: avatars hidden, names wrap, summary shortened to "88 picked" |
| `S13-picker-intro-ios` | iOS intro: "Next, the iOS contact picker opens: select contacts, then tap Done."; "Choose another source" → `S11-ios` |
| `S13-picked-ios` | iOS review list: page sheet, round selection marks |

**Fallback frames, not in the current design (D-18, A-156)**: `S13-ios` (iOS full contacts access list) and
`S13-ios-limited` (iOS 18 limited access, 40 shared contacts, "Share more contacts"). They apply only if
SwipeSort ever asks iOS for full contacts access; nothing links to them today.

**Offline**: not applicable on either path. Contacts come from the phone (or the system picker); the step
behaves identically without a connection, so there is no offline frame.

## 5. Interactions

- Tap anywhere on a row toggles it (checkbox animates 100 ms; selection haptic `selectionAsync` on
  Android/iOS). Long-press is not used.
- Android 16 and lower, Select all: unchecked/mixed → checks all (in search: all results); checked → unchecks
  all. The count updates with a 250 ms tick (reduced motion: instant).
- Search filters as you type (debounce 150 ms), matching name, phone (digits only, so "0500" finds "+90 500
  …") and email; accents and case are ignored (ç=c, ğ=g, ı=i=İ, ö=o, ş=s, ü=u). Selection survives
  searching and clearing. Clear (`x`) restores the full list at the previous scroll position.
- Fast-scroll index: drag or tap on the strip to jump to a letter; the bubble shows the letter; light
  selection haptic per letter change.
- **Picker path**:
  - "Choose contacts" opens the system picker: Android 17 `Intent.ACTION_PICK_CONTACTS` with multi-select
    and only the fields SwipeSort needs (name, phone numbers, email addresses, photo, plus the other fields
    S19 can map); iOS `CNContactPickerViewController` with multi-select (`didSelectContacts`), which needs
    no permission.
  - Picker access is temporary (D-18): the returned contacts are copied into the import draft at once, so
    leaving the app or rotating the phone never loses them.
  - **Add more** reopens the picker. New contacts are appended (already-picked ones are ignored by contact
    ID) and arrive checked; a snackbar says "Added 12 contacts" (or "Added 9 contacts. 3 were already
    picked."). Cancelling changes nothing.
  - Unchecking keeps the row in place (so it can be checked again); the summary switches to "{n} of {m}
    included".
  - "Show them" on the missing-field note filters the list to those contacts; "Show all" clears the filter.
    Missing values are never an error: the items import with what they have.
  - **Design assumption (Android 17, A-155):** the system picker allows selecting many contacts in one
    session. Bulk selection is unverified (D-18 spike). If the spike shows one tap per contact, D-18 keeps
    `READ_CONTACTS` on 17+ and those phones use the Android 16 frames; this path stays for iOS.
- Continue: pushes S19 with the selected contacts (field mapping detects Name, Phone (multi), Email, Photo
  and any other contact fields present). Nothing is written to the list until Finish.
- Close with a selection (or picked contacts) → "Discard import?" dialog; with nothing selected, close
  immediately.

## 6. Copy

| Element | String |
| --- | --- |
| App bar | "Import"; close label "Close import"; iOS back "Back" (label "Back to Choose source") |
| Stepper | "Select items", "Step 2 of 5" |
| Search | label "Search contacts" (picker path "Search picked contacts"), placeholder "Search name or number", clear "Clear search" |
| Select all (Android 16 and lower) | "Select all"; searching "Select all results" |
| Count (Android 16 and lower) | "88 of 96 selected"; "96 of 96 selected"; "0 of 96 selected"; large text "88 of 96"; "2,140 of 2,140 selected" |
| Hint (Android 16 and lower) | "All contacts are selected. Uncheck the ones you don't want to sort." |
| Row second line | "+90 500 000 97 62"; "2 phone numbers"; email; "No phone or email" |
| Search result header | "8 contacts match “oz”. Accents are ignored."; one result "1 contact matches “oz”. Accents are ignored." |
| No results | "No contacts match “Selim”" / "Check the spelling, or search by phone number." / "Clear search" |
| Continue | "Continue with 88 contacts"; one "Continue with 1 contact"; none "Continue" (disabled) |
| None selected note | "Select at least one contact to continue." (both paths) |
| Loading | "Reading contacts…" |
| Empty | "No contacts on this phone" / "Add contacts in your phone's Contacts app, or import them from a CSV file." / "Choose another source", "Import a CSV instead" |
| Error | "Contacts couldn't be read" / "Your phone didn't return the contacts. Try again, or import a CSV file instead." / "Import a CSV instead", "Try again" |
| Discard dialog | "Discard import?" / "Your selection of 88 contacts will be lost. Nothing has been added to SwipeSort yet." / "Keep importing", "Discard import" |
| Picker intro | title "Choose contacts"; lead "Pick the people you want to sort in your phone's contact picker. You can review them before anything is imported."; points "Only the contacts you pick" / "SwipeSort gets those contacts, not the rest of your address book."; "Stays with your list" / "SwipeSort keeps only the contacts you import. They leave this phone only when the list is backed up or shared." (iOS: "…leave this iPhone only…" and lead "…in your iPhone's contact picker…", A-137); "Your address book isn't changed" / "SwipeSort never edits, adds or deletes contacts. Decisions only change SwipeSort's copy."; buttons "Choose contacts", "Choose another source" |
| Picker intro note | Android "No permission needed. Next, Android's contact picker opens: select as many contacts as you like."; iOS "No permission needed. Next, the iOS contact picker opens: select contacts, then tap Done." |
| Review summary | "88 contacts picked"; one "1 contact picked"; "87 of 88 included"; "0 of 88 included"; large text "88 picked"; "312 contacts picked"; button "Add more" |
| Review hint | "These are the contacts you picked. Uncheck any you don't want to sort." |
| Few picked line | "Missed someone? Add more opens the picker again; contacts you already picked stay." |
| Add more snackbar | "Added 12 contacts"; "Added 9 contacts. 3 were already picked." |
| Missing fields | "5 contacts have no phone number" / "They're imported with the details they have, like an email address. Uncheck them if you only sort people you can call."; list header "Without a phone number"; "Show them"; "Show all" |
| iOS limited (fallback) | "SwipeSort can see 40 contacts" / "You chose which contacts to share with SwipeSort." / "Share more contacts" |
| Screen reader, row | "Ahmet Ateş, 2 phone numbers, selected, checkbox" |
| Screen reader, after select all | "All 96 contacts selected" / "96 contacts unselected" |
| Screen reader, picker returned | "88 contacts picked" (announced once on arrival) |

## 7. Accessibility

- Focus order: Close, title, stepper, search, Select all or the summary row (with Add more), (hint or note),
  list (section headers are headings, so screen-reader users jump by letter with heading navigation),
  Continue.
- Each row is a single `checkbox` element with the name and second line as its label; the visual checkbox
  and avatar are hidden from assistive tech.
- Select all is a tri-state checkbox (`aria-checked="mixed"`). The picker path has no Select all; its summary
  text is `role="status"` and announced politely after each change ("87 of 88 included").
- "Add more" is a button named "Add more contacts" whose result is announced ("Added 12 contacts").
- The fast-scroll index is hidden from screen readers (heading navigation replaces it) and has a 48-wide
  touch strip.
- Disabled Continue is a real disabled button; the explanation above it is full contrast.
- Large text (`S13-large-text`, `S13-picked-large-text`): avatars hide at ≥ 150% so names get the width;
  names and numbers wrap; rows grow; the summary shortens to "88 picked" and Add more stays one line.
- After the system picker closes, focus lands on the summary text so the result is read first.

## 8. Platform differences

- **Android 16 and lower** (reference frames `S13-default` … `S13-large-text`): `READ_CONTACTS` with
  `maxSdkVersion="36"` (D-18), pre-permission explainer in S12, full in-app list.
- **Android 17 and later** (`S13-picker-intro`, `S13-picked*`): the system contact picker, no permission;
  the review list is ours. Expo support for `ACTION_PICK_CONTACTS` is unverified (a small native module may be
  needed; D-18). Bulk selection in the picker is a design assumption until the spike (A-155).
- **iOS** (`S13-picker-intro-ios`, `S13-picked-ios`): `CNContactPickerViewController` (multi-select, Done),
  no permission; page sheet with "Back" (to Choose source) and `x`; round selection marks (iOS convention)
  instead of square checkboxes; swipe-down to dismiss is disabled once contacts are picked
  (`isModalInPresentation`), and `x` shows the discard confirmation as an action sheet.
- **iOS full access (fallback only, D-18)**: `S13-ios` and `S13-ios-limited` show the full list and iOS 18
  limited access ("Share more contacts" opens `ContactAccessPicker`). Kept so the fallback needs no redesign.
- **Web**: contacts import is unavailable (PLT-07); S13 is never reached on web. See S11 web frames.

## 9. Edge cases

- **Long names** truncate in rows (full name in the accessible label and in S19/S26); in large text they
  wrap.
- **Contacts without name** (only a number): shown as the number in the name position, sorted under "#".
- **Missing phone and email** (c014, c032, c044, c059, c072 have no phone): second line shows the email,
  or "No phone or email". On the picker path the missing-field note groups them (`S13-picked-missing`).
- **Several phone numbers** (c002, c009, c012, c027, c046 with 3, c057, c080, c083): marked with "2 phone
  numbers"/"3 phone numbers"; all numbers import into the multi-value Phone field (S19 decides display).
- **Duplicates inside the address book** (same person twice, or picked twice under two entries): both appear
  here; S20 handles them.
- **Contacts already in the list** (S21 context, both paths): rows show a second-line suffix "Already in
  Wedding guests" and start unchecked; checking them adds them as duplicates for S20 to resolve.
- **Very large address books** (2,000+, Android 16 and lower): virtualized list, index strip, search first. Up
  to 10,000 contacts per import (same row limit as files); above that the count reads "10,000 of 12,480
  selected" with the note "SwipeSort imports up to 10,000 contacts at a time." The picker path applies the
  same limit to the picked total ("SwipeSort imports up to 10,000 contacts at a time. The first 10,000 are
  included.").
- **Address book changes while open** (Android 16 and lower): the list refreshes in place on resume;
  selections of deleted contacts are dropped. On the picker path the picked contacts are already copied, so
  later address book changes don't affect this import.
- **Picker returns contacts without the requested fields** (no name): shown as the number or email in the
  name position, as above.
- **Offline**: not relevant (local data).
