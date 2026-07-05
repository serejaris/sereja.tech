#!/usr/bin/env bash
# Installs git hooks for this repo.
# Run once after cloning: ./scripts/install-hooks.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
HOOK_FILE="$HOOKS_DIR/pre-commit"

cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env bash
set -e
ROOT="$(git rev-parse --show-toplevel)"
# 1) validate frontmatter of staged blog posts
"$ROOT/scripts/validate-blog-post.sh"
# 2) regenerate README "Последние статьи" table + post count, then re-stage it
"$ROOT/scripts/update-readme.py"
git add "$ROOT/README.md"
EOF

chmod +x "$HOOK_FILE"
chmod +x "$REPO_ROOT/scripts/validate-blog-post.sh"
chmod +x "$REPO_ROOT/scripts/update-readme.py"

echo "✓ pre-commit hook installed at .git/hooks/pre-commit"
echo "  → validate-blog-post.sh + update-readme.py (auto-updates README on commit)"
