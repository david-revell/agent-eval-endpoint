"""
Simple callback API for receiving agent replies.

Run:
  python test_callbacks.py
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, ConfigDict, Field
import uvicorn

print("CWD:", os.getcwd())


load_dotenv(override=False)

# Configuration
API_KEY_NAME = "X-API-Key"
CALLBACK_PORT = int(os.getenv("CALLBACK_PORT", "8008"))
APP_KEY = os.getenv("APP_KEY")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_PATH = os.path.join(LOG_DIR, "callbacks.jsonl")

app = FastAPI(
    title="Agent Callback API",
    description="Callback endpoint for receiving agent responses",
    version="1.0.0",
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# API Key security setup
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: Optional[str] = Depends(api_key_header)) -> Optional[str]:
    """
    Validate API key from request header.

    Behavior:
    - If APP_KEY is set: require a matching key (401 on missing/invalid)
    - If APP_KEY is not set: accept any request (local testing)
    """
    if APP_KEY:
        if not api_key:
            logger.warning("Missing API key in request")
            raise HTTPException(status_code=401, detail="Missing API key")
        if api_key != APP_KEY:
            logger.warning("Invalid API key attempt")
            raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


class CallbackPayload(BaseModel):
    agent_answer: str = Field(..., description="Agent reply text")
    session_id: Optional[str] = Field(default=None)
    turn_id: Optional[str] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

    model_config = ConfigDict(extra="allow")


# Store received callbacks in memory for testing
received_callbacks: list[dict[str, Any]] = []


@app.get("/")
async def root() -> dict[str, Any]:
    """Health check."""
    return {
        "status": "Callback API is running",
        "endpoint": "/api/v1/callback",
        "total_callbacks": len(received_callbacks),
    }


@app.get("/api/v1/callbacks")
async def callbacks() -> dict[str, Any]:
    return {"count": len(received_callbacks), "items": received_callbacks}


@app.get("/api/v1/latest_callback")
async def latest_callback() -> dict[str, Any]:
    if not received_callbacks:
        return {"count": 0, "item": None}
    return {"count": len(received_callbacks), "item": received_callbacks[-1]}


@app.post("/api/v1/callback")
async def callback(
    payload: CallbackPayload,
    api_key: Optional[str] = Depends(get_api_key),
) -> JSONResponse:
    received_at = datetime.now().isoformat()
    callback_data = {
        "received_at": received_at,
        "api_key_provided": api_key is not None,
        "payload": payload.dict(),
    }
    received_callbacks.append(callback_data)
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(callback_data, ensure_ascii=True) + "\n")

    logger.info("Callback received at %s", received_at)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "received_at": received_at,
            "callback_id": len(received_callbacks),
        },
    )


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("AGENT CALLBACK API")
    print("=" * 80)
    print(f"Starting server on 0.0.0.0:{CALLBACK_PORT}")
    print(f"Endpoint: http://0.0.0.0:{CALLBACK_PORT}/api/v1/callback")
    print(f"Health:   http://0.0.0.0:{CALLBACK_PORT}/")
    print(f"Recent:   http://0.0.0.0:{CALLBACK_PORT}/api/v1/latest_callback")
    print("=" * 80 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=CALLBACK_PORT,
        log_level="info",
    )
