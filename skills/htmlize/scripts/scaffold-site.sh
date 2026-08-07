#!/usr/bin/env bash
# scaffold-site.sh <output-directory>
#
# Copies the multi-page technical briefing baseline. The destination must
# not already exist: refusing to merge prevents a scaffold from silently
# overwriting evidence or an in-progress briefing.
set -euo pipefail

usage() {
  echo "usage: $0 <output-directory>" >&2
  exit 2
}

[ "$#" -eq 1 ] || usage
destination=$1
[ ! -e "$destination" ] || {
  echo "error: destination already exists: $destination" >&2
  exit 1
}

script_dir=$(cd "$(dirname "$0")" && pwd)
template="$script_dir/../assets/templates/site"
[ -d "$template" ] || {
  echo "error: site template not found: $template" >&2
  exit 1
}

mkdir -p "$destination"
cp -R "$template"/. "$destination"/

echo "scaffolded: $destination"
echo "next: replace SLOT markers, remove unearned pages, then run:"
echo "  python3 $script_dir/check-site.py $destination"
