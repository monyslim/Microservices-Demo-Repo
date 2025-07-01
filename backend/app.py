from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "output.txt")
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/api")
def api():
    now = datetime.datetime.now().isoformat()
    log_entry = f"API accessed at {now}\n"

    # Write the log to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return jsonify({
        "message": "Hello from the backend!",
        "time": datetime.datetime.now().isoformat()
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)