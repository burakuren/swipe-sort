# SwipeSort: Build Planning Handoff

## Purpose of this document

The design phase for SwipeSort has run (or is running) in this repository, in `/design`. The next step is planning how to build the app. This document carries over every decision the founder made with a product owner before this session, so nothing is lost.

Each item has one of three statuses. Treat them differently:

- **Fixed:** confirmed by the founder and already built into the design. Reopen one only if you find a serious problem, and explain why.
- **Working proposal:** a starting point from a thought experiment, not a decision. Grill every one of these: challenge it, compare alternatives, and keep it only if it survives.
- **Open:** not answered yet. Ask the founder.

The goal of the session is a better result, not confirmation of what is written here.

## Read first

- `design/00-brief/brief.md`: the full product brief (features, decision model, platforms, screens)
- `design/00-brief/assumptions.md`: decisions the design run made on its own
- `design/02-architecture/navigation-map.md` and `domain-model.md`
- `design/HANDOFF.md`: how to build from the design
- `design/05-qa/coverage.md`: what the design covers and anything not finished

---

## 1. Fixed

### Product

- Name: SwipeSort. The app sorts any list; no domain-specific words (such as "guest") in the UI.
- Swipe right = Accept, left = Reject, up = Maybe. Every gesture has a button equivalent; undo is always available.
- Progress shown as "X / Y decided", with counts per decision.
- Sources: phone contacts, CSV, Excel, plain text, manual entry, Google Sheets, photos. The source picker is extensible so new sources can be added later. (Google Sheets timing is a working proposal, see 2.5.)
- Card templates: a ready-made library plus custom templates; users choose fields and layout only, not fonts or colors.
- Notes on items. Fields can be edited while sorting.
- The original source is never changed automatically. Edits live in SwipeSort's working copy; export adds Decision and Notes columns.
- Rounds: re-sort the Maybe pile, narrow down accepted items, or a custom selection. Card order: original, shuffled, or sorted by a field.
- Duplicate review on import.
- Collaboration:
  - Members decide independently; items are Pending, Agreed or Conflict.
  - Conflicts form their own list until resolved.
  - Three conflict rules: everyone must agree, majority decides, or the Decision Maker decides.
  - The Owner assigns the Decision Maker with a switch. The Decision Maker can resolve conflicts one by one or bulk-resolve with their own earlier decisions.
  - Other members' decisions are hidden by default while sorting.
  - Notes are shared by default and can be marked private.
- No account is needed for solo use. Sign-in is required for sharing and backup; local lists move into the account on sign-in.
- Monetization is out of scope for now. The founder will design and add paywall screens later.
- English only at launch; Turkish and other languages later.

### Platform and stack

- Expo, React Native, TypeScript.
- Android first, then iOS.
- A full web app, as far as Expo supports it. Features that cannot work on web (e.g., contacts import) are shown as unavailable there. Invitees can join and sort from a browser.
- Phone layouts only. On desktop browsers, the phone layout is centered.
- UI: React Native Reusables (shadcn style), NativeWind, Lucide icons, Inter (or the font the design run chose; see assumptions.md).
- Material 3 behavior on Android; Apple HIG for iOS differences. Calm and clean visual style.
- Gestures with react-native-gesture-handler and Reanimated.
- Light and dark mode. WCAG 2.1 AA.

### Process

- Design first. `/design` is the source of truth: HTML for visuals; specs, navigation map and domain model for behavior.
- `/design` must be kept up to date whenever the app changes.
- Development is done with Claude Code.
- The founder has a Google developer account. The Apple developer account comes later.

---

## 2. Working proposals (grill all of these)

### 2.1 Delivery approach

Proposal: build in milestones rather than one autonomous run. A kickoff session sets up the project, architecture and a roadmap file in the repository, then builds the first milestone. A short reusable "next milestone" prompt continues from the roadmap and a progress file. Each milestone ends with something the founder can install on their phone and review.

Questions to grill:
- Is this the right granularity?
- What does "done" mean for a milestone?
- How does the founder review?
- How is progress tracked between sessions?

### 2.2 Milestone order (a thought experiment, not a plan)

- **M1, solo core on the device:** import from contacts, CSV, text and manual entry; templates; sorting; results; rounds; CSV export. No account.
- **M2:** accounts and backup.
- **M3:** collaboration (invites, decision model, conflicts) and the web app for invitees.
- **M4:** Excel, Google Sheets, photos, duplicate review.
- **M5:** polish and Play Store release.

Questions to grill:
- Is M1 the smallest version that is useful for the founder's own guest list?
- Does the timeline (see Open questions) change the order?
- Should part of the web app come earlier, so members on iPhone can join?
- Should duplicate review be in M1, since contacts often contain duplicates?
- Which milestone should go to the Play Store first?

### 2.3 Architecture: local-first

Proposal: an on-device SQLite database is the source of truth on the phone, behind a clean data layer. In the backend milestone, a sync layer is added: actions save locally first and are sent to the server when online.

Rationale:
- Guest mode needs on-device storage anyway.
- Offline sorting is required.
- Sync is unusually simple here, because each member only writes their own decisions; shared edits are rare.
- M1 can be built without choosing a backend.

Questions to grill:
- The sync and conflict strategy for shared edits
- How guest data migrates into an account
- How storage works on web (SQLite on web vs. alternatives)

### 2.4 Backend

What the backend must provide:
- Authentication: Google, email, Apple on iOS, and upgrading guests into accounts
- A relational-friendly database
- Real-time updates on shared lists
- Server-side logic: list status under the three conflict rules, bulk resolve, invites, role enforcement
- Access control
- File storage for photo items
- Push notifications
- Web hosting, including the Android App Links verification file
- Account deletion (an app store requirement)

Proposal: leaning **Supabase**.
- The data is relational (members × items × decisions per round), and conflict status becomes a testable query or view.
- One SDK covers native and web.
- Access rules live in the database (row-level security).
- Less lock-in.

Alternative: **Firebase**.
- Built-in offline sync and anonymous-to-account upgrade.
- Native Android push.
- But it uses two SDKs (native vs. web), the document model is awkward for this data, and server functions need billing enabled.

Also consider local-first sync engines (PowerSync, InstantDB) and Convex.

The decision must be made before the backend milestone; M1 does not depend on it.

Questions to grill:
- The final choice
- Cost at realistic usage
- Supporting services:
  - Crash reporting: Sentry (native and web) vs. Crashlytics (native only)
  - Push notifications: Expo's push service
  - Web hosting: EAS Hosting or alternatives
  - Email sending for authentication in production

### 2.5 Google Sheets

Facts:
- A Google Cloud project is needed anyway for "Sign in with Google" (it holds the sign-in credentials). That part only needs a simple consent screen and a light review.
- Reading and writing users' Google Sheets is different. It adds the Sheets API and a sensitive permission scope, and Google's app verification for that can take weeks.

Proposal: request access only to files the user explicitly picks, which needs a much lighter review. Alternatively, postpone Google Sheets until after launch: CSV import and export already cover the need, since users can move data between Sheets and CSV themselves. The design includes the Google Sheets screens either way.

Questions to grill:
- Is Google Sheets needed for launch at all?
- If yes, which access model?

### 2.6 Quality bar

Proposal:
- Unit tests for core logic (decision model, conflict rules, import parsing, export)
- End-to-end tests for the main flows
- Crash reporting from the first build
- Automatic type, lint and test checks on every commit

Questions to grill:
- Which tools?
- How much testing per milestone?
- Testing on real devices vs. emulators
- Accessibility and performance checks (e.g., a 1,000-item list)
- What blocks a release?

### 2.7 Translation support from day one

Proposal: all UI copy goes through a translation layer from the first screen, even though only English ships at launch. Retrofitting later means touching every screen.

Questions to grill:
- Which library?
- How are strings organized?
- How are dates, numbers and plurals handled?

### 2.8 Repository

Proposal: the app lives in this repository next to `/design`, so the coding agent always has the design beside the code.

Question to grill: the folder layout.

---

## 3. Open questions for the founder

1. **Timing:** when does the founder need the app for their own guest list? This may reshape M1.
2. **Domain:** is there a domain for invite links and the web app (the design assumes something like `swipesort.app`), or should a placeholder be used for now?
3. **Devices:** a physical Android phone or an emulator for testing? Is there an Expo account?
4. **Apple:** when will the Apple developer account be set up? This decides when iOS testing and release can start.

---

## 4. Not discussed yet (cover in the session)

- **Architecture:**
  - Navigation structure (e.g., Expo Router), using `design/02-architecture/navigation-map.md`
  - State management
  - Local database and sync details
- **Performance:** large lists and image-heavy cards.
- **Security:** access rules for shared lists, protection of contacts data.
- **Build and release:** EAS Build, EAS Submit, over-the-air updates, versioning, environments (development, staging, production).
- **App identity:** package name / bundle ID, app signing.
- **Analytics:** whether to add it, and with what tool, while respecting privacy.
- **Play Store requirements:**
  - Privacy policy and the Data safety form; especially important because the app reads contacts
  - Permission declarations
  - Account deletion
  - Store listing
- **Costs:** expected monthly cost at launch and as usage grows.

---

## 5. Expected output of the session

Save the results in the repository (for example, `docs/build-decisions.md`):

1. **Decision record:** every decision with the chosen option, the alternatives considered, and the reason. Mark each as Fixed or still Open.
2. **Roadmap:** the final milestone order, each milestone's scope and definition of done.
3. **Risks:** open risks and how they will be handled.
4. **Inputs for the build kickoff prompt:** what the first build session needs to know.
