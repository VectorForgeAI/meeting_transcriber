#!/usr/bin/env python3
import os
import sys
from pathlib import Path


SYSTEM_PROMPT = (
    "Role: You are an expert meeting note-taker and summarizer. Generate clean, "
    "compressed (target 20–50% of original length) minutes in Markdown, using active "
    "voice and precise attributions. Enforce the exact section order: 1) Meeting Details, "
    "2) Agenda Overview, 3) Discussion Summary, 4) Key Decisions and Outcomes, 5) Action Items, "
    "6) Open Items and Risks, 7) Next Steps and Adjournment, 8) Notes (only if needed). "
    "Action Items must be a table with columns: Action Item | Owner | Deadline | Details/Notes. "
    "Treat content as confidential; avoid hallucinations. If unknown, mark TBD with rationale."
)


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Failed to read file '{path}': {exc}")


def write_text_file(path: Path, content: str) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except Exception as exc:
        raise RuntimeError(f"Failed to write file '{path}': {exc}")


def generate_minutes(transcript: str, model: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError(
            "The 'openai' package is required. Install with: pip install openai"
        ) from exc

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Please generate meeting minutes from the transcript below.\n\n" + transcript
                    ),
                },
            ],
        )
    except Exception as exc:
        raise RuntimeError(f"OpenAI API error: {exc}")

    try:
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Empty response from model")
        return content
    except Exception as exc:
        raise RuntimeError(f"Unexpected API response shape: {exc}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python scripts/minutes.gen.py <transcript.txt> <out.md>",
            file=sys.stderr,
        )
        return 2

    in_path = Path(argv[1])
    out_path = Path(argv[2])

    if not in_path.exists():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        return 2

    try:
        transcript = read_text_file(in_path)
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        minutes_md = generate_minutes(transcript, model)
        write_text_file(out_path, minutes_md)
        print(f"Wrote minutes to: {out_path}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))


