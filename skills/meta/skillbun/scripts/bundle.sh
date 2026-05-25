#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: bundle.sh <bundle-name> <skill-dir> [skill-dir...]"
    echo ""
    echo "Collect skill directories into a bundle staging area."
    echo "Does NOT generate BUNDLE.md or install.sh (the agent does that)."
    echo ""
    echo "Options:"
    echo "  --zip     Also create a .skillbun archive"
    echo "  --out     Output directory (default: current directory)"
    exit 1
}

[ $# -lt 2 ] && usage

ZIP=false
OUT_DIR="."
BUNDLE_NAME=""
SKILL_DIRS=()

while [ $# -gt 0 ]; do
    case "$1" in
        --zip)  ZIP=true; shift ;;
        --out)  OUT_DIR="$2"; shift 2 ;;
        -*)     echo "Unknown option: $1"; usage ;;
        *)
            if [ -z "$BUNDLE_NAME" ]; then
                BUNDLE_NAME="$1"
            else
                SKILL_DIRS+=("$1")
            fi
            shift
            ;;
    esac
done

[ -z "$BUNDLE_NAME" ] && usage
[ ${#SKILL_DIRS[@]} -eq 0 ] && usage

STAGING="$OUT_DIR/$BUNDLE_NAME"

if [ -d "$STAGING" ]; then
    echo "Staging directory exists: $STAGING"
    echo "Remove it first or choose a different name."
    exit 1
fi

mkdir -p "$STAGING/skills"

EXCLUDE_PATTERNS=(
    "__pycache__"
    "node_modules"
    ".DS_Store"
    "*.pyc"
    "*.pyo"
    "evals"
    "*-workspace"
    ".git"
)

build_exclude_args() {
    local args=()
    for pat in "${EXCLUDE_PATTERNS[@]}"; do
        args+=(--exclude="$pat")
    done
    echo "${args[@]}"
}

for skill_dir in "${SKILL_DIRS[@]}"; do
    skill_dir="${skill_dir%/}"

    if [ ! -f "$skill_dir/SKILL.md" ]; then
        echo "SKIP: $skill_dir (no SKILL.md)"
        continue
    fi

    skill_name=$(basename "$skill_dir")
    echo "  + $skill_name"

    rsync -a $(build_exclude_args) "$skill_dir/" "$STAGING/skills/$skill_name/"
done

echo ""
echo "Staged: $STAGING/skills/"
ls -1 "$STAGING/skills/"

if [ "$ZIP" = true ]; then
    ARCHIVE="$OUT_DIR/$BUNDLE_NAME.skillbun"
    (cd "$OUT_DIR" && zip -rq "$BUNDLE_NAME.skillbun" "$BUNDLE_NAME/")
    echo ""
    echo "Archive: $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"
fi

echo ""
echo "Next: generate BUNDLE.md and install.sh in $STAGING/"
