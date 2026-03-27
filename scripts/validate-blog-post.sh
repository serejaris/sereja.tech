#!/usr/bin/env bash
# Validates Hugo blog post frontmatter for staged files.
# Used by pre-commit hook and can be run standalone.
#
# Usage: ./scripts/validate-blog-post.sh [file ...]
#   If no files given, validates all staged content/blog/*.md files.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
ERRORS=0

RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

error() { echo -e "${RED}ERROR${NC} $1"; ERRORS=$((ERRORS + 1)); }
warn()  { echo -e "${YELLOW}WARN${NC}  $1"; }

validate_file() {
  local file="$1"
  local rel="${file#$REPO_ROOT/}"

  # Extract frontmatter block (between first pair of ---)
  local fm
  fm=$(awk '/^---/{if(++n==2) exit} n==1 && !/^---/' "$file")

  # --- title ---
  local title
  title=$(echo "$fm" | grep -E '^title:' | sed 's/^title:[[:space:]]*//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
  if [[ -z "$title" ]]; then
    error "$rel: missing 'title' field"
  else
    local title_len=${#title}
    if (( title_len > 60 )); then
      error "$rel: title is ${title_len} chars (max 60): \"$title\""
    fi
  fi

  # --- description ---
  local desc
  desc=$(echo "$fm" | grep -E '^description:' | sed 's/^description:[[:space:]]*//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
  if [[ -z "$desc" ]]; then
    error "$rel: missing 'description' field"
  else
    local desc_len=${#desc}
    if (( desc_len > 160 )); then
      error "$rel: description is ${desc_len} chars (max 160)"
    fi
  fi

  # --- date ---
  local date_val
  date_val=$(echo "$fm" | grep -E '^date:' | sed 's/^date:[[:space:]]*//')
  if [[ -z "$date_val" ]]; then
    error "$rel: missing 'date' field"
  else
    # Accept YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS formats
    if ! echo "$date_val" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
      error "$rel: invalid date format '${date_val}' (expected YYYY-MM-DD)"
    fi
  fi

  # --- tags ---
  local tags_line
  tags_line=$(echo "$fm" | grep -E '^tags:')
  if [[ -z "$tags_line" ]]; then
    error "$rel: missing 'tags' field"
  else
    # Inline array: tags: ["a", "b"] or tags: [a, b]
    local tags_content
    tags_content=$(echo "$tags_line" | sed 's/^tags:[[:space:]]*//')
    if echo "$tags_content" | grep -qE '^\[.*\]'; then
      # Check it's not empty array [] or [""]
      if echo "$tags_content" | grep -qE '^\[\s*\]$'; then
        error "$rel: 'tags' array is empty"
      fi
    else
      # Could be block sequence — check for at least one "- " entry after tags:
      local block_tags
      block_tags=$(echo "$fm" | awk '/^tags:/{found=1; next} found && /^  - /{print} found && !/^  /{exit}')
      if [[ -z "$block_tags" ]]; then
        error "$rel: 'tags' array is empty or has no items"
      fi
    fi
  fi

  # --- image ---
  local image_val
  image_val=$(echo "$fm" | grep -E '^image:' | sed 's/^image:[[:space:]]*//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
  if [[ -z "$image_val" ]]; then
    warn "$rel: no 'image' field (OG preview will be missing)"
  else
    # Strip leading slash to get path relative to static/
    local image_path="${image_val#/}"
    local full_path="$REPO_ROOT/static/$image_path"
    if [[ ! -f "$full_path" ]]; then
      error "$rel: image '$image_val' not found at static/$image_path"
    fi
  fi
}

# Determine files to validate
if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  # Get staged blog posts
  FILES=()
  while IFS= read -r line; do
    FILES+=("$REPO_ROOT/$line")
  done < <(git diff --cached --name-only --diff-filter=ACM | grep -E '^content/blog/.+\.md$' || true)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  exit 0
fi

for f in "${FILES[@]}"; do
  # Skip _index.md
  [[ "$(basename "$f")" == "_index.md" ]] && continue
  validate_file "$f"
done

if (( ERRORS > 0 )); then
  echo ""
  echo -e "${RED}Validation failed: $ERRORS error(s). Fix them or use 'git commit --no-verify' to skip.${NC}"
  exit 1
fi

exit 0
