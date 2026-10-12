# Release sequence: offline Android first, web with collaboration, iOS last

SwipeSort ships in six milestones (release plan, kept private: `private/docs/release-plan.md`): M1 offline guest-mode contacts sorting on
Android, M2 accounts and backup, M3 shared lists plus the web app, M4 the remaining sources and launch
completeness, M5 public launch on Google Play, M6 iOS. The founder's own guest list is the first real use, so
the number-one feature (contacts import and sorting) ships alone and offline first; the backend follows before
the other sources because sorting together is the real need and carries the architectural risk.

## Consequences

- **Web arrives with collaboration (M3), long before iOS.** iPhone users can only join a shared list through
  the web until M6, so web cannot wait (COL-04, SUC-05).
- **Sign in with Apple arrives in M6 on every platform at once**, not with the other sign-in methods in M2: the
  Android and web flow needs an Apple Services ID, which needs the Apple Developer Program (D-04). With no iOS
  app before M6 there are no Apple accounts to strand, so D-13's intent holds.
- **The 14-day Play closed test runs on the feature-complete M4 build**, not an early one: Google's
  production-access form asks whether testers used every feature and rejects for low engagement. The first
  closed-track release goes out at the end of M3 with only the founder and a second member, to absorb the extended
  first review for new accounts.
- Features not built yet are hidden in the UI (no "coming soon"); platform-unavailable features appear as
  designed (PLT-11).

## Considered Options

- **Backend first (accounts, then sorting):** data safety from day one, but the founder's first real use comes
  months later.
- **Accounts and collaboration in one milestone:** fewer milestones, one very large one, backup later.
- **iOS before public launch:** needs Apple enrollment now and delays Android, the Fixed first platform.
