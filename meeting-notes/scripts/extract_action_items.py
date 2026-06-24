#!/usr/bin/env python3
"""
Scans raw meeting notes and extracts action items.
Looks for common patterns like "ACTION:", "@mention", or "will do X".
"""

import sys
import re

def extract_action_items(text: str) -> list[str]:
    items = []
    patterns = [
        r"ACTION[:\s]+(.+)",           # "ACTION: John will send report"
        r"@(\w+)\s+(?:will|to|should)\s+(.+)",  # "@alice will update docs"
        r"(\w+)\s+(?:will|to)\s+(.+?)(?:\.|$)",  # "Bob will schedule a call"
    ]

    for line in text.splitlines():
        line = line.strip()
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                items.append(f"- {line}")
                break  # avoid duplicates per line

    return items if items else ["- No action items detected"]

if __name__ == "__main__":
    # Read from argument or stdin
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
    else:
        raw_text = sys.stdin.read()

    print("## Extracted Action Items\n")
    for item in extract_action_items(raw_text):
        print(item)