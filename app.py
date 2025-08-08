from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'anime.db')
ROOT_DIR = '/anime-data'

app = Flask(__name__, static_folder='static')

def get_tree():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT path FROM anime_files ORDER BY path")
    tree = {}
    for (fullpath,) in cur:
        rel = os.path.relpath(fullpath, ROOT_DIR)
        parts = rel.split(os.sep)
        node = tree
        for p in parts:
            node = node.setdefault(p, {})
    conn.close()
    return tree

@app.route('/api/tree')
def api_tree():
    return jsonify(get_tree())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def static_proxy(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
