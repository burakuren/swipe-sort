# PowerSync over Postgres as the single sync stack

Sync between devices and the server uses **PowerSync** with **Postgres** as the source database, on every
platform. Mobile uses `@powersync/react-native` with op-sqlite (SQLCipher available); web uses
`@powersync/web` (wa-sqlite in a Web Worker, IndexedDB/OPFS). Reads stream Postgres → PowerSync Service →
device; writes go device → our own API → Postgres, so business rules and validation stay in our code
(ADR-0001 rule 3). We chose it over writing our own sync because membership-driven partial sync,
resumable initial sync and convergence are off the shelf, op-sqlite is the fastest and encryptable SQLite
on mobile, and the web SDK avoids expo-sqlite's alpha web build. It wins on mobile merits alone; web was a
tie-breaker.

## Considered Options

- **Own sync (expo-sqlite + Drizzle + our push/pull protocol):** no extra service, full schema freedom; but
  every sync edge case is ours and expo-sqlite web is alpha (needs COOP/COEP).
- **Electric + TanStack DB:** the only other Postgres option with offline writes; two young pieces to
  assemble, shapes without joins. Recorded only as a whole-app replacement if PowerSync ever fails us.
- **Zero, Convex:** no persisted offline writes. **Jazz 2:** alpha, not Postgres. **LiveStore:** pre-1.0,
  event-sourced. **RxDB:** mobile SQLite storage appears paid. **WatermelonDB:** stalled.
  **InstantDB, Triplit:** shutting down / dead.

## Consequences

- One stack per concern: no platform-specific second sync stack. If the web pairing (RN-web glue, labeled
  beta) fails the day-1 spike: fix within PowerSync → degrade web on the same stack (in-memory DB, online
  web) → drop the feature on web → only then a second stack.
- Default PowerSync tables are JSON-backed views (text UUID ids, no local foreign keys); use raw tables
  where real SQLite tables are needed. Constraints live on the server.
- The main database must be Postgres with logical replication. PowerSync connects directly (Supabase direct
  connections are IPv6-only).
- PowerSync Cloud Free during development (sleeps after a week idle); self-hosted Open Edition (FSL) from
  public launch, Cloud Pro only as a fallback (build-decisions D-29). Same protocol, so switching needs no app
  change.
- Dev builds only (no Expo Go).
