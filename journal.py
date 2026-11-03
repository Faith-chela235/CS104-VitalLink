from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

JOURNAL_PATH = Path(__file__).with_name("vital_link_journal.txt")
ENTRY_SEPARATOR = "\n---\n"


def load_entries() -> list[str]:
    if not JOURNAL_PATH.exists():
        JOURNAL_PATH.write_text("", encoding="utf-8")
        return []

    content = JOURNAL_PATH.read_text(encoding="utf-8")
    if not content.strip():
        return []
    return [entry.strip() for entry in content.split("---") if entry.strip()]


def save_entries(entries: list[str]) -> None:
    JOURNAL_PATH.write_text(ENTRY_SEPARATOR.join(entries) + (ENTRY_SEPARATOR if entries else ""), encoding="utf-8")


def add_entry(title: str | None, text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if title:
        entry = f"[{timestamp}] {title}\n{text.strip()}"
    else:
        entry = f"[{timestamp}]\n{text.strip()}"
    entries = load_entries()
    entries.insert(0, entry)
    save_entries(entries)
    print(f"Entry added to {JOURNAL_PATH.name}")


def list_entries() -> None:
    entries = load_entries()
    if not entries:
        print("No journal entries yet.")
        return

    for index, entry in enumerate(entries, start=1):
        print(f"\nEntry {index}\n{'-' * 40}\n{entry}\n{'-' * 40}")


def search_entries(query: str) -> None:
    entries = load_entries()
    matches = [entry for entry in entries if query.lower() in entry.lower()]
    if not matches:
        print(f"No matches found for: {query}")
        return

    for entry in matches:
        print(f"\n{entry}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple journal tracker.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a journal entry")
    add_parser.add_argument("text", nargs="+", help="Text for the journal entry")
    add_parser.add_argument("--title", help="Optional title for the entry")

    list_parser = subparsers.add_parser("list", help="List all journal entries")
    list_parser.set_defaults(command="list")

    search_parser = subparsers.add_parser("search", help="Search journal entries")
    search_parser.add_argument("query", help="Search text")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.title, " ".join(args.text))
    elif args.command == "list":
        list_entries()
    elif args.command == "search":
        search_entries(args.query)


if __name__ == "__main__":
    main()
