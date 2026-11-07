# Mandatory Plugin & Skill First Execution Policy

This workspace and all projects built by Antigravity IDE operate under the **Mandatory Plugin & Skill First Execution Policy**.
Whenever Antigravity builds, refactors, tests, reviews, or automates code in ANY project, it MUST actively incorporate and prioritize installed plugins, skills, and MCP tools.

---

## 1. Core Operating Principles

1. **Skill & Plugin First (Zero Guesswork)**:
   - Never write code, mock APIs, or design layouts without first querying the corresponding specialized skill or MCP tool.
   - If a capability exists in an installed plugin or skill (e.g., Magic UI, Context7, Playwright, Strix, SkillSpector, NotebookLM, Token Optimizer), using it is MANDATORY.

2. **Continuous Maximum Effort & Intelligence**:
   - All pair programming, subagents, code generation, and reviews run at maximum reasoning effort (`effortLevel: high`, `maxThinkingTokens: 65536`).
   - All subagents use `Model: "pro"` or `Model: "inherit"`. Downgrading to light tiers is strictly prohibited.
   - AI credits are permanently enabled (`useAiCredits: true`).

---

## 2. Mandatory Plugin & Skill Orchestration by Domain

### A. Frontend & UI Engineering
- **Mandatory Tool / MCP**: `everything-claude-code_magic` (`searchRegistryItems`, `getRegistryItem`), `21st` MCP, and `21st-ui` skill.
- **Rules**:
  - Never hand-roll unstyled or generic UI components from scratch.
  - Query 21st / Magic MCP for production-grade React, Tailwind, and HTML5 components.
  - For brand, technology, or partner logos, use official SVGs from Magic MCP.
  - Ensure dark-mode elegance, fluid responsiveness (`clamp()`, container queries), and accessibility (WCAG 2.2 AA).

### B. Library Documentation & API Grounding
- **Mandatory Tool / MCP**: `everything-claude-code_context7` (`resolve-library-id`, `query-docs`) and `find-docs` skill.
- **Rules**:
  - Never guess library API signatures, deprecated methods, or breaking changes across major versions (FastAPI, Pydantic, Tailwind, React, etc.).
  - Always resolve library IDs and fetch authoritative docs before implementing unfamiliar integrations.

### C. Testing & End-to-End Verification
- **Mandatory Tool / MCP**: `everything-claude-code_playwright` (`browser_navigate`, `browser_snapshot`, `browser_evaluate`, `browser_take_screenshot`), `tdd-guide`, and `test-engineer`.
- **Rules**:
  - Minimum test coverage: **80%**.
  - All critical UI features must be verified across three viewports: Desktop (1440x900), Tablet (768x1024), and Mobile (390x844).
  - TDD cycle is strictly enforced: Red -> Green -> Refactor. Never alter tests to hide bugs.

### D. Security, Pentesting & Vulnerability Hardening
- **Mandatory Tool / MCP**: `security-reviewer`, `skillspector` (`scan_skill`), `strix` autonomous pentesting, and `armorantigravity`.
- **Rules**:
  - Zero hardcoded secrets, API tokens, private keys, or credentials.
  - Every external input must be validated via strict schemas (Pydantic / Zod / validation gates).
  - Test against OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, Path Traversal, SSRF).
  - Pre-vet any external agent tools or skills against the 71 SkillSpector security patterns.

### E. Code Quality, Immutability & Review
- **Mandatory Tool / MCP**: `code-reviewer`, `ponytail`, `code-simplifier`, and CodeRabbit standards.
- **Rules**:
  - Source files must remain under the 800-line maintainability ceiling.
  - Functions must remain focused (<50 lines).
  - Prefer immutable patterns: return fresh copies, never mutate objects in-place.
  - Run `code-reviewer` after any non-trivial code modification.

### F. Project Lifecycle & Autonomous Execution
- **Mandatory Tool / MCP**: `get-shit-done` (`/gsd-*`), `ralph-agent` autonomous loop, and `commit-reviewer`.
- **Rules**:
  - Plan before execution for complex initiatives.
  - Track atomic commits using Conventional Commits format (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).
  - Run full test verification suites before committing to git or pushing to remote.

---

## 3. Automation Sync Contract

Every project created or maintained by Antigravity must contain:
1. `.agents/rules/mandatory-plugins-and-skills.md` (or junction to master rules)
2. `.agents/skills/` with all 480+ available skills linked or accessible
3. `.mcp.json` configured with active MCP servers (Magic, 21st, Context7, Laya, etc.)
4. `.vscode/settings.json` configured with maximum reasoning effort and AI credit flags
5. Git hooks in `.git/hooks/` to auto-verify skill compliance on commit and checkout
