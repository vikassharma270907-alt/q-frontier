---
trigger: always_on
---
# Performance Optimization

## Model Selection & Maximum Effort Strategy (Mandatory)

**Best Model Tier Selection (Zero Downgrade Policy)**:
- **Pro / Opus / Sonnet / Gemini 3.8 Flash (High) / Gemini 3.1 Pro**:
  - Always select top-tier models for all tasks, pair programming, subagents, code generation, and reviews.
  - Never downgrade subagent models to light tiers (`haiku` or `flash_lite`). All subagents run with `model: pro` or `model: inherit`.
  - Deep architectural decisions, mission-critical security checks, and complex refactoring demand the highest intelligence ceiling available.

**Maximum Effort & Extended Thinking**:
- **Effort Level**: Always operate at maximum reasoning effort (`effortLevel: "max"`, `reasoningEffort: "high"`).
- **Thinking Budget**: Full 64,000 thinking tokens enabled (`maxThinkingTokens: 65536`).
- **Extended Thinking**: `alwaysThinkingEnabled: true` and `enableExtendedThinking: true` active on all sessions.
- **Max AI Credits**: `useAiCredits: true` is unconditionally enabled. Leverage credits fully to perform thorough TDD test suites, comprehensive verification loops, and exhaustive code quality passes without artificial frugality.

## Context Window Management

Avoid last 20% of context window for:
- Large-scale refactoring
- Feature implementation spanning multiple files
- Debugging complex interactions

Lower context sensitivity tasks:
- Single-file edits
- Independent utility creation
- Documentation updates
- Simple bug fixes

## Extended Thinking + Plan Mode

In Claude Code, adaptive reasoning lets the model choose how much to think for each task.
For Fable models, Sonnet 5 and later, and Opus 4.7 and later, use effort to control reasoning
rather than a fixed token budget. Available levels depend on the model.

Control thinking via:
- **Effort**: Use `/effort` in a session, `--effort <level>` at launch, or `CLAUDE_CODE_EFFORT_LEVEL`. Save a per-model level in `modelSettings` in `~/.claude/settings.json`; the older user-level `effortLevel` key does not apply to Opus 5.5 or newer models.
- **Toggle**: Option+T (macOS) / Alt+T (Windows/Linux), or `alwaysThinkingEnabled` in settings. These cannot disable thinking on Opus 5.5, Sonnet 5.5, or Fable models.
- **Fixed budget**: Claude Code ignores positive `MAX_THINKING_TOKENS` values on adaptive reasoning models. On Opus 4.6 or Sonnet 4.6, set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` to use a fixed budget with `MAX_THINKING_TOKENS`.
- **Verbose mode**: Ctrl+O to see thinking output

See [Claude Code model configuration](https://code.claude.com/docs/en/model-config#adjust-effort-level)
and [environment variables](https://code.claude.com/docs/en/env-vars) for supported controls.

For complex tasks requiring deep reasoning:
1. Choose a higher supported effort level, such as `/effort high`
2. Enable **Plan Mode** for structured approach
3. Use multiple critique rounds for thorough analysis
4. Use split role sub-agents for diverse perspectives

## Build Troubleshooting

If build fails:
1. Use **build-error-resolver** agent
2. Analyze error messages
3. Fix incrementally
4. Verify after each fix
