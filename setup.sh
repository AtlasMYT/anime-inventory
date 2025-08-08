#!/bin/bash
set -e

echo "📦 Installing dependencies..."
apt update && apt install -y python3 python3-pip python3-venv git curl

echo "📁 Cloning anime-inventory repo..."
git clone https://github.com/AtlasMYT/anime-inventory.git
cd anime-inventory

echo "🛠️ Writing config.json..."
cat > config.json <<EOF
{
  "ANIME_DIR": "/mnt/anime-hdd",
  "DB_PATH": "anime.db",
  "PORT": 5000
}
EOF

echo "🐍 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🧠 Running scanner to populate the database..."
python3 scanner.py

echo "🚀 Launching Flask app..."
nohup python3 app.py &

echo "✅ Setup complete. Visit your CT IP on port 5000 (e.g., http://192.168.x.x:5000)"
