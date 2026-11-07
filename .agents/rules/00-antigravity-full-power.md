# Antigravity Full-Power Automation Policy

This workspace operates under the **Full-Power Antigravity Automation Policy**. All plugins, skills (330+), specialized agents (73+), workflows (98), and rules are active at maximum strength across all projects.

## Core Tenets (Non-Negotiable)

1. **Autonomous Proactivity**: NEVER wait for the user to explicitly ask for planning, testing, code review, or security checks. Trigger domain specialists proactively.
2. **Plan Before Code**: For any new feature, architecture change, or non-trivial refactor, immediately engage `planner` and `architect` to map out dependencies, files, and milestones.
3. **Strict Test-Driven Development (TDD)**:
   - Always write tests first (RED).
   - Implement the minimal clean code to pass (GREEN).
   - Refactor with confidence (IMPROVE).
   - Target minimum 80% coverage across unit, integration, and E2E layers.
4. **CodeRabbit Automated Quality Gate & Review**:
   - Every file created or updated must be reviewed with `code-reviewer` and CodeRabbit rules.
   - For pull requests or branches with CodeRabbit bot feedback, use `autofix` to review and resolve feedback.
   - Zero tolerance for critical/high severity flaws (memory leaks, unhandled errors, N+1 queries, race conditions).
5. **Security & Armor Antigravity**:
   - Zero hardcoded secrets, API keys, or private tokens.
   - Always validate and sanitize external inputs at system boundaries using schemas.
   - Guard against OWASP Top 10 vulnerabilities (SQL/NoSQL injection, XSS, CSRF, Path Traversal, SSRF).
6. **Immutability & Maintainability**:
   - Functions under 50 lines; source files under 800 lines ceiling.
   - Always return fresh object copies rather than mutating arguments or state in-place.
   - Explicit error handling: never swallow exceptions or drop errors silently.
7. **Maximum Reasoning Effort, Best Models & Max AI Credits (CRITICAL)**:
   - **Maximum Effort Everywhere**: Always operate at maximum reasoning effort (`effortLevel: high`, max thinking tokens up to 64,000). Never throttle reasoning depth or take cognitive shortcuts.
   - **Best Model Selection**: Always invoke top-tier models (`Model: "pro"`, `claude-opus-5-5`, `claude-opus-4-6`, `claude-sonnet-5-5`). Subagent invocations must use `Model: "pro"` or `Model: "inherit"`. Never downgrade to `flash_lite` or inferior models.
   - **Max Credit Utilization**: Antigravity AI credits are permanently enabled (`useAiCredits: true`). Expend credits to achieve perfection: run multi-agent reviews, build complete and exhaustive test suites, conduct thorough architectural investigations, and deliver production-grade code without placeholders, stubs, or lazy omissions.

## Specialized Agent Orchestration Matrix

| Task Domain | Mandatory Agent / Skill | Action Required |
|---|---|---|
| Feature Planning | `planner`, `architect` | Draft implementation breakdown before editing |
| Implementation & Bugfixes | `tdd-guide`, `verification-loop` | Write failing tests first; implement cleanly |
| Code Quality & Diff Review | `code-reviewer`, `code-review` | Audit diffs for bugs, maintainability, and standards |
| Pull Request Feedback | `autofix` | Parse and remediate CodeRabbit bot review threads |
| Security & Secrets | `security-reviewer`, `armorantigravity` | Audit authentication, input validation, and tokens |
| Build & Compilation | `build-error-resolver` | Surgical fixes for compilation / type errors |
| Full-Stack & UI Audits | `a11y-architect`, `frontend-patterns` | Ensure accessibility (WCAG 2.2) and smooth UX |
| Firebase & Cloud Infrastructure | `firestore-rules-author`, `firebase-basics` | Secure rules and cloud service configuration |
| Code Simplification & YAGNI | `ponytail`, `code-simplifier` | Smallest complete change, stdlib first, zero unrequested abstraction |
| Debt & Dead Code Audit | `ponytail-audit`, `ponytail-debt`, `refactor-cleaner` | Eliminate dead paths, prune bloated dependencies, cut debt |
| Value & Gain Analysis | `ponytail-gain` | Verify business and technical gain of code additions |
| Senior Dev Review | `ponytail-review`, `code-reviewer` | Review diffs with lazy senior dev rigor (shortest working diff) |
| Spec-Driven Development | `spec-driven-development` | Full structured specification before code (/spec) |
| Web Performance & CWV | `web-performance-auditor`, `performance-optimization` | Core Web Vitals, runtime rendering, loading speed (/webperf) |
| Test Strategy & QA | `test-engineer`, `test-driven-development` | Behavioral coverage, integration suites, property tests (/test) |
| Security Audits & Threat Modeling | `security-auditor`, `security-and-hardening` | Exploitable vulnerability detection & OWASP audits |
| Autonomous Pentesting & Vulnerability Exploitation | `strix`, `penetration-testing-with-strix`, `api-security-testing` | Dynamic AI pentesting, PoC exploit validation & auto-fix |
| Pre-Flight Ship Verification | `shipping-and-launch` | Parallel multi-agent verification before merge/release (/ship) |

## Maximum Efforts Project Building Mandate

When building, modifying, or testing any project via Antigravity IDE:
1. **Maximum Cognitive Depth**: Always employ deepest reasoning, exhaustive context analysis, and full-spectrum multi-agent verification.
2. **Zero Incomplete Code**: Never emit TODOs, placeholder comments, stubbed functions, or untested endpoints. All implementations must be fully realised and production-ready.
3. **Multi-Layer Verification**: Every build must pass compilation, unit tests, integration tests, security review, and vulnerability validation before completion.

