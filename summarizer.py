import difflib

def summarize_change(prev_text: str, new_text: str) -> str:
    """
    Free offline summarizer.
    Uses difflib to detect what changed.
    Not as poetic as GPT, but costs nothing.
    """
    if prev_text == new_text:
        return ""

    differ = difflib.ndiff(prev_text.split(), new_text.split())
    added = []
    removed = []

    for line in differ:
        if line.startswith("+ "):
            added.append(line[2:])
        elif line.startswith("- "):
            removed.append(line[2:])

    summary_parts = []
    if removed:
        summary_parts.append(f"Removed: {' '.join(removed[:20])}...")
    if added:
        summary_parts.append(f"Added: {' '.join(added[:20])}...")

    if not summary_parts:
        return "Minor formatting or whitespace changes detected."

    return " | ".join(summary_parts)
