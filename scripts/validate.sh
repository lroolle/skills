#!/usr/bin/env bash
# validate.sh -- the proof behind the README's claims.
# For every skill: frontmatter name matches its directory, body is
# <= 500 lines, description is <= 1024 chars, and it is registered
# in plugin.json and listed in README.md. Exits non-zero on any
# failure, so CI and readers get the same verdict.
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0
printf '%-12s %7s %7s %8s %8s  %s\n' skill lines desc plugin readme verdict
for dir in skills/*/; do
  name=$(basename "$dir")
  fm_name=$(awk '/^name:/{print $2; exit}' "$dir/SKILL.md")
  lines=$(wc -l < "$dir/SKILL.md")
  desc=$(awk '/^description:/{f=1; next} f && /^[a-zA-Z_-]+:/{exit} f && /^---/{exit} f {gsub(/^ +| +$/, ""); printf "%s ", $0}' "$dir/SKILL.md")
  desc_len=${#desc}
  in_plugin=$(grep -c "\"./skills/$name\"" .claude-plugin/plugin.json || true)
  in_readme=$(grep -c "skills/$name/SKILL.md" README.md || true)

  verdict=ok
  [ "$fm_name" = "$name" ]   || { verdict="name!=dir"; fail=1; }
  [ "$lines" -le 500 ]       || { verdict="body>500";  fail=1; }
  [ "$desc_len" -le 1024 ]   || { verdict="desc>1024"; fail=1; }
  [ "$in_plugin" -ge 1 ]     || { verdict="no-plugin"; fail=1; }
  [ "$in_readme" -ge 1 ]     || { verdict="no-readme"; fail=1; }
  printf '%-12s %7s %7s %8s %8s  %s\n' "$name" "$lines" "$desc_len" "$in_plugin" "$in_readme" "$verdict"
done

# The multi-page baseline is allowed to contain SLOT markers, but its
# manifest, navigation, links, IDs, landmarks, and local assets must
# already satisfy the same checker generated briefings use.
python3 skills/htmlize/scripts/check-site.py --allow-slots \
  skills/htmlize/assets/templates/site || fail=1

# Single-page artifacts inline the same viewer that briefing sites load as
# a shared asset. Normalize the document template's two-space script
# indentation, then prove the behavior has not drifted between surfaces.
if ! cmp -s \
  <(awk '/DIAGRAM_VIEWER_START/{on=1;next}/DIAGRAM_VIEWER_END/{on=0}on' \
      skills/htmlize/assets/templates/site/assets/diagram-viewer.js) \
  <(awk '/DIAGRAM_VIEWER_START/{on=1;next}/DIAGRAM_VIEWER_END/{on=0}on' \
      skills/htmlize/assets/templates/document.html | sed 's/^  //'); then
  echo "htmlize: document diagram viewer drifted from site asset" >&2
  fail=1
fi

exit "$fail"
