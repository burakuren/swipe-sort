# Prototype flows

One file per flow: `tools/flows/<id>-<slug>.flow.mjs`, run with `npm run flows` (or `npm run flows -- <id>`).
See the header of `tools/flows.mjs` for the module shape. Paths passed to `open()` are relative to `/design`.
Prefer stable selectors such as `data-action="…"` or roles/text over Tailwind classes.
Failure screenshots land in `design/05-qa/flows/<flow>/`.
