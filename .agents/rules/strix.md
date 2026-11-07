# Strix — Multi-Agent Penetration Testing & Cybersecurity

Strix is an autonomous AI-driven penetration testing and security assessment suite integrated directly into Antigravity. It runs dynamic security tests, validates vulnerabilities using working proofs-of-concept (PoCs), and provides automated remediation and verification.

## Strix Skills Catalog

The following 9 Strix skills are active and available across all projects:

1. **`penetration-testing-with-strix`**: Run headless penetration tests against local source code, URLs, domains, or IP addresses.
2. **`api-security-testing`**: Security-test REST, GraphQL, and gRPC APIs against OWASP API Security Top 10 (BOLA/IDOR, authz, mass assignment, injection).
3. **`application-security-testing`**: Comprehensive full-product AppSec review, scoping targets and ranking findings.
4. **`find-security-vulnerabilities-in-code`**: White-box static and dynamic security review of repositories or working trees.
5. **`fix-security-vulnerabilities-with-strix`**: Remediate discovered security vulnerabilities and rerun verification scans.
6. **`owasp-top-10-testing`**: Systematic assessment of web applications against OWASP Top 10 vulnerability classes.
7. **`web-app-penetration-testing`**: Black-box penetration testing of live web applications and staging environments.
8. **`ci-security-scanning-with-strix`**: Integrate automated PR security scanning into GitHub Actions and CI/CD pipelines.
9. **`managed-pentesting-with-strix`**: Drive the managed cloud platform via `strix cloud` without local Docker requirements.

## Running Strix CLI

The Strix CLI (`strix 1.7.0`) is installed and available in PATH:

```powershell
# Quick code security scan (headless)
strix -n -t ./ --scan-mode quick --max-budget 10

# API specification security scan
strix -n -t ./openapi.yaml -t https://api.staging.example.com --max-budget 20

# Web app penetration test
strix -n -t https://staging.example.com --scan-mode standard

# Strix Cloud managed scan
strix cloud scans start --source . --yes --wait
```

## Security Findings Workflow

1. Execute scan with `-n` (non-interactive) and appropriate `--scan-mode` (`quick`, `standard`, `deep`).
2. Artifacts are generated in `strix_runs/<run-name>/`:
   - `penetration_test_report.md`
   - `vulnerabilities/*.md`
   - `vulnerabilities.json`
   - `findings.sarif`
   - `run.json`
3. Remediate all CRITICAL and HIGH severity findings using `fix-security-vulnerabilities-with-strix`.
4. Rerun verification tests before marking code production-ready.
