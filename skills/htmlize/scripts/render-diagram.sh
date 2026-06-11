#!/usr/bin/env bash
# render-diagram.sh <source.(dot|d2|mmd)> [output.svg]
#
# Renders a diagram source to inline-ready SVG with whatever
# engine is available, then strips the XML prolog/DOCTYPE so the
# result can be pasted straight into an HTML artifact.
# See references/diagrams.md for the doctrine.
set -euo pipefail

usage() { echo "usage: $0 <source.(dot|d2|mmd)> [output.svg]" >&2; exit 2; }

[ $# -ge 1 ] || usage
src=$1
[ -f "$src" ] || { echo "error: no such file: $src" >&2; exit 1; }
out=${2:-${src%.*}.svg}
ext=${src##*.}
script_dir=$(cd "$(dirname "$0")" && pwd)
theme="$script_dir/../assets/mermaid-theme.json"

inline_clean() {  # drop everything before <svg so the file inlines cleanly
  awk '!found { i = index($0, "<svg"); if (i) { found = 1; print substr($0, i) }; next } { print }' \
    "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

render_mmd() {
  local id cfg=()
  id=$(basename "${out%.*}")
  id=${id//[^a-zA-Z0-9]/-}
  if command -v mmdc >/dev/null 2>&1; then
    [ -f "$theme" ] && cfg=(-c "$theme")
    mmdc -i "$src" -o "$out" -b transparent --svgId "$id" ${cfg[@]+"${cfg[@]}"}
  elif command -v docker >/dev/null 2>&1; then
    # The mount must be visible to the Docker daemon: run from a
    # host-visible path, not a container-local /tmp.
    local dir base outbase
    dir=$(cd "$(dirname "$src")" && pwd)
    base=$(basename "$src")
    outbase=$(basename "$out")
    if [ -f "$theme" ]; then
      cp "$theme" "$dir/.mermaid-theme.json"
      cfg=(-c /data/.mermaid-theme.json)
    fi
    docker run --rm -u "$(id -u)" -v "$dir":/data minlag/mermaid-cli \
      -i "/data/$base" -o "/data/$outbase" -b transparent \
      --svgId "$id" ${cfg[@]+"${cfg[@]}"}
    rm -f "$dir/.mermaid-theme.json"
    [ "$dir/$outbase" -ef "$out" ] 2>/dev/null || mv "$dir/$outbase" "$out"
  else
    echo "error: mermaid needs mmdc or docker (minlag/mermaid-cli)." >&2
    echo "hint: flowcharts also render with graphviz dot -- no browser needed." >&2
    exit 1
  fi
}

case $ext in
  dot|gv)
    command -v dot >/dev/null 2>&1 \
      || { echo "error: graphviz not installed (apt/brew install graphviz)" >&2; exit 1; }
    dot -Tsvg "$src" -o "$out" ;;
  d2)
    command -v d2 >/dev/null 2>&1 \
      || { echo "error: d2 not installed (curl -fsSL https://d2lang.com/install.sh | sh -s --)" >&2; exit 1; }
    d2 "$src" "$out" ;;
  mmd|mermaid) render_mmd ;;
  *) echo "error: unknown diagram extension: .$ext" >&2; usage ;;
esac

inline_clean "$out"
echo "rendered: $out ($(wc -c < "$out" | tr -d ' ') bytes, inline-ready)"
