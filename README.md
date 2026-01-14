# Agent Eval Endpoint

This repo is a small scaffold for:

1. A public callback endpoint for external agents.
2. A synthetic user that can run scenarios against that endpoint.
3. A post-hoc evaluator for completed conversations.

There are no built-in demo agents here. The goal is to integrate external agents via the endpoint.

## Current files

- `test_callbacks.py`: simple callback endpoint (to customize)
- `NGROK_SETUP_GUIDE.md`: how to expose the endpoint with ngrok
- `evaluate_log.py`: post-hoc evaluator for conversation logs
- `requirements.txt`: Python dependencies

## Status

Scaffold in progress. The endpoint contract, synthetic user runner, and log format will be defined next.
