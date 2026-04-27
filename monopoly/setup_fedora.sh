#!/bin/bash
# Setup script for Fedora Linux
# This script installs all required dependencies for running Monopoly

set -e

echo "🔧 Setting up Monopoly for Fedora Linux..."

# Check if running on Fedora-like system
if ! command -v dnf &> /dev/null; then
    echo "⚠️  Warning: This script is optimized for Fedora Linux (dnf not found)"
    echo "Please ensure Python 3.10+ is installed on your system"
    exit 1
fi

# Install Python 3.10+ if needed
if ! command -v python3 &> /dev/null; then
    echo "📥 Installing Python 3..."
    sudo dnf install -y python3 python3-devel
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "✓ Python $PYTHON_VERSION already installed"
fi

# Verify Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
MIN_VERSION="3.10"
if ! [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$MIN_VERSION" ]; then
    echo "❌ Error: Python 3.10 or higher is required (found: $PYTHON_VERSION)"
    echo "Please install a newer Python version"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION available"
echo ""
echo "✅ Setup complete! You can now run the game with:"
echo "   ./run.sh"
echo ""
