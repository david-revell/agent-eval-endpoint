# Agent Eval Endpoint

## Table of contents

1. [Intent (two phases)](#intent-two-phases)
2. [Quick test (PowerShell)](#quick-test-powershell)
3. [Synthetic user runner](#synthetic-user-runner)
4. [Logs](#logs)
5. [Current files](#current-files)
6. [Status](#status)

This repo is a small scaffold for integrating external agents via a callback endpoint.
It provides a minimal local setup to receive agent replies, generate synthetic conversations,
and evaluate completed runs.

## Intent (two phases)

1. Receive-only integration.
   Start by exposing a public callback endpoint and accept agent replies.
   This proves the external agent can reach us and that our logging works.
   At this stage, we do not drive the conversation forward; we only receive.

2. Synthetic conversation generator.
   Use incoming agent replies to build conversation history, decide the next
   synthetic user turn (initially fixed messages, later state-based), and either continue or stop.
   This turns the endpoint into a controlled conversation loop and becomes the
   bridge to later evaluation.

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

## Public callback URL (ngrok)

To share the endpoint with an external agent, expose port 8008 with ngrok and use the public URL:

```
https://<your-ngrok-subdomain>.ngrok-free.dev/api/v1/callback
```

## Synthetic user runner

Send a minimal two-turn synthetic run into the callback endpoint:

```powershell
python synthetic_user.py
```

Optional env vars:

1. `CALLBACK_URL` (default: `http://127.0.0.1:8008/api/v1/callback`)
2. `APP_KEY` (adds `X-API-Key` header)

## Logs

Every callback received by the endpoint is appended to `logs/callbacks.jsonl` as a single JSON line.
This creates a simple, append-only record you can review or analyze later.

## Current files

- `test_callbacks.py`: simple callback endpoint (to customize)
- `NGROK_SETUP_GUIDE.md`: how to expose the endpoint with ngrok
- `evaluate_log.py`: post-hoc evaluator for conversation logs
- `requirements.txt`: Python dependencies

## Status

Scaffold in progress. The endpoint contract, synthetic user runner, and log format will be defined next.
