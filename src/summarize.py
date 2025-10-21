# import os
# from typing import Any, Dict, List

# from anthropic import Anthropic, APIStatusError


# class SummarizationError(Exception):
#     """Raised when the summarization step fails."""


# def _get_anthropic_client() -> Anthropic:
#     api_key = os.getenv("ANTHROPIC_API_KEY")
#     if not api_key:
#         raise SummarizationError(
#             "Missing ANTHROPIC_API_KEY. Set it in your environment or .env file."
#         )
#     return Anthropic(api_key=api_key)


# def summarize_findings(
#     topic: str,
#     search_results: List[Dict[str, Any]],
#     model: str = "claude-3.5-sonnet-latest",
# ) -> str:
#     """
#     Use Anthropic Claude to produce a concise, well-structured summary of the findings.
#     """
#     if not search_results:
#         raise ValueError("search_results must be a non-empty list")

#     client = _get_anthropic_client()

#     # Prepare a compact context for the model
#     # Keep each item small to avoid hitting token limits.
#     snippets: List[str] = []
#     for idx, r in enumerate(search_results, start=1):
#         title = (r.get("title") or "Untitled").strip()
#         url = (r.get("url") or "").strip()
#         content = (r.get("content") or "").strip()
#         # Truncate content to a reasonable size
#         if len(content) > 1500:
#             content = content[:1500] + "..."
#         snippets.append(f"[{idx}] {title}\nURL: {url}\nExcerpt: {content}")

#     context_block = "\n\n".join(snippets)

#     system_prompt = (
#         "You are a meticulous research assistant. You synthesize findings across sources, "
#         "note agreements/disagreements, caveats, and provide actionable insights."
#     )

#     user_prompt = (
#         f"Topic: {topic}\n\n"
#         "You will receive web research snippets labeled [1], [2], ... with URLs.\n"
#         "- Extract the key points concisely (bulleted).\n"
#         "- Note differing perspectives or uncertainties.\n"
#         "- Provide a brief, practical takeaway.\n"
#         "- List cited sources with their [index] and URL.\n\n"
#         "Snippets:\n" + context_block + "\n\n"
#         "Write the final answer only."
#     )

#     try:
#         msg = client.messages.create(
#             model=model,
#             max_tokens=10,
#             temperature=0.2,
#             system=system_prompt,
#             messages=[{"role": "user", "content": user_prompt}],
#         )
#     except APIStatusError as api_err:
#         raise SummarizationError(f"Anthropic API error: {api_err}") from api_err
#     except Exception as exc:
#         raise SummarizationError(f"Summarization failed: {exc}") from exc

#     parts = []
#     for block in getattr(msg, "content", []) or []:
#         text = getattr(block, "text", None)
#         if text:
#             parts.append(text)
#     result = "\n".join(parts).strip()
#     return result or "No summary generated."

import os
from openai import OpenAI

class SummarizationError(Exception):
    """Raised when the summarization step fails."""

def _get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SummarizationError("Missing OPENAI_API_KEY. Set it in your environment or .env file.")
    return OpenAI(api_key=api_key)

def summarize_findings(topic, search_results, model="gpt-4o-mini"):
    if not search_results:
        raise ValueError("search_results must be a non-empty list")

    client = _get_openai_client()

    snippets = []
    for idx, r in enumerate(search_results, start=1):
        title = (r.get("title") or "Untitled").strip()
        url = (r.get("url") or "").strip()
        content = (r.get("content") or "").strip()
        if len(content) > 1500:
            content = content[:1500] + "..."
        snippets.append(f"[{idx}] {title}\nURL: {url}\nExcerpt: {content}")

    context_block = "\n\n".join(snippets)

    system_prompt = (
        "You are a meticulous research assistant. You synthesize findings across sources, "
        "note agreements/disagreements, caveats, and provide actionable insights."
    )

    user_prompt = (
        f"Topic: {topic}\n\n"
        "You will receive web research snippets labeled [1], [2], ... with URLs.\n"
        "- Extract the key points concisely (bulleted).\n"
        "- Note differing perspectives or uncertainties.\n"
        "- Provide a brief, practical takeaway.\n"
        "- List cited sources with their [index] and URL.\n\n"
        "Snippets:\n" + context_block + "\n\n"
        "Write the final answer only."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        raise SummarizationError(f"OpenAI summarization failed: {exc}")



