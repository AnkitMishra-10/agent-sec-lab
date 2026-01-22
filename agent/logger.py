import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/session.jsonl")

def log_event(event_type: str, data: dict):
    record = {
        "time": datetime.utcnow().isoformat(),
        "type": event_type,
        "data": data
    }
    LOG_FILE.parent.mkdir(exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
