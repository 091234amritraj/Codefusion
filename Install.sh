#!/bin/bash
echo "🤖 Installing JARVIS AI Assistant..."
echo "Updating Termux packages..."
pkg update -y && pkg upgrade -y
echo "Installing Python and dependencies..."
pkg install python -y
pkg install espeak -y
pkg install termux-api -y
echo "Installing Python packages..."
pip install requests
echo "✅ JARVIS installation complete!"
echo ""
echo "🚀 To run JARVIS:"
echo "python jarvis.py"
