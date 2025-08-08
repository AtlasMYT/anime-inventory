from flask import Flask, jsonify, send_from_directory
import os
import json

# Load config
with open("config.json") as f:
    CONFIG = json.load(f)

ANIME_DIR = CONFIG["ANIME_DIR"]
DB_PATH = CONFIG["DB_PATH"]
PORT = CONFIG.get("PORT", 5000)

app = Flask(__name__)

def get_tree(path):
    tree = {"name": os.path.basename(path), "path": path, "children": []}
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                tree["children"].append(get_tree(entry.path))
            else:
                tree["children"].append({
                    "name": entry.name,
                    "path": entry.path
                })
    except PermissionError:
        pass
    return tree

@app.route("/api/tree")
def api_tree():
    return jsonify(get_tree(ANIME_DIR))

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
