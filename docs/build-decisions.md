# SwipeSort: Build Decisions

How SwipeSort will be built: technical and operational decisions from the build-planning grilling session
(started 2026-10-10). Inputs: `docs/swipesort-build-handoff.md` ("Fixed" items are settled; "Working
proposals" were challenged here), `/design`, `CONTEXT.md` (glossary), `docs/adr/` (architecture decision
records).

Out of scope: which version ships which features and milestone order (handoff 2.1, 2.2). Topics that affect
them are recorded in §6 as inputs for release planning.

**Resume note:** if this session stopped early, continue the grilling from the first topic in the scope
list that has no decision and no open item below.

## 1. Summary

| ID | Topic | Decision | Status | ADR |
| --- | --- | --- | --- | --- |
| D-01 | Timing | No hard deadline; quality and long-term fit beat speed. Contacts import + sorting is the #1 feature. | Decided | — |
| D-02 | Product name and domain | "SwipeSort" is a working name. Find a unique name (shortlist ready: `docs/research/naming.md`); fallback: tie to the founder's name, package `com.burakuren.<slug>`, a subdomain of `burakuren.com`. Final before backend setup and before the first Play upload. | Open (process decided) | — |
| D-03 | Test devices and Expo account | Founder's Redmi Note 12 Pro (Android 13) is the primary device; emulators for automated tests and other Android versions; founder's personal Expo account. | Decided | — |
| D-04 | Apple developer account | Individual enrollment, about 2 weeks before iOS work starts; nothing to do now. | Decided | — |
| D-05 | Architecture style | Offline-first, server-authoritative (not strict local-first); five rules incl. the online-only test. | Decided | [ADR-0001](adr/0001-offline-first-server-authoritative.md) |
| D-06 | Platform priority | Mobile first: when mobile and web needs conflict, mobile wins; web stays supported but never costs mobile a better tool, DB or certainty. One stack per concern; a platform-specific second stack is the last resort. | Decided | — |
| D-07 | Sync engine and local database | PowerSync over Postgres, single stack. Mobile: op-sqlite (SQLCipher available); web: @powersync/web (wa-sqlite). Day-1 web spike with a fallback ladder. | Decided | [ADR-0002](adr/0002-powersync-postgres-sync.md) |
| D-08 | Web guest storage | Keep web guest mode; request persistent storage; honest "browsers can clear lists" indicator and a sign-in nudge on web. | Decided | — |
| D-09 | Sync rules for concurrent and late changes | PowerSync defaults (per-field last write wins, deletes win, idempotent ops) + op-id dedup, always-2xx rejections and a per-user write-outcomes table for user notices. | Decided | — |
| D-10 | Moving lists (guest → account) | PowerSync's documented pattern: guest data in local-only tables; at sign-in copy list by list into synced tables (upload queue); photos via the PowerSync attachments helper; sample list stays local. | Decided | — |
| D-11 | Backend platform | Supabase (Postgres, Auth, Storage, Postgres functions + Edge Functions); writes via RPC functions. | Decided | [ADR-0003](adr/0003-supabase-backend.md) |
| D-12 | Authentication | Supabase Auth. Google via Supabase browser OAuth on all platforms for now (same path as Apple on Android/web); Universal Sign In ($79/yr, Credential Manager) is a later upgrade; email/password; guests have no server identity. | Decided | — |
| D-13 | Sign in with Apple everywhere | Apple on iOS (native), web and Android (Supabase OAuth with a Services ID); Apple secret rotated every 6 months. Changes the brief. | Decided | — |
| D-14 | Server write path | One batch RPC function `api.apply_ops` (security invoker, RLS kept, explicit checks, 2xx + outcomes, op-id dedup, one transaction); tables not exposed; online-only commands are `api` functions too. | Decided | [ADR-0004](adr/0004-batch-rpc-write-path.md) |
| D-15 | Supporting services | Photos: Supabase Storage + PowerSync attachments; push: Expo push service from Edge Functions; external jobs: Edge Functions; auth email: Resend SMTP; crash reporting: Sentry (PII scrubbed). | Decided | — |
| D-16 | Web hosting | Cloudflare Workers static assets on our domain (DNS already on Cloudflare); not EAS Hosting. | Decided | — |
| D-17 | Google Sheets access model + least-privilege rule | Only `drive.file` with Google's Picker; never sensitive/restricted scopes. General rule: seek a workaround before any sensitive permission or scope. Timing goes to release planning. | Decided | [ADR-0005](adr/0005-least-privilege-permissions.md) |
| D-18 | Contacts access | System contact picker where the OS has one (Android 17+, iOS) → our review list; `READ_CONTACTS` (maxSdkVersion 36) + custom list only on Android ≤16; keep `READ_CONTACTS` on 17+ only with spike evidence that the picker can't bulk-select. | Decided | — |
| D-19 | Security and privacy baseline | Membership-based RLS + sync streams; minimal invite preview; contacts field minimization; OS encryption (SQLCipher off), local DB excluded from OS backups; no end-to-end encryption; Sentry scrubbing; account deletion Edge Function + web page. | Decided | — |
| D-20 | Repository layout | Single Expo app at the repo root next to `/design`; design tooling merged into the root `package.json` as `design:*` scripts; folders `app/`, `src/`, `supabase/`, `design/`, `docs/`, `tools/`. | Decided | — |
| D-21 | Navigation | Expo Router, file routes as in `design/02-architecture/navigation-map.md`. | Decided | — |
| D-22 | State management | Persisted data only through PowerSync reactive queries (Drizzle); screen state in React; Zustand only for small cross-screen UI state; online-only commands as plain async calls with local pending state. | Decided | — |
| D-23 | Translation setup | i18next + react-i18next; English catalogs as TypeScript (`as const`) for typed keys and variables; one namespace per feature, semantic key per usage; no raw JSX text (lint); FormatJS plural polyfill; `Intl` for dates, numbers, Turkish collation. | Decided | — |
| D-24 | Quality bar | Static checks, Jest unit, RNTL component, pgTAP DB tests, Maestro mobile E2E, Playwright web E2E, manual Redmi pass; a11y and performance budgets; seven release blockers. | Decided | — |
| D-25 | Build and release pipeline | GitHub Actions for checks and Android builds (`eas build --local` on GitHub runners) + EAS for credentials, Submit and Update; tagged releases create a GitHub Release with the Play-signed universal APK; local `npm run verify`; SDK 58 if stable; dev/preview/production environments; fingerprint runtime versions; remote versioning; Play App Signing with backed-up EAS upload key. | Decided | — |
| D-26 | Open-source readiness | Repo on GitHub (private first, maybe public after first release): no secrets in git (gitleaks in CI), licensed code kept out, history scanned before going public. | Decided | — |
| D-27 | Play Store compliance | Privacy policy on our domain; Data safety declares backed-up/shared data only; contacts per D-18, photos via Photo Picker, unused permissions blocked; S12 explainers as prominent disclosure; account deletion in app + web; target API 36; EU data region (KVKK check open). Personal account (2026-09-22) → closed test ≥12 testers × 14 days. | Decided | — |
| D-28 | Analytics | Aptabase (anonymous, EU, no persistent identifiers) with a strict event list and no content; user switch in Settings › Privacy. | Decided | — |
| D-29 | PowerSync hosting | PowerSync Cloud Free during development and closed testing; self-hosted Open Edition at public launch (Cloud Pro only if self-hosting proves bad). | Decided | — |
| D-30 | Hosting option per service | Supabase Free in development → Pro at public launch; Sentry free cloud; Aptabase free cloud in development → self-hosted at launch; EAS Update free → self-hosted near 1k MAU; Resend free → Amazon SES if volume grows; Cloudflare web hosting. | Decided | — |
| D-31 | Expected costs | ≈ $0/month before launch; ≈ $35–45/month at Android launch (Supabase Pro + one small server); ≈ $90–150/month around 10k monthly users (rough). | Decided | — |
| D-32 | Photos source out of scope | The Photos source (each photo becomes a card) is removed from the current scope until its outcome makes sense; images still exist as contact photos and image fields. Changes a Fixed item. | Decided | — |
| D-33 | Per-list "keep on this device only" | Signed-in users can turn off backup for a single list; to be designed in the design-update session. Changes a Fixed item. | Decided (design pending) | — |

## 2. Facts and constraints

### Founder answers

- **Timing (2026-10-10):** plenty of time before the founder's own guest list is due; the date is not a constraint on architecture
  or process. Importing and sorting phone contacts is the number-one feature.
- **Domain (2026-10-10):** the founder owns no domain. `swipesort.app` belongs to someone else (registered
  2026-01-14 at Namecheap, parked).
- **Name (2026-10-10):** the founder wants a new, unique name that explains the product; many apps are
  already called SwipeSort. This reopens a "Fixed" handoff item (see D-02).
- **Own domain (2026-10-10):** `burakuren.com` belongs to the founder (registered 2022-07-12, renews
  2027-07-12, DNS on Cloudflare). It is the fallback home for the web app and auth email.
- **Device (2026-10-10):** Redmi Note 12 Pro, Android 13 (MIUI/HyperOS: aggressive battery management can
  delay push and background work). No iPhone.
- **Expo (2026-10-10):** the founder has a personal Expo account.
- **Hosting choices (2026-10-11):** for every service with a cloud free tier, a paid cloud plan and a
  self-hosted option, the agent presents all three with a recommendation; the founder decides.
- **Working rule (2026-10-11):** prefer PowerSync's documented, suggested solutions; only conflicts with
  them are put to the founder.
- **Founder profile and hosting preference (2026-10-11):** the founder is a backend developer experienced in
  server management, and prefers self-hosting open-source software over its cloud versions unless the
  self-hosted edition is clearly worse.
- **Least privilege (2026-10-11):** when a designed feature needs a sensitive permission or scope, find a
  workaround first; requesting it is the last resort.
- **Platform priority (2026-10-11):** mobile apps come before the web app. Web must stay supported, but never
  at the cost of a better tool, database or certainty on mobile.
- **Main database (2026-10-11):** Postgres is the founder's default choice.
- **Google Play account (2026-10-11):** personal developer account created 2026-09-22, identity verified. Because
  it is a personal account created after 2023-11-13, production access needs a closed test with at least 12
  testers opted in for 14 consecutive days.
- **Apple (2026-10-10):** no Apple developer account yet; enroll as an individual about 2 weeks before iOS
  work starts.
- **Apple Developer Program (checked 2026-10-10):** US$99/year; individuals show their legal name as seller;
  guideline 4.8 requires an equivalent privacy login next to Google sign-in (Sign in with Apple qualifies);
  5.1.1(v) requires in-app account deletion and revoking Sign in with Apple tokens; first external TestFlight
  build is reviewed; builds expire after 90 days. Sources in `docs/research/services-and-policies.md` §C.

### Verified external facts

Full research notes with source URLs: `docs/research/services-and-policies.md` (Play, OAuth, Apple, backend
and service pricing) and `docs/research/expo-stack.md` (Expo SDK, libraries, sync engines, EAS); both checked
2026-10-10. Facts that drive decisions are summarized here; each decision cites its own sources.

| Fact | Checked | Source |
| --- | --- | --- |
| Expo SDK 57 is stable (RN 0.86, React 19.2); SDK 58 is in beta, stable expected late Oct 2026; New Architecture mandatory since SDK 55 | 2026-10-10 | `expo-stack.md` §1 |
| expo-sqlite on web is "alpha" and needs COOP/COEP headers | 2026-10-10 | [Expo SQLite](https://docs.expo.dev/versions/latest/sdk/sqlite/) |
| PowerSync: Postgres → client SQLite; writes through our own backend; web SDK uses IndexedDB by default, multi-tab via SharedWorker; React Native Web pairing is beta; Open Edition free to self-host (FSL); Cloud Free sleeps after a week idle, Pro from $49/month | 2026-10-11 | [PowerSync web SDK](https://docs.powersync.com/client-sdk-references/javascript-web), [pricing](https://www.powersync.com/pricing) |
| PowerSync recommends 2xx (not 4xx) for validation failures, a batch endpoint and idempotent ops; default conflict result is per-field last write wins | 2026-10-11 | [writing client changes](https://docs.powersync.com/installation/app-backend-setup/writing-client-changes), [update conflicts](https://docs.powersync.com/usage/lifecycle-maintenance/handling-update-conflicts) |
| InstantDB cloud shuts down 2027-08-31; Triplit unmaintained; Zero has no offline writes | 2026-10-10 | `expo-stack.md` §3 |
| Supabase: Free (2 projects, pause after a week idle, no automatic backups), Pro from $25 (daily backups, 7 days); built-in auth email not for production; `public` tables not exposed to the Data API by default from 2026-10-30 | 2026-10-10/11 | [pricing](https://supabase.com/pricing), [backups](https://supabase.com/docs/guides/platform/backups), [Supabase integration](https://docs.powersync.com/integrations/supabase) |
| Free `@react-native-google-signin` uses Google's deprecated legacy Android SDK; Universal Sign In (Credential Manager) costs $79/year | 2026-10-11 | [install](https://react-native-google-signin.github.io/docs/install), [pricing](https://universal-sign-in.com/) |
| Apple OAuth (web/Android) client secret must be regenerated every 6 months | 2026-10-11 | [Supabase Apple login](https://supabase.com/docs/guides/auth/social-login/auth-apple) |
| Google scopes: `drive.file` non-sensitive; `spreadsheets(.readonly)` sensitive; `drive.metadata.readonly` restricted (CASA) | 2026-10-10 | `services-and-policies.md` §B |
| Google Play: closed test (12 testers, 14 days) for personal accounts created after 2023-11-13; target API 36 since 2026-08-31; account deletion in app + web; Photo Picker required unless gallery app | 2026-10-10 | `services-and-policies.md` §A |
| Google Play contacts policy: for API 37+ targets, `READ_CONTACTS` only if the Contact Picker can't support core features ("a custom contact picker does not qualify"); mandatory from 2027-01-27 | 2026-10-11 | [policy](https://support.google.com/googleplay/android-developer/answer/16935362), [Contact Picker](https://developer.android.com/about/versions/17/features/contact-picker) |
| Safari deletes script-writable storage after 7 days of use without a visit (long-standing ITP rule; 2025–26 status and OPFS coverage unconfirmed) | 2026-10-11 | [WebKit bug 237350](https://bugs.webkit.org/show_bug.cgi?id=237350) |
| Hermes lacks `Intl.PluralRules` (polyfill needed for i18next plurals) | 2026-10-11 | [i18next plurals](https://www.i18next.com/translation-function/plurals) |
| EAS free: 15 Android builds/month, 1,000 Update MAU hard cap; EAS Hosting custom domain only from $19/month | 2026-10-10 | [Expo pricing](https://expo.dev/pricing) |
| GitHub Actions: standard runners (macOS included) free for public repos; private repos 2,000 min/month, macOS 10× | 2026-10-11 | [GitHub billing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions) |
| `swipesort.app` is registered by someone else (2026-01-14, Namecheap) | 2026-10-10 | RDAP |

## 3. Decisions

### D-01 Timing

- **Decision:** No deadline drives the build. Choose what is best long-term rather than what is fastest.
  Contacts import and sorting is the number-one feature and must be excellent first.
- **Status:** Decided
- **Alternatives considered:** a deadline-driven solo-only build installed directly on the founder's phone;
  using a spreadsheet for the founder's own guest list and building without dogfooding.
- **Reasons:** the founder has plenty of time; the brief's priorities (sorting feel, data safety) matter more
  than speed.
- **Consequences and follow-up:** no shortcuts justified by time (for example, no throwaway storage that
  would be replaced by a backend later). The founder can still dogfood early through direct-install builds
  (see D-xx on build pipeline).
- **Design changes needed:** none.

### D-02 Product name and domain

- **Decision:** "SwipeSort" stays the working name in code and docs until a final name is chosen. A naming
  shortlist (brand-strategy approach, availability-checked) is prepared and the founder picks. If no unique
  name survives, fall back to the founder's own identity: Android package / iOS bundle
  `com.burakuren.<slug>` and the web app on a subdomain of `burakuren.com`. The name never blocks the Play
  Store or backend work: whichever gate comes first triggers the fallback.
- **Gates:** final name and domain before backend setup (auth email, Google sign-in branding, invite links,
  App Links); final package name before the first Play Console upload (it can never change afterwards; iOS
  bundle ID likewise once the App Store Connect record exists).
- **Status:** Open (process decided, name not chosen)
- **Conflict with a Fixed item:** the handoff fixed the name as SwipeSort. The founder reopened it because
  the name is not unique and `swipesort.app` is taken. Reason accepted: a store name collision hurts
  discovery, and the domain is needed for invite links, sign-in branding and auth email.
- **Alternatives considered:** keep SwipeSort with a different domain (`getswipesort.app`, `swipesort.io`).
- **Consequences and follow-up:**
  - App display name comes from one config value plus one translation string, so a rename is a one-line
    change. Development builds may use a temporary package name (reinstall when it changes).
  - Naming shortlist (2026-10-10, 162 names checked): `docs/research/naming.md`. Top picks: [name candidate]
    (.app free, .com parked), [name candidate] (.app/.com/.io all free), [name candidate], [name candidate], [name candidate]. Before choosing:
    trademark search (USPTO, EUIPO, TÜRKPATENT, classes 9 and 42) and a Turkish say-and-spell test.
  - Once chosen: register the domain with auto-renew, verify it in Google Search Console, update the design
    (below).
- **Design changes needed (once a name is chosen):** brand assets in `design/01-foundations/brand/`
  (logo wordmark, app icon if it uses letters), every "SwipeSort" string in specs and HTML, the domain in
  A-54, A-56, navigation-map §4 and the S07, S32, S39 copy.

### D-03 Test devices and Expo account

- **Decision:** The founder's Redmi Note 12 Pro (Android 13) is the primary device for manual testing and
  dogfooding (gesture feel, haptics, high refresh rate, a real address book of hundreds of contacts).
  Android emulators run automated end-to-end tests and cover other Android versions, including one
  low-end, older image for performance checks and the newest API level. The web app is tested in desktop
  Chrome and mobile emulation. EAS projects live under the founder's personal Expo account; an Expo
  organization is created only if another person joins.
- **Status:** Decided
- **Alternatives considered:** emulator only (cannot judge swipe feel, haptics or a real contact book);
  buying test devices now (premature).
- **Reasons:** the number-one feature is contacts import and sorting, which needs a real phone with real
  contacts; emulators are enough for repeatable automated checks.
- **Consequences and follow-up:**
  - Android 13 has no Android 17 Contact Picker, so the `READ_CONTACTS` path is needed on this device
    regardless of Play's API 37 restriction (see the Play Store topic).
  - Test notifications on the Redmi with battery optimization on (MIUI/HyperOS delays background work).
  - Borrow an iPhone or use a cloud device only once iOS work starts (see Apple decision).
- **Design changes needed:** none.

### D-04 Apple developer account

- **Decision:** Enroll in the Apple Developer Program as an individual (seller name "the founder's legal name") about two
  weeks before iOS work starts. Nothing to do now.
- **Status:** Decided
- **Alternatives considered:** enroll now (pays for months of no use; only useful for TestFlight before the
  web app exists); organization enrollment (needs a legal entity and a D-U-N-S number).
- **Reasons:** members on iPhone are covered by the web app; iOS simulator builds need no account, so iOS
  readiness can be checked for free; individual enrollment matches the `burakuren` fallback identity.
- **Consequences and follow-up:**
  - Code stays iOS-ready (no Android-only APIs without an iOS path); iOS simulator builds are checked
    occasionally.
  - At enrollment: create the bundle ID (permanent), Sign in with Apple capability and key, push key,
    App Store Connect record.
  - Optional now: confirm the Apple Account has two-factor authentication and the legal name matches ID.
- **Design changes needed:** none.

### D-05 Architecture style: offline-first, server-authoritative

- **Decision:** The UI reads only a local database; offline writes apply locally and queue; the server is
  the authority for account data and devices converge to it; guest data is device-authoritative until it
  moves to the account. An action is **online-only** if it (T1) needs server-only knowledge, (T2) changes
  what other members may do or see, or (T3) destroys shared data; everything else is queued and validated
  by the server on arrival.
- **Status:** Decided
- **Alternatives considered:** strict local-first (CRDT merging, server optional): peers cannot settle
  roles, conflict rules and Decision Maker resolutions without an authority. Cloud-first with a cache:
  guest mode and offline sorting need a full local replica.
- **Reasons:** matches every behavior in the design; the handoff's "local-first" label was imprecise. The
  online-only list was rederived from the T1–T3 test rather than copied from the design.
- **Online-only / queued (result of the test):**

  | Action | Verdict |
  | --- | --- |
  | Decide, undo, note, field edit; anything on a solo list; rename a shared list | Queued |
  | Change card template on a shared list; add items to a shared list | Queued (not stated in the design) |
  | Resolve one conflict (Decision Maker) | Queued; server checks the conflict is still open and the role still held |
  | Bulk resolve | Online (T1: the summary needs fresh state). Debatable, kept as designed |
  | Start a round (shared), change conflict rule | Online (T1, T2) |
  | Create invite link, join | Online (T1, T2) |
  | Roles, Decision Maker, remove member, transfer ownership | Online (T2) |
  | Leave a list | Online (T2 weak; no undo, so a confirmed result is better) |
  | Archive / delete for everyone, account deletion | Online (T2, T3) |

- **Consequences and follow-up:**
  - Open sync question: a member sorts Round 1 offline while the Owner starts Round 2. Where do the late
    Round 1 decisions go? (Covered in the sync strategy decision.)
- **Design changes needed:** spec clarifications only. S22 (change mode) and S21 must not block on shared
  lists when offline; their offline states queue the change.
- **ADR:** [ADR-0001](adr/0001-offline-first-server-authoritative.md)

### D-06 Platform priority: mobile first

- **Decision:** When a technical choice trades mobile against web, mobile wins. The web app stays a
  supported target (a Fixed requirement: invitees join and sort in a browser), but it may use a different
  implementation behind the same interface, or degrade gracefully, rather than pull mobile onto a weaker
  tool.
- **Status:** Decided
- **Alternatives considered:** equal priority (lowest-common-denominator choices); web first (invitees
  arrive on web) — rejected because the founder's own use and the number-one feature (contacts) are mobile.
- **Reasons:** founder's explicit priority; Android first is already Fixed.
- **Corollary (2026-10-11): one stack per concern.** A platform-specific second stack (for example a
  different sync engine only for web) is the last resort, ranked below degrading or dropping the feature on
  that platform.
- **Consequences and follow-up:** every later decision states whether web influenced it. Fallback order
  when a mobile-best tool is weak on web: fix within the tool → degrade on web with the same tool → drop
  the feature on web → second stack.
- **Design changes needed:** none.

### D-07 Sync engine and local database

- **Decision:** PowerSync is the single sync stack, with Postgres as the source database.
  - Mobile: `@powersync/react-native` + `@powersync/op-sqlite` (SQLite via JSI; SQLCipher encryption
    available).
  - Web: `@powersync/web` (SQLite compiled to WebAssembly, in a Web Worker, stored in IndexedDB or OPFS).
  - Query layer: SQL with Drizzle (`@powersync/drizzle-driver`) on both.
  - Writes: device → our API → Postgres (business rules stay ours); reads: Postgres → PowerSync Service →
    device, filtered per user by sync streams.
- **Status:** Decided
- **Alternatives considered:** own sync with expo-sqlite + Drizzle; Electric + TanStack DB; Zero; Convex;
  Jazz 2; LiveStore; RxDB; WatermelonDB; InstantDB; Triplit (see ADR-0002 for why each lost).
- **Reasons:** only GA option for Postgres + offline writes + Expo native and web; membership-driven partial
  sync and resumable initial sync come built in; op-sqlite is the fastest, encryptable SQLite on mobile. B
  wins on mobile alone (D-06); web was a tie-breaker.
- **Consequences and follow-up:**
  - **Day-1 spike** in the first build session: Expo web + PowerSync web SDK + worker assets on the real web
    host. Fallback ladder if it fails: fix within PowerSync → web with the in-memory database (online
    web, nothing persists between visits) → drop guest mode on web → second stack (last resort).
  - Rung 2 or 3 would need a design change (A-81 "Lists are in this browser only"); add it to the register
    only if it happens.
  - Default tables are JSON-backed views with text UUID ids and no local foreign keys; raw tables where real
    tables are needed. Composite keys (decision per item, member, round) need a deterministic id.
  - Hosting: PowerSync Cloud Free in development, self-hosted Open Edition from public launch (D-29).
  - Dev builds only (no Expo Go).
- **Design changes needed:** none (unless the web fallback reaches rung 2).
- **ADR:** [ADR-0002](adr/0002-powersync-postgres-sync.md)

### D-08 Web guest storage

- **Decision:** Guest users on the web keep lists in the browser as designed (A-81), hardened: request
  persistent storage (`navigator.storage.persist()`) when the first list is created; the web
  not-backed-up indicator says plainly that browsers can clear lists not opened for a while and that
  signing in keeps them; after the first round on web, a gentle sign-in nudge.
- **Status:** Decided
- **Alternatives considered:** web requires sign-in to create lists (conflicts with the Fixed "no account
  for solo use"); session-only guest lists on web (data vanishes on tab close; kept as the D-07 fallback
  rung 2).
- **Reasons:** browsers do not guarantee storage (Safari ITP deletes script-writable storage after 7 days of
  Safari use without a visit; Chrome/Firefox evict best-effort storage under pressure). Mobile and
  signed-in web users are unaffected. Honest copy keeps design goal 3 without breaking a Fixed item.
- **Consequences and follow-up:**
  - Test on current iOS Safari whether IndexedDB/OPFS still fall under the 7-day cap (no 2025–26
    confirmation found) and whether home-screen web apps are exempt.
  - Handle a wiped web database gracefully (the app starts empty, no error).
- **Design changes needed:** S08 web indicator copy (A-81: currently "Lists are in this browser only");
  sign-in nudge on S27 for web guests; S05 copy may reference the risk.

### D-09 Sync rules for concurrent and late changes

- **Decision:** the server applies queued writes with PowerSync's defaults plus four additions:

  | # | Situation | Server rule | Mechanism | User sees |
  | --- | --- | --- | --- | --- |
  | 1 | Two members edit the same field | Per-field last write wins by arrival | PowerSync default (PATCH carries changed fields); `trackPrevious` on edited tables; if the previous value differs from the server's, apply and record an outcome for the overwritten member | Overwritten member: "Keep mine / Use Mert's" (A-70) |
  | 2 | Round 1 decisions arrive after Round 2 started | Accepted into Round 1 | Decision rows carry their round id; only membership is checked | Local notice: "Round 2 started. Your Round 1 decisions were saved." |
  | 3 | Undo | Delete own decision row | `DELETE`; re-deciding is a `PUT` with the same deterministic id; resolutions are separate rows, so undo never reopens one | Nothing |
  | 4 | Removed member's queued writes | Rejected | 2xx + ignore → client rollback; list leaves the member's sync streams; outcome in the per-user stream | "You were removed from X." |
  | 5 | Resolution arrives after members agreed | Dropped | Conflict must still be open at arrival; else 2xx + ignore + outcome | "2 conflicts were already agreed." |
  | 6 | Decision Maker lost the role | Rejected | Role check at arrival; 2xx + ignore + outcome | "You're no longer the Decision Maker. 5 resolutions weren't applied." |
  | 7 | Write to a deleted item | Dropped | PowerSync default: deletes take precedence | Nothing |
  | 8 | Duplicate upload | Idempotent | Upserts on deterministic / UUIDv7 ids; DELETE of a missing row is a no-op; dedup by (client id, op id) so a replayed PATCH can't overwrite a newer edit | Nothing |
  | 9 | Conflict rule changed meanwhile | Statuses recompute on the server | Normal sync | Updates on next sync |
  | 10 | Validation or permission failure | Never block the queue | Always 2xx + outcome; 4xx/5xx only for transient errors and bugs (a bug blocks that client's queue and alerts crash reporting) | Rolled-back value + message |
  | 11 | Telling users about rejections | Server writes outcome rows | `write_outcomes` table scoped per user, synced to their devices; the app shows the message and deletes the row; no client-side dead-letter queue | S40-style snackbar or dialog |

- **Status:** Decided
- **Alternatives considered:** first write wins for shared fields (later edit rejected): safer for intent,
  more friction for a rare case; rejecting late decisions from an earlier round (loses user work, against
  design goal 3); a client-side dead-letter queue (PowerSync advises against it).
- **Reasons:** aligned with PowerSync's documented defaults and recommendations (checked 2026-10-11:
  [update conflicts](https://docs.powersync.com/usage/lifecycle-maintenance/handling-update-conflicts),
  [custom conflict resolution](https://docs.powersync.com/usage/lifecycle-maintenance/handling-update-conflicts/custom-conflict-resolution),
  [write validation errors](https://docs.powersync.com/usage/lifecycle-maintenance/handling-write-validation-errors));
  decisions and notes have a single writer each, so real collisions are limited to shared fields and
  Decision Maker actions.
- **Consequences and follow-up:** decision ids are deterministic from (item, member, round); other new rows
  use client-generated UUIDv7; the backend keeps a (client id, op id) dedup record; sync-layer unit tests
  cover every row of this table.
- **Design changes needed:** sync outcome messages for rows 1, 2, 4, 5, 6 in S40 (row 1 partly covered by
  A-70).

### D-10 Moving lists (guest → account)

- **Decision:** follow PowerSync's documented pattern.
  - Guest data lives in **local-only tables** (never queued, so nothing grows for people who never sign in).
  - At sign-in, lists are copied **one at a time** into the synced tables in one local transaction each
    (local-only rows deleted in the same transaction, so the UI never shows a gap). The copy enters the
    normal upload queue; the backend receives batched ops (`getCrudBatch`) through the same write path as
    every other write.
  - A list counts as **moved** when its queued ops are uploaded and confirmed by a sync checkpoint (A-46);
    the next list starts after that. Order: the list that triggered sign-in, then latest activity.
  - **Ids are kept** (client UUIDs), so open screens, undo history and rounds keep working.
  - Interrupted moves resume from the queue on next start (ops are idempotent, D-09 row 8).
  - **Photos** use the PowerSync attachments helper (local queue with retries, our storage adapter with
    signed URLs); rows move first, files upload in the background with the "Backing up…" state (A-52).
  - The **sample list** is not copied: it stays device-only.
  - Same mechanism on web.
- **Status:** Decided
- **Alternatives considered:** a per-list bulk "move" server call (all-or-nothing per list, but a second
  write path); writing guest data straight into synced tables and keeping it queued until sign-in (PowerSync
  warns the queue grows forever).
- **Reasons:** founder's rule (2026-10-11): prefer PowerSync's suggested solutions and only debate points
  that conflict with them. No conflict with the design was found: per-list confirmation, order and the
  usable local copy all fit the queue-based pattern.
- **Consequences and follow-up:** the data layer defines each table twice (local-only and synced) and
  switches at sign-in; the attachments helper's current package name and status (was beta) are checked at
  kickoff. A user's other signed-in device may briefly see a list whose items are still uploading.
- **Design changes needed:** A-79 does not say what happens to the sample list at sign-in: state that it
  stays on the device and is not backed up.

### D-11 Backend platform: Supabase

- **Decision:** Supabase for the database (Postgres), authentication, file storage and server logic.
- **Status:** Decided
- **Alternatives considered:** Neon + separate auth + R2/S3 + Cloudflare Workers; self-hosted Postgres and
  services; Firebase and Convex (not Postgres, ruled out by D-07).
- **Reasons:** one vendor for every backend need; first-class PowerSync integration (fits the vendor-default
  rule); open source and self-hostable, plain Postgres underneath.
- **Hosting (2026-10-11):** Supabase stays on Supabase's cloud; the founder prefers self-hosting open-source
  software in general, but keeps the main database managed ("a sync service is different from hosting the
  main source").
- **Consequences and follow-up:**
  - PowerSync's `uploadData` calls Postgres functions over RPC; tables in `public` are not exposed to the
    Data API (Supabase default from 2026-10-30 on existing projects).
  - Development on the free plan (pauses after a week idle); production on Pro (cost topic).
  - PowerSync needs a direct (IPv6) connection to Postgres.
  - Custom SMTP for auth email (see the auth email decision).
- **Design changes needed:** none.
- **ADR:** [ADR-0003](adr/0003-supabase-backend.md)

### D-12 Authentication

- **Decision:** Supabase Auth with:
  - **Google, all platforms, for now:** Supabase browser OAuth (`signInWithOAuth`; Android Custom Tab, iOS
    auth session, web redirect), the same path Apple uses on Android and web (D-13). *Revised 2026-10-11 in
    the costs topic; it replaces "buy Universal Sign In when auth is built".*
  - **Later upgrade (revisit trigger):** `@react-native-google-signin/google-signin`, **Universal Sign In** tier
    ($79/year; Credential Manager on Android; accepts a nonce so Supabase's default nonce check stays on),
    ID token passed to `signInWithIdToken`. Switch before public launch if sign-in friction shows up
    (analytics: sign-in started vs completed) or in tester feedback. Switching is easy: same Google project,
    same `sub`, so the same Supabase users; one sign-in module + config plugin + a new native build (about a
    day).
  - **Email and password:** Supabase Auth, custom SMTP (see auth email decision).
  - **Apple:** see D-13.
  - **Guest users have no server identity:** no Supabase anonymous users; guest data is local-only (D-10).
- **Status:** Decided
- **Alternatives considered:** free "Original" tier of the same library (Supabase's sample code, but built
  on Google's deprecated legacy Android SDK, and nonce support unconfirmed, which may force "Skip nonce
  check"); browser OAuth on mobile (free and future-proof, but not Supabase's recommended Expo path and a
  browser hop on the main sign-in); community Credential Manager libraries (unknown maintenance); Supabase
  anonymous users for guests (unneeded with local-only tables, adds cleanup and abuse surface).
- **Reasons:** Universal is the only option matching both Supabase's recommended flow (this library, ID
  token) and its described Android behavior (Credential Manager), with the nonce check kept on; the founder
  chose to start with browser OAuth to keep pre-launch costs at $0, since the upgrade path is cheap and
  browser OAuth is already needed for Apple. Mobile
  first (D-06). Sources (checked 2026-10-11):
  [Supabase Google login, React Native](https://supabase.com/docs/guides/auth/social-login/auth-google?queryGroups=platform&platform=react-native),
  [library install: Original vs Universal](https://react-native-google-signin.github.io/docs/install),
  [Universal Sign In pricing](https://universal-sign-in.com/).
- **Consequences and follow-up:** Google Cloud OAuth: a Web client for Supabase's OAuth flow now; at the
  Universal upgrade add Android (SHA-1 of debug, upload and Play App Signing keys) and iOS clients and pass a
  hashed nonce on every native sign-in. Redirect deep links are shared with Apple (D-13).
- **Design changes needed:** none.

### D-13 Sign in with Apple on every platform

- **Decision:** offer Sign in with Apple on iOS (native: `expo-apple-authentication` + `signInWithIdToken`),
  web and Android (Supabase OAuth flow with an Apple Services ID; Android returns by deep link). Available
  from Apple enrollment (D-04).
- **Status:** Decided
- **Conflict with the brief:** the brief says "add Sign in with Apple on iOS". Changed because an Apple
  account (often with a Hide My Email relay address and no password) cannot sign in anywhere else, which
  breaks design flow 3 (partner opens an invite on a laptop) and device switches.
- **Alternatives considered:** iOS + web only (Android switchers stranded); iOS only with a prominent "add a
  password" path in S07 (pushes the work onto the user).
- **Reasons:** removes the only sign-in method that can strand a user; web and Android share one OAuth code
  path. Neither Supabase nor Apple requires or recommends either way (Supabase documents every platform;
  App Review 4.8 concerns the iOS app only); this is our call.
- **Consequences and follow-up:**
  - Apple's OAuth client secret must be regenerated from the `.p8` key every 6 months or sign-in breaks
    on web and Android: scripted task + calendar reminder (native iOS is unaffected).
  - Save the full name on first Apple sign-in (`updateUser`): Apple returns it only once.
  - Source: [Supabase: Login with Apple](https://supabase.com/docs/guides/auth/social-login/auth-apple)
    (checked 2026-10-11).
- **Design changes needed:** Apple button on S03 Android and web variants, S05 (sign-in prompt) Android and
  web, S07 sign-in methods (A-53) on all platforms; brief/requirements note that Apple is no longer
  iOS-only.

### D-14 Server write path

- **Decision:** PowerSync's `uploadData` sends each batch to one Postgres function, `api.apply_ops(batch)`,
  via `supabase.rpc()`. It runs as `security invoker` (RLS still applies), checks membership, role and
  "conflict still open" explicitly, skips failing ops with an outcome row and returns 2xx, raises only on
  unexpected errors, deduplicates by (client id, op id), and runs the batch in one transaction. Only the
  `api` schema is exposed to the Data API; tables live in unexposed schemas. Online-only commands (D-05)
  are further `api` functions called directly.
- **Status:** Decided
- **Alternatives considered:** direct table writes + grants + RLS (the PowerSync Supabase integration
  guide's path); one Edge Function in TypeScript.
- **Reasons:** the vendors' docs pull in two directions: the integration guide shows direct writes, while
  PowerSync's general recommendations say batch endpoint, synchronous writes, and 2xx + error table instead of
  4xx (which blocks the queue). B meets PowerSync's recommendations and Supabase's Data API hardening
  guidance (dedicated `api` schema, explicit EXECUTE grants, prefer `security invoker`). Sources (checked
  2026-10-11): [PowerSync Supabase integration](https://docs.powersync.com/integrations/supabase),
  [PowerSync writing client changes](https://docs.powersync.com/installation/app-backend-setup/writing-client-changes),
  [Supabase hardening the Data API](https://supabase.com/docs/guides/database/hardening-data-api),
  [Supabase database functions](https://supabase.com/docs/guides/database/functions).
- **Consequences and follow-up:** list-status and conflict-rule logic exists in TypeScript (device) and SQL
  (server); a shared JSON test-vector file runs against both in CI. Revoke default EXECUTE grants; grant to
  `authenticated` explicitly.
- **Design changes needed:** none.
- **ADR:** [ADR-0004](adr/0004-batch-rpc-write-path.md)

### D-15 Supporting services (vendor defaults)

- **Decision:**
  - **Photo files:** Supabase Storage, private bucket, access per list via RLS, signed URLs; client side via
    the PowerSync attachments helper (D-10).
  - **Push:** Expo push service (free); sent by a Supabase Edge Function when activity rows are created
    (A-101 batching: one new-conflict push per list per hour); FCM v1 credentials stored in EAS; web stays
    in-app only (as designed; `expo-notifications` has no web push).
  - **Jobs that call outside services:** Edge Functions (account deletion: storage cleanup and Apple token
    revoke; push sending; Apple secret rotation). Data logic stays in Postgres functions (D-14).
  - **Auth email:** custom SMTP through **Resend** (free plan 3,000/month, 100/day, SMTP on all plans),
    sending from the chosen domain (D-02) with SPF/DKIM.
  - **Crash reporting:** **Sentry** (`@sentry/react-native` with the Expo config plugin, covering native and
    web; Deno SDK in Edge Functions). Free Developer plan (5k errors/month). Contacts data, item fields and
    notes are never sent: scrubbed in `beforeSend`, no screenshots or session replay of list content.
- **Status:** Decided (recorded as defaults on 2026-10-11; the founder raised no objection)
- **Alternatives considered:** Firebase Crashlytics (no web, needs Firebase), EAS Observe (native crashes
  only); Postmark or Amazon SES for email; FCM directly for push.
- **Reasons:** each is the documented default of the chosen vendors (Supabase, PowerSync, Expo) and has no
  conflict with the design. Facts in `docs/research/` (checked 2026-10-10).
- **Consequences and follow-up:** Resend's 100/day cap is the first limit to watch (cost topic); Sentry PII
  scrubbing is part of the security decisions.
- **Design changes needed:** none.

### D-16 Web hosting

- **Decision:** host the static Expo web export on **Cloudflare Workers static assets**, on our own domain.
  `.well-known/assetlinks.json` and `apple-app-site-association`, PowerSync worker assets and cache headers
  are served from there.
- **Status:** Decided
- **Alternatives considered:** EAS Hosting (custom domain only on paid plans, from $19/month; its main
  advantage, Expo Router server routes, is unused because the backend is Supabase); Vercel Hobby
  (non-commercial only); Netlify.
- **Reasons:** free with a custom domain; the founder's DNS is already on Cloudflare; static files keep
  lock-in near zero. Not driven by web needs over mobile.
- **Consequences and follow-up:** App Links require `assetlinks.json` on the invite-link domain, so
  production web must run on the final domain (D-02). Revisit only if EAS Starter is bought anyway for
  builds (pipeline and cost topics).
- **Design changes needed:** none.

### D-17 Google Sheets access model (and the least-privilege rule)

- **Decision:** Google Sheets uses only the non-sensitive **`drive.file`** scope. Users pick a spreadsheet
  in **Google's Picker**; the app reads its tabs and rows and can write to it (new columns or a new tab, after
  the S39 confirmation) or create a new spreadsheet. No sensitive or restricted Google scope is ever
  requested. **General rule:** when a designed feature needs a sensitive or restricted permission or scope,
  find a workaround first; requesting it is the last resort.
- **Status:** Decided
- **Conflict with the design:** S15 (A-60) lists all recent spreadsheets with Drive search, which needs
  `drive.metadata.readonly` (restricted: yearly third-party CASA assessment) and `spreadsheets.readonly`
  (sensitive); A-91 asks for `spreadsheets` to write to the original sheet (sensitive: demo video, about
  3–10 business days' review, 100-user cap and warning screen until verified).
- **Alternatives considered:** the design's scopes with Google verification; postponing Sheets and relying on
  CSV round trips.
- **Reasons:** `drive.file` covers every brief need (import, tabs, write-back to the picked sheet, new
  spreadsheet) with no review, no cap and far better privacy. Picker: web JS Picker; Android documented
  "desktop and mobile apps" mode via the system browser (`drive.file` only); iOS undocumented, same flow
  expected. Sources in `docs/research/services-and-policies.md` §B (checked 2026-10-10).
- **Consequences and follow-up:**
  - Verify the Picker flow on iOS when iOS work starts; Android flow uses `trigger_onepick` and needs its own
    client ID.
  - "Launch or later" no longer has a Google lead time; the founder's order (after the backend, D-01) goes
    to release planning.
  - The least-privilege rule is applied to contacts and photos in the security and Play Store decisions.
- **Design changes needed:** S15: replace the "Recent" spreadsheet list, Drive search and their states with a
  Google Picker step (tab selection stays); A-60 and A-91: rewrite scope text (`drive.file` only, no
  separate read and write scopes, no write-permission prompt at export for picked sheets); S39 Google
  destination copy if it mentions extra permission.
- **ADR:** [ADR-0005](adr/0005-least-privilege-permissions.md)

### D-18 Contacts access

- **Decision:** contacts import sits behind one "contact source" interface with two selection modes:
  - **Android 17+ and iOS:** the system contact picker (Android `ACTION_PICK_CONTACTS` with multi-select and
    only the fields we need; iOS contact picker, which needs no permission), then our review list (search,
    deselect, duplicates).
  - **Android 16 and lower:** `READ_CONTACTS` declared with `maxSdkVersion="36"`, pre-permission explainer
    (S12) and our full in-app list, as designed (S13, A-58).
  - An early spike on an Android 17 emulator with 300+ contacts measures the picker. If it cannot select in
    bulk, that evidence supports keeping `READ_CONTACTS` on 17+ with a Play declaration ("bulk import of the
    address book is core; the picker requires one tap per contact").
- **Status:** Decided
- **Alternatives considered:** `READ_CONTACTS` + custom list everywhere (as designed; Play says a custom
  picker "does not qualify" as a reason to keep access for API 37+ targets); picker only (single-pick on
  Android ≤16 makes importing hundreds of contacts unusable).
- **Reasons:** least privilege (D-17 rule) wherever the OS offers a picker, without breaking the
  number-one feature on today's phones (the founder's Android 13 phone has no new picker). Sources (checked
  2026-10-11): [Android 17 Contact Picker](https://developer.android.com/about/versions/17/features/contact-picker),
  [Play contacts permission policy](https://support.google.com/googleplay/android-developer/answer/16935362).
- **Consequences and follow-up:**
  - Expo support for `ACTION_PICK_CONTACTS` is unverified: a small Expo native module may be needed.
  - Verify whether limiting the permission with `maxSdkVersion="36"` avoids the Play declaration.
  - The picker grants temporary access only: copy picked data into items immediately.
  - The Play deadline applies when the app targets API 37 (mandatory for those targets from 2027-01-27;
    the yearly target bump will force it).
- **Design changes needed:** S13: add the picker path for Android 17+ and iOS (explainer → system picker →
  review list with search and deselect; "all selected" no longer applies on that path); S12: contacts
  explainer only on Android ≤16 (iOS picker needs none); A-57 and A-58 updated (iOS limited-access frames
  become the fallback only if full access is ever requested).

### D-19 Security and privacy baseline

- **Decision:**
  - **Shared-list access:** membership is the only key. RLS on every table and PowerSync sync streams both
    filter by "lists I'm a member of"; private notes filtered in both (`private = false or author = me`);
    Storage RLS per list.
  - **Invite links:** 128-bit random tokens; preview through one `security definer` function returning only
    inviter name, list name and role, never contents (A-78); Supabase rate limits on join.
  - **Contacts minimization:** import reads only the fields field mapping (S19) offers (name, phones, emails,
    photo, organization…), never contact notes, relations or account metadata; the picker path requests
    only those data types.
  - **On the device:** OS file encryption; SQLCipher off (PowerSync default; avoids key-loss risk and a speed
    cost); the local database is excluded from Android Auto Backup and iCloud backup ("On this phone only"
    stays true; no stale-sync restores).
  - **On the server:** Supabase encryption at rest and TLS; **no end-to-end encryption** (revisit only if users
    ask; list-status logic doesn't need item fields, so it stays possible later).
  - **Telemetry:** Sentry scrubs item fields, notes and contacts; no session replay of list content (D-15).
  - **Account deletion:** Edge Function implementing A-54 (transfer or delete owned shared lists, remove the
    person's decisions and notes, delete Storage files, revoke the Apple token, delete the auth user); in the
    app (S07) and on a web page on our domain (Play requirement). The privacy policy states that deleted data
    may persist in Supabase backups for their retention window (7 days on Pro, checked 2026-10-11).
  - **Abuse:** Supabase Auth rate limits; CAPTCHA only if abuse appears.
- **Status:** Decided
- **Alternatives considered:** per-list end-to-end encryption (key distribution and recovery, risk of losing
  lists, against design goal 3); SQLCipher on by default; including the local database in OS backups.
- **Reasons:** vendor defaults with no design conflict; lists hold third-party personal data, so access,
  minimization and telemetry scrubbing are strict, while E2E costs outweigh its benefit for now.
- **Consequences and follow-up:** tests for RLS and sync streams (a non-member gets nothing; private notes never leave their author).
- **Design changes needed:** none.

### D-20 Repository layout

- **Decision:** one Expo app at the repository root, next to `/design` (handoff 2.8 survives). The app's root
  `package.json` absorbs today's design tooling: scripts renamed `design:build-css`, `design:shots`,
  `design:a11y`, `design:flows`, `design:lint`, `design:qa`; `tools/` stays. Layout:

  ```
  /            package.json (app + design:* scripts), app.config.ts, CLAUDE.md, CONTEXT.md
  app/         expo-router routes
  src/         features, data layer (PowerSync, Drizzle), domain logic, components
  supabase/    migrations, api functions, edge functions, tests
  design/      unchanged
  docs/        build decisions, ADRs, research
  tools/       design tooling + app scripts
  ```
- **Status:** Decided
- **Alternatives considered:** monorepo with workspaces (`apps/mobile`, `packages/domain`); design tooling in
  its own `design/package.json`. (The first recommendation in the session was the latter; it was revised
  after weighing shared Tailwind 3 and Playwright.)
- **Reasons:** industry practice for a single-app repo is one root `package.json`, with supporting dev tools
  (the Storybook equivalent here) as devDependencies and namespaced scripts; the design tooling's Tailwind 3
  is the version NativeWind 4 needs and Playwright is reused for web E2E; nothing moves. A monorepo pays off
  only with several packages or shared server TypeScript (the server is SQL, D-14).
- **Consequences and follow-up:** the merge happens at build kickoff (after the design-update session, which
  runs on today's layout); CLAUDE.md script names updated then. **Revisit trigger:** split the design tooling
  into its own package if its dependencies ever conflict with the app's (for example the app moving to
  Tailwind 4 / NativeWind 5 while the mockups stay on Tailwind 3).
- **Design changes needed:** none.

### D-21 Navigation

- **Decision:** Expo Router with file-based routes matching `design/02-architecture/navigation-map.md`
  (tabs Lists / Activity / Settings, `list/[listId]` stack, full-screen modals for sorting, import, export,
  round, auth; `join/[token]`), deep links on our domain plus the custom scheme.
- **Status:** Decided (vendor default; no conflict)
- **Alternatives considered:** React Navigation directly (Expo Router is Expo's default and the navigation
  map was written for it).
- **Reasons:** Expo's default; the design already names routes in its conventions; web URLs come for free.
- **Consequences and follow-up:** Expo Router is versioned with the SDK; SDK 58 reworks the navigation core
  (stable expected late Oct 2026), so pick the SDK at kickoff (pipeline topic).
- **Design changes needed:** none.

### D-22 State management

- **Decision:** persisted data is read only through PowerSync reactive queries (Drizzle) — the local
  database is the single source of truth (ADR-0001 rule 1). Screen-local state uses React state. Zustand
  only for small cross-screen UI state (for example the import draft across steps). Online-only commands
  (D-05) are plain async calls to `api` functions with local pending/error state; no TanStack Query unless
  non-synced server reads grow.
- **Status:** Decided (vendor default; no conflict)
- **Alternatives considered:** TanStack Query for server state (unneeded: data arrives through sync);
  Redux / Jotai / Legend-State.
- **Reasons:** a second cache next to the synced database would duplicate truth; PowerSync's watch queries
  re-render on local and synced changes alike.
- **Consequences and follow-up:** undo history (A-29) lives in the database, not in memory.
- **Design changes needed:** none.

### D-23 Translation setup

- **Decision:** i18next + react-i18next from the first screen (handoff 2.7 survives).
  - English catalogs as TypeScript (`src/i18n/en/<feature>.ts`, `as const`): typed keys and required
    interpolation variables (i18next `parseInterpolation`, v26.2+).
  - One namespace per feature (`sorting`, `import`, `results`, `members`, `common`…); a semantic key per usage
    (`sorting.buttonMaybe`), never shared only because the English matches; `common.*` only for truly identical
    actions (Undo, Cancel), which also enforces the brief's "same action, same name" rule.
  - Lint rule: no raw text in JSX.
  - Plurals: `_one` / `_other` keys over `Intl.PluralRules`, polyfilled with `@formatjs/intl-pluralrules`
    (`polyfill-force`, English and Turkish data only); `Intl.RelativeTimeFormat` polyfilled if Hermes lacks it.
  - Dates and numbers through `Intl.DateTimeFormat` / `NumberFormat` helpers; `Intl.Collator` for
    Turkish-aware search and sort (A-58).
  - `expo-localization` for the device locale; language setting in S06 as designed.
- **Status:** Decided
- **Alternatives considered:** Lingui (English inline, ICU, `.po` workflow; IDs generated from English text
  by default, so identical English strings share one translation unless context or explicit IDs are added,
  plus a macro and compile step); i18n-js (Expo's guide example, fewer features).
- **Reasons:** Turkish (the next language) often needs different words where English uses the same one;
  explicit per-usage keys let translators vary them without code changes. Typed keys and variables, and no
  build step. Polyfills are needed either way (Lingui also needs `Intl.Locale`). Sources (checked
  2026-10-11): [Expo localization](https://docs.expo.dev/guides/localization/),
  [i18next TypeScript](https://www.i18next.com/overview/typescript),
  [i18next plurals](https://www.i18next.com/translation-function/plurals),
  [Lingui React Native](https://lingui.dev/tutorials/react-native).
- **Consequences and follow-up:** check Hermes `RelativeTimeFormat` at kickoff. **Revisit trigger:** if
  typechecking slows with thousands of keys, switch to `enableSelector: "optimize"` as i18next advises.
- **Design changes needed:** none.

### D-24 Quality bar

- **Decision:**

  | Level | Tool | Covers |
  | --- | --- | --- |
  | Static | TypeScript strict, ESLint (Expo config), Prettier, i18n no-raw-text rule | Everything |
  | Unit | Jest + `jest-expo` | Decision model, list status, conflict rules, bulk resolve, round selection, import parsing (CSV, XLSX, text), field detection, duplicate detection, export, shared test vectors (D-14), sync rules (D-09) |
  | Component | React Native Testing Library | Swipe card accessibility actions, decision buttons, forms, error and empty states |
  | Database | pgTAP via `supabase test db` | RLS (non-members get nothing, private notes stay private), `apply_ops` for every D-09 row, the same test vectors in SQL |
  | E2E mobile | Maestro (CLI, Android emulator) | Design flows 1–4, contacts import, offline sorting then sync |
  | E2E web | Playwright | Flow 3 (invite → web join → sort), keyboard sorting |
  | Manual | Founder's Redmi | Per milestone: swipe feel, haptics, real address book, TalkBack pass |

  - **Accessibility:** accessibility lint plugin and RNTL role/label queries; axe on web through Playwright;
    a manual TalkBack pass of the main flows each release; 200% text and reduced-motion checks on the four
    flows.
  - **Performance budgets** (on the Redmi Note 12 Pro; Flashlight for Android FPS/CPU): sorting smooth at the
    screen's refresh rate with a 1,000-item list and working with 10,000 (the import cap); cold start to Home
    under 2 s; importing 10,000 CSV rows under 10 s; long lists use FlashList; a seed generator creates
    1k / 10k-item lists.
  - **Release blockers:** (1) any red static, unit, component or database test; (2) any failing main-flow E2E;
    (3) any open data-loss bug; (4) crash-free sessions below 99.5% on the last beta (Sentry); (5) performance
    budgets missed on the Redmi; (6) serious or critical axe violations on web, or a main flow unusable with
    TalkBack; (7) the Sentry scrubbing (privacy) test failing.
- **Status:** Decided
- **Alternatives considered:** Detox instead of Maestro (more setup, flakier with Expo); emulator-only
  testing (cannot judge feel, haptics or a real address book).
- **Reasons:** vendor defaults (Expo recommends Maestro; Supabase ships pgTAP testing); the handoff proposal
  (2.6) survives and becomes concrete.
- **Consequences and follow-up:** where CI runs is decided in the pipeline topic. Maestro on EAS Workflows
  needs a paid plan; the CLI is free.
- **Design changes needed:** none.

### D-25 Build and release pipeline

- **Decision:**

  | Area | Choice |
  | --- | --- |
  | CI | GitHub Actions on every push: static, unit, component, pgTAP (Supabase CLI in Docker), Playwright web; Maestro on an Android emulator for release candidates. Local `npm run verify` runs the same checks before pushing. |
  | CD (Android) | GitHub Actions runs `eas build --local` on GitHub runners (no EAS build quota used; EAS supplies credentials and config); EAS Submit to Play; EAS Update for OTA |
  | CD (iOS, later) | EAS servers while the repo is private (macOS runners bill at 10× on private repos); GitHub macOS runners once the repo is public (standard runners are free for public repos) |
  | Release on tag `vX.Y.Z` | (1) all checks → `eas build --local` → AAB; (2) EAS Submit → Play internal track; (3) wait for Play processing, download the **Play-signed universal APK** through the Play Developer API (`generatedapks`); (4) create a **GitHub Release** with notes generated from conventional commits and the APK attached |
  | Expo SDK | SDK 58 if stable at kickoff (stable expected late Oct 2026), otherwise 57 then upgrade; dev builds only |
  | Environments | development: local Supabase (CLI, Docker) + local PowerSync (Docker); preview: free Supabase project + PowerSync Cloud Free; production: Supabase Pro + PowerSync (hosting per cost decision). One EAS build profile and EAS environment per environment. |
  | Builds | EAS free plan (15 Android builds/month, low-priority queue); `expo run:android` daily; `eas build --local` when the queue is slow |
  | Distribution | Founder's phone: EAS internal distribution; store: AAB → Play internal → closed → production |
  | Submit | EAS Submit to Play, internal track first (verify whether the first upload must be manual; Expo docs conflict) |
  | OTA updates | EAS Update, one channel per environment, runtime version policy `fingerprint`; free up to 1,000 MAU; the design's "App update required" (A-116) enforced by a minimum client version checked in `apply_ops` |
  | Versioning | Semver marketing version; Android `versionCode` / iOS build number managed remotely by EAS (`appVersionSource: remote`, auto-increment) |
  | Package name | From D-02 (chosen name or `com.burakuren.<slug>`); permanent after the first Play upload; dev builds use a temporary id until then |
  | Signing | Play App Signing (Google holds the app key); EAS generates and stores the upload key; a backup downloaded with `eas credentials` into the founder's password manager; SHA-1/SHA-256 of both keys registered in Google OAuth (D-12) and `assetlinks.json` (D-16) |

- **Status:** Decided
- **Alternatives considered:** EAS Workflows as CI (60 free minutes, Maestro only on paid plans); local-only
  checks; builds on EAS servers triggered from Actions (uses the free 15 builds/month); plain `expo prebuild`
  + Gradle without EAS (we would manage keystores ourselves); a GitHub APK signed with our own key (signature
  mismatch with Play installs).
- **Reasons:** the common Expo setup (GitHub Actions for tests, EAS for native builds); vendor defaults
  elsewhere; the founder will host the repo on GitHub.
- **Consequences and follow-up:** the founder creates the GitHub repository and pushes (the agent never
  touches remotes); GitHub secrets hold CI credentials (EXPO_TOKEN, Play service account).
  - **APK signing (why the Play-signed APK):** with Play App Signing, Play re-signs the app with Google's key.
    An APK built and signed by us with the upload key would have a different signature: installs from GitHub
    and Play could not update each other, and `assetlinks.json`, Google OAuth (SHA-1) and Android developer
    verification would each need the extra certificate. The universal APK that Play generates is signed with
    the app-signing key, so one signature covers Play, GitHub, App Links and sign-in.
  - GitHub billing (checked 2026-10-11): standard GitHub-hosted runners, macOS included, are free in public
    repositories; private repos on GitHub Free get 2,000 minutes/month with macOS at 10×. Sources:
    [About billing for GitHub Actions](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions),
    [GitHub Actions pricing update, Dec 2025](https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/).
- **Design changes needed:** none.

### D-26 Open-source readiness

- **Decision:** the repo goes on GitHub, private at first; the founder may make it public after the first
  release. From day 1: (1) no secrets in git (server-only keys in EAS environment variables, GitHub secrets
  or Supabase secrets; gitleaks in CI from the first commit, and a full-history scan before going public);
  publishable values (Supabase anon key, Google OAuth client IDs, Sentry DSN) may be committed;
  (2) the paid Universal Sign In package and its registry token stay out of git; builds without the token
  fall back to the free library or a dev stub; (3) server code (RLS, `apply_ops`) being visible is fine
  because security rests on tested RLS (D-24), not obscurity.
- **Status:** Decided
- **Alternatives considered:** deciding later (secrets committed while private would be exposed by history).
- **Reasons:** git history is permanent; the hygiene is cheap from the start.
- **Consequences and follow-up:** founder's own choice: commit author email is the personal Gmail today;
  switching to GitHub's noreply address before going public is the founder's decision (the agent does not
  change git config). License (for example MIT vs AGPL) and trademark are open items.
- **Design changes needed:** none.

### D-27 Play Store compliance

- **Decision:**

  | Requirement | Plan |
  | --- | --- |
  | Privacy policy | Plain-language page on our domain (`/privacy`, Cloudflare), linked in the Play listing and in the app (S06 privacy information). Covers data collected (below), sub-processors (Supabase, PowerSync, Sentry, Resend, Expo push, Google, Apple), retention including backups (D-19), deletion, contact. Drafted by us; the founder owns it legally. |
  | Data safety form | Device-only data (guest lists) is not "collected". Declared for backed-up or shared lists and accounts: Contacts (including contact photos), Photos only if the Photos source returns (D-32), Name, Email address, User IDs, Other user-generated content (lists, decisions, notes), Crash logs and Diagnostics (Sentry), Device or other IDs (push tokens); analytics data if D-28 adds it. Purpose: app functionality. Encrypted in transit; deletion available; not shared (service providers don't count). |
  | Permissions | `READ_CONTACTS` with `maxSdkVersion="36"` (D-18; a declaration only if kept on Android 17+); no photo-library access while the Photos source is out of scope (D-32; when it returns: system Photo Picker, never `READ_MEDIA_IMAGES`); `POST_NOTIFICATIONS` at runtime; permissions added by libraries but unused are removed with `android.blockedPermissions`. |
  | Prominent disclosure | The S12 contacts and photos explainers are the in-app disclosure with affirmative consent before access; they stay on every permission path. |
  | Account deletion | In the app (S07) and a web page on our domain, URL entered in Play Console (D-19). |
  | Target API | 36 (required for new apps and updates since 2026-08-31); moving to 37 triggers the D-18 contacts declaration question. |
  | Store listing | Content rating questionnaire (lists are shared only by invite, no public content); target audience 13+; no ads; screenshots from the real app. |
  | Data region | Supabase project in an EU region (Frankfurt): closest to Turkey, GDPR-friendly. |
  | Closed testing | Personal account created 2026-09-22 → closed test with ≥12 testers opted in for 14 consecutive days before applying for production. |

- **Status:** Decided
- **Alternatives considered:** a generated privacy policy (generic, misses contacts specifics); a US data region.
- **Reasons:** Play policies checked 2026-10-10 (`docs/research/services-and-policies.md` §A); least privilege
  (D-17).
- **Consequences and follow-up:** legal check of Turkish KVKK cross-border transfer rules (amended 2024) before
  launch (open item); confirm which permissions Expo libraries add, at kickoff.
- **Design changes needed:** none (S06 already has privacy information).

### D-28 Analytics

- **Decision:** Aptabase (free cloud, EU, during development; self-hosted from launch, D-30), React Native + web
  SDK. Strict event list only: `app_open`,
  `onboarding_step`, `import_started` / `import_completed` {source type, item-count bucket}, `first_decision`
  {seconds bucket}, `round_completed` {size bucket}, `list_shared`, `invite_joined` {platform}, `export`
  {format}. Never item content, names, list names or free text. A "Share anonymous usage data" switch in
  Settings › Privacy (on by default, since events are anonymous) turns it off; the privacy policy describes it.
- **Status:** Decided
- **Alternatives considered:** PostHog (stronger funnels and retention, free 1M events/month, but device
  identifiers and replay generally need consent); no analytics (no evidence for the brief's "first decision
  in under a minute" success criterion).
- **Reasons:** measures the brief's success criteria and source usage with the least data; vendor states no
  persistent identifiers and no consent banner needed (vendor claim, not legal advice); open source and
  self-hostable. Free up to 20k events/month, then from $10/month (checked 2026-10-10).
- **Consequences and follow-up:** add "App interactions" (analytics purpose) to the Data safety form (D-27);
  an event schema file in the code is the only allowed source of event names and properties.
- **Design changes needed:** S06 Privacy: a "Share anonymous usage data" switch with one line of explanation.

### D-29 PowerSync hosting

- **Decision:** PowerSync Cloud Free during development and the closed test (50 peak clients cover the
  testers); self-hosted **Open Edition** from public launch, on a small server run by the founder, with bucket
  storage in a dedicated schema and user (Postgres 14+ allows the same server as the source database; a
  separate small Postgres is the alternative). Cloud Pro only if self-hosting proves clearly worse.
- **Status:** Decided
- **Alternatives considered:** Cloud Pro at launch (from $49/month, then $1/GB synced or hosted and $30 per
  extra 1,000 concurrent clients; zero operations).
- **Reasons:** founder's preference for self-hosting open-source software and server experience; Open Edition
  has all core features (FSL licence); same protocol, so moving between Cloud and self-hosted needs no app
  change. Source: [PowerSync pricing](https://www.powersync.com/pricing) (checked 2026-10-11).
- **Consequences and follow-up:**
  - The Cloud Free instance sleeps after a week without activity: wake it when development pauses.
  - Self-hosting needs IPv6 to reach Supabase's direct connection (or Supabase's IPv4 add-on), uptime
    monitoring, upgrades and a restart policy; bucket storage can be rebuilt from Postgres, so it needs no
    backups.
  - The move from Cloud to self-hosted happens before public launch and is a server-side migration.
- **Design changes needed:** none.

### D-30 Hosting option per service

- **Decision (founder picked "as recommended" for every row):**

  | Service | Choice |
  | --- | --- |
  | Supabase | Free plan in development and the closed test, with a scheduled `db dump` to the founder's server; **Pro ($25/month) at public launch** (daily backups kept 7 days, never pauses). PITR not needed. Cloud only (D-11). |
  | Sentry | Free cloud (5k errors/month); Team ($26) only if errors exceed that. Self-hosting rejected: very heavy. |
  | Aptabase | Free cloud during development; **self-hosted at launch** (Docker Compose: Postgres + ClickHouse + app). |
  | EAS Update | Free (1,000 MAU hard cap; users beyond it run the embedded bundle); **self-hosted** Expo Updates protocol server (Expo's reference server, assets on Cloudflare R2) as usage nears 1k MAU, instead of paid plans. |
  | Auth email | Resend free (3k/month, 100/day); Amazon SES if volume grows. No own mail server (deliverability). |
  | Web hosting | Cloudflare (D-16). |
  | PowerSync | Cloud Free → self-hosted at launch (D-29). |

- **Status:** Decided
- **Alternatives considered:** per row in the table above (free cloud, paid cloud, self-hosted).
- **Reasons:** founder's hosting preference (self-host open source when comparable; keep the main database
  managed) and process rule (the agent presents, the founder decides). Sources (checked 2026-10-11):
  [Supabase backups](https://supabase.com/docs/guides/platform/backups),
  [Expo custom updates server](https://docs.expo.dev/eas-update/custom-updates-server),
  [Expo Updates v1 spec](https://docs.expo.dev/technical-specs/expo-updates-1/),
  [Aptabase self-hosting](https://github.com/aptabase/self-hosting).
- **Consequences and follow-up:** one founder-run server hosts PowerSync, Aptabase and later the updates
  server (size it for ClickHouse); uptime monitoring for all three. Supabase Free has no automatic backups,
  so the scheduled dump runs from day one of real data (the founder's own guest list).
- **Design changes needed:** none.

### D-31 Expected costs

- **Decision (estimate, to be checked against real bills):**

  | Phase | Monthly cost | Made of |
  | --- | --- | --- |
  | Development, founder's own use, closed test | **≈ $0** | Free tiers: Supabase, PowerSync Cloud, Sentry, Aptabase cloud, EAS, Resend, Cloudflare, GitHub; browser OAuth (no Universal licence). Domain ≈ $1 if bought (or a `burakuren.com` subdomain, $0). Google Play fee already paid. |
  | Public launch, Android | **≈ $35–45** | Supabase Pro $25; one small server for self-hosted PowerSync + Aptabase (≈ €8–15, sized for ClickHouse); domain ≈ $1 |
  | + iOS | +$8 | Apple Developer Program $99/year |
  | + Universal Sign In (if upgraded) | +$7 | $79/year |
  | ~1k monthly users | ≈ $40–55 | Same; EAS Update moves to the self-hosted server near the 1k MAU cap (R2 storage with free egress) |
  | ~10k monthly users (rough) | ≈ $90–150 | Supabase compute/disk +$15–35; bigger server +$10–20; Sentry Team $26 if needed; email via SES (a few dollars) |

- **Status:** Decided (as the planning baseline)
- **Alternatives considered:** all-cloud setup (≈ $82/month at launch, ≈ $200–400 at 10k users, mainly PowerSync
  Cloud and EAS Update paid plans).
- **Reasons:** follows D-29 and D-30. Assumptions: about 2 lists × 500 items per user, few photo lists.
- **Consequences and follow-up:** biggest cost drivers to watch: photo storage and egress (Supabase), server
  size, Sentry error volume; review the bills monthly after launch.
- **Design changes needed:** none.

### D-32 Photos source out of scope (for now)

- **Decision:** the **Photos** source (S18: each photo becomes a card) is out of the current scope. It returns
  when its outcome is designed: today a photo sort ends in nothing useful, because exports leave image fields out
  (A-94) and the original source is never changed (so rejected photos are not deleted from the gallery).
  Images still exist inside other lists: **contact photos** and **image fields**, stored as files and synced to
  Supabase Storage (D-15).
- **Status:** Decided (2026-10-11)
- **Conflict with a Fixed item:** the handoff lists photos among the launch sources, and the brief's sample
  data includes a photo clean-up list. The founder removed it because the feature has no meaningful result yet.
  The source picker is data-driven (A-55), so it can return as one more tile.
- **Alternatives considered:** keep photos and design an outcome (export a contact sheet, album, or a
  "delete rejected photos" action, which would break "the source is never changed automatically").
- **Reasons:** a sort whose result can't be used doesn't serve the founder or users; less scope, less storage
  cost and one fewer permission path.
- **Consequences and follow-up:**
  - No photo-library access at all for now (no Photo Picker path); Data safety declares photos only as part of
    contacts (contact photos).
  - Supabase Storage remains for contact photos and image fields, so the **Storage backup gap stays** (smaller):
    Postgres backups do not include Storage files (open item).
  - Release planning: photos is a later feature, with its outcome to be designed first.
- **Design changes needed:** remove or mark as "later" the Photos tile (S11, including the web "Upload photos"
  tile), the photos pre-permission explainer and denied states (S12), S18 entirely, the photo clean-up sample
  list from first-run and samples where it is the subject; decide whether the built-in **Photo** card template
  stays (useful for CSVs with image links) or goes; check prototype flows and coverage/traceability for photo
  references.

### D-33 Per-list "keep on this device only" (turn off backup for one list)

- **Decision:** a signed-in user can keep a single list on the device only, with backup turned off for that
  list. Included in the design-update session; the design decides the details below.
- **Status:** Decided (2026-10-11); design pending
- **Conflict with a Fixed item:** the handoff and brief say local lists move into the account on sign-in, and
  A-81 says signed-in lists are always backed up. The founder wants users to be able to keep private lists
  off the server.
- **Alternatives considered:** every signed-in list is backed up (as designed).
- **Reasons:** privacy for sensitive lists (for example contact data a user doesn't want on any server); the
  architecture makes it cheap: device-only lists use the same local-only tables as guest lists (D-10), and
  "Back up this list" reuses the moving-lists mechanism.
- **Questions the design session must answer:**
  1. Where the switch lives (S09 list overview, S10 list menu, S06 backup page) and its label.
  2. Sharing needs backup: what happens when the user shares a device-only list (prompt to back it up first).
  3. Turning backup off for a backed-up list deletes the account copy: confirmation copy; not allowed for
     shared lists (or only for the Owner after removing everyone?).
  4. Sign-in: do all guest lists still move automatically, or can the user keep some on the device?
  5. Sign-out: backed-up lists leave the phone (A-52); do device-only lists stay, and whose are they after
     another account signs in on the same phone?
  6. Labels: the "On this phone only" indicator per list for signed-in users (A-35, A-81), and on web the
     browser-storage warning (D-08).
  7. Account deletion and moving to a new phone: device-only lists are not recoverable; how this is explained.
- **Consequences and follow-up:** no new technology; data layer keeps a per-list storage mode (device-only /
  backed up); Data safety unaffected (device-only data is not collected).
- **Design changes needed:** see the questions above and the register (§7).

## 4. Risks

| Risk | Likelihood / impact | Handling |
| --- | --- | --- |
| PowerSync's React Native Web pairing is labeled beta (Metro resolver and worker-asset glue). | Medium / medium | Day-1 spike on the real host; fallback ladder in D-07; mobile unaffected. |
| Browser clears a web guest's lists (Safari 7-day cap, eviction). | Medium / medium | D-08: persistent-storage request, honest indicator, sign-in nudge; mobile and signed-in users unaffected. |
| Apple OAuth secret expires (6 months) and Apple sign-in breaks on web/Android. | Medium / medium | D-13: scripted rotation + calendar reminder; monitor auth errors in crash reporting. |
| List-status logic drifts between the device (TypeScript) and the server (SQL). | Medium / high | D-14: shared JSON test vectors run against both implementations in CI. |
| A secret gets committed and later exposed when the repo goes public. | Low / high | D-26: gitleaks in CI from the first commit, full-history scan before going public; rotate any leaked key. |
| Storage files (contact photos, image fields) are not covered by Supabase's database backups. | Low / medium | Open item: bucket sync to the founder's server or R2 with versioning before public launch. |
| Self-hosted PowerSync goes down: devices keep working offline but stop syncing. | Low / medium | D-29: uptime monitoring and alerting, restart policy, documented redeploy; Cloud Pro as fallback (same protocol). |
| PowerSync vendor risk (pricing change, company failure). | Low / high | Self-hostable Open Edition (FSL), Apache-2.0 client SDKs, same protocol; Postgres stays the source of truth. |
| Google Play restricts `READ_CONTACTS` for apps targeting API 37+: allowed only when the Android 17 Contact Picker can't support core features, with a Play Console declaration (mandatory from 2027-01-27 for API 37 targets). Contacts import is the #1 feature. | Medium / high | D-18: picker on Android 17+ and iOS, permission only on Android ≤16; spike evidence backs a declaration if the picker can't bulk-select. |
| Sync bug loses or corrupts user data (design goal 3). | Medium / high | D-09 rules unit-tested row by row; pgTAP tests for `apply_ops`; an open data-loss bug blocks release (D-24). |
| No backups while the founder's real guest list lives on Supabase Free during development. | Medium / high | D-30: scheduled `db dump` to the founder's server from the first real data; Pro (daily backups) at public launch. |
| Expo has no support for the Android 17 Contact Picker. | Medium / low | D-18: a small Expo native module; the `READ_CONTACTS` path covers Android ≤16 meanwhile. |
| Google Picker flow on iOS is undocumented. | Medium / low | D-17: verify when iOS starts; CSV/XLSX file import is the fallback. |
| Recruiting 12 closed-test testers for 14 consecutive days delays the Play release. | Medium / medium | D-27: recruit early; release planning input. |
| KVKK cross-border transfer rules affect storing contacts in an EU region. | Low–medium / high | Legal check before public launch (open item). |
| Name and domain not chosen when the backend or the first Play upload is due. | Low / low | D-02 fallback: `com.burakuren.<slug>` and a `burakuren.com` subdomain. |
| Expo SDK 58 slips or regresses at kickoff. | Low / medium | D-25: start on SDK 57 and upgrade. |

## 5. Open items

| Item | Why open | Needed to decide |
| --- | --- | --- |
| Product name and domain (D-02) | Founder has not picked from the shortlist | Pick from `docs/research/naming.md` (top: [name candidate], [name candidate]); trademark search (USPTO, EUIPO, TÜRKPATENT, classes 9 and 42) and a Turkish say-and-spell test; register the domain. Deadline: before backend setup and before the first Play upload, otherwise the `burakuren` fallback applies. |
| KVKK legal check (D-27) | Turkish rules on transferring personal data abroad (amended 2024) apply to contacts stored in an EU Supabase region | A legal opinion before public launch |
| Open-source licence and trademark (D-26) | Only needed if the repo goes public | Choose MIT vs AGPL (AGPL stops a closed hosted clone); protect the final name |
| Commit author email (D-26) | Personal Gmail is in commit history | Founder decides whether to switch to GitHub's noreply address before going public |
| Backup of Supabase Storage files (contact photos, image fields) | Supabase's database backups do not include Storage objects ("the database only includes metadata"), so a deleted or corrupted file can't be restored | Choose: scheduled sync of the bucket to the founder's server or Cloudflare R2 with versioning (agent's lean), object versioning, or accept (the device keeps a copy until sign-out). Before public launch. |

Not open, but with revisit triggers: Universal Sign In upgrade (D-12), split design tooling into its own
package (D-20), i18next selector mode (D-23), PowerSync Cloud Pro fallback (D-29), self-hosted EAS Update
near 1k MAU (D-30).

## 6. Inputs for release planning

- **Founder's ordering preference (D-01):** offline contacts import + sorting first; then the backend; only then
  the sources that need more work (Google Sheets and the like). Recorded, not decided here.
- **Design-update session before any coding** (§7): the design register below is applied first.
- **Name and domain gate (D-02):** before backend setup (auth email, Google brand verification, invite links,
  App Links) and before the first Play upload (package name is permanent).
- **Google sign-in branding (D-12, D-17):** brand verification takes minutes but needs the final domain with a
  homepage and a privacy policy. Google Sheets has no verification lead time (`drive.file` only), so it can
  ship whenever release planning puts it.
- **App Links (D-16):** `assetlinks.json` changes can take up to 7 days to propagate on Android 15+; publish it
  well before testing invite links on devices.
- **Play closed testing (D-27):** personal account created 2026-09-22 → at least 12 testers opted in for 14
  consecutive days, then a production-access review. Recruit testers (Android phone + Google account) early;
  opting out and back in restarts the count.
- **Target API (D-18, D-27):** API 36 now; the yearly bump to 37 (expected around Aug 2027, unverified) triggers
  the contacts declaration question, and Play's contacts rule is mandatory for API 37 targets from 2027-01-27.
- **Android developer verification:** the founder's account is verified; enforcement goes global in 2027.
- **Before public launch:** Supabase Pro (D-30), PowerSync moved to self-hosted (D-29), Aptabase self-hosted
  (D-30), privacy policy and account-deletion page live (D-27), KVKK legal check (open item), decide on the
  Universal Sign In upgrade (D-12).
- **Apple (D-04, D-13):** iOS device testing, TestFlight, Sign in with Apple and iOS push start only after
  enrollment (allow about 2 weeks) plus TestFlight review of the first external build; Apple's OAuth secret then
  needs rotation every 6 months.
- **Photos source (D-32):** out of the current scope; returns as a later feature once its outcome is designed.
- **Expo SDK (D-25):** SDK 58 stable expected late Oct 2026; Expo Router's navigation core changes in 58.
- **EAS Update (D-30):** the free plan stops serving updates beyond 1,000 MAU; move to the self-hosted updates
  server before that.

## 7. Inputs for the build kickoff

The first build session (after the design-update session) must:

1. **Read:** CLAUDE.md, CONTEXT.md, this file, `docs/adr/`, `design/HANDOFF.md`, the navigation map and domain
   model.
2. **Spikes first:**
   - **Web + PowerSync (D-07):** Expo web + PowerSync web SDK + worker assets deployed to Cloudflare (D-16); apply
     the fallback ladder if it fails.
   - **Contacts (D-18):** Android 17 emulator with 300+ contacts: Contact Picker bulk selection, returned fields,
     Expo support (native module needed?), `maxSdkVersion="36"` behavior.
3. **Project setup:** Expo SDK 58 if stable, else 57 (D-25); TypeScript strict; dev builds only (no Expo Go);
   Expo Router routes from the navigation map (D-21); NativeWind 4 + Tailwind 3 with `design/01-foundations`
   tokens, React Native Reusables, Lucide, Reanimated + Gesture Handler, Inter (design HANDOFF §2).
4. **Repository (D-20):** merge the design tooling into the root `package.json` as `design:*` scripts; update
   CLAUDE.md (new phase: build; script names).
5. **Data layer:** PowerSync schema with local-only and synced variants (D-10), Drizzle driver, deterministic
   decision ids and UUIDv7 (D-09), database excluded from Android Auto Backup / iCloud (D-19); reactive queries
   only (D-22).
6. **Local backend for development:** Supabase CLI (Docker) with migrations in `supabase/`, the `api` schema and
   default EXECUTE grants revoked (D-14), local PowerSync (Docker); PowerSync Cloud Free + a free Supabase project
   for preview.
7. **i18n (D-23):** i18next with TypeScript catalogs, namespaces, no-raw-text lint rule, plural polyfill.
8. **Quality harness (D-24):** Jest + jest-expo, RNTL, pgTAP, Maestro, Playwright; the shared list-status test
   vectors file; a seed generator for 1k / 10k-item lists.
9. **Pipeline (D-25, D-26):** EAS project under the founder's account, build profiles and environments
   (development / preview / production), `fingerprint` runtime version, remote versioning, temporary package id
   until D-02; GitHub Actions workflow, local `npm run verify`, gitleaks.
10. **Observability (D-15, D-28):** Sentry with PII scrubbing; Aptabase cloud with the event schema file.
11. **Android manifest (D-27):** block unused permissions; `READ_CONTACTS` with `maxSdkVersion="36"`; no
    `READ_MEDIA_IMAGES`.

### Design update task (before any coding session)

The founder decided (2026-10-10) that all design changes found in this session are collected here and handed to
a dedicated design-update session (a well-prompted agent with the design skills and context) before any coding
starts. `/design` is not edited in this session.

| From | Change | Status |
| --- | --- | --- |
| D-02 | New product name and domain: brand assets, every "SwipeSort" string, domain in A-54, A-56, navigation-map §4, S07/S32/S39 copy (once the name is chosen) | Skipped: no final product name is chosen yet (D-02 open); see `design/00-brief/assumptions.md` A-128 and `docs/design-update-report.md` |
| D-05 | S21 and S22 change mode: on shared lists, offline changes are queued, not blocked; state this in specs and A-88 | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-08 | S08 web guest indicator: say browsers can clear lists not opened for a while and that signing in keeps them (replaces A-81 web copy); S27 web: gentle sign-in nudge after a guest's first round; S05 may mention the risk | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-09 | S40: sync outcome messages for an overwritten field edit (beyond A-70's inline choice), late Round 1 decisions saved after a new round, removed from a list while offline, resolutions dropped because members already agreed, resolutions rejected because the Decision Maker role moved | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-10 | A-79 / S05: the sample list stays on the device at sign-in and is not moved to the account | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-13 | Sign in with Apple on all platforms: S03 (Android, web), S05 (Android, web), S07 sign-in methods; update requirements/brief note (Apple was iOS-only) | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-17 | S15: replace "Recent" spreadsheet list and Drive search with a Google Picker step (keep tab selection); rewrite A-60 / A-91 scopes to `drive.file` only; S39 Google copy about permissions | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-18 | S13: picker path for Android 17+ and iOS (system picker → review list); S12 contacts explainer only on Android ≤16; update A-57 / A-58 | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-28 | S06 Privacy: "Share anonymous usage data" switch (on by default) with a one-line explanation | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-32 | Photos source out of scope: remove or mark "later" the S11 Photos tile (and web "Upload photos"), S12 photos explainer and denied states, S18 entirely, photo clean-up sample list where it is the subject; decide whether the built-in Photo template stays; check prototype flows, coverage and traceability for photo references | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
| D-33 | Per-list "keep on this device only" for signed-in users: design the switch, labels, share/sign-in/sign-out/deletion behavior and confirmations (questions 1–7 in D-33); update A-35, A-46, A-52, A-81, S05, S06, S09, S10 | Done in b854621 (QA fixes ba6fcbd, e1bb89b); see `docs/design-update-report.md` |
