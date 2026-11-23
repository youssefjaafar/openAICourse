# Ticket Triage API (learning project)

A minimal local API built with [Flask](https://flask.palletsprojects.com/).
It runs only on your own computer (`127.0.0.1`), calls no external systems,
stores no data, and needs no credentials. All ticket text in this guide is
fictional.

## File structure

```
API_deployment_foundations/
├── app.py            # The API: routes + input validation
├── triage.py         # Placeholder triage logic (swap in real logic later)
├── requirements.txt  # Python dependencies
├── .gitignore        # Keeps .venv/ and __pycache__/ out of git
└── README.md         # This file
```

## 1. Install dependencies

Requires Python 3.9+.

```bash
cd API_deployment_foundations
python3 -m venv .venv              # create an isolated environment
source .venv/bin/activate          # activate it (Windows: .venv\Scripts\activate)
pip install -r requirements.txt    # install Flask
```

## 2. Run the API

```bash
python app.py
```

You should see `Running on http://127.0.0.1:8000`. Leave this terminal open
and run the test commands below in a **second** terminal. Stop the server with
`Ctrl+C`.

> Port 8000 is used instead of Flask's default 5000, because macOS uses 5000
> for AirPlay Receiver.

## 3. Success test commands

Each command uses `-w` to print the HTTP status after the response body.

**Health check**

```bash
curl -s -w '\nHTTP status: %{http_code}\n' http://127.0.0.1:8000/health
```

```
{"status":"ok"}

HTTP status: 200
```

**Triage a ticket**

```bash
curl -s -w '\nHTTP status: %{http_code}\n' \
  -X POST http://127.0.0.1:8000/triage-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "Hi, I cannot log in to my ExampleApp account after resetting my password. The login page just reloads."}'
```

```
{"category":"general_inquiry","summary":"Placeholder summary for a 102-character ticket. No real triage was performed."}

HTTP status: 200
```

## 4. Error test commands

**Missing `ticket_text`**

```bash
curl -s -w '\nHTTP status: %{http_code}\n' \
  -X POST http://127.0.0.1:8000/triage-ticket \
  -H "Content-Type: application/json" \
  -d '{}'
```

```
{"error":{"code":"missing_field","message":"ticket_text is required."}}

HTTP status: 400
```

**Empty `ticket_text`** (whitespace-only like `"   "` gives the same result)

```bash
curl -s -w '\nHTTP status: %{http_code}\n' \
  -X POST http://127.0.0.1:8000/triage-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": ""}'
```

```
{"error":{"code":"empty_value","message":"ticket_text must not be empty or whitespace-only."}}

HTTP status: 400
```

**Numeric `ticket_text`** (`null`, lists, etc. give the same result)

```bash
curl -s -w '\nHTTP status: %{http_code}\n' \
  -X POST http://127.0.0.1:8000/triage-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": 12345}'
```

```
{"error":{"code":"invalid_type","message":"ticket_text must be a string."}}

HTTP status: 400
```

**Body is not a JSON object** (malformed JSON, a JSON array, or a missing
`Content-Type: application/json` header)

```bash
curl -s -w '\nHTTP status: %{http_code}\n' \
  -X POST http://127.0.0.1:8000/triage-ticket \
  -H "Content-Type: application/json" \
  -d '["hello"]'
```

```
{"error":{"code":"invalid_body","message":"Request body must be a JSON object sent with Content-Type: application/json."}}

HTTP status: 400
```

## 5. Request/response contract

### `GET /health`

| | |
|---|---|
| Request | No body |
| `200 OK` | `{"status": "ok"}` |

### `POST /triage-ticket`

**Request.** Header `Content-Type: application/json`. The body is a JSON object:

| Field | Type | Required | Rule |
|---|---|---|---|
| `ticket_text` | string | yes | Must contain at least one non-whitespace character |

Any other fields in the body are ignored.

**`200 OK`.** The values are placeholders. No real triage happens.

```json
{"category": "general_inquiry", "summary": "Placeholder summary for a <N>-character ticket. No real triage was performed."}
```

**`400 Bad Request`.** Every error has the same shape:

```json
{"error": {"code": "<error_code>", "message": "<human-readable explanation>"}}
```

| `code` | When |
|---|---|
| `invalid_body` | Body is not a JSON object (malformed, array, or wrong/missing Content-Type) |
| `missing_field` | `ticket_text` key is absent |
| `invalid_type` | `ticket_text` is not a string (number, `null`, list, object, boolean) |
| `empty_value` | `ticket_text` is `""` or whitespace-only |

The checks run in that order, and the API returns the first one that fails.
