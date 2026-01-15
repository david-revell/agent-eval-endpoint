# Agent Eval Endpoint

This repo is a small scaffold for:

1. A public callback endpoint for external agents.
2. A synthetic user that can run scenarios against that endpoint.
3. A post-hoc evaluator for completed conversations.

There are no built-in demo agents here. The goal is to integrate external agents via the endpoint.

## What we are doing

We are building a minimal, local-first scaffold that lets you:

- Run a FastAPI callback endpoint for agent replies.
- Send synthetic user traffic into that endpoint.
- Evaluate completed conversations after the run.

## Quick test (PowerShell)

Start the server:

```powershell
python test_callbacks.py
```

Send a test callback (PowerShell 5.1):

```powershell
Invoke-WebRequest `
  -Uri http://127.0.0.1:8008/api/v1/callback `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"agent_answer":"Hello"}' `
  -UseBasicParsing
```

Note: The `-UseBasicParsing` flag avoids the Windows PowerShell 5.1 "Script Execution Risk" prompt.

## Current files

- `test_callbacks.py`: simple callback endpoint (to customize)
- `NGROK_SETUP_GUIDE.md`: how to expose the endpoint with ngrok
- `evaluate_log.py`: post-hoc evaluator for conversation logs
- `requirements.txt`: Python dependencies

## Status

Scaffold in progress. The endpoint contract, synthetic user runner, and log format will be defined next.
