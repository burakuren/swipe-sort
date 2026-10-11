# SwipeSort design principles

The rules every screen follows. Written for designers, subagents and QA; this file stands on its own.
Where it is silent, follow `00-brief/brief.md`; where the brief is silent, record a decision in
`00-brief/assumptions.md`.

## 1. What we are designing

SwipeSort turns any list into a deck of cards. People look at one item at a time and decide: swipe right to
**Accept**, left to **Reject**, up for **Maybe**. Typical lists: guests, job candidates, products, trips,
apartments, tasks, ideas. People often decide together (a couple, a family, a small team).

The product's emotional job: make a long, tiring narrowing-down task feel light and safe. Users must feel
fast while sorting, in control of their data, and fairly heard when deciding with others.

## 2. Direction: calm surroundings, one bold object

- **The card is the hero.** It is the largest, roundest, most elevated object in the app, and the only
  place that moves boldly. Everything else is quiet: neutral surfaces, few borders, no decoration.
- **Content is the star, chrome steps back.** Users' names, photos and prices carry the color and
  personality. The interface itself uses neutrals plus one accent.
- **One accent color: ink indigo** (`primary`). It marks the main action on a screen, selection, focus and
  links. Never use it decoratively. At most one filled `primary` button per screen.
- **Decision colors are semantic, not decorative.** Green, rose red and amber only ever mean Accept, Reject
  and Maybe. Do not use them for unrelated success, error or warning states (errors use `destructive`;
  general success uses neutral copy with an icon).
- **No decorative gradients**, no glassmorphism, no glow, no illustrations-as-filler. Photos in sample data
  may contain natural gradients; UI surfaces never do.

## 3. Surface hierarchy (radius and elevation vary on purpose)

Never style everything as identical rounded cards with the same shadow. Each surface type has its own
treatment:

| Surface | Use | Radius | Elevation | Background |
| --- | --- | --- | --- | --- |
| Canvas | Screen background | none | none | `background` |
| Group | A set of rows (settings, members, fields) | `rounded-group` 16 | none; separated by background change, no border in light, hairline `border` in dark | `card` |
| Row | Item inside a group or a full-bleed list | 0 (rows never have their own radius) | none; `border` hairline divider inset 16 | inherits |
| Tile | Tappable choice in a grid (source tiles, templates) | `rounded-tile` 16 | none at rest; `border` 1px; selected = 2px `ring`/`primary` border | `card` |
| Control | Buttons, inputs, selects | `rounded-control` 12 (chips and icon buttons: `rounded-full`) | none | per variant |
| Sheet | Bottom sheets (notes, filters, actions) | `rounded-t-sheet` 24 | `shadow-sheet` | `popover` |
| Dialog | Confirmations | `rounded-dialog` 24 | `shadow-dialog` | `popover` |
| Snackbar | Transient feedback | `rounded-control` 12 | `shadow-overlay` | `foreground` (inverse) |
| **Sort card** | The card being decided | **`rounded-hero` 28** | **`shadow-hero`, `shadow-hero-drag` while dragging** | `card` |

Rules:
- Flat is the default. A shadow means "this floats above the page and can move or be dismissed".
- Lists of items (results, contacts) are full-bleed rows with dividers, not stacks of cards.
- Do not nest groups inside groups or cards inside cards.
- Dark mode: elevation comes from lighter surfaces (`card` > `background`) plus hairline borders; shadows
  only for overlays and the sort card.

## 4. Color usage

Tokens live in `tokens.json` → `tokens.css`. Use only Tailwind classes mapped to tokens (`bg-card`,
`text-muted-foreground`, `bg-accept-soft`…). No hex, rgb or arbitrary color values in screens.

- `background` / `foreground`: canvas and primary text.
- `card`: groups, tiles, sort card. `popover`: sheets, dialogs, menus.
- `muted` / `muted-foreground`: secondary text, placeholders, inactive icons, skeletons.
- `secondary`: secondary button fill and segmented-control track.
- `accent` / `accent-foreground` (shadcn meaning): **hover and pressed backgrounds** of rows and ghost
  buttons. It is not the brand accent — the brand accent is `primary`.
- `primary`, `primary-soft`, `primary-soft-foreground`: main action, selection, links, focus ring, the
  current-step marker, info notices.
- `destructive`: delete, remove, discard, errors. Stronger and more saturated than `reject` on purpose:
  losing data is alarming; rejecting an item is not.
- `accept`, `reject`, `maybe` (+ `-foreground`, `-soft`, `-soft-foreground`): decisions only.
- `conflict` / `conflict-foreground`: inverted neutral chip for list status Conflict.
- `scrim`: modal backdrop, always with opacity (`bg-scrim/50`).

Amber (`maybe`) is a light color: in light mode a `bg-maybe` fill always carries `text-maybe-foreground`
(dark) content; never rely on the edge of an amber fill against the page.

## 5. The decision language

Every decision appears as **icon + label + color**, never color alone.

| Decision | Icon (Lucide) | Label | Solid | Soft (chips, tints) |
| --- | --- | --- | --- | --- |
| Accept | `check` | Accept / Accepted | `bg-accept text-accept-foreground` | `bg-accept-soft text-accept-soft-foreground` |
| Reject | `x` | Reject / Rejected | `bg-reject text-reject-foreground` | `bg-reject-soft text-reject-soft-foreground` |
| Maybe | `circle-help` | Maybe | `bg-maybe text-maybe-foreground` | `bg-maybe-soft text-maybe-soft-foreground` |
| No decision yet | `circle-dashed` | Not decided | `bg-muted text-muted-foreground` | — |

Labels: buttons use the verb ("Accept"); badges on decided items use the state ("Accepted", "Rejected",
"Maybe"). The order is always **Reject · Maybe · Accept** left to right, mirroring the gestures (left, up,
right).

List status on shared lists (separate from decisions):

| Status | Icon | Treatment |
| --- | --- | --- |
| Agreed | `check-check` | Outline chip, label "Agreed"; the final decision badge sits next to it |
| Pending | `clock` | Muted chip, "Pending" + who is missing ("Waiting for Selin") |
| Conflict | `git-compare-arrows` | Inverted `conflict` chip, "Conflict" |

Who decided what: a row of member avatars, each with a small decision badge (icon on the decision color)
at the bottom-right; with a text alternative "Deniz: Accept, Mert: Reject, Selin: not decided".

## 6. Typography

- **Inter** (variable), one family for everything. Turkish characters ğ ş ı İ are fully supported.
  `font-feature-settings: "cv11"` (single-storey a) gives a softer, friendlier texture without a second face.
- Use the named scale only: `text-display`, `text-card-title`, `text-title-1/2/3`, `text-body-lg`,
  `text-body`, `text-body-sm`, `text-label`, `text-label-lg`, `text-caption`. Minimum body size 16; 14 for
  secondary text; 12 only for captions and badges.
- Numbers that update (counts, progress) use `tabular-nums`.
- Sentence case everywhere: titles, buttons, tabs, labels. **No all-caps labels, no tracked-out eyebrows.**
- No single-word emphasis in headings (no one word bold, italic or colored).
- Line length ≤ 64ch for any paragraph (`max-w-prose`).
- Left-align text on content screens. Center only on single-purpose moments: splash, empty states,
  onboarding steps, round summary.

## 7. Layout and spacing

- 4 dp grid (Tailwind scale). Horizontal gutter `px-gutter` (20). Section spacing 24–32.
- App bar height 64 (`h-app-bar`): back/close icon button (48 target), title `text-title-3`, up to two
  trailing icon buttons. Large-title variant for top-level tabs: `text-title-1` below the bar.
- Bottom navigation (Home, Activity, Settings): 80 high (`h-bottom-nav`), icon + label, active item uses
  `primary-soft` pill behind the icon (Material 3 pattern).
- Primary actions sit at the bottom of the screen (thumb zone), full width, `h-12` minimum.
- Every tappable element has a 48×48 dp target minimum (`min-h-touch min-w-touch`), even when the visible
  icon is 20–24.
- Respect the frame: content must never overflow the 412×915 frame; scrolling content is shown cut by the
  bottom edge or the bottom bar, never by overlapping text.

## 8. Icons and imagery

- Keyboard hints (`kbd`) use Inter like all other text (no monospace).
- Lucide only: `<i class="i-lucide-<name> size-5" aria-hidden="true"></i>`; 20 in rows and buttons, 24 in
  app bars and navigation, 16 inside chips. Stroke icons only; no filled icon sets.
- Icon-only buttons always have `aria-label`.
- Images come from `02-data/images` (generated, no text). Avatars without a photo show initials on
  `bg-muted`. Missing product or photo images show a neutral placeholder with an `image-off` icon.
- Never put text inside images.

## 9. Motion (summary; details in motion.md)

- Motion answers the user's action; nothing animates on its own except loading indicators.
- The swipe is the single orchestrated moment: tilt, tint, label, commit, the next card rising, the
  count ticking up. Everything else uses short standard transitions (150–300 ms).
- Every animation has a reduced-motion alternative (cross-fade or instant).

## 10. Copy

Voice: plain, calm, helpful; like a well-organized friend. Never cute, never alarmed.

- **Plain verbs, sentence case, no filler.** "Import contacts", not "Let's get started importing!".
- **Name things the way users see them** and use the glossary exactly: List, Item, Field, Source, Card
  template, Round, Accept, Reject, Maybe, Decided, My decision, Final decision, Conflict, Owner, Decision
  Maker, Collaborator, Member.
- **Never use domain words for items in UI**: no "guest", "invitee", "wedding", "attendee", "RSVP",
  "candidate" (except as a template name), "product" (except as a template name). Sample data and
  template names may use domain language.
- **An action keeps its name through the flow**:

  | Button | Progress | Success | Failure |
  | --- | --- | --- | --- |
  | Export | Exporting… | Exported to Google Sheets | Couldn't export. … |
  | Import | Importing 88 items… | Imported 88 items | Imported 84 of 88 items |
  | Invite | — | Invite link copied | — |
  | Start round | — | Round 2 started | — |
  | Resolve all | Resolving… | Resolved 12 conflicts | — |
  | Undo | — | Undid Accept on Ayşe Demir | — |
  | Delete list | — | List deleted (with Undo) | — |
  | Back up | Backing up… | Backed up | Backup paused |

- **Buttons say what happens**: "Delete list", not "OK"; "Keep editing" / "Discard changes", not
  "Cancel" / "Yes". Destructive confirmations name the object and the consequence.
- **No arrows or ornaments appended to button or link text** (no "Continue →").
- **No middle-dot meta strings in UI** ("100 items · Shared · 2d ago" is out). Use separate, labeled pieces
  of text, or a comma when it reads naturally. (Frame labels on the mockup canvas are presentation, not UI,
  and use the brief's "S25 · State · theme" format.)
- **Numbers**: "76 / 100 decided" (thin spaces not needed; regular spaces around the slash). Counts with
  their noun: "12 conflicts", "1 conflict".
- **Dates**: relative within a week ("Yesterday", "3 days ago"), then "Oct 2", then "Oct 2, 2025".

### Errors

Pattern: **what happened. How to fix it.** No apology, no blame, no "Oops", no error codes in the main text.

- "This file can't be read. Save it as .csv or .xlsx and try again."
- "No connection. Your decisions are saved on this phone and will sync when you're back online."
- "Google Sheets didn't respond. Check your connection and try again."
- Error actions are specific: "Try again", "Choose another file", "Open settings".

### Empty states

Pattern: one short sentence saying what will be here, one primary action that creates it. Optional icon
(Lucide, 32, `text-muted-foreground`), no illustrations.

- "No lists yet. Import a list or try a sample to see how sorting works." → **Import a list**, secondary
  **Try a sample list**.
- "Nothing in Maybe. Items you swipe up will wait here."

### Confirmations

Title = the action as a question with the object: "Delete “Desk setup”?". Body = the consequence in one or
two sentences, including what is not affected ("Your original file isn't changed."). Buttons: specific
destructive verb (destructive variant) + "Cancel".

## 11. Accessibility floor

- WCAG 2.1 AA contrast: 4.5:1 text, 3:1 large text and meaningful non-text (icons, focus rings, input
  borders where they identify the control). Token pairs are checked by `npm run build:tokens`
  (`01-foundations/contrast.md`).
- 48×48 dp touch targets minimum.
- Every gesture has a visible button and a screen-reader action (custom accessibility actions "Accept",
  "Reject", "Maybe", "Undo" on the card).
- Every control has an accessible name; icon-only buttons use `aria-label`; decorative icons
  `aria-hidden="true"`.
- Color is never the only signal (decisions: icon + label; status: icon + label; errors: icon + text).
- Disabled controls use the real `disabled` attribute (or `aria-disabled` on a role) and may use
  `opacity-50`; text that explains why something is unavailable is never dimmed below AA.
- Focus order follows reading order; visible focus ring (`ring-2 ring-ring ring-offset-2`).
- Large text: layouts reflow at 200% font scale; rows grow in height, labels wrap rather than truncate
  where the label is the information (truncate only secondary metadata). Key screens show a large-text
  frame.
- Reduced motion: every animation in `motion.md` has a fallback.

## 12. Text expansion (Turkish and beyond)

- Design every label to survive +40% length. Buttons grow in width or wrap to two lines; never fixed-width
  buttons with single-line truncation.
- Bottom navigation labels: short nouns, allow 2 lines at large text.
- Don't put labels side by side if +40% would collide; stack instead.
- Examples to test: "Accept" → "Kabul et", "Start sorting" → "Sıralamaya başla", "Decision Maker" →
  "Karar verici".

## 13. Platform patterns

- **Android (reference)**: Material 3 behavior — system back closes sheets/dialogs first, then pops the
  stack; snackbars above bottom navigation; bottom sheets with drag handle; predictive back.
- **iOS variant** (393×852 frame) when behavior differs: back chevron with previous title and edge-swipe
  back; sheets as iOS page sheets with grabber; Sign in with Apple first in the sign-in button stack;
  action sheets for destructive menus; no FAB, primary actions in the nav bar or at the bottom.
- **Web (mobile browser)**: same layout as Android; no system bars in the frame; browser back = app back.
- **Web (desktop)**: phone layout centered in a 412-wide column on a `muted` page (see `.desktop` frame);
  keyboard hints appear only here (`kbd` chips: ← Reject, ↑ Maybe, → Accept, Z Undo).
- **Web-unavailable features** (contacts import, gallery picker, haptics, push notifications): the control
  stays visible but unavailable: title and icon in `text-muted-foreground`, dashed border on tiles, the
  control itself (switch, checkbox) at `opacity-50`, a `monitor-smartphone` icon, a one-line reason
  ("Contacts import needs the Android or iOS app.") and a link "Get the app". Never dim the explanation
  text with opacity: it must stay readable (AA contrast). Tapping the tile opens a sheet with the reason and
  "Get the app". Push becomes in-app notifications only. (The Photos source and its web "Upload photos"
  tile are out of scope for now, D-32.)

## 14. Mockup conventions (for every screen file)

- Page skeleton: `<html lang="en" data-theme="light">`, `<title>`, `<link rel="stylesheet"
  href="../assets/css/app.css">`, `<body class="mock-page">`, a `<header class="mock-doc">` with the
  screen name and a link to its spec, then `<main class="mock-canvas">` with frames.
- Frame: `<figure class="frame" data-frame="S25-default" id="S25-default">` → `<figcaption
  class="frame-label">S25 · Default · <span class="theme-name"></span></figcaption>` → `<div
  class="phone">` (or `phone-ios`, `desktop`) → `sysbar-top` (aria-hidden), `.screen`, `sysbar-nav`.
  Frame IDs are unique across all files: `S<nn>-<state>`, lowercase, hyphenated.
- Group frames into labeled sections with `<h2 class="mock-section">` when a file has many frames.
- Web mobile frames use `.phone` without system bars; desktop frames use `.desktop` with
  `.desktop-chrome` and `.desktop-column`.
- Prototype links: `<a href="S13-contacts-import.html#S13-select-default" data-action="continue">`.
  Opening a file with `#frame-id` shows only that frame (prototype mode).
- No inline styles, no `<style>` blocks with colors or sizes, no arbitrary Tailwind values except the
  sizes already provided by the mockup plugin and tokens. If something needs a value that does not exist,
  propose a token.
- Use real records from `02-data/sample-data.json`; refer to them by ID in the spec.

## 15. Template tells to avoid

QA rejects a frame that shows any of these:

1. Identical rounded cards with the same soft shadow for every kind of content.
2. One border radius on everything regardless of hierarchy.
3. Gradient washes, glows or decorative blobs.
4. All-caps or tracked-out eyebrow labels above headings.
5. Middle-dot meta strings in UI ("A · B · C").
6. "WORD — fragment" labels with spaced em dashes.
7. `→` appended to buttons or links.
8. Monospace for small data labels.
9. Big-number-with-small-label stat blocks used as decoration (numbers only where they inform a decision,
   e.g. round summary counts).
10. Numbered markers (01 / 02) on content that isn't a sequence (the import stepper is a real sequence).
11. Hover/entrance animations on every element.
12. Cute or apologetic copy ("Oops!", "Sorry!", "Whoops", exclamation marks in errors).
13. Placeholder content ("Lorem ipsum", "John Doe", "Item 1").
14. More than one filled `primary` button in a view.

## 16. Self-critique with screenshots (required before reporting)

After `npm run build:css` and `npm run shots -- <your IDs>`, open every PNG (light and dark) and check:

- [ ] Nothing overflows the frame, clips, overlaps or truncates the main information.
- [ ] The sort card (where present) is clearly the hero; everything else is quieter.
- [ ] Radius and elevation follow the surface table; not everything is a card.
- [ ] Exactly one accent use for the main action; decision colors only for decisions.
- [ ] Every decision/status has icon + label.
- [ ] Contrast looks right in dark mode; no washed-out text on `muted`.
- [ ] Touch targets ≥ 48; buttons at the bottom are reachable.
- [ ] Copy follows section 10; no forbidden domain words; action names match the flow.
- [ ] Empty, loading, error, offline and web-unavailable states exist where they apply.
- [ ] None of the template tells in section 15.
- [ ] Remove one accessory: is there an element that could go?
