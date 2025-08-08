# 🎌 anime-inventory

A self-hosted inventory system for your anime collection, designed for Proxmox setups with HDD bind mounts. Scans and catalogs files into an SQLite database and provides a browsable web UI to prevent duplicate downloads.

---

## 📦 Features

- 🗂️ Scans mounted anime HDDs
- 🧠 Stores metadata in SQLite (`anime.db`)
- 🌐 Simple Flask-based API
- 🧭 Collapsible tree-view web UI
- ⚡ One-command setup with `setup.sh`

---

## 🚀 Quick Start

> ✅ Requirements: a clean Ubuntu-based LXC with `curl` or `wget` installed, and the HDD bind-mounted at your target location.

Run this in your LXC container:

```bash
bash <(curl -s https://raw.githubusercontent.com/AtlasMYT/anime-inventory/main/setup.sh)

After installation, visit:

        

text

http://<your-container-ip>:5000

🛠️ Configuration

Modify config.json to customize:

        

json

{
  "ANIME_DIR": "/mnt/anime-hdd",
  "DB_PATH": "anime.db",
  "PORT": 5000
}

    ANIME_DIR: Path to your mounted anime HDD.
    DB_PATH: SQLite database location (default: anime.db).
    PORT: Port for the Flask web server.

📁 Project Structure

        

text
anime-inventory/
├── app.py              # Flask app for API and UI
├── scanner.py          # File scanner + DB updater
├── config.json         # User-defined settings
├── requirements.txt    # Python dependencies
├── setup.sh            # One-shot installer script
├── static/             # Frontend HTML/CSS/JS
└── .gitignore

🔄 Rescanning

If you add new anime files or update folders:

        

bash

source venv/bin/activate
python3 scanner.py

🧩 Future Ideas

    🔍 Search bar in the frontend
    📝 Tags & notes per file
    🧾 Export as CSV
    🔐 Auth for remote access

🧼 License
