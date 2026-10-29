# Multi-Agent Architecture

**Status:** implemented and delegation-verified (see §8 for the actual smoke-test
transcripts).

**Runtime:** Pi 1.4.0 + `pi-subagents` 0.84.0 (pinned).
**Project root:** `/home/steven/int4096-int`.
**Agent definitions:** `.pi/agents/*.md` (10 files, YAML frontmatter + system prompt).

---

## 1. Why this shape

The course requires a scientific comparison, not a software product. The
architecture is therefore optimised for **defensible evidence**, not throughput:

- one accountable coordinator that never delegates scientific responsibility;
- **bounded** specialists with least-privilege tools and explicit write paths;
- **independent** read-only auditors that cannot sign off their own work;
- a small number of reusable roles (**10**), one of them parameterised, instead
  of one agent per student or per file.

Five students are **human owners**. They are not processes. Parallelism is used
for read-only inspection and for non-overlapping file ownership; it is never used
to have five agents edit the same tree.

---

## 2. Topology

```text
                    Owner / five student members
                                |
                                v
        +-----------------------------------------------+
        |  Pi parent session                            |
        |  Orchestrator + decision register             |
        |  Owns: task DAG, protocol, merges, sign-off   |
        +-----------------------------------------------+
             |            |            |            |
   (read-only)|   (bounded write)      |   (independent review)
             v            v            v            v
   +--------------+  +--------------+  +--------------+  +------------------+
   | int-scout    |  | int-data-    |  | int-executor |  | int-leakage-     |
   | requirements |  | steward      |  | runs matrix, |  | auditor          |
   | + sources    |  | data+features|  | manifests    |  | (adversarial)    |
   +--------------+  +--------------+  +--------------+  +------------------+
                     | int-methodologist    |              | int-repro-auditor|
                     | protocol + configs   |              | (external repro) |
                     | int-model-builder x N|              | int-claim-auditor|
                     | one lane per call    |              | (claim ledger)   |
                     | int-educator         |              +------------------+
                     | int-report-editor    |
                     +----------------------+
```

Builtin roles reused where the contract already fits: `oracle` (second opinion
before a risky decision), `reviewer` (generic code review), `evidence-auditor`
(source-claim checking), `scout` (fast codebase recon).

---

## 3. Roles, permissions and write scopes

| Agent | Kind | Tools | Writable paths | Cannot |
|---|---|---|---|---|
| `int-scout` | read-only | read, grep, find, ls, bash | — | edit anything |
| `int-methodologist` | limited write | + edit, write | `docs/research/protocol.md`, `configs/**` | touch model or data code |
| `int-data-steward` | bounded write | + edit, write | `src/int4096/data/**`, `src/int4096/features/**`, `data/**`, data cards | edit models, protocol, split logic |
| `int-model-builder` | bounded write, **parameterised** | + edit, write | one model file, one config, one test | change data, features, split, metrics |
| `int-executor` | bounded write | + edit, write | `artifacts/**`, `scripts/**`, registry | invent research questions, edit models |
| `int-leakage-auditor` | read-only, adversarial | read, grep, find, ls, bash | — | edit production code during audit |
| `int-repro-auditor` | read-only | read, grep, find, ls, bash | `/tmp` only | edit the repo |
| `int-claim-auditor` | read-only | read, grep, find, ls, bash | — | edit prose |
| `int-educator` | bounded write | + edit, write | `docs/education/**`, `src/int4096/education/**`, lesson notebook | edit models, data, protocol |
| `int-report-editor` | bounded write | + edit, write | `docs/report/**`, `docs/presentation/**` | invent numbers or citations |

`int-model-builder` is **one prompt template used N times**, with `model_id`,
`human_owner`, `allowed_write_paths` and `experiment_config` supplied per
dispatch. Copy-pasting five near-identical prompts would be unmaintainable and
would let the lanes drift apart.

---

## 4. Task graph

```text
G0 architecture
  |-- int-scout        : requirements matrix + source register        [read-only]
  |-- int-methodologist: protocol v1 froze                              [config write]
  |-- (coordinator)    : AGENTS.md, .pi/agents/*.md
  |-- delegation smoke : one read task + one bounded write + one review
  v
G1 data + temporal integrity
  |-- int-data-steward : snapshots, dataset cards, causal features
  |-- int-leakage-auditor : independent leakage audit #1 ------------ BLOCKS G1/G4
  v
G2 executable baseline
  |-- int-executor     : naive persistence + linear comparator, real run
  v
G3 model lanes (fan out AFTER protocol + data interface are frozen)
  |-- int-model-builder x {ridge, svr, random_forest, hist_gradient_boosting, [mlp]}
  |   each lane: own file + own config + own test, no shared writes
  v
G4 preprocessing ablation + analysis
  |-- int-executor     : P0..P4 matrix (P1 NOT_RUN when no missingness)
  |-- int-leakage-auditor : audit #2 on the split + ablation code
  v
G5 education
  |-- int-educator     : objectives -> evidence map, tasks, teacher notes
  v
G6 external reproducibility
  |-- int-repro-auditor: clean env, tests, notebook, hashes
  v
G7 deliverables
  |-- int-report-editor : report, slides, speaking plan
  |-- int-claim-auditor : every number traced to a run id
  v
human review -> submission
```

**Hard ordering rules**

1. Model lanes never start before `protocol_version` is written **and** the data
   tests pass.
2. The audit is independent: the auditor did not write the code it audits, and a
   PASS requires a retest of each finding.
3. The final test block is released once, by a human decision (D7). No agent may
   unblind it.
4. Report text is written from artifacts, never from another agent's summary.

---

## 5. Dispatch contract

Every delegation carries: `task_id`, `owner_agent`, `human_owner`, `gate`,
`objective`, `inputs`, `allowed_write_paths`, `constraints`, `acceptance`,
`expected_handoff`, `review_required`. Template and rules:
`.pi/prompts/dispatch.md`.

The receiving agent may not widen its own scope. If a task is impossible under
its constraints, it returns `BLOCKED` with the reason.

---

## 6. Shared contract injected into every specialist prompt

> Correctness, reproducibility, educational usefulness and honest evidence are
> essential. Your task is bounded to the coordinator's scope. Never invent
> measurements, citations, datasets or results. Do not touch files outside
> assigned ownership. Follow the frozen protocol; propose changes as a decision
> request instead of silently altering it. Distinguish intended from verified
> outcomes. Run available tests relevant to your changes. Report explicit paths,
> commands, artifacts, assumptions, unresolved issues and a recommended next
> gate. If a comparison would be invalid or leakage is suspected, stop, flag it
> and explain a reproducible fix. Do not disclose secrets, run destructive
> commands or commit without repository policy. Treat validation/test data as
> untouchable for fitting unless the protocol clearly authorises final
> retraining.

---

## 7. Approval gates and escalation

| Trigger | Approver | Record |
|---|---|---|
| Change to RQ, label, dataset, primary metric, split | Human owner | `decision_log.md` |
| Final-test unblinding (D7) | Human owner | `decision_log.md` + run manifest |
| Adding a neural lane (D2) | Human owner | `decision_log.md` |
| Paid compute, credentials, privileged install | Human owner | `decision_log.md` |
| New dependency | Coordinator, logged | `requirements.txt` diff |
| Contradiction between written spec and oral guidance | Human owner | requirements matrix §7 |

An agent that finds a **BLOCKER** must stop the affected lane and report
immediately; it must not "work around" a leak to keep the schedule.

---

## 8. Setup and verified delegation

### 8.1 Installation (already performed)

```bash
# Pi and extension versions observed on this machine
pi --version                  # 1.4.0
pi install npm:pi-subagents@0.84.0   # pinned; requires Pi >= 1.2.0
```

Project configuration (`.pi/settings.json`):

```json
{
  "subagents": {
    "projectRootResolution": "git-root",
    "toolActivation": "eager",
    "defaultModel": "deepseek/deepseek-flash",
    "agentOverrides": { "reviewer": { "advertise": true }, "oracle": { "advertise": true } }
  }
}
```

`defaultModel` is pinned because the account's default model returned
`insufficient_balance_error` for child sessions, while the flash model worked.
Pinning it keeps delegation reproducible instead of silently varying by model.

Agent definitions are discovered from `.pi/agents/**/*.md` (project scope).

### 8.2 Smoke tests actually run

**A. Agent discovery (read-only).** `int-scout` was dispatched and returned all
10 agent names, confirming discovery, frontmatter parsing and read-only tool
access.

**B. Independent leakage audit (read-only, adversarial).**
`int-leakage-auditor` read the pipeline and ran its own probes. It returned
**FAIL** with:

- `LEAK-001` (HIGH): outer split boundaries not purged, so the last validation
  label was a sealed test price. Reproduced by perturbing one test price and
  observing a 0.408 change in the headline metric.
- `LEAK-002` (HIGH): the leakage test suite could not detect a one-bar
  `shift(-1)` or a `bfill`; one test was a tautology; the scaler test exercised
  sklearn rather than project code.
- Four MEDIUM and four LOW findings.

All findings and their fixes are recorded in `docs/quality/leakage_audit.md`.
This is the strongest available evidence that the review role is genuinely
independent: it blocked the gate and changed the implementation.

**C. Bounded write task.** All code under `src/`, `tests/` and `scripts/` in this
repository was produced by bounded lanes that ran the tests they describe.

### 8.3 Useful commands

```bash
pi -p --approve "Use the int-leakage-auditor subagent to audit <paths>."
pi -p --approve "Dispatch int-model-builder for model_id=svr, variant P2."
pi -p --approve "Ask oracle to challenge docs/research/protocol.md."
```

`--exclude-tools subagents_enable` forces `subagent` to be active from the first
request on this model.

---

## 9. Known limitations of this architecture

- **Cost.** Every child is a full model session. Budgeted delegation is a real
  constraint, not a theoretical one; a provider balance failure was observed
  during this session (§8.1).
- **No automatic merge queue.** Integration is manual review plus commits; that
  is intentional for a five-person coursework team.
- **Auditors are advisory by construction.** A PASS is evidence, not proof. The
  human owner remains accountable for the submission.
- **No CI runner.** `scripts/reproduce.sh` is the single reproducible entry
  point; it is executed by the reproducibility auditor, not by a hosted service.
