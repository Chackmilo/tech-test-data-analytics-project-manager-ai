# Verification Architecture

*Supporting material. The assessment deliverables are `ASSESSMENT.md`, `PLAN.md`, `SCOPE.md`,
`MBR.md`, `CFO_MESSAGE.md` and `AI_WORKFLOW.md`; `README.md` is the brief as issued and is
unmodified.*

Every figure published in those six documents is derived from `artifacts/` by a script rather than
asserted in prose. This file documents how that harness is organised and how to run it. The reasoning
behind it — including the occasion when an earlier version of the harness passed 246 checks while
failing to detect a wrong cutover date — is in `AI_WORKFLOW.md` §3.6.

**The short version:**

```bash
python verify.py         # 276 checks against the artifacts and the deliverables
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
│   ├── test_full_verification.py  # End-to-end certification (276 / 276 checks)
│   ├── test_harness_mutations.py  # Parameterized adversarial mutation test suite (8 cases)
│   ├── test_reconciliation.py     # Domain unit tests for ledger variance & order anomalies
│   ├── test_schedule.py           # Domain unit tests for workdays, holidays & blackout windows
│   └── test_telemetry.py          # Domain unit tests for Pareto usage triage & ghost reports
│
├── prompts/                       # PromptOps: Versioned system prompts for AI-assisted audit
│   ├── 01_reconciliation_forensics.prompt.md
│   ├── 02_resource_collision_mapping.prompt.md
│   ├── 03_report_telemetry_triage.prompt.md
│   ├── 04_constraint_schedule_modeling.prompt.md
│   └── 05_adversarial_review_audit.prompt.md
│
├── README.md                      # The assessment brief, exactly as issued (unmodified)
├── ARCHITECTURE.md                # This file
├── artifacts/                     # The inherited handover folder (unmodified)
├── verify.py                      # Root backwards-compatible verification entrypoint (276 checks)
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
Run the full 276-check deterministic verification audit from the repository root:
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
make verify   # Run the 276-check verification harness
make mutate   # Run the 8-case mutation test suite
make test     # Run pytest suite
make lint     # Run Ruff linter
make all      # Run full verification and mutation suite
```

### 3. PromptOps & AI Verification Guardrails
As detailed in `AI_WORKFLOW.md`, large language models cannot be trusted with arithmetic, counting, or unconstrained schedule modeling. The `prompts/` directory captures each forensic prompt template used in the assessment, while `src/mythril/` acts as an automated, deterministic verification guardrail ensuring zero hallucinated figures reach executive deliverables.
