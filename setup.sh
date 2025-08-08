#!/bin/bash

set -e  # Exit on error

echo "📦 Updating packages and installing dependencies..."
apt update && apt install -y python3 python3-pip python3-venv curl git

echo "📁 Cloning anime-inventory repo..."
git clone https://github.com/yourusername/anime-inventory.git
cd anime-inventory

echo "🐍 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 Scanning anime directory and creating database..."
python3 scanner.py

echo "🚀 Starting the Flask app..."
nohup python3 app.py &

echo "✅ Setup complete. Visit your CT IP on port 5000 (e.g., http://192.168.x.x:5000)"
