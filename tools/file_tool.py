from pathlib import Path

# -------------------------------------------------
# Tool sandbox: all file operations are confined
# to the workspace directory
# -------------------------------------------------
BASE_DIR = Path("workspace").resolve()


def safe_path(filename: str) -> Path:
    """
    Resolve a file path safely inside the workspace.
    Prevents path traversal and enforces sandboxing.
    """
    path = (BASE_DIR / filename).resolve()

    if not str(path).startswith(str(BASE_DIR)):
        raise ValueError("Path traversal blocked")

    return path


def write_file(filename: str, content: str):
    """
    Write content to a file inside the workspace.
    """
    path = safe_path(filename)
    path.write_text(content, encoding="utf-8")

    return f"Wrote {len(content)} bytes to {filename}"


def read_file(filename: str):
    """
    Read content from a file inside the workspace.
    """
    path = safe_path(filename)

    if not path.exists():
        return "File not found"

    return path.read_text(encoding="utf-8")
