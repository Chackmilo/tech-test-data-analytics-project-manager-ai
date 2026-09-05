# Data & Analytics Project Manager (AI) — Technical Assessment

**Time limit:** 3 hours max.

---

## Context

**Twin Hearth Studios** is migrating its enterprise data warehouse to a new cloud platform. The
programme is called **Mythril**. Cutover is committed to the board for **12 October 2026**.

The project manager who ran it is leaving on 30 September. It is **31 August 2026** and you have
just been handed their folder. The last status report says green on everything that matters.

You present to the Steering Committee at the end of September. Between now and then, your job is to
work out what you have actually inherited.

## What you're given

Everything in `artifacts/` is what was in the folder. Nothing has been curated for you.

```
artifacts/project-plan.csv              the schedule: tasks, owners, dates, dependencies, % complete
artifacts/resource-allocation.csv       who is planned on what, by week
artifacts/report-usage.csv              telemetry for the 120 legacy reports in scope
artifacts/status-report-2026-08.md      last month's status report
artifacts/reconciliation-2026-08-28.md  the parallel-run reconciliation that passed
artifacts/vendor-notice.md              a notice from the storefront aggregator
artifacts/steering-notes-2026-08.md     notes from the August steering meeting
artifacts/team-notes.md                 the outgoing PM's notes on the team
```

Some of these documents disagree with each other. Reconciling them is the assessment.

## What to deliver

### 1. `ASSESSMENT.md` — what you actually inherited

Everything you found that the status report does not say, **ranked by what it does to the
programme**, not by the order you found it in.

For each one: the evidence. Name the artifact and the number or the line that proves it. A finding
with no evidence is an opinion, and opinions are what got this programme to green.

Say plainly what colour this programme is, and why.

### 2. `PLAN.md` — the revised plan

- The real critical path, and what is actually on it.
- A cutover plan: sequence, go/no-go criteria, who decides, and **what rollback looks like** after
  the switch has been made.
- A date you can defend, with the reasoning that produces it. If it is not 12 October, show your
  work — you will be asked to justify it to the person who committed that date.
- What has to change about how the work is staffed for your date to hold.

### 3. `SCOPE.md` — the 120 reports

A recommendation on scope, with a number, defended with the evidence in `artifacts/`. Include
**what you are cutting and what it would take to bring it back** — a scope decision nobody can
reverse is not a decision, it's a demand.

### 4. `MBR.md` — the Monthly Business Review

**This is the centrepiece.** One page, for the September Steering Committee: CFO, VP Publishing
Operations, Head of Studio Relations, IT Director.

They have twenty minutes and they are going to ask about the date. Status, the decisions you need
from them, and what happens if they don't make them. Executive register: no task lists, no
narrating the artifacts back at them.

### 5. `CFO_MESSAGE.md` — the hard conversation

The CFO committed 12 October to the board. Write what you actually send them before the meeting.
Under 300 words.

### 6. `AI_WORKFLOW.md`

How you used AI while doing this:

1. Which tool(s) and why.
2. 3–5 concrete prompts and what came back.
3. One moment where the AI was confidently wrong — a plausible finding that the artifacts did not
   support — and how you caught it.
4. If you used AI to analyse the CSVs, say how, and how you checked the output.

## Tooling

Whatever you use to run projects: spreadsheets, Jira, a Gantt tool, plain Markdown, a script over
the CSVs. Commit whatever supports your conclusions. Deliverables must be readable in the repo —
if you build in a tool, export it.

Use AI. This role is graded partly on how well you drive it.

## Out of scope

Writing SQL, designing the target architecture, choosing the platform, cost modelling of the cloud
bill. You are managing this programme, not building it.

## Evaluation

| Area | Weight |
|---|---|
| `MBR.md` — executive communication and the status call it makes | 25% |
| `ASSESSMENT.md` — what you found, ranked, with evidence | 25% |
| `PLAN.md` — critical path, cutover, rollback, and a defensible date | 20% |
| `SCOPE.md` — the scope decision and what you cut | 10% |
| `CFO_MESSAGE.md` — the hard conversation | 10% |
| Use of AI (`AI_WORKFLOW.md`) | 10% |

Two things that sink an otherwise strong submission:

- **A status report that is still green.** Or one that is red with no ask attached.
- **Findings with no number on them.** "Resourcing is a concern" is worth nothing. The artifacts
  contain the figures; use them.

## How to submit

1. **Fork** this repo.
2. Create branch `submission/<your-name>`.
3. Write your deliverables at the root of the repo.
4. Open a **Pull Request** to `main` of this repo.
5. In the PR: time spent, your recommended cutover date in one line, and the single decision you
   most want the Steering Committee to make.

Expect to defend the date live.

---

## Senior AI Engineer Architecture & Tooling

To ensure enterprise-grade reproducibility, continuous verification, and robust separation of concerns, the repository has been refactored into a modular architecture under Senior AI / Analytics Engineer standards, while strictly preserving 100% backward compatibility with all deliverables and evaluation harnesses.

### 1. Repository Architecture

```text
E:\RVS\
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
├── artifacts/                     # Raw enterprise data and inherited documentation (unmodified)
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
