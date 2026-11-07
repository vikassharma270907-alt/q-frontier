---
name: notebooklm
description: Research, document grounding, source ingestion, citation-backed QA, and Audio Overview podcasts using Google NotebookLM via MCP.
---

# NotebookLM Skill

Integrate Google NotebookLM into your development workflow for citation-backed research, architecture doc synthesis, source ingestion, and audio generation.

## Capabilities

1. **Citation-Backed QA**: Ask questions against ground-truth project documentation, specifications, or uploaded sources.
2. **Source Ingestion**: Add documentation URLs or text snippets to a notebook.
3. **Session Continuity**: Maintain conversational context across follow-up queries using `session_id`.
4. **Audio Overviews**: Generate two-host deep dive audio discussions (podcasts) summarizing documents or project plans.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `get_health` | Check authentication status and active notebook |
| `setup_auth` | Launch browser for Google login (persists session) |
| `list_notebooks` | View all registered notebooks in the library |
| `add_notebook` | Register a new NotebookLM notebook by share URL |
| `select_notebook` | Set the active notebook for queries |
| `add_source` | Ingest web URLs or text snippets into the notebook |
| `ask_question` | Query Gemini 2.5 grounded on notebook sources |
| `generate_audio` | Trigger Audio Overview generation |
| `get_audio_status` | Check if audio overview rendering is complete |
| `download_audio` | Save rendered audio overview mp3 to disk |

## Typical Workflows

### 1. First-Time Authentication
If `authenticated` is false:
1. Call `call_mcp_tool(notebooklm, setup_auth, {})`
2. Complete Google login in the browser tab that opens
3. Session cookies persist across IDE restarts

### 2. Querying Project Sources
```text
User: "What does our architecture doc say about rate limiting?"
Agent -> call_mcp_tool(notebooklm, ask_question, { question: "How is rate limiting designed in the architecture doc?" })
```

### 3. Adding Code or Documentation as a Source
```text
Agent -> call_mcp_tool(notebooklm, add_source, {
  title: "API Specification v2",
  text_content: "...",
  wait_for_index: true
})
```
