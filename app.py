from __future__ import annotations

import secrets
import string
from datetime import datetime, timezone
from typing import Dict, List

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "change-me-in-production"

rooms: Dict[str, Dict[str, object]] = {}


def make_code(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_room() -> str:
    while True:
        code = make_code()
        if code not in rooms:
            rooms[code] = {"messages": []}
            return code


@app.get("/")
def index():
    return render_template("index.html", active_code=session.get("room_code"), role=session.get("role"))


@app.post("/create")
def create():
    code = create_room()
    session["room_code"] = code
    session["role"] = "initiator"
    return redirect(url_for("chat", code=code))


@app.post("/join")
def join():
    code = request.form.get("code", "").strip().upper()
    if code not in rooms:
        return render_template("index.html", error="That pairing code does not exist.", active_code=None, role=None), 404

    session["room_code"] = code
    session["role"] = "receiver"
    return redirect(url_for("chat", code=code))


@app.route("/chat/<code>", methods=["GET", "POST"])
def chat(code: str):
    code = code.upper()
    room = rooms.get(code)
    if room is None:
        return redirect(url_for("index"))

    role = session.get("role") if session.get("room_code") == code else "guest"

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            entry = {
                "author": role,
                "text": message,
                "time": datetime.now(timezone.utc).strftime("%H:%M UTC"),
            }
            messages: List[dict] = room["messages"]  # type: ignore[assignment]
            messages.append(entry)
        return redirect(url_for("chat", code=code))

    return render_template("chat.html", code=code, role=role, messages=room["messages"])


@app.post("/leave")
def leave():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
