#!/usr/bin/env bash
# Installs git hooks for this repo.
# Run once after cloning: ./scripts/install-hooks.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
HOOK_FILE="$HOOKS_DIR/pre-commit"

cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env bash
exec "$(git rev-parse --show-toplevel)/scripts/validate-blog-post.sh"
EOF

chmod +x "$HOOK_FILE"
chmod +x "$REPO_ROOT/scripts/validate-blog-post.sh"

echo "✓ pre-commit hook installed at .git/hooks/pre-commit"
