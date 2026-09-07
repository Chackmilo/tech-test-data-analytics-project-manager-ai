# How the numbers were verified

*Supporting material. The graded documents are `ASSESSMENT.md`, `PLAN.md`, `SCOPE.md`, `MBR.md`,
`CFO_MESSAGE.md` and `AI_WORKFLOW.md`, all at the repository root. `README.md` is the brief as
issued, unmodified.*

Every figure published in those six documents is derived from `artifacts/` by a script rather than
asserted in prose. Three of them say so in their own opening lines and name the command. This file
says where that command lives and how it is organised. Why it exists — including the occasion when
an earlier version passed 246 checks while failing to notice a wrong cutover date — is in
`AI_WORKFLOW.md` §3.

```bash
python verify.py             # 283 checks against the artifacts and the deliverables
python verify.py --selftest  # 8 deliberate corruptions, all of which must be caught
```

A green harness is a claim. The second command is the evidence: it corrupts one source of truth at a
time and fails if the harness does not notice.

---

## Layout

The repository root holds the brief, the six deliverables, the artifacts as inherited, and the one
command those documents cite. Everything else is one level down, in `analysis/`.

```text
.
├── README.md                  the brief, exactly as issued
├── ASSESSMENT.md              what was inherited, ranked, with line citations
├── PLAN.md                    critical path, cutover, rollback, dual-scenario date
├── SCOPE.md                   the 38-report recommendation and what reverses it
├── MBR.md                     one page for the September Steering Committee
├── CFO_MESSAGE.md             the pre-meeting note
├── AI_WORKFLOW.md             how AI was used, and where it was confidently wrong
├── artifacts/                 the outgoing PM's folder, unmodified
├── verify.py                  the command the deliverables name
└── analysis/
    ├── mythril/
    │   ├── core/              working-day calendar, check harness
    │   ├── parsers/           markdown tables, citations, CSV ingestion
    │   ├── domain/            one module per artifact and per deliverable
    │   ├── engine.py          orchestrates the nine sections
    │   └── cli.py             python -m mythril
    ├── tests/                 pytest, including the end-to-end 283-check certification
    ├── prompts/               refined prompt templates (see §3)
    ├── mutation_test.py       the eight corruptions
    ├── pyproject.toml         packaging and tool config
    ├── Makefile               task shortcuts
    └── ARCHITECTURE.md        this file
```

Dotfiles stay at the root because their tools require it: `.github/workflows/ci.yml` (GitHub Actions
resolves it only from the root), `.gitignore`, `.editorconfig`.

## Running it

`verify.py` needs no dependencies and runs from the repository root. The rest expects
`pip install -e ".[dev]"` from inside `analysis/`, and runs from there:

```bash
make verify     # or: python ../verify.py
make mutate     # or: python mutation_test.py
make test       # pytest
make lint       # ruff
```

## On `analysis/prompts/`

`AI_WORKFLOW.md` §1 sets out the rule this repository runs on: a language model is never asked for a
number, only for the script that computes one. `analysis/mythril/` is the enforcement.

`analysis/prompts/` holds **refined templates as they stand after the assessment**. It is not a
transcript. The prompts actually issued are quoted verbatim in `AI_WORKFLOW.md` §2, and each template
carries a header saying so. Template 04 in particular now includes the peak-trading and
month-boundary constraints whose *absence* §3.5 identifies as the cause of a wrong recommended date —
so it documents the fix, not the original ask.
