import json
import os
from datetime import datetime

MEMORY_FILE = "agent_memory.json"

VALID_MEMORY_TYPES = [
    "instruction",
    "preference",
    "observation"
]

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def write_memory(source, mem_type, content):
    if mem_type not in VALID_MEMORY_TYPES:
        raise ValueError("Invalid memory type")

    memory = load_memory()

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "type": mem_type,
        "content": content
    }

    memory.append(entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    return entry

def retrieve_memory():
    return load_memory()
