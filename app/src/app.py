import os
import socket
import signal
import sys
import time
from flask import Flask, jsonify

app = Flask(__name__)
is_shutting_down = False


@app.route("/")
def home():
    if is_shutting_down:
        return jsonify({"status": "error", "message": "Service unavailable"}), 503
    return jsonify(
        {
            "status": "success",
            "message": "Hello from the Senior-Level DevOps Monorepo backend API!",
            "hostname": socket.gethostname(),
            "environment": os.getenv("ENV", "production"),
        }
    )


@app.route("/health")
def health():
    # Senior Strategy: Fail health checks immediately during graceful shutdown
    # This forces Load Balancers to stop routing new traffic here before the app stops
    if is_shutting_down:
        return jsonify({"status": "terminating"}), 503
    return jsonify({"status": "healthy"}), 200


def handle_graceful_shutdown(signum, frame):
    global is_shutting_down
    print(
        f"Received signal {signum}. Initiating senior graceful shutdown process...",
        flush=True,
    )
    is_shutting_down = True

    # Simulate waiting 3 seconds for current HTTP flights to cleanly finish drain lines
    time.sleep(3)
    print("All requests drained. Process exiting safely.", flush=True)
    sys.exit(0)


# Connect system OS kill signals to our graceful lifecycle handler
signal.signal(signal.SIGTERM, handle_graceful_shutdown)
signal.signal(signal.SIGINT, handle_graceful_shutdown)

if __name__ == "__main__":
    # Production note: In a true production environment, Gunicorn/Uvicorn would wrap this.
    app.run(host="0.0.0.0", port=5000)
