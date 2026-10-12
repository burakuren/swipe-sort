# Public open-source repo from day one

The repo became public on 2026-10-12, before any app code, instead of "private first, maybe public after the
first release" (D-26). The code is licensed AGPL-3.0-or-later and the docs, design and sample data CC BY 4.0;
the name, logo and brand are not licensed. AGPL means a modified hosted copy must publish its changes, which
fits the self-hosting stance (D-29, D-30). A CLA keeps the app-store and relicensing options open (Signal's
model). Public visibility also makes GitHub-hosted CI and macOS runners free (D-25).

## Considered options

- Stay private until the first release (D-26 as written): CI minutes run out under unattended agent work, and
  the history rewrite only gets harder with time.
- MIT or Apache-2.0: simpler, but allows a closed clone, which matters before the name is protected.
- No licence (source-visible only): not open source.

## Consequences

- Everything committed is published. The repo holds what contributors need: code, design, `GLOSSARY.md`, ADRs,
  build decisions and technical research. What only the founder needs (release plan with dates, testers and
  legal steps, the name shortlist, founder agent rules) lives in a private companion repo cloned into a
  gitignored `private/` folder, loaded through a gitignored `CLAUDE.local.md`.
- No real personal data in the repo: sample people are fictional (`example.com`, fake numbers), device
  artifacts come only from the preview build, and feedback from testers reaches Issues only scrubbed.
- Outside input goes to GitHub Discussions; Issues are the maintainer's work tracker, and issues from
  non-collaborators are closed with a pointer to Discussions. Outside PRs open after M1: each must link a
  `help wanted` issue, its author signs the CLA, fork CI runs only after approval and never gets secrets, and a
  merge needs the maintainer's `maintainer-approved` label.
- History was rewritten once, before the first push: noreply author email, generated screenshots and files
  that moved to `private/` removed. Screenshots are generated, not committed.
- Third-party agent skills are restored from `skills-lock.json`, not committed, so cloud agent sessions see
  them only after that install step.
