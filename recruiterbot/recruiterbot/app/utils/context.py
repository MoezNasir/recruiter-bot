import os
import re

DATA_DIR = "data"
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _load_stripped(filename: str) -> str:
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return COMMENT_RE.sub("", text).strip()


def load_about() -> str:
    return _load_stripped("about.md")


def load_boundaries() -> str:
    return _load_stripped("boundaries.md")


def get_deflection_message() -> str:
    """Pull the exact deflection message from boundaries.md rather than
    letting an LLM improvise one — keeps the response deterministic and
    immune to prompt-injection attempts embedded in the recruiter's question."""
    text = load_boundaries()
    match = re.search(r"## Deflection message\s*\n(.+?)(?=\n##|\Z)", text, re.DOTALL)
    if match:
        return match.group(1).strip().strip('"')
    return "That's something I'd rather discuss directly — feel free to reach out."