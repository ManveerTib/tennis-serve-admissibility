#!/usr/bin/env bash
#
# Applies the four blocking changes before publishing the README.
# Run from the repository root.
#
#   bash apply_blocking_changes.sh
#
# Requires: README.md and LICENSE downloaded into this directory
# from the chat, as README_new.md and LICENSE respectively.

set -euo pipefail

if [ ! -d .git ]; then
  echo "ERROR: run this from the repository root (no .git directory found)."
  exit 1
fi

if [ ! -f README_new.md ]; then
  echo "ERROR: README_new.md not found. Download the new README from the chat,"
  echo "       rename it to README_new.md, and place it in the repo root."
  exit 1
fi

if [ ! -f LICENSE ]; then
  echo "ERROR: LICENSE not found. Download it from the chat into the repo root."
  exit 1
fi

echo "==> 1/4  Moving current README to research_note.md"
git mv README.md research_note.md

echo "==> 2/4  Renaming continuation.py to boundary_solver.py"
git mv src/continuation.py src/boundary_solver.py
# Nothing imports this module (verified: 0 references in tests/ and notebooks/),
# so no import statements need updating.

echo "==> 3/4  Removing the superseded, contradictory heatmap"
if [ -f figures/supporting/19_spin_azimuth_heatmap_alternate.png ]; then
  git rm -q figures/supporting/19_spin_azimuth_heatmap_alternate.png
else
  echo "     (already removed, skipping)"
fi

echo "==> 4/4  Installing the new README and LICENSE"
mv README_new.md README.md
git add README.md LICENSE

echo
echo "==> Verifying: every image referenced by README.md exists on disk"
missing=0
grep -oE '(\!\[[^]]*\]\(|src=")figures/[^")]+' README.md \
  | sed -E 's/^(\!\[[^]]*\]\(|src=")//' \
  | sort -u \
  | while read -r img; do
      if [ ! -f "$img" ]; then
        echo "     MISSING: $img"
        missing=1
      fi
    done
[ "$missing" -eq 0 ] && echo "     all referenced figures present"

echo
echo "==> Verifying: files referenced by README.md exist"
for f in research_note.md data/README.md LICENSE requirements.txt; do
  if [ -f "$f" ]; then echo "     ok        $f"; else echo "     MISSING:  $f"; fi
done

echo
echo "==> Running the test suite"
python -m pytest -q

echo
echo "==> Staged changes:"
git status --short

cat <<'EOF'

Next, review and commit:

    git add -A
    git commit -m "Restructure README with embedded figures; move full write-up to research_note.md; rename boundary solver; add MIT license"
    git push

Then open the repo page and confirm:
  - LaTeX renders (GitHub needs $$ ... $$)
  - all 22 figures load
  - the CI badge shows passing
EOF
