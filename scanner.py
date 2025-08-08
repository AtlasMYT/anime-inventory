import os
import sqlite3
import time
import json

# Load config
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
            size INTEGER,
            mtime REAL
        )
    ''')
    conn.commit()
    return conn

def scan_and_update(conn):
    c = conn.cursor()
    for root, dirs, files in os.walk(ANIME_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                stat = os.stat(full_path)
                c.execute('''
                    INSERT OR REPLACE INTO anime_files (path, size, mtime)
                    VALUES (?, ?, ?)
                ''', (full_path, stat.st_size, stat.st_mtime))
            except FileNotFoundError:
                continue
    conn.commit()

if __name__ == "__main__":
    conn = init_db()
    scan_and_update(conn)
    print("Scan complete.")
