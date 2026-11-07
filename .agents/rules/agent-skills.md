# Addy Osmani's Agent-Skills Engineering Framework

This workspace integrates the **addyosmani/agent-skills** suite (25 production-grade skills, 4 specialized agents, and 9 lifecycle workflows).

## Intent → Skill Mapping

When a user request matches any of the following lifecycle stages, invoke the corresponding skill immediately:

- **New Feature / Ambiguous Scope**: Use `spec-driven-development` (`/spec`). Write structured specification before touching code. For multi-module scopes, generate a capability map first.
- **Task Planning & Decomposition**: Use `planning-and-task-breakdown` (`/planning`). Produce dependency-ordered, reviewable task increments with clear validation gates.
- **Test-Driven Development**: Use `test-driven-development` (`/test`). Strictly follow RED-GREEN-REFACTOR. Tests must run and pass before declaring tasks done.
- **Incremental Implementation**: Use `incremental-implementation`. Land small, atomic, self-verifying increments.
- **Bug Fixes & Diagnosis**: Use `debugging-and-error-recovery`. Reproduce, isolate root cause, verify fix with a regression test.
- **Code Review**: Use `code-review-and-quality` (`/review`) and the `code-reviewer` agent. Audit correctness, readability, architecture, security, and performance.
- **Security & Hardening**: Use `security-and-hardening` and the `security-auditor` agent. Audit input validation, secrets, auth, OWASP vectors, and supply chain.
- **Performance Optimization**: Use `performance-optimization` and the `web-performance-auditor` agent (`/webperf`). Optimize Core Web Vitals, memory, I/O, bundle sizes, and query efficiency.
- **Code Simplification**: Use `code-simplification` (`/code-simplify`). Simplify control flow, prune redundant code, and maintain functional equivalence.
- **Release & Pre-Flight Verification**: Use `shipping-and-launch` (`/ship`). Run parallel verification (build, tests, security, performance) and synthesize a release report.
- **UI & Frontend Engineering**: Use `frontend-ui-engineering` and `browser-testing-with-devtools`.
- **API & Interface Design**: Use `api-and-interface-design`. Define ergonomic, typed contracts before implementation.
- **Constraints & Guardrails**: Use `constraint-driven-development` (`/constraints`).
- **Context Management**: Use `context-engineering`.
- **Doubt & Risk Analysis**: Use `doubt-driven-development`.
- **Architecture Decisions**: Use `documentation-and-adrs`.

## Specialized Agents

- `security-auditor`: Focuses on practical vulnerability detection, threat modeling, and hardening.
- `test-engineer`: Focuses on test architecture, behavioral coverage, property tests, and regression prevention.
- `web-performance-auditor`: Deep audit of Core Web Vitals, runtime rendering, loading waterfall, and asset delivery.
- `addy-code-reviewer`: Staff-level 5-dimensional review (Correctness, Readability, Architecture, Security, Performance).
