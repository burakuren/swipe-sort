# Contributing to SwipeSort

Thanks for your interest. SwipeSort is a small project run by one maintainer, and most of its code and docs
are written by Claude Code (Anthropic) under the maintainer's direction. The rules below keep that workable.
Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Where things go

| You want to… | Go to |
| --- | --- |
| Report a bug | [Discussions › Bug reports](https://github.com/burakuren/swipe-sort/discussions/categories/bug-reports) |
| Suggest a feature or change | [Discussions › Ideas](https://github.com/burakuren/swipe-sort/discussions/categories/ideas) |
| Ask a question | [Discussions › Q&A](https://github.com/burakuren/swipe-sort/discussions/categories/q-a) |
| Report a security problem | Privately, see [SECURITY.md](SECURITY.md). Never in public. |

**Issues are the maintainer's work tracker only.** Issues opened by anyone who is not a collaborator are
closed automatically with a pointer to Discussions. When a discussion leads to work, the maintainer opens an
issue for it and links back.

Never paste real personal data (contacts, guest lists, phone numbers) into a discussion, screenshot or test
file. Use made-up examples.

## Pull requests

**Until milestone M1 ends, pull requests from outside contributors are closed automatically.** The project
is still finding its shape and cannot review outside code yet. Ideas are very welcome in Discussions
meanwhile.

After M1, pull requests are welcome under these rules:

1. **Link an issue labelled `help wanted`.** Pick one, say in the issue that you are taking it, and write
   `Closes #<number>` in the PR description. Pull requests without such an issue are closed.
2. **Sign the [Contributor Licence Agreement](CLA.md).** The CLA Assistant bot asks you to sign once, with a
   comment on your first pull request. The CLA lets the maintainer ship the AGPL code through app stores and
   relicense it later; you keep the copyright to your work.
3. **CI runs after approval.** Workflows on pull requests from forks start only after the maintainer approves
   them, and they never receive repository secrets.
4. **Review.** Claude reviews every pull request against the linked issue, `GLOSSARY.md` and the ADRs; the
   maintainer reads that review and decides.
5. **Merge.** A pull request is merged only once the maintainer adds the `maintainer-approved` label.

Keep pull requests small and focused on one issue, and fill in the pull request template.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/): `type(scope): summary`, for example
`feat(sorting): add undo for the last decision` or `fix(import): keep leading zeros in phone numbers`.
Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`. Release notes are generated from
these messages.

If an AI assistant wrote a meaningful part of your change, say so with a `Co-Authored-By:` trailer, as the
maintainer's commits do.

## Development setup

Design phase (now):

```bash
npm ci
npx playwright install chromium   # once
npm run qa                        # build CSS, screenshots, accessibility, click-through tests, lint
```

See [`README.md`](README.md) and [`CLAUDE.md`](CLAUDE.md) for the individual scripts and design conventions.
App setup instructions arrive with the app code.

### Agent skills

The repo uses third-party agent skills for Claude Code and other coding agents. They are not committed;
[`skills-lock.json`](skills-lock.json) pins each one by source and content hash. Restore them with the
[`skills`](https://www.npmjs.com/package/skills) CLI:

```bash
npx skills experimental_install   # restores every skill listed in skills-lock.json
```

The command name may change as the CLI matures; `npx skills --help` lists the current one.

## Language and decisions

- [`GLOSSARY.md`](GLOSSARY.md) is the shared vocabulary. Use its terms (list, item, field, source, decision…)
  in code, UI copy, issues and pull requests, and avoid the words it marks as _Avoid_.
- [`docs/adr/`](docs/adr/) holds the architecture decision records, and
  [`docs/build-decisions.md`](docs/build-decisions.md) the wider build decisions. Read the relevant ones
  before proposing a change to architecture; a change that reverses one starts as a discussion.

## Licence

By contributing you agree that your contribution is licensed under the project's licences (code under
AGPL-3.0-or-later, docs and design under CC BY 4.0) and under the terms of the [CLA](CLA.md).
