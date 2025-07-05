from flask import Flask, jsonify
import datetime
import sqlite3
import os

app = Flask(__name__)

# File logging setup
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "output.txt")
os.makedirs(LOG_DIR, exist_ok=True)

# SQLite database setup
DB_FILE = "logs.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                access_time TEXT
            )
        ''')
        conn.commit()

init_db()

@app.route("/api")
def api():
    now = datetime.datetime.now().isoformat()
    log_entry = f"API accessed at {now}\n"

    # 1. Log to file (for Docker bind mount)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    # 2. Log to SQLite database
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO api_logs (access_time) VALUES (?)", (now,))
        conn.commit()

    return jsonify({
        "message": "Hello from the backend!",
        "time": now
    })

# ✅ New: Return all logged access times
@app.route("/logs")
def get_logs():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, access_time FROM api_logs ORDER BY id DESC")
        rows = cursor.fetchall()

    logs = [{"id": row[0], "time": row[1]} for row in rows]
    return jsonify(logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
