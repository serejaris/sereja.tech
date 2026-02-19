#!/bin/bash
# OG Preview Generator for sereja.tech blog posts
#
# Usage:
#   ./scripts/og-preview/generate.sh \
#     --title "Homebrew: тысяча инструментов для агента" \
#     --command "brew install yt-dlp ffmpeg whisper pandoc htop" \
#     --tools "yt-dlp,ffmpeg,whisper,ImageMagick,pandoc,htop" \
#     --output static/images/blog/homebrew-cli-vibecoding-preview.png
#
# Options:
#   --title     Required. Post title.
#   --subtitle  Optional. Short description below title.
#   --command   Optional. Terminal command to display.
#   --tools     Optional. Comma-separated list of tool/tag badges.
#   --visual    Optional. Emoji or symbol shown above title.
#   --output    Required. Output PNG path.
#
# Layouts (auto-detected):
#   title + command + tools  → Terminal style (like homebrew post)
#   title + subtitle         → Clean style
#   title + tools            → Badge style
#   title only               → Minimal style

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="$SCRIPT_DIR/template.html"

# Parse arguments
TITLE="" SUBTITLE="" COMMAND="" TOOLS="" VISUAL="" OUTPUT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --title)    TITLE="$2";    shift 2 ;;
    --subtitle) SUBTITLE="$2"; shift 2 ;;
    --command)  COMMAND="$2";  shift 2 ;;
    --tools)    TOOLS="$2";    shift 2 ;;
    --visual)   VISUAL="$2";   shift 2 ;;
    --output)   OUTPUT="$2";   shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$TITLE" || -z "$OUTPUT" ]]; then
  echo "Error: --title and --output are required"
  echo "Usage: $0 --title \"Title\" --output path.png [--subtitle \"...\"] [--command \"...\"] [--tools \"a,b,c\"] [--visual \"emoji\"]"
  exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

# Build HTML from template using Python (handles special chars reliably)
TMPHTML=$(mktemp /tmp/og-preview-XXXXXX.html)
trap "rm -f $TMPHTML" EXIT

python3 - "$TEMPLATE" "$TMPHTML" "$TITLE" "$SUBTITLE" "$COMMAND" "$TOOLS" "$VISUAL" << 'PYEOF'
import sys

template_path, output_path, title, subtitle, command, tools, visual = sys.argv[1:8]

with open(template_path) as f:
    html = f.read()

# Replace title (appears in text and data-text attribute)
html = html.replace('{{TITLE}}', title)

# Unhide and fill optional sections
if subtitle:
    html = html.replace('hidden" id="subtitle"', '" id="subtitle"')
    html = html.replace('{{SUBTITLE}}', subtitle)

if command:
    html = html.replace('hidden" id="terminal"', '" id="terminal"')
    html = html.replace('{{COMMAND}}', command)

if tools:
    html = html.replace('hidden" id="tools"', '" id="tools"')
    tools_html = ''.join(f'<div class="tool">{t.strip()}</div>' for t in tools.split(','))
    html = html.replace('{{TOOLS}}', tools_html)

if visual:
    html = html.replace('hidden" id="visual"', '" id="visual"')
    html = html.replace('{{VISUAL}}', visual)

with open(output_path, 'w') as f:
    f.write(html)
PYEOF

# Generate screenshot with Playwright
npx playwright screenshot \
  "file://$TMPHTML" \
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
