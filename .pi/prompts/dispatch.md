# Task Dispatch Contract (template)

Every delegated task in this project uses this format. The coordinator fills it;
the receiving agent may not silently widen it.

```yaml
task_id: EXP-MODEL-SVR-001
owner_agent: int-model-builder
human_owner: "Person 3"
gate: G3
objective: >
  Implement and smoke-test the SVR lane under protocol v1.
context_files:
  - AGENTS.md
  - docs/research/protocol.md
  - configs/research_protocol.yaml
inputs:
  - src/int4096/data/
  - src/int4096/features/
allowed_write_paths:
  - src/int4096/models/svr.py
  - configs/experiments/svr.yaml
  - tests/test_model_svr.py
constraints:
  - "Do not read or optimize against final test labels"
  - "All preprocessing fitted on training indices only"
  - "Respect max_trials and max_seconds from the protocol"
  - "Do not modify shared data, split, label or metrics"
acceptance:
  - "pytest tests/test_model_svr.py passes"
  - "A real smoke run produces finite predictions and a valid metrics.json"
  - "A valid run_manifest.json is emitted with a real git commit and data hash"
  - "Search log records every attempted configuration"
acceptance_gate: ".venv/bin/python -m pytest -q tests/test_model_svr.py"
expected_handoff:
  - "Changed files + git diff --stat"
  - "Actual commands and observed outcomes"
  - "Run IDs and artifact paths"
  - "Limitations, blockers, next action"
review_required: int-leakage-auditor
```

## Rules for the coordinator

1. **One `task_id` per bounded unit of work.** No mega-tasks.
2. **`allowed_write_paths` is exhaustive.** If an agent needs another file, it
   must raise a decision request, not broaden its own scope.
3. **Acceptance must be executable**, not aspirational. A shell command or a
   named test is preferred over prose.
4. **Every writer task gets an independent reviewer** (`review_required`) that
   did not write the code.
5. **Never dispatch model lanes before the protocol and data interface are
   frozen.** Evidence: `protocol_version` present and data tests green.
6. **Never dispatch the final-test run.** That is a human decision, executed by
   `int-executor` under explicit approval recorded in the decision log.

## Rules for the receiving agent

- If the brief is ambiguous in a way that changes the science, **stop and ask**.
- If a constraint makes the task impossible, report `BLOCKED` with the reason.
- Do not perform work outside `allowed_write_paths`, even if it seems helpful.
- Do not mark your own output `verified`.
