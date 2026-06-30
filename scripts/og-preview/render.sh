#!/bin/bash
# OG Preview HTML Renderer for sereja.tech blog posts
#
# Renders an arbitrary, self-contained HTML file into a 1200x630 PNG.
# Use this for BESPOKE per-post OG covers authored as HTML in covers/.
# (The legacy generate.sh + template.html flow remains for the old
#  title-driven template style.)
#
# Usage:
#   ./scripts/og-preview/render.sh <input.html> <output.png>
#
# Example:
#   ./scripts/og-preview/render.sh \
#     scripts/og-preview/covers/text-evals-grader.html \
#     static/images/blog/text-evals-grader-preview.png
#
# Invariants:
#   - viewport strictly 1200x630
#   - deviceScaleFactor = 1 (same as generate.sh, which sets none)
#   - reuses the Playwright mechanism from generate.sh (no new deps)

set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "Usage: $0 <input.html> <output.png>"
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Error: input HTML not found: $INPUT"
  exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

# Resolve absolute path for file:// URL
ABS_INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

# Generate screenshot with Playwright (same invocation shape as generate.sh)
npx playwright screenshot \
  "file://$ABS_INPUT" \
  "$OUTPUT" \
  --viewport-size=1200,630 \
  --full-page \
  2>/dev/null

# Verify output
if [[ -f "$OUTPUT" ]]; then
  SIZE=$(wc -c < "$OUTPUT" | xargs)
  echo "Generated: $OUTPUT ($SIZE bytes)"
else
  echo "Error: Failed to generate $OUTPUT"
  exit 1
fi
