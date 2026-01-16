# DESIGN

## Table of contents

1. [End-to-end flow](#end-to-end-flow)
2. [Workboard](#workboard)

## End-to-end flow

1. [x] Run the callback endpoint locally (`python test_callbacks.py`).
2. [x] Expose it with ngrok (`ngrok http 8008`) and share the public `/api/v1/callback` URL.
3. Confirm you can receive a single agent reply.
   3.1 [x] Manual local POST (self-test).
   3.2 [ ] Reply from external Palete agent.
4. [x] Log incoming callbacks (`callbacks.jsonl`).
5. [ ] Define a minimal per-session conversation state (simple JSON).
6. [ ] On each callback, append the agent reply to that state.
7. [ ] Build a synthetic loop that reads the state, produces the next user turn, and decides stop/continue.
8. [ ] Run one full conversation end-to-end (single session, low volume).
9. [ ] Once stable, scale to multiple conversations/turns.
10. [ ] Finally, wire the evaluator to read the new log format and produce scores.

## Workboard

Planned:

1. Revisit End-to-end flow 3.1 and clarify the meaning of "manual" and "self-test".
2. Ensure documentation mentions the public callback URL (not only local).

In Progress:

Done:
