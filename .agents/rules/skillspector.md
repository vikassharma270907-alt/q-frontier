# NVIDIA SkillSpector & Maximum-Effort Governance

## 1. Skill & Extension Security Verification
- **Skill Safety Verification**: Whenever introducing, downloading, reviewing, or generating new AI agent skills, plugins, or MCP tools, run NVIDIA SkillSpector:
  ```bash
  skillspector scan "<target-folder-or-file>" --no-llm --format json
  ```
- **Review Line**:
  1. Static check: Verify risk score < 20 and no unexplained HIGH or CRITICAL findings.
  2. Semantic check: Inspect declared tools, network endpoints, file system access, and prompt instructions.
  3. Verdict: Only integrate when marked `APPROVE` or well-justified `CAUTION`. Immediately quarantine `REJECT` targets.

## 2. Maximum Effort, Best Model Tier & Max AI Credits
- **Maximum Reasoning Depth**:
  - Always execute tasks at maximum reasoning effort (`high` / `max` / up to 64k thinking tokens).
  - Extended thinking and deep reflection must be enabled for all planning, architecture, test writing, refactoring, and code generation.
  - Never take shortcuts, skip tests, or produce truncated code placeholders.
- **Best Model Selection**:
  - Always select top-tier models (`pro` / `opus` / `sonnet` / `Gemini 3.8 Flash (High)`).
  - Subagents must be invoked with `Model: "pro"` or `"inherit"` to ensure maximum capability.
- **Full AI Credits Utilization**:
  - Antigravity AI credits are enabled without restriction (`useAiCredits: true`).
  - Maximize thoroughness: run comprehensive test suites, verify all edge cases, and execute end-to-end audits without artificial frugality.
