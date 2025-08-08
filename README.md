# 🎌 Anime Inventory

A self-hosted anime collection inventory for Proxmox LXC setups or standalone servers.  
It scans your mounted HDD folders, catalogs them into an SQLite database, and serves a simple web interface to browse and prevent duplicate downloads.

---

## 📦 Features
- 🗂 Scans mounted anime HDDs automatically or on demand
- 📦 Stores results in SQLite (`anime.db`)
- 🌐 Flask-based API with HTML frontend
- 📂 Collapsible tree-view UI of your collection
- 🔍 Search support (via Web UI)
- 📑 Export listing as CSV
- ⚡ One-command setup
- 🔄 Web-based **Rescan** (no CLI needed!)

---

## 🚀 Quick Install
Requires:
- Ubuntu-based LXC or VM
- HDD bind-mounted to your container (e.g., `/mnt/anime-hdd`)

Run:
```bash
bash <(curl -s https://raw.githubusercontent.com/AtlasMYT/anime-inventory/main/setup.sh)

Access at:

http://<your-LXC-IP>:5000

---

## 🛠 Configuration
The `config.json` file:
json
{
  "ANIME_DIR": "/mnt/anime-hdd",
  "DB_PATH": "anime.db",
  "PORT": 5000
}
- **ANIME_DIR** → Path to your mounted anime HDD
- **DB_PATH** → Path to SQLite database file
- **PORT** → HTTP port for Flask server

---

## 🔄 Updating Your Inventory
You can **rescan from the Web UI** after adding new anime, or from CLI:
bash
source venv/bin/activate
python3 scanner.py

---

## 🔁 Updating the Repo (Without Deleting)
In your anime-inventory folder:
bash
git pull
source venv/bin/activate
pip install -r requirements.txt
This **pulls new changes** without removing your config, database, or downloaded files.

---

## 🔌 Auto-Start on Boot
To make anime-inventory start automatically on LXC boot:
bash
nano /etc/systemd/system/anime-inventory.service
Paste:
ini
[Unit]
Description=Anime Inventory Flask App
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/anime-inventory
ExecStart=/root/anime-inventory/venv/bin/python3 /root/anime-inventory/app.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
Then:
bash
systemctl daemon-reload
systemctl enable anime-inventory
systemctl start anime-inventory

---

## 📁 Project Structure

anime-inventory/
├── app.py              # Flask backend
├── scanner.py          # Anime folder scanner
├── config.json         # Configuration file
├── requirements.txt    # Python dependencies
├── setup.sh            # Automated installer
├── static/             # HTML, CSS, JS
└── anime.db            # SQLite database

---

## 🧼 License
MIT


---

## **3️⃣ .gitignore**
Here’s a sensible `.gitignore` for your project:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.db

# Virtual environment
venv/
env/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
nohup.out

# Config and local data
config.json
anime.db
