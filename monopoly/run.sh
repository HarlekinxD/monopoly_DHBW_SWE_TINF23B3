#!/bin/bash
# Monopoly CLI - Start Script
# This script starts the Monopoly game

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "On Fedora Linux, install it with: sudo dnf install python3"
    exit 1
fi

# Check Python version (>= 3.10)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
MIN_VERSION="3.10"
if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$MIN_VERSION" ]; then
    echo "✓ Python $PYTHON_VERSION available"
else
    echo "❌ Error: Python 3.10 or higher is required (found: $PYTHON_VERSION)"
    exit 1
fi

# Add src directory to PYTHONPATH
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

# Start the game
echo "Starting Monopoly CLI..."
python3 -m monopoly "$@"
