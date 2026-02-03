#!/bin/bash

set -e

# Check and install GitHub CLI
echo "🔍 Checking for GitHub CLI..."
if ! command -v gh &> /dev/null; then
    echo "📥 GitHub CLI not found. Installing..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install gh
        else
            echo "❌ Homebrew not found. Install from: https://brew.sh"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
            sudo apt update
            sudo apt install gh -y
        elif command -v dnf &> /dev/null; then
            sudo dnf install gh -y
        else
            echo "❌ Unsupported package manager. Install manually: https://cli.github.com"
            exit 1
        fi
    else
        echo "❌ Unsupported OS. Install manually: https://cli.github.com"
        exit 1
    fi
    
    echo "✅ GitHub CLI installed"
fi

# Check authentication
echo "🔐 Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "🔑 Not authenticated. Starting authentication..."
    gh auth login
    echo "✅ Authentication complete"
else
    echo "✅ Already authenticated"
fi

echo "🔍 Analyzing project..."

# Detect project type and set prefix
CURRENT_DIR=$(basename "$PWD")
PREFIX=""

if [ -f "wp-content" ] || [ -f "style.css" ] || grep -q "Plugin Name:" *.php 2>/dev/null; then
    echo "📦 WordPress plugin detected"
    PREFIX="wp-"
elif [ -f "composer.json" ] && grep -q "wordpress-plugin" composer.json 2>/dev/null; then
    echo "📦 WordPress plugin detected (composer)"
    PREFIX="wp-"
fi

REPO_NAME="${PREFIX}${CURRENT_DIR}"

echo "📝 Repository will be named: $REPO_NAME"

# Check SSH configuration
echo "🔐 Checking SSH keys..."
if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "⚠️  SSH key not configured properly"
    echo "💡 GitHub CLI can use HTTPS instead, continuing..."
fi

# Handle existing git repo
if [ -d .git ]; then
    echo "📂 Git repository already exists"

    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

    if [ -n "$REMOTE_URL" ]; then
        echo "🔗 Remote already configured: $REMOTE_URL"
        echo "✅ Nothing to do - repository already set up"
        exit 0
    fi

    echo "📝 Local repository exists but no remote configured"
    echo "Will add remote and push..."
else
    echo "🆕 Initializing new git repository"
    git init
fi

# Smart .gitignore creation
echo "📄 Setting up .gitignore..."
if [ ! -f .gitignore ]; then
    cat > .gitignore <<EOL
# Dependencies
node_modules/
vendor/
bower_components/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.sublime-*

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# WordPress specific
wp-config.php
.htaccess
EOL
    echo "✅ Created .gitignore"
else
    echo "✅ .gitignore already exists"
fi

# Stage and commit
echo "📤 Staging files..."
git add .

if git diff --staged --quiet; then
    echo "⚠️  No changes to commit"
else
    git commit -m "Initial commit: ${REPO_NAME}"
    echo "✅ Files committed"
fi

# Create GitHub repo
echo "🚀 Creating GitHub repository..."
gh repo create "$REPO_NAME" --private --source=. --push

echo ""
echo "✅ Success! Repository created and pushed"
echo "🔗 https://github.com/$(gh api user -q .login)/$REPO_NAME"
