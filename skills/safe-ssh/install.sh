#!/bin/bash
# safe-ssh installer - creates symlinks in ~/Tools/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$HOME/Tools"

# Create Tools directory if needed
mkdir -p "$TOOLS_DIR"

echo "Installing safe-ssh wrappers to $TOOLS_DIR..."

for script in "$SCRIPT_DIR"/scripts/ssh-*; do
    name=$(basename "$script")

    # Remove existing symlink if present
    if [ -L "$TOOLS_DIR/$name" ]; then
        rm "$TOOLS_DIR/$name"
    fi

    # Create symlink
    ln -s "$script" "$TOOLS_DIR/$name"
    echo "  Linked: $name"
done

# Make scripts executable
chmod +x "$SCRIPT_DIR"/scripts/ssh-*

echo ""
echo "Done! Add these to your Claude Code settings.json:"
echo ""
echo '"permissions": {'
echo '  "allow": ['
for script in "$SCRIPT_DIR"/scripts/ssh-*; do
    name=$(basename "$script")
    echo "    \"Bash(~/Tools/$name:*)\","
done
echo '  ]'
echo '}'
