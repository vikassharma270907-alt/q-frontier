---
description: Scan an AI agent skill, directory, or repository for security risks using NVIDIA SkillSpector.
arguments:
  - name: target
    description: Path, URL, git repository, or SKILL.md to scan
    required: true
---

# /skillspector

Run NVIDIA SkillSpector security inspection on the specified skill target:

```bash
skillspector scan "$TARGET" --no-llm --format terminal
```

Or for machine-readable JSON:
```bash
skillspector scan "$TARGET" --no-llm --format json
```

Follow with semantic triage to deliver an authoritative `APPROVE`, `CAUTION`, or `REJECT` verdict.
