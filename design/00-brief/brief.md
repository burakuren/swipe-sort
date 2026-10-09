<role>
You are the lead product designer and design orchestrator for a new app,
SwipeSort. You have senior experience in consumer mobile apps, gesture-driven
interfaces and collaborative tools. You will produce the complete design of the
product in this repository, coordinating subagents to do so.
</role>

<mission>
Produce a complete, implementation-ready design of SwipeSort: every screen,
every state and every feature in this brief, as HTML mockups with written specs.

The purpose of this phase is to let the founder see and judge every page of the
product before development starts. Afterwards, an AI coding agent will build
the app from your design with Expo, React Native and TypeScript. That agent
should never have to invent a screen, a flow or a feature behavior. It may only
fill in platform-default details listed in <out_of_scope>.

A missing screen or an undesigned feature is the worst possible outcome. Polish
on secondary screens matters less than completeness.

You are running in auto mode. Never stop to ask questions or wait for
confirmation; this brief is the confirmed client brief. When it is ambiguous,
make the decision a strong product designer would make, record it in the
assumptions file, and continue.

The environment is already set up: read CLAUDE.md first and use its npm
scripts (build:css, shots, a11y, flows) and conventions.
</mission>

<context>
SwipeSort turns any list into a deck of cards that users sort with swipe
gestures: right to Accept, left to Reject, up for Maybe.

The idea comes from a real need: building a guest list out of hundreds of
phone contacts. Scrolling a long list and
ticking checkboxes is slow, tiring and error-prone; looking at one item at a
time and making a quick decision is faster and more enjoyable. SwipeSort
generalizes this to any list: guests, job candidates, product shortlists,
photos to clean up, apartments, tasks, ideas.

Target users: everyday people with a list to narrow down, often deciding
together with a partner, family members or a team.
</context>

<design_goals>
In priority order. When goals conflict, the higher one wins.
1. Sorting must feel effortless and satisfying. The sorting screen is the heart
   of the product and deserves the most craft.
2. The app must work for any kind of list, not only guests.
3. Users must never fear losing or damaging their data.
4. Group decisions must be fair and transparent, and disagreements easy to
   resolve.
5. The design must scale: new data sources and features should fit in without
   redesign.
</design_goals>

<platforms>
- Android phones first, then iPhone. Design every screen in an Android phone
  frame (412x915). Where iOS differs meaningfully (navigation, back gesture,
  sheets, sign-in options), add an iOS variant frame and describe the
  difference in the spec.
- Web app: the same phone layout runs in mobile browsers. On desktop browsers,
  show the phone layout centered on the page; do not design wide layouts. On
  desktop, arrow keys sort (Right = Accept, Left = Reject, Up = Maybe,
  Z = Undo); show these hints only on web.
- Some features are not available on web: phone contacts import, the photo
  gallery picker (web uses photo file upload instead), haptics and push
  notifications (web uses in-app notifications). Design how unavailable
  features appear on web: a disabled state with a short explanation and a link
  to get the Android or iOS app.
- Phones only. No tablet or desktop layouts in this phase.
- Accessibility: WCAG 2.1 AA contrast, minimum 48x48 dp touch targets, screen
  reader labels, support for large text sizes, and a reduced-motion
  alternative for every animation. Every swipe must have a visible button
  equivalent and a screen-reader action.
- Copy is English only, but layouts must tolerate text 30–40% longer, because
  other languages (starting with Turkish) will be added later. Never put text
  inside images.
- Light and dark mode for every screen.
</platforms>

<design_stack>
Design with the same building blocks the app will be built with, so every
value in the mockups maps directly to code.
- Visual language: shadcn/ui style. Neutral, clean and token-driven, with one
  accent color.
- Component reference: React Native Reusables (the React Native port of
  shadcn/ui). Name and structure components the way they exist there; when a
  needed component does not exist, design it in the same style.
- Styling: Tailwind CSS, mirroring NativeWind. Mockups use Tailwind utility
  classes and CSS-variable tokens in the shadcn convention (background,
  foreground, primary, muted, accent, destructive, border, ring, etc.), extended
  with SwipeSort tokens for Accept, Reject and Maybe.
- Platform behavior: Material 3 for Android patterns (navigation, back
  behavior, bottom sheets, snackbars, system bars). Apple HIG for iOS
  differences. These guide behavior, not visual style.
- Icons: Lucide.
- Typography: Inter by default. During the Phase 2 exploration you may choose
  another open-licensed sans-serif family if it clearly serves the calm and
  clean direction better. Any choice must support Turkish characters
  (ğ, ş, ı, İ) and be available for both React Native and web. Document the
  choice.
- Motion reference: Material 3 motion durations and easing; gestures will be
  built with react-native-gesture-handler and Reanimated, so specify values
  those libraries can use.
</design_stack>

<visual_direction>
Calm and clean: generous whitespace, restrained color, clear hierarchy, quiet
surfaces, one accent color. The cards and the user's content are the stars;
the interface steps back.

Spend boldness in one place: the card and the moment of swiping it. Keep
everything around it quiet and disciplined.

Avoid the look of a stock component kit. Corner radius and elevation vary with
hierarchy (the sorting card is not styled like a settings row), and surfaces
are not all identical rounded cards with the same soft shadow. Do not use
decorative gradients.

Decision colors: green for Accept, red for Reject and amber for Maybe, always
paired with an icon (check, cross, question mark) and a label, so color is
never the only signal. Keep the red calm rather than alarming, since users
often reject people they care about.

Copy: plain verbs, sentence case, no filler. An action keeps the same name
through its whole flow (an "Export" button leads to an "Exported" message).
Errors say what happened and how to fix it, without apologizing. Empty screens
invite the next action.

Before designing the full app, explore two or three variations of the sorting
screen within this direction (e.g., accent color, card style, density, type).
Pick the strongest, keep the others in the design folder, and document the
reasoning in assumptions.md.
</visual_direction>

<terminology>
Use exactly these terms in the UI and specs.
- List: a collection of items to sort
- Item: a single record (a contact, a spreadsheet row, a photo)
- Field: a piece of information on an item (name, phone, price…)
- Source: where items come from
- Card template: which fields appear on a card and how they are laid out
- Round: one sorting pass over a set of items
- Decisions: Accept, Reject, Maybe
- Decided: an item that has a decision
- My decision: the current user's decision on an item
- Final decision: the list-level decision on a shared list (see <decision_model>)
- Conflict: an item that members of a shared list decided differently
- Owner, Decision Maker, Collaborator: roles on a shared list
- Member: anyone on a shared list, whatever their role

Never use domain-specific words such as "guest" or "invitee" for items in the
UI. The app is general-purpose, and domain words would make it feel like a
wedding app. Domain language may appear only in sample data and template names.
</terminology>

<decision_model>
This model must be visible and consistent across all screens.
- Solo list: my decision is the final decision.
- Shared list: every member decides every item independently. Each item has a
  list status:
  - Pending: not every member has decided it yet
  - Agreed: every member chose the same decision; this becomes the final
    decision
  - Conflict: members chose differently (Maybe vs. Accept counts as a
    difference)
- Conflict rule, chosen by the Owner:
  1. Everyone must agree: conflicts stay open until members change their
     decisions to match. Members can review conflicts and see others'
     decisions.
  2. Majority decides: the majority decision becomes final; ties go to the
     Decision Maker, or stay as conflicts if there is none.
  3. Decision Maker decides: every conflict is resolved by the Decision Maker,
     whose resolution is final.
- The Owner assigns the Decision Maker role to any member (including
  themselves) with a single switch on the members screen.
- Bulk resolve: the Decision Maker applies their own earlier decisions to all
  open conflicts in the current round in one action. Conflicts on items the
  Decision Maker never decided stay open, and the confirmation summary shows
  how many.
- Progress: while sorting, show the user's own progress ("76 / 100 decided")
  and counts per decision. On shared lists, the list overview also shows list
  progress: items Agreed, Pending and in Conflict.
- Rounds on shared lists are started by the Owner and apply to every member.
- A member who joins mid-round sorts all items of the current round.
- When a member is removed, the Owner chooses in the confirmation dialog
  whether to keep or discard that member's decisions.
- Notes are visible to all members by default; a note can be marked private,
  and private notes are visibly distinguished.
</decision_model>

<features>

<accounts>
- No account is needed to use the app alone. Lists are stored on the device,
  and a subtle indicator shows they are not backed up.
- Signing in is required to share a list or back up lists. When a guest user
  tries either, show a sign-in prompt explaining why, and after sign-in move
  their existing lists to the account.
- Sign in with Google and email on all platforms; add Sign in with Apple on
  iOS. Include forgot password.
</accounts>

<data_sources>
Sources at launch: phone contacts, CSV, Excel (.xlsx), plain text (paste or
.txt, one item per line), manual entry, Google Sheets, and photos (each photo
becomes a card). See <platforms> for web availability.

More sources will be added later. Design the source picker as a modular
pattern (e.g., a grid of source tiles that all lead into the same import flow
structure) so a new source is one more tile and reuses the same steps.

Import flow:
1. Choose a source. Before any system permission prompt (contacts, photos), show
   a pre-permission screen explaining why access is needed and how the data is
   used. Design the "permission denied" recovery state too.
2. Select which items to include: search and multi-select contacts, pick a file
   or a sheet tab, select photos.
3. Map fields: show detected fields with sample values; let users rename them,
   hide them, set their type (text, number, phone, email, date, link, image),
   and choose the title field. Handle multi-value fields such as contacts with
   several phone numbers.
4. Review duplicates: when items look duplicated (common when combining
   sources), let users merge, keep both or skip.
5. Choose a card template.
6. Name the list and start sorting.

A list can combine several sources, and items can be added to an existing list
later. Design import errors: unreadable file, empty file, too many columns,
Google connection failure, partial import.
</data_sources>

<card_templates>
- A library of ready-made templates: Person, Product, Photo, Task, Candidate,
  Generic.
- A template editor where users choose which fields appear and arrange their
  layout (title, subtitle, image area, field rows, tags). Fonts and colors are
  not customizable in this version.
- A live preview using real items from the current list, including how the
  card handles missing values and very long text.
- Custom templates can be saved, renamed, duplicated, deleted and reused across
  lists. The template can be changed for a list at any time.
</card_templates>

<rounds>
- Starting a round: choose which items to include (all, the Maybe pile,
  accepted items to narrow down further, or a custom selection, e.g., filtered
  by a field) and the card order (original, shuffled, or sorted by a field).
- Round history per list, with each round's results.
</rounds>

<sorting_screen>
The most important screen in the app.
- A card stack: the current card on top, the next card visible behind it.
- Gestures: swipe right = Accept, left = Reject, up = Maybe.
- While dragging, show which decision will be made (card tilt, color tint, icon
  and label). The decision commits only past a threshold; releasing earlier
  snaps the card back. Commit with haptic feedback. Specify thresholds,
  velocities and animation timings in the motion spec.
- Visible Reject, Maybe, Accept and Undo buttons.
- Undo the last decision at any time; multiple undos step back in order.
- Always-visible progress ("76 / 100 decided") plus a compact count for each
  decision.
- Add or edit a note on the current card without leaving the screen.
- Tap a card to open item details and edit its fields on the spot.
- On shared lists, members can choose whether to see others' decisions on the
  card before deciding (off by default, to avoid bias).
- Progress saves automatically; users can leave and resume exactly where they
  stopped. Sorting works offline and syncs later.
- First-time coach marks teaching the gestures.
- At the end of a round, a summary screen with next actions: review results,
  re-sort Maybe, start a new round, export.
</sorting_screen>

<data_safety>
- The original source is never changed automatically.
- Edits and notes live in SwipeSort's working copy; edited fields are visibly
  marked and can be reverted to the original value.
- At export, users choose the output: a new file with added "Decision" and
  "Notes" columns, or, for Google Sheets, new columns in the original sheet or
  a new tab, only after an explicit confirmation.
</data_safety>

<results>
- Results with segments for Accept, Reject, Maybe and Conflicts, each with
  counts, search, filters and sorting. On shared lists, a toggle between final
  decisions and my decisions.
- Any decision can be changed from results.
</results>

<collaboration>
- Invite any number of people via link or the system share sheet; set their
  role while inviting.
- Opening an invite link: in the app if installed on Android or iOS; otherwise
  in the web app, where the person can sign in, join and sort right away
  without installing anything, with an option to get the app.
- Joining a list: see who invited you, the list, your role, and start sorting.
- Members screen: see each member's progress, change roles, assign the
  Decision Maker, remove a member, transfer ownership, leave a list.
- Conflict rule settings (see <decision_model>).
- Conflict resolution: one by one (swipe through conflicts with each member's
  decision and notes on the card) and bulk resolve (with confirmation and
  summary).
- Every item shows who decided what.
- Activity feed and notifications for: someone joined, someone finished
  sorting, new conflicts, conflicts resolved, a new round started, a role
  changed. Include notification preferences and a pre-permission screen for
  push notifications.
</collaboration>

<export>
- Export to CSV, Excel or Google Sheets, or share a plain-text summary.
- Export everything or only Accept, Reject, Maybe or Conflict items.
- Include decisions, notes and, for shared lists, each member's decision.
- Show export success, failure and Google write confirmation.
</export>

<settings>
Profile, connected accounts (Google), backup status, theme (system, light,
dark), haptics, notification preferences, language (English only for now),
privacy information, help and feedback, about, sign out, and account deletion
(required by both app stores).
</settings>

<branding>
App name: SwipeSort. Create a simple logo, wordmark and app icon (including an
Android adaptive icon) that work at small sizes, in light and dark contexts.
</branding>

</features>

<screens>
Design every screen below with all applicable states: default, empty, loading,
error, offline, web-unavailable where relevant, and any screen-specific states
named in <features>. IDs are used for file names and traceability.

A. Onboarding and account
S01 Splash
S02 Onboarding with an interactive gesture demo
S03 Sign up / sign in (Google, email; Apple on iOS)
S04 Forgot password
S05 Sign-in prompt from guest mode (sharing or backup) and moving lists to
    the account
S06 Settings and all its sub-pages
S07 Profile, connected accounts and account deletion

B. Lists
S08 Home (including first-run empty state with an option to try a sample list,
    and the not-backed-up indicator)
S09 List overview (solo and shared variants)
S10 List management: rename, duplicate, archive, delete, leave; archived lists

C. Import
S11 Source picker (including web-unavailable tiles)
S12 Pre-permission explainers (contacts, photos, notifications) and
    permission-denied recovery
S13 Contacts import
S14 File import (CSV and Excel)
S15 Google Sheets connection and sheet/tab selection
S16 Plain-text import
S17 Manual entry
S18 Photos import (gallery on mobile, file upload on web)
S19 Field mapping
S20 Duplicate review
S21 Add items to an existing list

D. Templates
S22 Template library
S23 Template editor with live preview

E. Sorting
S24 Start a round (item selection and card order)
S25 Sorting screen (including coach marks, note entry, undo, offline, and the
    web version with keyboard hints)
S26 Item detail, editing and notes
S27 Round summary

F. Results
S28 Results
S29 Filter and sort sheet
S30 Round history

G. Collaboration
S31 Invite (sender side)
S32 Opening an invite link (app installed, and web app in a browser)
S33 Join a list
S34 Members and roles
S35 Conflict rule settings
S36 Conflicts: one-by-one resolution
S37 Bulk resolve: confirmation and summary
S38 Activity and notifications

H. Export
S39 Export flow

I. Global patterns
S40 Dialogs (all destructive confirmations), snackbars, offline banner, sync
    notice, generic error and not-found screens, and the desktop-browser frame
    (phone layout centered)
</screens>

<out_of_scope>
Do not design these; the coding agent will use platform defaults:
- Native system dialogs themselves (permission prompts, share sheet, file and
  date pickers, keyboard). Design only the screens that lead into them.
- Status bar, safe areas and OS-level gestures
- Tablet and wide desktop layouts
- Backend, APIs, data storage and sync mechanics
- Analytics, crash reporting and push notification infrastructure
- Monetization, paywalls and subscriptions (a later phase)
- Translations (copy is English only)
- A marketing website
</out_of_scope>

<sample_data>
Use realistic data, never placeholders. Create one shared sample data file and
use it everywhere:
- A wedding guest list of about 100 contacts with name, phone, email, photo for
  some, family side (bride's / groom's) and relationship (family, friend,
  colleague). Include edge cases: very long names, missing phone numbers,
  duplicates, contacts with several phone numbers.
- A product shortlist of about 20 items with photo, price, rating and store.
- A photo clean-up list of about 30 photos with date and location.
- Shared-list data: three members with different decisions, several conflicts,
  shared and private notes, and items at every status.
For photos, use locally stored placeholder images or generated illustrations;
never hotlink images from the internet.
</sample_data>

<deliverables>
Put everything in a /design folder:

  /design
    README.md                    How to navigate the design; start here
    HANDOFF.md                   Guide for the coding agent (see below)
    00-brief/brief.md            This prompt, copied verbatim
    00-brief/requirements.md     Every requirement in this brief, with an ID
    00-brief/assumptions.md      Every decision you made that the brief did not
    01-foundations/
      design-principles.md       The design and copy rules every agent follows
                                 (see Phase 1)
      tokens.json                Single source of truth for design tokens
      tokens.css                 Tokens as CSS variables (light and dark),
                                 shadcn naming convention
      tailwind.config.js         Tailwind theme mapped to the tokens, usable by
                                 NativeWind
      tokens.ts                  Tokens for React Native
      design-system.html         Colors, type, spacing, radii, elevation,
                                 icons and text-expansion rules
      components.html            Every component in every variant and state
      components.md              Component specs: anatomy, variants, states,
                                 props, accessibility; mapped to React Native
                                 Reusables components where one exists
      motion.md                  Gesture thresholds, velocities, timings,
                                 easing, haptics, reduced-motion fallbacks
      brand/                     Logo, wordmark, app icon and Android adaptive
                                 icon (SVG)
    02-architecture/
      navigation-map.md          Every screen ID, how screens connect, tabs,
                                 stacks, modals and deep links (invite links)
      domain-model.md            The entities the UI shows (list, item, field,
                                 template, round, decision, note, member) and
                                 their fields and statuses
    02-data/sample-data.json
    03-screens/
      Sxx-name.html              All frames of the screen: default, every
                                 state, key interaction steps, and iOS or web
                                 variants where relevant, side by side
      Sxx-name.md                Screen spec (template below)
    04-explorations/             The sorting screen directions not chosen
    04-prototype/
      index.html                 Clickable prototype of the main flows
      swipe-demo.html            A working swipe interaction (touch, mouse and
                                 keyboard) implementing the motion spec
    05-qa/
      screenshots/               Light and dark PNG of every frame
      a11y-report.md             axe-core results
      coverage.md                Every screen ID: Done / Partial / Not started
      traceability.md            Every requirement ID mapped to screen IDs
      review-report.md           QA findings and how each was resolved

Rules for screen HTML:
- Plain HTML with Tailwind CSS compiled by the build:css script, so every file
  opens offline. Fonts and icons are served locally. No JavaScript frameworks;
  small vanilla scripts only where an interaction must be shown.
- Use only tokens and Tailwind utilities mapped to them: no hard-coded colors,
  sizes or fonts.
- Follow the frame and theme conventions in CLAUDE.md, so the shots script
  captures every frame in light and dark.
- Each frame has a visible label (e.g., "S25 · Conflict state · dark").
- Use real content from sample-data.json.

Screen spec template (Sxx-name.md):
1. Purpose and the requirement IDs it covers
2. Entry points and exits (where users come from and go to)
3. Layout and components used
4. States and what triggers each
5. Interactions, gestures and transitions
6. Copy: every string on the screen, including errors
7. Accessibility: labels, focus order, screen-reader actions
8. iOS and web differences
9. Edge cases (long text, missing data, very large lists, offline)

HANDOFF.md tells the coding agent:
- The HTML is the visual reference; the specs, navigation map and domain model
  are the source of truth for behavior. Do not copy HTML structure literally.
- Build with React Native Reusables, NativeWind and the provided tokens.
- Where to find each screen, component and motion value.
- The recommended build order: tokens and components, sorting screen, then the
  main flows.

Main flows the prototype must cover end to end:
1. First launch → onboarding → import contacts as a guest → map fields →
   review duplicates → sort → round summary
2. Re-sort the Maybe pile → results → export to Google Sheets
3. Invite a partner → sign-in prompt → partner opens the link in the web app →
   both sort → conflicts → Decision Maker bulk resolves → export
4. Create a list from CSV with a custom template
</deliverables>

<process>
Skills: Use the frontend-design skill for visual and copy decisions. This brief
overrides it wherever they differ: the direction is calm and clean,
shadcn-based, and you must not pause to confirm anything with the client. Use
the webapp-testing skill, if available, alongside the npm scripts for
screenshots and browser tests.

Commit after each phase with a clear message. Never push.

Use subagents to protect your context. Run them in parallel where the work is
independent.

Phase 1, Foundations (you, no subagents):
1. Read CLAUDE.md. Copy this prompt to 00-brief/brief.md.
2. Extract every requirement into requirements.md with an ID. Be exhaustive:
   every bullet in <features>, <decision_model>, <platforms> and
   <visual_direction> becomes at least one requirement.
3. Write assumptions.md with every decision you make along the way.
4. Load the frontend-design skill. Write design-principles.md: the guidance
   from that skill that applies to this product (template tells to avoid,
   restraint, copy and error-message rules, self-critique with screenshots),
   reconciled with <visual_direction>. Subagents and QA follow this file, so it
   must stand on its own.
5. Create sample-data.json, navigation-map.md and domain-model.md.
6. Create the full design system: tokens, Tailwind config, design-system.html,
   components.html, components.md, motion.md, brand assets.
7. Run build:css, shots and a11y on the foundations, look at the screenshots
   and fix problems.

Phase 2, Reference screen (you):
Explore two or three directions for S25 Sorting screen, critique them with
screenshots against <visual_direction> and design-principles.md, and choose
one. Then design S25 and swipe-demo.html completely. This sets the quality bar
and visual language every subagent will follow.

Phase 3, Screens (subagents):
Dispatch one subagent per screen group (A through I) using the subagent brief
below. Run up to five in parallel. Wait for all reports, promote any proposed
components into the foundations, and ask the relevant subagents to update
their screens.

Phase 4, QA (a fresh subagent that did not design anything):
The QA agent uses Playwright through the npm scripts and checks:
- Coverage: every screen ID exists with every applicable state.
- Traceability: every requirement ID maps to at least one designed screen.
  Any unmapped requirement is a blocking issue.
- The decision model is applied consistently on every screen that shows
  decisions.
- Platform coverage: iOS and web variants exist wherever behavior differs, and
  web-unavailable features are handled everywhere they appear.
- Terminology: search all HTML and specs for forbidden domain words outside
  sample data; terms match <terminology>.
- Consistency: only tokens and library components are used; no hard-coded
  values.
- Accessibility: run the a11y script and fix every serious or critical
  violation; check touch target sizes, button equivalents for gestures, and
  that color is never the only signal.
- Visual quality: review the light and dark screenshots of every frame for
  overflow, clipping, misalignment, broken layouts, and the template tells
  listed in design-principles.md.
- Copy: action names stay consistent through flows, and errors and empty
  states follow design-principles.md.
- Flow integrity: every entry point and exit in the specs and the navigation
  map leads to a designed screen; no dead ends.
- Prototype: write Playwright tests in /tools/flows that click through all four
  main flows end to end, simulate a swipe drag in each direction on
  swipe-demo.html, and fail on any console error. Run them with the flows
  script.
It writes review-report.md. Dispatch fixes, then run QA again. Repeat until no
blocking issues remain.

Phase 5, Assembly (you):
Build the clickable prototype, README.md, HANDOFF.md, and final versions of
coverage.md and traceability.md. Run shots, a11y and flows one last time.
Finish with a short summary: what was designed, notable assumptions and
anything that is not Done.

If you are running out of context at any point, update coverage.md with exact
progress and next steps, and commit, before stopping, so the work can resume
with "continue".

Subagent brief (send this with every Phase 3 dispatch, filled in):
- Your assignment: screens [IDs and names].
- Read first: CLAUDE.md, 00-brief/brief.md, requirements.md, assumptions.md,
  all of 01-foundations (especially design-principles.md) and 02-architecture,
  sample-data.json, and S25 as the quality reference.
- For each screen produce Sxx-name.html and Sxx-name.md following the rules and
  template in <deliverables>. Run build:css and shots for your own screen IDs,
  look at every screenshot, and fix what you see before reporting.
- Do not edit foundation or architecture files. If you need a component that
  does not exist, build it inside your screen, mark it "Proposed", and list it
  in your report.
- Never ask questions; make decisions and list them in your report.
- Definition of done: every applicable state is designed, iOS and web variants
  exist where behavior differs, screenshots render without overflow in light
  and dark, the spec is complete, and every relevant requirement ID is listed.
- Report back: files created, requirement IDs covered, assumptions made,
  proposed components and open issues.
</process>

<success_criteria>
The work is complete only when:
- coverage.md shows every screen as Done.
- traceability.md maps every requirement ID to at least one screen, with no
  gaps.
- The QA report has no open blocking issues, the a11y report has no serious or
  critical violations, and all flow tests pass.
- A first-time user could import a list and make a first decision in under a
  minute without creating an account, as shown in prototype flow 1.
- An invited partner could join and sort from a web browser without installing
  anything, as shown in prototype flow 3.
- Someone could use the app for a product shortlist without seeing
  wedding-specific wording.
- "X / Y decided" and per-decision counts are visible whenever sorting.
- Every gesture has a visible, accessible button equivalent.
- The source picker can take a new source by adding one tile.
- A coding agent could implement any screen from its HTML, spec, the
  architecture files and the foundations alone.
</success_criteria>
