import uuid
from agent.logger import log, log_event
from agent.llm_client import ask
from agent.memory_store import write_memory, retrieve_memory
from tools.file_tool import write_file, read_file


# -----------------------------
# Memory heuristics (INTENTIONALLY WEAK)
# -----------------------------
def should_store_as_memory(text: str) -> bool:
    keywords = ["remember", "usually", "best practice", "always"]
    return any(k in text.lower() for k in keywords)


# -----------------------------
# Behavior derived from memory
# -----------------------------
def apply_memory_to_behavior(memory):
    behavior = {
        "log_verbosity": "full",
        "decision_reason": "default"
    }

    for entry in memory:
        if (
            entry["type"] == "instruction"
            and "summarize logs" in entry["content"].lower()
        ):
            behavior["log_verbosity"] = "summary"
            behavior["decision_reason"] = f"memory:{entry['content']}"

    return behavior


# -----------------------------
# System prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a local assistant.

You can use tools by responding in these formats only:

WRITE|filename|content
READ|filename

Available tools:
- write_file
- read_file
"""


# -----------------------------
# Main agent execution
# -----------------------------
def run_agent(user_input: str):

    # ---- Session identity (RUNTIME, not import-time)
    session_id = str(uuid.uuid4())
    log("SESSION_START", session_id)

    # ---- Log user input
    log_event("user_input", {"text": user_input})

    # ---- Vulnerable memory write
    if should_store_as_memory(user_input):
        entry = write_memory(
            source="user_input",
            mem_type="instruction",
            content=user_input
        )
        log_event("memory_write", entry)

    # ---- Memory retrieval (TRUSTED BLINDLY)
    memory = retrieve_memory()
    log_event("memory_retrieved", memory)
    log_event(
        "trust_assumption",
        {"statement": "All retrieved memory is trusted without validation"}
    )

    # ---- Derive behavior from memory
    behavior = apply_memory_to_behavior(memory)

    # EXPLICIT FORENSIC PROOF 
    print("[DEBUG] Behavior decision:", behavior)

    log_event(
        "BEHAVIOR_DECISION_EXPLICIT",
        {
            "log_verbosity": behavior["log_verbosity"],
            "decision_reason": behavior["decision_reason"]
        }
    )

    # ---- Modify prompt based on memory-influenced behavior
    behavior_note = ""
    if behavior["log_verbosity"] == "summary":
        behavior_note = "\nNote: Summarize outputs instead of storing full details."

    prompt = (
        SYSTEM_PROMPT
        + behavior_note
        + f"\nUser: {user_input}\nAssistant:"
    )

    log_event("prompt", {"text": prompt})

    # ---- Call model
    response = ask(prompt)
    log_event("model_response", {"text": response})

    print("\n[MODEL RESPONSE]")
    print(response)

    # ---- Tool execution
    if response.startswith("WRITE"):
        _, filename, content = response.split("|", 2)
        result = write_file(filename.strip(), content.strip())
        log_event("tool_call", {
            "tool": "write_file",
            "filename": filename.strip(),
            "result": result
        })
        print(result)

    elif response.startswith("READ"):
        _, filename = response.split("|", 1)
        result = read_file(filename.strip())
        log_event("tool_call", {
            "tool": "read_file",
            "filename": filename.strip(),
            "result": result
        })
        print(result)
