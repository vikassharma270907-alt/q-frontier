---
trigger: always_on
description: Use agent-reach for live internet platform access across YouTube transcripts, Reddit, GitHub, Twitter/X, Bilibili, V2EX, and web reading without API keys.
---

## Agent Reach

When the user asks to search, fetch transcripts, read articles, or analyze discussions from online platforms (YouTube, GitHub, Reddit, Twitter/X, Bilibili, V2EX, Xueqiu, LinkedIn, Xiaohongshu, or direct web URLs) and native web fetch/search is insufficient:

- Use the `agent-reach` CLI:
  - `agent-reach read <url>` — automatically routes to the matching platform.
  - `agent-reach youtube subtitle <video_url>` — fetches complete video transcripts/subtitles.
  - `agent-reach github read <owner/repo>` — reads repositories, READMEs, PRs, and issue comments.
  - `agent-reach web search "<query>"` — searches the web via Exa engine with clean markdown extraction.
  - `agent-reach v2ex hot` / `agent-reach reddit search "<query>"` — pulls live community discussions.
  - `agent-reach channels` — inspects all available channels, actions, and parameters.
- Outputs are delivered in clean structured JSON (`ok`, `items`, `meta`, `error`).
- Read-only operations only: never attempts unauthorized write operations.
