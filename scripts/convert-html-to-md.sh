#!/bin/bash
# Convert existing HTML blog posts to Hugo Markdown
# Usage: ./scripts/convert-html-to-md.sh blog/article.html

set -e

INPUT="$1"
FILENAME=$(basename "$INPUT" .html)
OUTPUT="content/blog/${FILENAME}.md"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <html-file>"
  exit 1
fi

echo "Converting: $INPUT -> $OUTPUT"

# Extract metadata using grep/sed
TITLE=$(grep -o '<title>[^<]*</title>' "$INPUT" | sed 's/<[^>]*>//g' | sed 's/ | Сережа Рис//')
DATE=$(grep -o 'datePublished.*"[0-9-]*"' "$INPUT" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' | head -1)
DESC=$(grep 'name="description"' "$INPUT" | grep -o 'content="[^"]*"' | sed 's/content="//;s/"$//')

# Extract tags from article:tag
TAGS=$(grep 'article:tag' "$INPUT" | grep -o 'content="[^"]*"' | sed 's/content="//;s/"$//' | tr '\n' ',' | sed 's/,$//')

# Create frontmatter
cat > "$OUTPUT" << EOF
---
title: "$TITLE"
date: $DATE
description: "$DESC"
tags: [$(echo "$TAGS" | sed 's/,/", "/g' | sed 's/^/"/;s/$/"/' | sed 's/""/"/g')]
---

EOF

# Extract body content (simplified - manual review needed)
echo "# Manual conversion needed for content body"
echo "# Check: $OUTPUT"

echo "Created: $OUTPUT (frontmatter only, content needs manual migration)"
