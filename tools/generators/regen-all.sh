#!/usr/bin/env bash
# Regenerates every screen file in design/03-screens from its generator (order matters:
# S25 and S08–S10 first, because other generators copy their markup).
set -euo pipefail
cd "$(dirname "$0")/../.."
S=design/03-screens
run() { echo "→ $*"; python3 "$@" > /dev/null; }
run tools/generators/S25-sorting.py $S/S25-sorting.html
run tools/generators/S08-S10-lists.py
for g in S01-splash S02-onboarding S03-sign-in S04-forgot-password S05-sign-in-prompt S06-settings S07-profile; do run tools/generators/$g.py; done
run tools/generators/S11-S15-import.py
for g in S16-plain-text S17-manual-entry S18-photos-import S19-field-mapping S20-duplicate-review S21-add-items; do run tools/generators/$g.py; done
run tools/generators/S22-S23-templates.py
for g in S24-start-round S26-item-detail S27-round-summary; do run tools/generators/$g.py $S/$g.html; done
run tools/generators/S28-S30-results.py
run tools/generators/S31-S34-collaboration.py
run tools/generators/S35-S38-collaboration.py
run tools/generators/S39-export.py $S/S39-export.html
run tools/generators/S40-global-patterns.py $S/S40-global-patterns.html
echo "regen-all OK"
