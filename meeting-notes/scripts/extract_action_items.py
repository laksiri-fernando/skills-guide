#!/usr/bin/env python3
"""
Scans raw meeting notes and extracts action items as "WHO will WHAT".

Splits the text into sentences (notes are often one long line), then for each
sentence pulls out the actor and the action. Handles:
  - "@alice to update the docs"        -> "Alice will update the docs"
  - "John will send the report by Fri" -> "John will send the report by Fri"
  - "Bob to schedule a call"           -> "Bob will schedule a call"

Decision statements ("Decided to ...", "Agreed to ...") are NOT action items
and are skipped.
"""

import sys
import re

# Verbs that introduce a decision, not an assignment. Used as the leading word
# these would otherwise look like "<who> to <action>", so we exclude them.
DECISION_WORDS = {
    "decided", "agreed", "approved", "rejected", "deferred", "discussed",
    "resolved", "concluded",
}

# Sentence-level patterns. Each captures (who, action).
PATTERNS = [
    # "ACTION: John will send report"
    (re.compile(r"ACTION[:\s]+(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
    # "@alice will/to/should update the docs"
    (re.compile(r"@(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
    # "John will/to/should send the report by Friday"
    (re.compile(r"\b(?P<who>\w+)\s+(?:will|to|should)\s+(?P<action>.+)", re.IGNORECASE), None),
]


def split_sentences(text: str) -> list[str]:
    # Split on sentence terminators and newlines; keep non-empty fragments.
    parts = re.split(r"[.\n!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def extract_action_items(text: str) -> list[str]:
    items = []
    seen = set()
    for sentence in split_sentences(text):
        for pattern, _ in PATTERNS:
            match = pattern.search(sentence)
            if not match:
                continue
            who = match.group("who")
            if who.lower() in DECISION_WORDS:
                break  # a decision, not an action item
            action = match.group("action").strip().rstrip(".")
            who = who.capitalize()
            item = f"{who} will {action}"
            if item.lower() not in seen:
                seen.add(item.lower())
                items.append(f"- {item}")
            break  # first matching pattern wins for this sentence

    return items if items else ["- No action items detected"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
    else:
        raw_text = sys.stdin.read()

    print("## Extracted Action Items\n")
    for item in extract_action_items(raw_text):
        print(item)
