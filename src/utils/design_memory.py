"""Design memory system to track recent design choices and encourage variation."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import TypedDict


class DesignSummary(TypedDict):
    """Summary of a design from a specific day."""

    date: str
    brief: str


# Memory file location (at project root)
MEMORY_FILE = Path(__file__).parent.parent.parent / "design_memory.json"

# How many days of design history to keep
MEMORY_WINDOW_DAYS = 10

# Aesthetic patterns to detect in design briefs
# Maps aesthetic name to keywords/phrases that indicate its use
AESTHETIC_PATTERNS: dict[str, list[str]] = {
    "terminal/CRT/hacker": [
        "terminal",
        "crt",
        "command line",
        "command-line",
        "monospace",
        "green on black",
        "green text",
        "matrix",
        "hacker",
        "dos",
        "console",
        "scanline",
        "phosphor",
        "retro computer",
    ],
    "newspaper/broadsheet": [
        "newspaper",
        "broadsheet",
        "editorial",
        "gazette",
        "print journalism",
        "masthead",
        "column layout",
        "front page",
    ],
    "dark/somber/urgent": [
        "dark background",
        "somber",
        "urgent",
        "emergency",
        "crisis",
        "alarm",
        "warning",
        "dark mode",
        "black background",
    ],
    "minimalist typography": [
        "typographic hierarchy",
        "typography only",
        "pure type",
        "minimal decoration",
        "whitespace",
        "type hierarchy",
    ],
    "government/classified": [
        "classified",
        "redacted",
        "government",
        "dossier",
        "intelligence",
        "confidential",
        "top secret",
    ],
}


def extract_design_summary(html: str, date: str) -> DesignSummary:
    """
    Extract design summary from generated HTML.

    Looks for the DESIGN BRIEF comment and extracts it.
    If not found, creates a minimal summary.
    """
    # Try to find the DESIGN BRIEF comment
    brief_match = re.search(
        r"<!--\s*DESIGN BRIEF:\s*(.*?)\s*-->", html, re.DOTALL | re.IGNORECASE
    )

    if brief_match:
        brief = brief_match.group(1).strip()
        # Clean up excessive whitespace
        brief = re.sub(r"\s+", " ", brief)
    else:
        # Fallback if no design brief found
        brief = "No design brief found in generated HTML"

    return {"date": date, "brief": brief}


def save_design_summary(summary: DesignSummary) -> None:
    """
    Append today's design to memory file.

    Keeps only the last MEMORY_WINDOW_DAYS days of designs.
    """
    memories = load_design_memory()

    # Add new summary
    memories.append(summary)

    # Keep only last N days
    memories = memories[-MEMORY_WINDOW_DAYS:]

    # Save back to file
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memories, indent=2))


def load_design_memory() -> list[DesignSummary]:
    """Load recent design summaries from file."""
    if MEMORY_FILE.exists():
        try:
            content = MEMORY_FILE.read_text()
            data = json.loads(content)
            # Validate structure
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, ValueError):
            # If file is corrupted, start fresh
            pass

    return []


def get_recent_designs(n: int = 3) -> list[DesignSummary]:
    """Get the N most recent design summaries."""
    memories = load_design_memory()
    return memories[-n:] if memories else []


def format_design_memory(recent_designs: list[DesignSummary]) -> str:
    """
    Format recent designs as context for the prompt.

    Returns XML-formatted section describing recent designs.
    """
    if not recent_designs:
        return """<recent_designs>
No previous designs on record. This is your first design!
</recent_designs>"""

    lines = ["<recent_designs>"]
    lines.append(
        "The following designs were used in recent days. DO NOT repeat these approaches—find something different.\n"
    )

    for design in recent_designs:
        # Truncate brief if too long
        brief = design["brief"]
        if len(brief) > 300:
            brief = brief[:297] + "..."

        lines.append(f"**{design['date']}**: {brief}\n")

    lines.append("</recent_designs>")
    return "\n".join(lines)


def get_today_date() -> str:
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def detect_tired_aesthetics(memories: list[DesignSummary]) -> list[str]:
    """
    Analyze recent design briefs to detect which aesthetics have been used.

    Returns a list of aesthetic names that appear in recent designs.
    These are "tired" and should be avoided until they fall out of the window.
    """
    if not memories:
        return []

    # Combine all recent briefs into one text blob for searching
    combined_briefs = " ".join(m["brief"].lower() for m in memories)

    tired = []
    for aesthetic_name, keywords in AESTHETIC_PATTERNS.items():
        # Check if any keyword appears in recent briefs
        for keyword in keywords:
            if keyword.lower() in combined_briefs:
                tired.append(aesthetic_name)
                break  # Found this aesthetic, move to next

    return tired


def format_tired_aesthetics(tired: list[str]) -> str:
    """
    Format the tired aesthetics warning for the prompt.

    Returns XML-formatted section listing aesthetics to avoid,
    or empty string if no tired aesthetics.
    """
    if not tired:
        return ""

    tired_list = ", ".join(tired)
    return f"""<tired_aesthetics>
The following aesthetic directions have been used in the last {MEMORY_WINDOW_DAYS} days and should be AVOIDED today:
{tired_list}

These aren't permanently banned—they'll become available again once they fall out of the {MEMORY_WINDOW_DAYS}-day window. But for today, choose something different.
</tired_aesthetics>"""


def get_tired_aesthetics_context() -> str:
    """
    Get the tired aesthetics context for the builder prompt.

    Loads memory, detects tired aesthetics, and formats the warning.
    """
    memories = load_design_memory()
    tired = detect_tired_aesthetics(memories)
    return format_tired_aesthetics(tired)
