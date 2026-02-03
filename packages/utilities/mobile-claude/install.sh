#!/bin/bash
# Install dependencies for mobile-claude transcript viewer

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Installation complete!"
echo "To start the server: python server.py"
echo "Then visit: http://localhost:8080/transcript"
