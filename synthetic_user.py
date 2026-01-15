"""
Minimal synthetic user runner.

Run:
  python synthetic_user.py
"""

from __future__ import annotations

import json
import os
import uuid
from urllib import request


ENDPOINT_URL = os.getenv("CALLBACK_URL", "http://127.0.0.1:8008/api/v1/callback")
API_KEY = os.getenv("APP_KEY")


def post_json(url: str, payload: dict) -> str:
    data = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    req = request.Request(url, data=data, headers=headers, method="POST")
    with request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8")


def main() -> None:
    session_id = str(uuid.uuid4())
    turns = [
        "Hello, this is a synthetic user.",
        "Can you confirm you received my message?",
    ]

    for idx, text in enumerate(turns, start=1):
        payload = {
            "agent_answer": text,
            "session_id": session_id,
            "turn_id": f"turn-{idx:03d}",
            "metadata": {"source": "synthetic_user"},
        }
        response_text = post_json(ENDPOINT_URL, payload)
        print(f"Sent turn {idx}: {response_text}")


if __name__ == "__main__":
    main()
