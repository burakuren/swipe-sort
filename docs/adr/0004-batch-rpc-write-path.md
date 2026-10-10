# Client writes go through one batch RPC function, not direct table writes

PowerSync's Supabase integration guide uploads queued writes as direct table writes through the Data API
(supabase-js, explicit grants, RLS). We instead send each upload batch to **one Postgres function,
`api.apply_ops(batch)`**, called with `supabase.rpc()`. Direct table writes return a permission error (4xx)
when RLS denies a write, which PowerSync says blocks its upload queue, so the client would have to discard the
write silently. The function meets PowerSync's general backend recommendations (batch endpoint, synchronous
writes, 2xx plus a synced error table for validation failures) and Supabase's Data API hardening guidance
(expose only a dedicated `api` schema; keep tables in unexposed schemas; explicit EXECUTE grants).

Properties:

1. `uploadData` sends a batch via `supabase.rpc('apply_ops', { batch })`.
2. `security invoker`: RLS still applies to every row the function touches (defense in depth).
3. Membership, role and "conflict still open" are checked explicitly first; a failing op is skipped, an
   outcome row is written (`write_outcomes`), and the response is 2xx.
4. Only unexpected errors (bugs) raise, which blocks that client's queue and alerts crash reporting.
5. Deduplication by (client id, op id); the whole batch runs in one transaction.

## Considered Options

- **Direct table writes + grants + RLS (the integration guide's path):** simplest, but rejected writes are
  silently discarded, no op-id dedup, and every table must be exposed to the Data API.
- **One Edge Function in TypeScript:** could share domain code with the app, but adds cold starts and a hop
  on the hot sync path.

## Consequences

List-status and conflict-rule logic exists twice: TypeScript on the device (statuses offline) and SQL on
the server (the authority). One shared JSON test-vector file must pass against both in CI. Online-only
commands (ADR-0001 rule 4) are also functions in the `api` schema, called directly rather than queued.
