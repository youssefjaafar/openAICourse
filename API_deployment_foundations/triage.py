"""
Placeholder triage logic.

This is deliberately fake: it always returns the same category and a canned
summary. It gives the API one clear place where real logic (rules, a model
call, ...) could be added later without touching the HTTP code in app.py.
"""

PLACEHOLDER_CATEGORY = "general_inquiry"


def triage_ticket(ticket_text: str) -> dict:
    return {
        "category": PLACEHOLDER_CATEGORY,
        "summary": (
            f"Placeholder summary for a {len(ticket_text)}-character ticket. "
            "No real triage was performed."
        ),
    }
