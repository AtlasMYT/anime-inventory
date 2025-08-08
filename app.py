import sqlite3
import os
import csv
import json
import subprocess
from flask import Flask, jsonify, send_from_directory, request, Response

# Load config
if not os.path.exists("config.json"):
    raise FileNotFoundError("config.json missing. Please create it.")

with open("config.json") as f:
    CONFIG = json.load(f)

ANIME_DIR = CONFIG["ANIME_DIR"]
DB_PATH = CONFIG["DB_PATH"]
PORT = CONFIG.get("PORT", 5000)

app = Flask(__name__)

def db_connect():
    return sqlite3.connect(DB_PATH)

def get_tree_from_db():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT path, name FROM anime_files ORDER BY path ASC")
    rows = cursor.fetchall()
    conn.close()

    tree = {"name": os.path.basename(ANIME_DIR), "children": {}}
    for path, name in rows:
        # Handle case if ANIME_DIR not present
        try:
            rel_path = os.path.relpath(path, ANIME_DIR)
        except ValueError:
            rel_path = path
        parts = rel_path.split(os.sep)
        node = tree
        for part in parts[:-1]:
            node = node["children"].setdefault(part, {"children": {}})
        node["children"][parts[-1]] = {}
    return tree

@app.route("/api/tree")
def api_tree():
    return jsonify(get_tree_from_db())

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").lower()
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, path, size, mtime_str FROM anime_files WHERE lower(name) LIKE ?", (f"%{q}%",))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"name": r[0], "path": r[1], "size": r[2], "mtime": r[3]} for r in rows])

@app.route("/api/export_csv")
def api_export_csv():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name, path, size, mtime_str FROM anime_files ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()

    def generate():
        output = csv.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Name", "Path", "Size (bytes)", "Last Modified"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for row in rows:
            writer.writerow(row)
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=anime_inventory.csv"})

@app.route("/api/rescan", methods=["POST"])
def api_rescan():
    subprocess.run(["python3", "scanner.py"])
    return jsonify({"status": "Rescan complete"})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
