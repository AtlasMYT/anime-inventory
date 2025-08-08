#!/bin/bash
set -e

echo "📦 Installing dependencies..."
apt update && apt install -y python3 python3-pip python3-venv git curl lsof

# Variables
APP_DIR="/root/anime-inventory"
SERVICE_FILE="/etc/systemd/system/anime-inventory.service"

echo "📁 Cloning anime-inventory repo..."
if [ -d "$APP_DIR" ]; then
    echo "⚠️  Directory $APP_DIR already exists. Skipping clone."
else
    git clone https://github.com/AtlasMYT/anime-inventory.git "$APP_DIR"
fi
cd "$APP_DIR"

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

echo "🛑 Killing any old instances..."
if lsof -ti:5000 >/dev/null; then
    kill -9 $(lsof -ti:5000)
fi

echo "📝 Creating systemd service..."
cat > "$SERVICE_FILE" <<EOL
[Unit]
Description=Anime Inventory Flask App
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python3 $APP_DIR/app.py
Restart=always
User=root
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOL

echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload
systemctl enable anime-inventory
systemctl restart anime-inventory

echo "✅ Setup complete!"
echo "🌐 Visit your CT IP on port 5000 (e.g., http://192.168.x.x:5000)"
echo "📄 Service status:"
systemctl status anime-inventory --no-pager
