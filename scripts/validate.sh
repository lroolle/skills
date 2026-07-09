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

exit "$fail"
