"""
A minimal local API for learning purposes.

Endpoints:
  GET  /health         -> {"status": "ok"}
  POST /triage-ticket  -> placeholder category + summary for a support ticket

Runs only on your own machine (127.0.0.1). It does not call any external
service, store any data, or use any credentials.
"""

from flask import Flask, jsonify, request

from triage import triage_ticket

app = Flask(__name__)


def error_response(code, message, status=400):
    """Build a consistent JSON error: {"error": {"code": ..., "message": ...}}."""
    return jsonify({"error": {"code": code, "message": message}}), status


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/triage-ticket")
def triage_ticket_endpoint():
    # 1. The body must be a JSON object, e.g. {"ticket_text": "..."}.
    #    silent=True makes Flask return None (instead of an HTML error page)
    #    when the JSON is malformed or the Content-Type header is missing.
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error_response(
            "invalid_body",
            "Request body must be a JSON object sent with Content-Type: application/json.",
        )

    # 2. ticket_text must be present.
    if "ticket_text" not in body:
        return error_response("missing_field", "ticket_text is required.")

    ticket_text = body["ticket_text"]

    # 3. ticket_text must be a string (not a number, list, null, ...).
    if not isinstance(ticket_text, str):
        return error_response("invalid_type", "ticket_text must be a string.")

    # 4. ticket_text must contain something other than whitespace.
    if not ticket_text.strip():
        return error_response(
            "empty_value", "ticket_text must not be empty or whitespace-only."
        )

    # All checks passed: run the placeholder triage logic.
    result = triage_ticket(ticket_text.strip())
    return jsonify(result), 200


if __name__ == "__main__":
    # 127.0.0.1 = "this computer only"; other machines cannot reach the API.
    app.run(host="127.0.0.1", port=8000)
