import argparse
import os
import sys
from typing import Optional

from dotenv import load_dotenv

from utils.io_utils import save_summary
from search import search_web, SearchError
from summarize import summarize_findings, SummarizationError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Personal Research Assistant: search, analyze, and summarize a topic."
    )
    parser.add_argument("topic", type=str, help="Research topic or question")
    
    parser.add_argument(
        "--max-results",
        type=int,
        default=8,
        help="Number of web results to analyze (default: 8)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="gpt-4o-mini model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save summaries (default: ./outputs)",
    )
    return parser.parse_args()


def main(argv: Optional[list] = None) -> int:
    load_dotenv() 

    args = parse_args()
    topic = args.topic

    try:
        results = search_web(topic, max_results=args.max_results)
    except SearchError as err:
        print(f"[error] Web search failed: {err}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"[error] Unexpected search error: {exc}", file=sys.stderr)
        return 2

    try:
        summary = summarize_findings(topic, results, model=args.model)
    except SummarizationError as err:
        print(f"[error] Summarization failed: {err}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"[error] Unexpected summarization error: {exc}", file=sys.stderr)
        return 3

    try:
        path = save_summary(topic, summary, output_dir=args.output_dir)
    except Exception as exc:
        print(f"[error] Failed to save summary: {exc}", file=sys.stderr)
        return 4

    print("\n=== Summary ===\n")
    print(summary)
    print("\nSaved to:")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


