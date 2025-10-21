import os
import re
from datetime import datetime
from typing import Optional


def _slugify_topic(topic: str) -> str:
    """Create a filesystem-friendly slug from the topic string."""
    slug = re.sub(r"\s+", "-", topic.strip().lower())
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    return slug or "topic"


def save_summary(topic: str, summary_text: str, output_dir: Optional[str] = None) -> str:
    """
    Save the summary to a timestamped text file and return the absolute path.

    - Creates `outputs/` if it does not exist
    - Filename format: <topic-slug>__YYYYmmdd-HHMMSS.txt
    """
    base_dir = output_dir or os.path.join(os.getcwd(), "outputs")
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{_slugify_topic(topic)}__{timestamp}.md"
    file_path = os.path.join(base_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    return os.path.abspath(file_path)


