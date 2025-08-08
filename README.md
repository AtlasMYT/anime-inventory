# 🎌 anime-inventory

A self-hosted inventory system for your anime collection, designed for Proxmox setups with HDD bind mounts.  
Scans and catalogs files into an SQLite database and provides a browsable web UI to prevent duplicate downloads.

---

## 📦 Features

- 🗂️ Scans mounted anime HDDs
- 🧠 Stores metadata in SQLite (`anime.db`)
- 🌐 Simple Flask-based API
- 🧭 Collapsible tree-view web UI
- ⚡ One-command setup with automatic **systemd** startup

---

## 🚀 Quick Start (with systemd auto-start)

> ✅ **Requirements:**  
> - Fresh Ubuntu or Debian LXC/VM  
> - `curl` or `wget` installed  
> - HDD bind-mounted at your target location (`/mnt/anime-hdd` by default)

Run this in your container:

```bash
bash <(curl -s https://raw.githubusercontent.com/AtlasMYT/anime-inventory/main/setup.sh)

After installation, the app will be running automatically as a **systemd service**.

Visit:


http://<your-container-ip>:5000

---

## 🛠️ Configuration

Edit **`config.json`** in the repository directory (`/root/anime-inventory/config.json`):

json
{
  "ANIME_DIR": "/mnt/anime-hdd",
  "DB_PATH": "anime.db",
  "PORT": 5000
}

- **ANIME_DIR** – Path to your mounted HDD containing anime files  
- **DB_PATH** – Path to SQLite database (default: `anime.db` in repo)  
- **PORT** – Port number for the Flask server  

After changing the port or directory, restart the service:

bash
systemctl restart anime-inventory

---

## 🖥️ Service Management

The setup script installs a **systemd service** so your app runs on boot.

**Start**
bash
systemctl start anime-inventory

**Stop**
bash
systemctl stop anime-inventory

**Restart**
bash
systemctl restart anime-inventory

**Check Status**
bash
systemctl status anime-inventory

**View Logs**
bash
journalctl -u anime-inventory -f

---

## 🔄 Rescanning for New Files

If you add new anime or change the folder structure, you can rescan without restarting:

bash
cd /root/anime-inventory
source venv/bin/activate
python3 scanner.py

---

## 🧰 Troubleshooting

**Port Already in Use**  
This should no longer happen since systemd now manages the process, but if it does:

bash
lsof -ti:5000 | xargs kill -9
systemctl restart anime-inventory

**Logs Not Showing in Browser**  
Check service logs:
bash
journalctl -u anime-inventory -f

---

## 📁 Project Structure


anime-inventory/
├── app.py              # Flask app for API and UI
├── scanner.py          # File scanner + DB updater
├── config.json         # User-defined settings
├── requirements.txt    # Python dependencies
├── setup.sh            # One-shot installer script with systemd integration
├── static/             # Frontend HTML/CSS/JS
└── anime-inventory.service (installed in /etc/systemd/system)

---

## 🧩 Roadmap

- 🔍 Search bar in the frontend
- 📝 Tags & notes per file
- 🧾 Export as CSV
- 🔐 Auth for remote access

---

## 🧼 License

MIT License – Free to use, modify, and distribute.


---

### ✅ Changes from Original README
- **Removed nohup instructions** → replaced with **systemd-based autostart**
- Added `systemctl` commands  
- Added troubleshooting commands for port issues  
- Clarified config file editing  
- Updated project structure to mention systemd service  

---

If you want, I can also **add a section for custom port configuration directly from `setup.sh` as an argument**, so in README it can say:  

```bash
bash setup.sh --port 5050
