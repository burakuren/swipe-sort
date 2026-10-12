# Real user data only ever lives in permanent homes

Once anyone's real data (the founder's guest list, later closed testers' lists) is in a build or a backend,
that home must survive to production; no throwaway package id or test backend holds real data.

1. **The Android package id is fixed before the founder puts real data into M1**, not only before the first
   Play upload (D-02's gate): a new package id is a new app and would wipe device-only lists. If no final name
   exists then, the D-02 fallback `com.burakuren.swipesort` is used permanently; the display name can still
   change.
2. **From M2, real data goes to the production environment** (D-25): the production Supabase project starts on
   the Free plan (allowed by D-30) and is upgraded to Pro in place at public launch; PowerSync moves from
   Cloud Free to self-hosted against the same database (D-29). The closed test runs on production builds.
   The preview environment holds test data only.

## Consequences

- Changes D-02's package-name gate (earlier) and makes explicit which Supabase project D-30's "Free during
  development and the closed test" refers to.
- The production database needs the scheduled `db dump` (D-30) and keep-alive from M2, since it holds real data
  on a free plan.
- Every milestone's definition of done includes an upgrade test from the previous milestone's last release.
