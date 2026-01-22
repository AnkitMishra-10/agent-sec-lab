import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

def ask(prompt: str) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    r.raise_for_status()
    return r.json()["response"]

if __name__ == "__main__":
    print(ask("Say hello in one short sentence."))
