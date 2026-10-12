# SwipeSort

SwipeSort turns any list into a deck of cards that people sort one at a time with swipe gestures, alone or
together with others: right to **Accept**, left to **Reject**, up for **Maybe**. Lists come from phone
contacts, CSV or spreadsheet files, Google Sheets or plain text.

"SwipeSort" is a working name; the final name is not chosen yet.

## Status

- **Design: done.** Every screen and state, light and dark, as static HTML mockups in [`design/`](design/).
- **App: build starting.** Expo, React Native and TypeScript; Android first, then web and iOS.

There is no app code or release yet.

## Repo layout

| Path | What it is |
| --- | --- |
| [`design/`](design/) | The complete design: brief, foundations, screens, prototype, QA ([`design/README.md`](design/README.md) is the entry point) |
| [`docs/`](docs/) | Build decisions, architecture decision records ([`docs/adr/`](docs/adr/)), research |
| [`GLOSSARY.md`](GLOSSARY.md) | The shared language for UI, specs and code |
| `tools/` | Build and QA scripts for the design mockups |

## View the mockups

Open [`design/04-prototype/index.html`](design/04-prototype/index.html) in a browser. Everything works
offline from the file system; no server needed.

## Run the design QA

Needs Node.js. The scripts drive headless Chromium over `file://` URLs.

```bash
npm ci
npx playwright install chromium   # once, if Chromium is not installed yet
npm run build:css                 # Tailwind → design/assets/css/app.css
npm run shots                     # screenshots of every frame, light + dark → design/05-qa/screenshots/
npm run a11y                      # axe-core (WCAG 2.2 AA) → design/05-qa/a11y-report.md
npm run flows                     # prototype click-through tests
npm run qa                        # all of the above plus the design lint
```

Filter any script by screen ID, for example `npm run shots -- S25`. [`CLAUDE.md`](CLAUDE.md) lists every
option.

## How this project is built

Almost all code and docs are written by [Claude Code](https://claude.com/claude-code) (Anthropic) under the
founder's direction. Commits that Claude helped write carry a `Co-Authored-By: Claude` trailer. The founder
makes the product and architecture decisions, recorded in [`docs/adr/`](docs/adr/) and
[`docs/build-decisions.md`](docs/build-decisions.md).

AI-written work goes through the same gates as any other: automated accessibility checks, screenshot review
and click-through tests for the design; for the app, strict TypeScript, linting, unit, component, database
and end-to-end tests in CI, plus manual checks on a real device before each release.

## Contributing

Questions, bug reports and ideas go to [GitHub Discussions](https://github.com/burakuren/swipe-sort/discussions).
Issues are the maintainer's work tracker. Pull requests from outside contributors open after the first
milestone. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Report
security problems privately: [`SECURITY.md`](SECURITY.md).

## Licence

- **Code**: [GNU Affero General Public License v3.0 or later](LICENSE) (AGPL-3.0-or-later).
- **Docs, design mockups and sample data**: [Creative Commons Attribution 4.0](LICENSE-docs) (CC BY 4.0).
  This covers `design/`, `docs/`, Markdown files and `design/02-data/`.
- **Name, logo and brand** (including `design/01-foundations/brand/`) are not licensed; all rights reserved.
  You may not use them for your own builds or forks.
- Bundled third-party content (Inter font, Lucide icons, Tailwind CSS output) keeps its own licence; see
  [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Sample data is fictional

No real personal data is ever committed. Every person, phone number, email address and photo in the sample
data and mockups is made up; portraits are generated illustrations. Any resemblance to real people is
coincidental.
