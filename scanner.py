#!/usr/bin/env python3
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'anime.db')
ROOT_DIR = '/anime-data'

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

def scan(conn):
    c = conn.cursor()
    for dirpath, _, files in os.walk(ROOT_DIR):
        for fn in files:
            full = os.path.join(dirpath, fn)
            try:
                st = os.stat(full)
            except FileNotFoundError:
                continue
            c.execute('''
              INSERT INTO anime_files(path, size, mtime)
              VALUES (?, ?, ?)
              ON CONFLICT(path) DO UPDATE SET
                size=excluded.size,
                mtime=excluded.mtime
            ''', (full, st.st_size, st.st_mtime))
    conn.commit()

if __name__ == '__main__':
    conn = init_db()
    scan(conn)
    conn.close()
    print("Scan complete.")
