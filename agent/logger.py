import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "session.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

def log(event, data):
    # simple human-readable log 
    print(f"[LOG] {event}: {data}")

def log_event(event, data):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "data": data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()
