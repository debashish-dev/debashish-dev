# Barebone E-Reader Pair Chat

A minimal, private, text-only web chat designed for old/simple browsers (like Kindle/Kobo experimental browsers).

## Features

- No JavaScript required.
- Initiator creates a unique 6-character pairing code.
- Receiver enters that code to join the same chat room.
- Plain form-based messaging.
- Auto-refresh every 8 seconds using HTML meta refresh.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:8000`

## Notes

- This is intentionally barebone and keeps data in-memory only.
- Restarting the server clears all chat rooms/messages.
- For real private deployment, set a strong `app.secret_key` and run behind HTTPS.
