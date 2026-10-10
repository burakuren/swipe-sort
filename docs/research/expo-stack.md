# SwipeSort stack research (checked 2026-10-10)

Format: fact | source | checked date. "npm" = registry.npmjs.org `dist-tags.latest` + publish time, queried 2026-10-10.
UNVERIFIED = could not confirm from a primary source.

## 1. Expo SDK / RN / Router

- The latest stable Expo SDK is **57** (`expo@57.0.27` on the `latest` tag, published 2026-10-06). SDK 57 was released 2026-06-30. | https://expo.dev/changelog/sdk-57 , npm `expo` | checked 2026-10-10
- SDK 57 bundles **React Native 0.86.3**, **React 19.2.3**, react-dom 19.2.3 and react-native-web ~0.21.0. | https://unpkg.com/expo@57.0.27/bundledNativeModules.json , https://docs.expo.dev/versions/latest/ | checked 2026-10-10
- **SDK 58 is in beta**. The beta was announced 2026-09-15 and is published as `expo@58.0.7` on the `next` tag. It uses the RN 0.88 release candidate (bundles `react-native 0.88.0-rc.4`) and React 19.3.0. The beta lasts "three to four weeks", and the stable release ships "shortly after" RN 0.88 stable. RN 0.88 is still at rc.4 on npm (RN `latest` = 0.87.1). Inference: SDK 58 stable is likely late Oct 2026. | https://expo.dev/changelog/sdk-58-beta , npm `expo`, `react-native` | checked 2026-10-10
- SDK 58 breaking changes: Strict TypeScript API is the default (deep `react-native/Libraries/*` imports become type errors). R8 is on by default for Android release builds. iOS uses the scene-based lifecycle by default (iOS 27 SDK). expo-sqlite drops libSQL. In Expo Router, loaders, SSR, middleware and native tabs become stable and the navigation core is reworked. | https://expo.dev/changelog/sdk-58-beta | checked 2026-10-10
- **New Architecture is mandatory** from SDK 55 on. SDK 54 was the last SDK with Legacy Architecture, and the `newArchEnabled` option was removed. Reanimated 4 and Gesture Handler 3 also require the New Architecture. | https://expo.dev/changelog/sdk-55 | checked 2026-10-10
- Since SDK 55, all Expo SDK packages share the SDK major version. **Expo Router for SDK 57 is `expo-router ~57.0.25`**; SDK 58 uses `~58.0.17`. | https://expo.dev/changelog/sdk-55 , bundledNativeModules.json | checked 2026-10-10
- Since SDK 56, Expo Router no longer depends on React Navigation. Most direct `@react-navigation/*` imports stop working, and a codemod handles the migration. | https://expo.dev/changelog/sdk-56.md | checked 2026-10-10
- SDK 57 minimums: **iOS 16.4+**, **Android 7+ (API 24)** and Xcode 26.4+. The iOS minimum was raised to 16.4 in SDK 56. | https://docs.expo.dev/versions/latest/ , https://expo.dev/changelog/sdk-56.md | checked 2026-10-10
- Hermes V1 has been the default JS engine since RN 0.84. | https://reactnative.dev/blog/2026/02/11/react-native-0.84 | checked 2026-10-10
- Expo Go now requires login to run projects (2026-09-03). Remote push does not work in Expo Go on Android (since SDK 53), so a dev build is needed. | https://expo.dev/changelog , https://docs.expo.dev/versions/latest/sdk/notifications/ | checked 2026-10-10

## 2. Local database (native + web)

- **expo-sqlite web support is still "alpha and may be unstable"**. It needs Metro configured for `.wasm` and the COOP/COEP headers that enable SharedArrayBuffer. On EAS Hosting these headers are set through the `expo-router` plugin `headers` option (`credentialless` + `same-origin`). Not supported on web: the `directory` param, `withExclusiveTransactionAsync`, extensions, and the `localStorage` shim (no-op). | https://docs.expo.dev/versions/latest/sdk/sqlite/ | checked 2026-10-10
- The expo-sqlite web implementation runs **wa-sqlite (WASM) in a Web Worker on OPFS `AccessHandlePoolVFS`**, with MemoryVFS for in-memory databases. Inference: AccessHandlePool takes exclusive handles, so multi-tab use is a risk. | https://github.com/expo/expo/blob/sdk-57/packages/expo-sqlite/web/worker.ts | checked 2026-10-10
- expo-sqlite has a session/changeset extension (`createSessionAsync`, changesets as Uint8Array) on all platforms including web. Change listeners need `enableChangeListener: true`. `syncLibSQL` exists in SDK 57 but is removed in SDK 58. | https://docs.expo.dev/versions/latest/sdk/sqlite/ , https://expo.dev/changelog/sdk-58-beta | checked 2026-10-10
- **Drizzle + expo-sqlite** migrations work like this: `drizzle-kit generate` with `driver: 'expo'`, then `babel-plugin-inline-import` for `.sql`, `sql` added to Metro `sourceExts`, and the `useMigrations(db, migrations)` hook. `useLiveQuery` needs `enableChangeListener`. The docs page does not mention web. drizzle-orm stable is 0.45.4 and 1.0 is in beta (`1.0.0-beta.22`). | https://orm.drizzle.team/docs/connect-expo-sqlite , npm `drizzle-orm` | checked 2026-10-10
- **op-sqlite** 18.2.5 (2026-09-20, active). The README claims "iOS, Android, macOS and web support", plus SQLCipher, libSQL/Turso, FTS5, sqlite-vec and reactive queries. Requires a dev build (no Expo Go). Web maturity is UNVERIFIED (docs web page 404). | https://github.com/OP-Engineering/op-sqlite , npm | checked 2026-10-10
- **WatermelonDB** is effectively stalled. Latest is 0.28.0 (2025-04-07), and the last publish was 0.28.1-0 on 2025-07-24. Web via the LokiJS adapter is UNVERIFIED for current versions. | npm `@nozbe/watermelondb` | checked 2026-10-10
- **TinyBase** 10.0.1 (2026-09-24, active). Has expo-sqlite persisters (the docs call the modern one "experimental") and IndexedDB/remote persisters for web. | npm, https://tinybase.org/api/persister-expo-sqlite | checked 2026-10-10
- **LiveStore** 0.4.0 (2026-06-02). Event-sourced, with adapters for Web, Expo, Node and others. Sync backends: Cloudflare, ElectricSQL, S2, or custom. The docs are "still work in progress", so it is pre-1.0. | https://docs.livestore.dev/ , npm | checked 2026-10-10
- **Legend-State**: stable `latest` is still 2.1.15 (2024-08-30). v3 is in beta (`3.0.0-beta.48`, 2026-07-12). Its v3 plugin list (expo-sqlite, Supabase, etc.) is UNVERIFIED (docs page did not render). | npm | checked 2026-10-10
- **RxDB** 17.6.0 (2026-10-05). Its SQLite storage works on Expo via expo-sqlite, but the example imports from `rxdb-premium`, so free vs paid for mobile storage is unclear (UNVERIFIED). The Expo Filesystem storage is premium. | https://rxdb.info/react-native-database.html , npm | checked 2026-10-10

## 3. Sync engines

- **PowerSync**: Postgres (incl. Supabase), MongoDB, MySQL and SQL Server feed client SQLite. Writes go through your own backend (for Supabase, via supabase-js / Data API) from a local upload queue, so offline writes are supported. **Sync Streams** are production-ready and recommended over Sync Rules (Feb 2026); they define per-user row access. | https://docs.powersync.com/integrations/supabase , https://powersync.com/blog/powersync-changelog-february-2026.md | checked 2026-10-10
- PowerSync pricing: **Free $0** (2 GB synced/mo, 500 MB hosted, 50 peak concurrent clients, 2 instances; deprovisioned after ~1 week inactive). Pro from $49/mo, Team from $599/mo. **Self-host "Open Edition" is free and source-available** (license name not stated). | https://powersync.com/pricing.md | checked 2026-10-10
- PowerSync on RN uses OP-SQLite (`@powersync/op-sqlite`), which requires a dev build; `@powersync/adapter-sql-js` covers Expo Go. **React Native Web support is still beta** and uses `@powersync/web` (wa-sqlite). No expo-sqlite adapter was found. Latest versions: @powersync/react-native 2.3.1, @powersync/web 2.4.2. | https://docs.powersync.com/client-sdks/frameworks/react-native-web-support.md , https://docs.powersync.com/client-sdks/frameworks/expo-go-support , npm | checked 2026-10-10
- Supabase Data API change: since 2026-05-30, new projects do not expose `public` tables to the Data API by default, and this is **enforced on existing projects from 2026-10-30**. This affects PowerSync's Supabase write path. | https://docs.powersync.com/integrations/supabase (citing Supabase) | checked 2026-10-10
- **ElectricSQL** is read-path sync only ("does not do write-path sync"), so writes go through your own API. Offline writes require local DB patterns, e.g. TanStack DB 0.6 (2026-03-25), which adds SQLite persistence and offline transactions for RN/Expo via op-sqlite. Electric Cloud pricing is pay-as-you-go: $0 base, bills under $5/mo waived (~5M writes free), $1 per 1M writes. Pro is $249/mo. Self-host: Apache 2.0. | https://electric.ax/docs/guides/writes , https://electric-sql.com/blog/2026/04/02/electric-cloud-pricing , https://tanstack.com/blog/tanstack-db-0.6-app-ready-with-persistence-and-includes | checked 2026-10-10
- **Zero (Rocicorp)** 1.0 shipped 2026-03-24 (now 1.10.0) and is declared stable. Postgres-backed with query-based permissions. Supports React Native/Expo. **"Zero does not support offline writes"**: writes queue only for about 1 minute while connecting, then are rejected. Hosting pricing is UNVERIFIED. | https://zero.rocicorp.dev/docs/connection.md , https://zero.rocicorp.dev/docs/release-notes/1.0 , https://zero.rocicorp.dev/docs/react-native , npm | checked 2026-10-10
- **InstantDB is sunsetting.** The team joined OpenAI (announced 2026-08-22). Cloud signups are closed, cloud apps shut down 2027-08-31, and the code remains open source and self-hostable. **Avoid.** | https://www.instantdb.com/ (banner), https://www.instantdb.com/pricing | checked 2026-10-10
- **Triplit** is effectively unmaintained. Its co-founder joined Supabase on 2025-10-08, and the last npm publish of `@triplit/client` was 1.0.50 on 2025-07-31. **Avoid.** | https://supabase.com/blog/triplit-joins-supabase , npm | checked 2026-10-10
- **Convex** has no built-in persistent offline or local-first mode for end users. Optimistic updates are not persisted, and the "object sync engine" is still in development (UNVERIFIED if shipped). PowerSync added Convex as an **experimental** source on 2026-06-10. Free plan: 1M function calls/mo, 0.5 GB DB, 1 GB DB I/O, 1–6 devs. Pro: 25M calls, 50 GB. | https://docs.convex.dev/production/state/limits , https://releases.powersync.com/announcements/ann_ZLQJV3dnA4HR0 | checked 2026-10-10
- **Jazz**: "Jazz 2" is a relational DB with a Rust engine (WASM in browser, native module in RN) and RLS policies in TypeScript over JWT claims. Writes are local-first. Supports React Native (Expo) and web. Pricing: included 1 GB RAM instance, 1 GB storage, 5 GB egress, then usage. The server is open source and self-hostable. **But npm `latest` is still 0.20.19 ("classic", 2026-07-03), and v2 is `2.0.0-alpha.59`, so v2 is alpha.** | https://jazz.tools/ , npm `jazz-tools` | checked 2026-10-10
- Fit, one line each (relational / per-user rules / offline writes / Expo native + web):
  - PowerSync: yes / yes (Sync Streams) / yes / native GA, web beta. **Best fit.**
  - Electric (+ TanStack DB): yes / via shapes + your API / DIY / yes.
  - Zero: yes / yes / **no** / yes.
  - Convex: doc-relational / yes / **no** / yes.
  - Jazz 2: yes / yes / yes / alpha.
  - LiveStore: event-sourced / DIY / yes / yes, pre-1.0.
  - InstantDB: **sunsetting**.
  - Triplit: **dead**.

## 4. NativeWind / React Native Reusables

- **NativeWind stable is 4.2.7** (2026-09-14) and uses **Tailwind CSS v3** (`tailwindcss@^3.4.17`). 4.2.7 adds Expo SDK 57 support; on SDK 57 you install react-native-worklets alongside Reanimated 4. | https://www.nativewind.dev/docs/getting-started/installation , npm | checked 2026-10-10
- **NativeWind v5 is a release candidate** (`5.0.0-rc.0`, 2026-09-13, `preview` tag). It requires Tailwind >4.1.11 and `react-native-css` 3.1.0-rc.0, RN 0.81+ and Reanimated 4+. Babel config is removed and Tailwind v4 CSS imports are used. | npm `nativewind`, https://www.nativewind.dev/v5/guides/migrate-from-v4 | checked 2026-10-10
- **Uniwind** 1.12.2 (2026-10-05) is a Tailwind v4 alternative. Peers: `tailwindcss >=4`, `react-native >=0.81`. | npm `uniwind` | checked 2026-10-10
- **React Native Reusables** is active (last commit 2026-09-27, ~8.7k stars). It supports **two styling libraries: NativeWind (v4 / Tailwind 3) and Uniwind (Tailwind 4)**, with separate registries `packages/registry/src/nativewind` and `/uniwind`. CLI `@react-native-reusables/cli` is at 0.7.1. Commands: `init` (templates `minimal`, `minimal-uniwind`, `clerk-auth`) and `add <component>` with `--styling-library nativewind|uniwind`. There is no NativeWind v5 support found. | https://github.com/founded-labs/react-native-reusables , https://github.com/founded-labs/react-native-reusables/blob/main/apps/docs/content/docs/cli.mdx | checked 2026-10-10
- The RNR templates still target **Expo SDK 56** (expo ~56.0.13, RN 0.85.3; last updated 2026-07-02). The `minimal` template uses nativewind ^4.2.6 and tailwindcss ^3.4.14; `minimal-uniwind` uses uniwind ^1.9.0 and tailwindcss ^4.2.1. SDK 57 support in the templates is UNVERIFIED. | https://github.com/founded-labs/react-native-reusables-templates | checked 2026-10-10
- Lucide: `lucide-react-native` is now 1.55.0 (v1.x), but RNR pinned/downgraded to 0.577.0 in June 2026. Check icon compatibility. | npm, RNR commit log 2026-06-19 | checked 2026-10-10

## 5. Reanimated / Worklets / Gesture Handler

- Latest versions are react-native-reanimated 4.7.1 (2026-10-02), react-native-worklets 0.13.0 and react-native-gesture-handler 3.3.0 (2026-09-11). GH 2.x is still patched (v2.33.0, 2026-09-14). | npm, https://github.com/software-mansion/react-native-gesture-handler/releases | checked 2026-10-10
- **SDK 57 bundles Reanimated 4.5.1, Worklets 0.10.1 and Gesture Handler ~2.32.0** (still v2). SDK 58 bundles Reanimated 4.7.0, Worklets 0.13.0 and **GH ~3.2.1**. | bundledNativeModules.json (57.0.27, 58.0.7) | checked 2026-10-10
- Reanimated 4 is New Architecture only. Compatibility: 4.5.x supports RN 0.83–0.86 with worklets 0.10/0.11; 4.7.x supports RN 0.86–0.88 with worklets 0.13. | https://docs.swmansion.com/react-native-reanimated/docs/guides/compatibility/ | checked 2026-10-10
- Reanimated runs on web in pure JS, so it is slower than native. Keep the `react-native-worklets/plugin` Babel plugin; it is the only tested configuration. | https://docs.swmansion.com/react-native-reanimated/docs/guides/web-support/ | checked 2026-10-10
- Gesture Handler 3.0.0 (2026-05-28) is a hook-based API that is New-Arch only and requires min RN 0.82. Callbacks are renamed (onStart→onActivate, onEnd→onDeactivate). GH3 web support is UNVERIFIED (docs did not render; GH2 supported web). | https://github.com/software-mansion/react-native-gesture-handler (README), https://swmansion.com blog "Introducing Gesture Handler 3.0" | checked 2026-10-10

## 6. i18n

- Versions: i18next 26.4.3, react-i18next 17.0.16, @lingui/core and @lingui/metro-transformer 6.9.1 (Lingui 6 is out), expo-localization 57.0.2. | npm | checked 2026-10-10
- **Hermes Intl supports** Collator, NumberFormat, DateTimeFormat, getCanonicalLocales and the `toLocale*` methods. It does **not list PluralRules, Locale, RelativeTimeFormat or ListFormat**. iOS lacks compact notation in NumberFormat. The doc was last changed 2025-01-30, and Hermes V1 Intl changes are UNVERIFIED. | https://github.com/facebook/hermes/blob/main/doc/IntlAPIs.md | checked 2026-10-10
- **i18next v4 JSON plurals need `Intl.PluralRules`**: "You may need to polyfill ... (e.g. React Native on Hermes)". Since v24 there is no v3 fallback. | https://www.i18next.com/misc/json-format | checked 2026-10-10
- **Lingui on RN** needs Hermes (RN 0.76+ / Expo 52+) plus polyfills `@formatjs/intl-locale` and `@formatjs/intl-pluralrules` (import `/polyfill-force`). `@lingui/metro-transformer` is optional and compiles `.po` files in Metro. | https://lingui.dev/tutorials/react-native | checked 2026-10-10
- `expo-localization` provides `getLocales()` and `getCalendars()`, plus per-app language via the `supportedLocales` config plugin option. Expo's guide lists i18n-js, Lingui, react-i18next, fbtee and Intlayer as options. | https://docs.expo.dev/guides/localization/ | checked 2026-10-10

## 7. State management

- Zustand 5.0.15 (2026-08-13), **Jotai 3.0.1** (2026-09-29; new major), and @tanstack/react-query and query-async-storage-persister 5.104.1 (2026-10-02). Legend-State: see §2. | npm | checked 2026-10-10
- TanStack Query on RN: wire `onlineManager` to NetInfo or expo-network, and `focusManager` to AppState. | https://tanstack.com/query/latest/docs/framework/react/react-native | checked 2026-10-10

## 8. Testing / CI

- Versions: jest-expo 57.0.5, @testing-library/react-native **14.1.0** (2026-10-08), @playwright/test 1.64.0, detox 20.51.4 (2026-06-16; repo active, pushed 2026-10-05). | npm, https://github.com/wix/Detox | checked 2026-10-10
- Expo docs recommend `jest-expo` with RNTL; `react-test-renderer` is deprecated with React 19. For UI, Expo recommends E2E tests with **Maestro via EAS Workflows** instead of snapshots. Playwright is not mentioned in Expo's testing docs. | https://docs.expo.dev/develop/unit-testing/ | checked 2026-10-10
- **EAS Workflows** is EAS CI/CD defined in YAML under `.eas/workflows/`. Job types: build, submit, update, fingerprint/get-build, **maestro** and custom. Triggers: GitHub events, cron, manual, API. | https://docs.expo.dev/eas/workflows/introduction/ | checked 2026-10-10
- Maestro inside EAS Workflows: **not available on Free**; on paid plans it costs $0.05 per job plus CI minutes. Free plan includes 60 CI/CD minutes. Per-minute rates: Linux medium $0.018/min, macOS medium $0.075/min. | https://expo.dev/pricing | checked 2026-10-10
- **Maestro Cloud** costs $250 per device per month (Android, iOS or web), plus custom Enterprise. The CLI and Maestro Studio are free and open source for local devices. | https://maestro.dev/pricing | checked 2026-10-10

## 9. EAS pricing

- **Free**: up to 15 Android + 15 iOS builds/mo, low-priority queue, 1 concurrency, 45-min timeout, **1,000 Update MAUs** (hard cap), 60 Workflows minutes, Hosting 100k requests/mo, **no custom domain**. | https://expo.dev/pricing | checked 2026-10-10
- **Starter $19/mo** + usage: $45 build credit (Android $1/$2, iOS $2/$4 per build), high priority, 1 concurrency, **3,000 MAUs**, custom domain (1/project). **Production $199/mo**: $225 credit, 2 concurrency, **50,000 MAUs**. Enterprise: 1M MAUs. MAU overage starts at $0.005/MAU. | https://expo.dev/pricing | checked 2026-10-10
- **EAS Hosting** runs on Cloudflare Workers and serves Expo Router web in `single`, `static` and `server` (API routes) modes. All plans include 100k requests and 1M CPU-ms per month; paid overage is $2 per 1M requests. Custom domains require a paid plan. | https://docs.expo.dev/eas/hosting/introduction/ , https://expo.dev/pricing | checked 2026-10-10
- `.well-known` files are served from `public/.well-known/` in an Expo Router project and deployed with EAS Hosting. Expo's guide shows `apple-app-site-association`. `assetlinks.json` is not shown explicitly, though the same mechanism applies (UNVERIFIED). | https://expo.dev/blog/universal-and-app-links | checked 2026-10-10
- **EAS Submit to Google Play**: the current manual-submission page says "A manual upload is optional". It also says `eas submit` "can create your app's first release directly", by default on the internal track (page modified 2026-07-17). Older EAS Submit pages still say a manual first upload is required, so the docs conflict. | https://docs.expo.dev/submit/android-manual.md , https://docs.expo.dev/submit/introduction | checked 2026-10-10

## 10. Push notifications

- The Expo push service is **free**, with a rate limit of 600 notifications/sec per project. | https://docs.expo.dev/push-notifications/faq/ | checked 2026-10-10
- Android push uses the **FCM V1** protocol, which requires uploading a Google Service Account JSON key to EAS. | https://docs.expo.dev/push-notifications/fcm-credentials/ | checked 2026-10-10
- `expo-notifications` platforms are Android and iOS only, so there is **no web push** via Expo. Web push would need its own Web Push / service worker implementation. | https://docs.expo.dev/versions/latest/sdk/notifications/ | checked 2026-10-10
- SDK 58: foreground notifications show by default. | https://expo.dev/changelog/sdk-58-beta | checked 2026-10-10

## 11. Crash reporting

- `@sentry/react-native` 8.30.0 is the latest; SDK 57 bundles ~7.11.0 and SDK 58 ~8.28.0. It has the Expo config plugin `@sentry/react-native/expo` and Metro `getSentryExpoConfig`. Source maps upload automatically during EAS builds (`SENTRY_AUTH_TOKEN` as an EAS secret). | https://docs.sentry.io/platforms/react-native/manual-setup/expo/ , npm | checked 2026-10-10
- `@sentry/react-native` **supports web via react-native-web**, with browser integrations added automatically. `sentry-expo` has been deprecated since SDK 50. | https://docs.sentry.io/platforms/react-native/migration/sentry-expo/ | checked 2026-10-10
- **Sentry Developer (free)**: $0, 1 user, 5k errors, 5M spans, 50 replays, 5 GB logs, 1 GB attachments, 1 cron + 1 uptime monitor. Team is $26/mo (annual) with 50k errors. | https://sentry.io/pricing/ | checked 2026-10-10
- **Crashlytics** needs `@react-native-firebase/crashlytics` (26.4.0) with a dev build and config plugin; it does not work in Expo Go. It is native-only; on web RNFirebase falls back to the firebase-js-sdk, which has no Crashlytics. | https://rnfirebase.io/ , npm | checked 2026-10-10
- Alternative: **EAS Observe** went GA on 2026-08-20 and has recorded native crashes alongside JS errors since 2026-10-07 (SDK 57, expo ≥57.0.21). Free plan: 100K events/mo. | https://expo.dev/changelog , https://expo.dev/pricing | checked 2026-10-10

## 12. Contacts / Photos

- **expo-contacts**: the object-based API (previewed as `expo-contacts/next` in SDK 55) became **stable in SDK 56 at the root import**. The old API is deprecated and lives at `expo-contacts/legacy`. The package still exports `./next`. Platforms: Android and iOS; no web. | https://expo.dev/changelog/sdk-56.md , https://docs.expo.dev/versions/latest/sdk/contacts/ , https://github.com/expo/expo/blob/sdk-57/packages/expo-contacts/package.json | checked 2026-10-10
- iOS 18 limited contacts: `accessPrivileges: 'all' | 'limited' | 'none'`, `Contact.presentAccessPicker()` and `ContactAccessButton` (iOS 18+). `Contact.presentPicker()` opens the native picker on Android and iOS. | https://docs.expo.dev/versions/latest/sdk/contacts/ | checked 2026-10-10
- **Android 17 (API 37)** adds a system Contact Picker (`Intent.ACTION_PICK_CONTACTS`). Google Play policy: apps targeting API 37+ may request `READ_CONTACTS` only if the picker is insufficient, and need a declaration form. Console prompts started September 2026; **compliance is mandatory 2027-01-27**. Note: secondary sources said 2026-10-28; the official page says 2027-01-27. Expo support for `ACTION_PICK_CONTACTS` is UNVERIFIED. | https://support.google.com/googleplay/android-developer/answer/16935362?hl=en , https://android-developers.googleblog.com/2026/03/contact-picker-privacy-first-contact.html | checked 2026-10-10
- **expo-image-picker on Android uses the system Photo Picker** (`ActivityResultContracts.PickVisualMedia`) and declares **no READ_MEDIA_IMAGES**. It only declares CAMERA and READ/WRITE_EXTERNAL_STORAGE with maxSdk 32; `legacy: true` switches to ACTION_GET_CONTENT. It works on web, where it must be triggered by a user gesture. | https://github.com/expo/expo/blob/sdk-57/packages/expo-image-picker/android/src/main/AndroidManifest.xml , https://docs.expo.dev/versions/latest/sdk/imagepicker/ | checked 2026-10-10
- Google Play Photo/Video policy: only apps with core broad-media needs may request READ_MEDIA_IMAGES/VIDEO (mandatory since 2025-05-28). **expo-media-library** is for gallery-style access and declares `READ_MEDIA_VISUAL_USER_SELECTED`. Avoid it for a simple photo pick. | https://support.google.com/googleplay/android-developer/answer/14115180?hl=en , https://github.com/expo/expo/blob/sdk-57/packages/expo-media-library/android/src/main/AndroidManifest.xml | checked 2026-10-10

## 13. Excel / CSV

- **SheetJS current is 0.20.3** and is distributed only from the SheetJS CDN (`npm i https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`). npm `xlsx` is stuck at 0.18.5 (2022-03-24), which SheetJS calls out of date. | https://docs.sheetjs.com/docs/getting-started/installation/frameworks , https://cdn.sheetjs.com/xlsx.lst | checked 2026-10-10
- **exceljs** 4.4.0 is stale: last npm publish 2023-10-19, repo last pushed 2025-01-21, 816 open issues. | npm, https://github.com/exceljs/exceljs | checked 2026-10-10
- **read-excel-file** 9.3.12 (2026-10-07) is active, read-only and lightweight (deps: fflate, saxen). | npm | checked 2026-10-10
- **papaparse** 5.7.0 (2026-08-24) is active. | npm | checked 2026-10-10
