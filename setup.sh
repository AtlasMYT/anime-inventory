#!/bin/bash
set -e

echo "📦 Installing system dependencies..."
if [ -x "$(command -v apt)" ]; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv git curl
elif [ -x "$(command -v yum)" ]; then
    sudo yum install -y python3 python3-pip python3-venv git curl
else
    echo "❌ Unsupported package manager. Install Python 3 manually."
    exit 1
fi

echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📜 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f config.json ]; then
cat > config.json <<EOF
{
  "ANIME_DIR": "/mnt/anime-hdd",
  "DB_PATH": "anime.db",
  "PORT": 5000
}
EOF
echo "📝 Created default config.json"
fi

echo "🔍 Running initial scan..."
python3 scanner.py || echo "⚠ Initial scan skipped (HDD not present)."

echo "🚀 Launching server..."
nohup python3 app.py > server.log 2>&1 &

echo "✅ Installation complete. Visit http://localhost:5000"
