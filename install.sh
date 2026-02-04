#!/usr/bin/env bash
#
# Claude Multitool Installer
# Run: curl -fsSL https://raw.githubusercontent.com/MarcinDudekDev/claude-multitool/main/install.sh | bash
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPO_URL="https://github.com/MarcinDudekDev/claude-multitool.git"
INSTALL_DIR="${CLAUDE_MULTITOOL_DIR:-$HOME/.claude-multitool}"
BIN_DIR="${HOME}/.local/bin"

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           Claude Multitool Installer                      ║"
echo "║   Run multiple Claude Code sessions like a team           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check requirements
check_requirements() {
    local missing=()

    command -v git >/dev/null 2>&1 || missing+=("git")
    command -v python3 >/dev/null 2>&1 || missing+=("python3")
    command -v tmux >/dev/null 2>&1 || missing+=("tmux")

    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}Missing required tools: ${missing[*]}${NC}"
        echo "Please install them first:"
        echo "  brew install ${missing[*]}"
        exit 1
    fi

    # Optional tools
    if ! command -v fzf >/dev/null 2>&1; then
        echo -e "${YELLOW}Optional: fzf not found (needed for project picker)${NC}"
        echo "  Install with: brew install fzf"
    fi

    if ! command -v docker >/dev/null 2>&1; then
        echo -e "${YELLOW}Optional: docker not found (needed for memory system)${NC}"
        echo "  Install Docker Desktop for full memory features"
    fi
}

# Create bin directory
setup_bin() {
    mkdir -p "$BIN_DIR"

    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo -e "${YELLOW}Adding $BIN_DIR to PATH...${NC}"

        # Detect shell
        if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
            echo "Added to ~/.zshrc"
        elif [ -f "$HOME/.bashrc" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            echo "Added to ~/.bashrc"
        fi
    fi
}

# Clone or update repo
clone_repo() {
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${BLUE}Updating existing installation...${NC}"
        cd "$INSTALL_DIR"
        git pull --ff-only
    else
        echo -e "${BLUE}Cloning repository...${NC}"
        git clone "$REPO_URL" "$INSTALL_DIR"
    fi
}

# Install Layer 0 (standalone tools)
install_layer0() {
    echo -e "${GREEN}Installing Layer 0 (standalone tools)...${NC}"

    ln -sf "$INSTALL_DIR/packages/layer-0/pane-status/pane-status" "$BIN_DIR/pane-status"
    ln -sf "$INSTALL_DIR/packages/layer-0/p/p" "$BIN_DIR/p"

    echo "  ✓ pane-status"
    echo "  ✓ p (project picker)"
}

# Install Layer 1 (messaging)
install_layer1() {
    echo -e "${GREEN}Installing Layer 1 (messaging)...${NC}"

    ln -sf "$INSTALL_DIR/packages/layer-1/msg/msg" "$BIN_DIR/msg"
    ln -sf "$INSTALL_DIR/packages/layer-1/inbox-daemon/inbox-daemon" "$BIN_DIR/inbox-daemon"

    echo "  ✓ msg"
    echo "  ✓ inbox-daemon"
}

# Install Layer 2 (orchestration)
install_layer2() {
    echo -e "${GREEN}Installing Layer 2 (orchestration)...${NC}"

    ln -sf "$INSTALL_DIR/packages/layer-2/op/op" "$BIN_DIR/op"

    echo "  ✓ op (session orchestrator)"
}

# Install memory system
install_memory() {
    echo -e "${GREEN}Installing memory system...${NC}"

    ln -sf "$INSTALL_DIR/packages/memory/helix-memory/memory" "$BIN_DIR/memory"
    ln -sf "$INSTALL_DIR/packages/memory/memorize/memorize" "$BIN_DIR/memorize"

    echo "  ✓ memory"
    echo "  ✓ memorize"

    if command -v docker >/dev/null 2>&1; then
        echo -e "${BLUE}To start the memory database:${NC}"
        echo "  cd $INSTALL_DIR/packages/memory/helix-memory && docker-compose up -d"
    fi
}

# Install utilities
install_utilities() {
    echo -e "${GREEN}Installing utilities...${NC}"

    ln -sf "$INSTALL_DIR/packages/utilities/t/t" "$BIN_DIR/t"
    ln -sf "$INSTALL_DIR/packages/utilities/img-optimize/img-optimize" "$BIN_DIR/img-optimize"

    echo "  ✓ t (tool selector)"
    echo "  ✓ img-optimize"
}

# Install skills
install_skills() {
    echo -e "${GREEN}Installing Claude Code skills...${NC}"

    local skills_dir="$HOME/.claude/skills"
    mkdir -p "$skills_dir"

    for skill in "$INSTALL_DIR/skills/"*/; do
        local name=$(basename "$skill")
        ln -sf "$skill" "$skills_dir/$name"
        echo "  ✓ $name"
    done
}

# Main installation
main() {
    echo "Checking requirements..."
    check_requirements

    echo ""
    setup_bin
    clone_repo

    echo ""
    install_layer0
    install_layer1
    install_layer2

    echo ""
    install_memory
    install_utilities

    echo ""
    install_skills

    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Installation Complete!                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Quick start:"
    echo "  op --status          # See all Claude sessions"
    echo "  op myproject         # Open/create a session"
    echo "  memory search 'auth' # Search your memories"
    echo ""
    echo -e "${YELLOW}Restart your terminal or run: source ~/.zshrc${NC}"
    echo ""
    echo "Documentation: https://github.com/MarcinDudekDev/claude-multitool"
}

# Parse arguments
case "${1:-}" in
    --layer)
        check_requirements
        setup_bin
        clone_repo
        case "$2" in
            0) install_layer0 ;;
            1) install_layer0; install_layer1 ;;
            2) install_layer0; install_layer1; install_layer2 ;;
            *) echo "Usage: install.sh --layer [0|1|2]"; exit 1 ;;
        esac
        ;;
    --memory)
        check_requirements
        setup_bin
        clone_repo
        install_memory
        ;;
    --skills)
        clone_repo
        install_skills
        ;;
    --all|"")
        main
        ;;
    --help|-h)
        echo "Claude Multitool Installer"
        echo ""
        echo "Usage: install.sh [option]"
        echo ""
        echo "Options:"
        echo "  (no args)     Install everything"
        echo "  --layer N     Install up to layer N (0, 1, or 2)"
        echo "  --memory      Install only memory system"
        echo "  --skills      Install only Claude Code skills"
        echo "  --all         Install everything (default)"
        echo "  --help        Show this help"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Run with --help for usage"
        exit 1
        ;;
esac
