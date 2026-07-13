#!/usr/bin/env bash
# render-diagram.sh [--figure] [--caption TEXT] <source.(dot|d2|mmd)> [output.svg]
#
# Renders a diagram source to inline-ready SVG with whatever
# engine is available, strips the XML prolog/DOCTYPE, and remaps
# the baseline palette hexes inside embedded <style> blocks to
# CSS variables with hex fallbacks -- so the SVG themes itself
# when inlined into an artifact and still renders standalone.
# Presentation-attribute hexes (graphviz output) are left literal;
# the artifact's `.diagram svg [fill=...]` rules remap those.
#
# --figure additionally writes <output>.html: a ready-to-paste
# <figure class="diagram"> fragment with figcaption and the
# escaped diagram source in a collapsed <details>.
# See references/diagrams.md for the doctrine.
set -euo pipefail

usage() {
  echo "usage: $0 [--figure] [--caption TEXT] <source.(dot|d2|mmd)> [output.svg]" >&2
  exit 2
}

figure=0
caption=""
args=()
while [ $# -gt 0 ]; do
  case $1 in
    --figure) figure=1 ;;
    --caption) shift; [ $# -gt 0 ] || usage; caption=$1 ;;
    -h|--help) usage ;;
    *) args+=("$1") ;;
  esac
  shift
done
[ ${#args[@]} -ge 1 ] || usage
src=${args[0]}
[ -f "$src" ] || { echo "error: no such file: $src" >&2; exit 1; }
out=${args[1]:-${src%.*}.svg}
ext=${src##*.}
script_dir=$(cd "$(dirname "$0")" && pwd)
theme="$script_dir/../assets/mermaid-theme.json"

inline_clean() {  # drop everything before <svg so the file inlines cleanly
  awk '!found { i = index($0, "<svg"); if (i) { found = 1; print substr($0, i) }; next } { print }' \
    "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

# Inside <style> blocks and style="" attributes -- where CSS
# attribute selectors cannot reach -- swap baseline hexes for
# var(--token, #hex). The fallback keeps standalone SVGs correct.
remap_style_hexes() {
  perl -0777 -pe '
    sub remap {
      my $c = shift;
      $c =~ s/#ffffff\b/var(--surface, #ffffff)/gi;
      $c =~ s/#faf9f7\b/var(--bg, #faf9f7)/gi;
      $c =~ s/#1d1d20\b/var(--ink, #1d1d20)/gi;
      $c =~ s/#5c5c66\b/var(--ink-2, #5c5c66)/gi;
      $c =~ s/#e6e4de\b/var(--rule, #e6e4de)/gi;
      $c =~ s/#1a6db0\b/var(--accent, #1a6db0)/gi;
      # mermaid derives these internally; theme variables cannot pin them
      $c =~ s/#eaeaea\b/var(--rule, #eaeaea)/gi;
      $c =~ s/#a3a399\b/var(--ink-2, #a3a399)/gi;
      $c =~ s/#(?:000000|050608)\b/var(--ink, #000000)/gi;
      $c =~ s/#(?:666|999)\b/var(--ink-2, #5c5c66)/gi;
      return $c;
    }
    s{(<style[^>]*>)(.*?)(</style>)}{$1 . remap($2) . $3}ges;
    s{(style=")([^"]*)(")}{$1 . remap($2) . $3}ge;
  ' "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

html_escape() { sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' "$1"; }

emit_figure() {
  local frag=${out%.*}.html id
  id=$(basename "${out%.*}")
  id=fig-${id//[^a-zA-Z0-9]/-}
  {
    printf '<figure class="diagram" id="%s">\n' "$id"
    cat "$out"
    printf '\n  <figcaption>%s</figcaption>\n</figure>\n' \
      "${caption:-SLOT: caption naming what the diagram shows.}"
    printf '<details>\n  <summary>Diagram source</summary>\n  <pre><code>'
    html_escape "$src"
    printf '</code></pre>\n</details>\n'
  } > "$frag"
  echo "figure fragment: $frag"
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
remap_style_hexes "$out"
echo "rendered: $out ($(wc -c < "$out" | tr -d ' ') bytes, inline-ready)"
[ $figure -eq 1 ] && emit_figure
exit 0
