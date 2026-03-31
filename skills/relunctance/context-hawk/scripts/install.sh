#!/usr/bin/env bash
# install.sh — Auto-link hawk command to ~/bin
# Run after: openclaw skills install ./context-hawk.skill

set -e

echo "[install] Context-Hawk — creating symlinks..."

# Ensure ~/bin exists and is in PATH
mkdir -p "$HOME/bin"
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo "[install] Adding ~/bin to PATH in ~/.bashrc..."
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/bin:$PATH"
fi

# Create symlink
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ln -sf "$SCRIPT_DIR/hawk" "$HOME/bin/hawk"

echo "[install] Symlink created: ~/bin/hawk"
echo "[install] Run: source ~/.bashrc && hawk status"
