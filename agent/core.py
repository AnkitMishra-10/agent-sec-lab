from agent.logger import log_event
from agent.llm_client import ask
from tools.file_tool import write_file, read_file

SYSTEM_PROMPT = """
You are a local assistant.

You can use tools by responding in these formats only:

WRITE|filename|content
READ|filename

Available tools:
- write_file
- read_file
"""

def run_agent(user_input: str):
    prompt = SYSTEM_PROMPT + f"\nUser: {user_input}\nAssistant:"

    log_event("user_input", {"text": user_input})
    log_event("prompt", {"text": prompt})

    response = ask(prompt)

    log_event("model_response", {"text": response})

    print("\n[MODEL RESPONSE]")
    print(response)

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

