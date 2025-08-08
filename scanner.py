import os
import sqlite3
import json
from datetime import datetime

# Load config
if not os.path.exists("config.json"):
    raise FileNotFoundError("config.json is missing. Please create it.")

with open("config.json") as f:
    CONFIG = json.load(f)

ANIME_DIR = CONFIG["ANIME_DIR"]
DB_PATH = CONFIG["DB_PATH"]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS anime_files (
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            name TEXT,
            size INTEGER,
            mtime REAL,
            mtime_str TEXT
        )
    ''')
    conn.commit()
    return conn

def scan_and_update(conn):
    if not os.path.exists(ANIME_DIR):
        print(f"⚠ Anime directory '{ANIME_DIR}' not found. Using offline DB.")
        return

    print(f"📂 Scanning '{ANIME_DIR}'...")
    c = conn.cursor()
    for root, dirs, files in os.walk(ANIME_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                stat = os.stat(full_path)
                mtime_str = datetime.fromtimestamp(stat.st_mtime).isoformat()
                c.execute('''
                    INSERT INTO anime_files (path, name, size, mtime, mtime_str)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(path) DO UPDATE SET
                        size=excluded.size,
                        mtime=excluded.mtime,
                        mtime_str=excluded.mtime_str
                ''', (full_path, file, stat.st_size, stat.st_mtime, mtime_str))
            except FileNotFoundError:
                continue
    conn.commit()
    print("✅ Scan complete.")

if __name__ == "__main__":
    conn = init_db()
    scan_and_update(conn)
