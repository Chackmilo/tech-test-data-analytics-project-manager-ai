# Verification Architecture

*Supporting material, kept out of the repository root so the graded documents stand alone.
The assessment deliverables are `ASSESSMENT.md`, `PLAN.md`, `SCOPE.md`,
`MBR.md`, `CFO_MESSAGE.md` and `AI_WORKFLOW.md`; `README.md` is the brief as issued and is
unmodified.*

Every figure published in those six documents is derived from `artifacts/` by a script rather than
asserted in prose. This file documents how that harness is organised and how to run it. The reasoning
behind it — including the occasion when an earlier version of the harness passed 246 checks while
failing to detect a wrong cutover date — is in `AI_WORKFLOW.md` §3.6.

**The short version:**

```bash
python verify.py         # 283 checks against the artifacts and the deliverables
python mutation_test.py  # 8 deliberate corruptions, all of which must be caught
```

A green harness is a claim. `mutation_test.py` is the evidence: it corrupts one source of truth at a
time and fails if the harness does not notice.

---

### 1. Repository Architecture

```text
.
├── .github/workflows/ci.yml       # Multi-platform CI pipeline (Ubuntu, macOS, Windows)
├── .gitignore                     # Python, cache, IDE, and OS ignore specifications
├── .editorconfig                  # Uniform formatting configuration across editors
├── pyproject.toml                 # Modern PEP 518/621 packaging & test config (zero external core deps)
├── Makefile                       # Developer task runner (make verify, make test, make lint)
│
├── src/mythril/                   # Modular verification & domain audit engine
│   ├── core/                      # Temporal constraint solver, calendar logic, harness reporter
│   ├── parsers/                   # Markdown table & citation extraction, CSV ingestion
│   ├── domain/                    # Financial reconciliation, vendor freeze, team capacity,
│   │                              # schedule float/WBS, report telemetry, deliverable audits
│   ├── engine.py                  # Complete 9-section audit orchestrator
│   └── cli.py                     # Unified CLI interface (args: --quiet, --selftest, --root)
│
├── tests/                         # Pytest test suite
│   ├── conftest.py                # Reusable session fixtures for paths and engine
│   ├── test_full_verification.py  # End-to-end certification (283 / 283 checks)
│   ├── test_harness_mutations.py  # Parameterized adversarial mutation test suite (8 cases)
│   ├── test_reconciliation.py     # Domain unit tests for ledger variance & order anomalies
│   ├── test_schedule.py           # Domain unit tests for workdays, holidays & blackout windows
│   └── test_telemetry.py          # Domain unit tests for Pareto usage triage & ghost reports
│
├── prompts/                       # Refined prompt templates (post-assessment; see the header in each)
│   ├── 01_reconciliation_forensics.prompt.md
│   ├── 02_resource_collision_mapping.prompt.md
│   ├── 03_report_telemetry_triage.prompt.md
│   ├── 04_constraint_schedule_modeling.prompt.md
│   └── 05_adversarial_review_audit.prompt.md
│
├── README.md                      # The assessment brief, exactly as issued (unmodified)
├── docs/ARCHITECTURE.md           # This file
├── artifacts/                     # The inherited handover folder (unmodified)
├── verify.py                      # Root backwards-compatible verification entrypoint (283 checks)
├── mutation_test.py               # Root adversarial mutation test entrypoint (cross-platform)
│
├── ASSESSMENT.md                  # Inherited state forensic findings (ranked with line citations)
├── PLAN.md                        # Revised dual-scenario critical path, WBS, and cutover plan
├── SCOPE.md                       # Defended 38-report scope recommendation and descoping criteria
├── MBR.md                         # One-page executive review for September Steering Committee
├── CFO_MESSAGE.md                 # Pre-meeting executive brief (<300 words)
└── AI_WORKFLOW.md                 # AI methodology, prompt forensics, failure analysis & audit
```

### 2. Execution & Developer Workflows

#### Core Verification Harness (Zero External Dependencies)
Run the full 283-check deterministic verification audit from the repository root:
```bash
python verify.py
# Or with quiet flag:
python verify.py --quiet
```

#### Adversarial Mutation Suite
Prove that the verification harness can actively fail by deliberately injecting corruptions into sources of truth:
```bash
python mutation_test.py
# Or via verify.py:
python verify.py --selftest
```

#### Modern CLI Invocation
The verification engine can be executed as a modular Python package:
```bash
python -m mythril --help
python -m mythril --quiet
python -m mythril --selftest
```

#### Pytest Test Suite
If development tools are installed (`pip install -e ".[dev]"`):
```bash
pytest -v
```

#### Makefile Automation
```bash
make verify   # Run the 283-check verification harness
make mutate   # Run the 8-case mutation test suite
make test     # Run pytest suite
make lint     # Run Ruff linter
make all      # Run full verification and mutation suite
```

### 3. PromptOps & AI Verification Guardrails
`AI_WORKFLOW.md` §1 sets out the rule this repository runs on: a language model is never asked for a number, only for the script that computes one. `src/mythril/` is the enforcement.

The `prompts/` directory holds **refined templates as they stand after the assessment**. It is not a transcript. The prompts actually issued are quoted verbatim in `AI_WORKFLOW.md` §2, and each template here carries a header saying so. Template 04 in particular now includes the peak-trading and month-boundary constraints whose *absence* §3.5 identifies as the cause of a wrong recommended date — so it documents the fix, not the original ask.
