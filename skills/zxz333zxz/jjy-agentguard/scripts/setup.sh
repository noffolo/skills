#!/bin/bash
# AgentGuard Setup - Auto-detect, install, and start
set -e

INSTALL_URL="https://www.agentguard.site/download/install.sh"

echo "🛡️  AgentGuard Setup"
echo "================================"

# Check if agentguard is already installed
if command -v agentguard &>/dev/null; then
    CURRENT_VERSION=$(agentguard --version 2>/dev/null || echo "unknown")
    echo "✅ AgentGuard is installed (version: $CURRENT_VERSION)"
else
    echo "📦 AgentGuard not found. Installing..."
    echo ""
    curl -fsSL "$INSTALL_URL" | sh
    echo ""

    # Verify installation
    if command -v agentguard &>/dev/null; then
        CURRENT_VERSION=$(agentguard --version 2>/dev/null || echo "unknown")
        echo "✅ AgentGuard installed successfully (version: $CURRENT_VERSION)"
    else
        echo "❌ Installation failed. Please install manually:"
        echo "   curl -fsSL $INSTALL_URL | sh"
        exit 1
    fi
fi

echo ""

# Check if daemon is running
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:19821/health 2>/dev/null | grep -q "200"; then
    echo "✅ AgentGuard daemon is running"
else
    echo "🚀 Starting AgentGuard daemon..."
    agentguard daemon start 2>/dev/null || true
    sleep 1

    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:19821/health 2>/dev/null | grep -q "200"; then
        echo "✅ AgentGuard daemon started"
    else
        echo "⚠️  Daemon may need manual start: agentguard daemon start"
    fi
fi

echo ""
echo "================================"
echo "🛡️  AgentGuard is ready"
echo "   Dashboard: http://127.0.0.1:19821"
echo "   Status:    agentguard status"
