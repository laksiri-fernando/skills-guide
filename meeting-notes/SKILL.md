---
name: meeting-notes
description: Format raw meeting notes into a structured summary. Use when
  the user pastes meeting notes, says "format my notes", "clean up these
  notes", or "summarize this meeting". Extracts action items, decisions,
  and attendees automatically.
allowed-tools: Bash(python3 *)
---

# Meeting Notes Formatter

Turns raw, messy meeting notes into a clean structured summary.

## Steps

1. Read the raw notes the user provides
2. Use the template in [assets/template.md](assets/template.md) as your output structure
3. Follow the style rules in [references/formatting-guide.md](references/formatting-guide.md)
4. Run the action item extractor script for accuracy:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract_action_items.py "$ARGUMENTS"
```

5. Fill in the template with your analysis + the script's extracted action items
6. Output the completed template as a markdown block

## Notes
- If attendees aren't listed, write "Not specified"
- If no decisions were made, write "No decisions recorded"
- Keep the summary under 5 bullet points