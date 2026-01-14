"""
Test API to receive callbacks from aivoice transcription service.

This API simulates a webhook endpoint that receives transcription results
from the aivoice transcription service after processing audio files.

Usage:
    python test_scripts/test_transcription_callback.py

The API will run on http://127.0.0.1:8008 by default.

You can configure the webhook_url in your aivoice transcription request
to point to this endpoint (e.g., http://your-server:8008/api/v1/transcription_callback)
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from config/dev.env
dev_env_file = project_root / 'config' / 'dev.env'
if dev_env_file.exists():
    load_dotenv(dev_env_file, override=False)
    print(f"✓ Loaded environment from: config/dev.env")
else:
    # Fallback to root .env if config/dev.env doesn't exist
    load_dotenv(override=False)
    print(f"⚠ config/dev.env not found, using default .env")

from db.message_logs_repository import AsyncMessageLogsRepository,TaskType, TaskStatus
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
API_KEY_NAME = "X-API-Key"
CALLBACK_PORT = int(os.getenv("CALLBACK_PORT", 8008))
APP_KEY = os.getenv("APP_KEY")

app = FastAPI(
    title="Transcription Callback Test API",
    description="Test API to receive transcription callbacks from aivoice service",
    version="1.0.0"
)

# API Key security setup
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: Optional[str] = Security(api_key_header)):
    """
    Validate API key from request header.
    
    Behavior:
    - If APP_KEY is set: Requires valid API key (returns 401 if missing or invalid)
    - If APP_KEY is not set: Accepts any request (for local testing without auth)
    """
    # If APP_KEY is configured, require authentication
    if APP_KEY:
        if not api_key:
            logger.warning("Missing API key in request")
            raise HTTPException(
                status_code=401,
                detail="Missing API Key. Please provide X-API-Key header."
            )
        if api_key != APP_KEY:
            logger.warning(f"Invalid API key attempt: {api_key[:5]}...")
            raise HTTPException(
                status_code=401,
                detail="Invalid API Key"
            )

    return api_key

# Store received callbacks in memory for testing
received_callbacks = []

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "Callback Test API is running",
        "endpoint": "/api/v1/callback",
        "total_callbacks": len(received_callbacks)
    }

@app.post("/api/v1/callback")
async def callback(
    request: Request,
    api_key: Optional[str] = Depends(get_api_key)
):
    """
    Generic webhook endpoint that accepts any JSON payload structure.
    
    This endpoint does NOT validate or require specific fields - it accepts
    any valid JSON object. This makes it flexible for testing different
    callback formats from various services.

    """
    try:
        # Get request body
        body = await request.json()
        
        # Log the callback
        callback_data = {
            "received_at": datetime.now().isoformat(),
            "headers": dict(request.headers),
            "api_key_provided": api_key is not None,
            "payload": body
        }
        
        received_callbacks.append(callback_data)
        
        logger.info("=" * 80)
        logger.info("RECEIVED CALLBACK")
        logger.info("=" * 80)
        logger.info(f"Timestamp: {callback_data['received_at']}")
        logger.info(f"API Key Provided: {callback_data['api_key_provided']}")

        
        # Print formatted output to console
        print("\n" + "=" * 80)
        print("CALLBACK RECEIVED")
        print("=" * 80)
        print(f"Time: {callback_data['received_at']}")
        print(f"\nPayload:")
        print(json.dumps(body, indent=2))
        print("=" * 80 + "\n")
        
        # Return success response
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Callback received successfully",
                "received_at": callback_data['received_at'],
                "callback_id": len(received_callbacks)
            }
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request body: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing callback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    print(f"\n{'=' * 80}")
    print("TRANSCRIPTION CALLBACK TEST API")
    print(f"{'=' * 80}")
    print(f"Starting server on 0.0.0.0:8008")
    print(f"\nEndpoint: http://0.0.0.0:8008/api/v1/callback")
    print(f"Health check: http://0.0.0.0:8008/")
    print(f"View callbacks: http://0.0.0.0:8008/api/v1/callbacks")
    print(f"Latest callback: http://0.0.0.0:8008/api/v1/latest_callback")
    print(f"\nUse this URL as webhook_url in your transcription requests:")
    print(f"  http://0.0.0.0:8008/api/v1/callback")
    print(f"\n{'=' * 80}\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=CALLBACK_PORT,
        log_level="info"
    )

