import os
from typing import Any, Dict, List

from tavily import TavilyClient


class SearchError(Exception):
    """Raised when the web search fails."""
def _get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise SearchError(
            "Missing TAVILY_API_KEY. Set it in your environment or .env file."
        )
    return TavilyClient(api_key=api_key)


def search_web(topic: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """
    Search the web for the given topic using the Tavily API.
    Returns a list of results, each containing at least: title, url, content.
    """
    if not topic or not topic.strip():
        raise ValueError("Topic must be a non-empty string")

    client = _get_tavily_client()

    try:
        response = client.search(
            query=topic.strip(),
            max_results=max(1, int(max_results)),
            search_depth="advanced",
            include_answers=False,
            include_raw_content=True,
        )
    except Exception as exc:
        raise SearchError(f"Tavily search failed: {exc}") from exc

    results = response.get("results", []) if isinstance(response, dict) else []

    normalized: List[Dict[str, Any]] = []
    for item in results:
        normalized.append(
            {
                "title": item.get("title") or "Untitled",
                "url": item.get("url") or item.get("source_url") or "",
                "content": item.get("content") or item.get("raw_content") or "",
            }
        )

    if not normalized:
        raise SearchError("No results returned from Tavily for this query.")

    return normalized


