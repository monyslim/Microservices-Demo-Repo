from flask import Flask, jsonify
import datetime
import mysql.connector
import os
import time
import socket

app = Flask(__name__)

# File logging setup
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "output.txt")
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ MySQL DB config strictly from environment (no defaults!)
DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
    "port": int(os.environ["DB_PORT"])
}

# ✅ Wait for MySQL to be reachable before connecting
def wait_for_mysql(host, port, timeout=60):
    print(f"⏳ Waiting for MySQL at {host}:{port} ...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("✅ MySQL is ready!")
                return
        except OSError:
            time.sleep(1)
    raise RuntimeError(f"❌ Could not connect to MySQL at {host}:{port} after {timeout} seconds.")

# ✅ Database setup
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            access_time DATETIME
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# ⏱️ Wait for MySQL before running init_db
wait_for_mysql(DB_CONFIG["host"], DB_CONFIG["port"])
init_db()

# ✅ Main API route
@app.route("/api")
def api():
    now = datetime.datetime.now()
    log_entry = f"API accessed at {now.isoformat()}\n"

    # 1. Log to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    # 2. Log to MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO api_logs (access_time) VALUES (%s)", (now,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Hello from the backend!",
        "time": now.isoformat()
    })

# ✅ View logged entries
@app.route("/logs")
def get_logs():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, access_time FROM api_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    logs = [{"id": row[0], "time": row[1].isoformat()} for row in rows]
    return jsonify(logs)

# ✅ Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
