# Forensic Audit Prompt 05: Adversarial Review & Red-Team Audit

## Objective
Act as a skeptical external auditor or assessor grading the entire submission against the project brief, attacking claims, testing for tautological assertions, and seeking unstated assumptions.

## Target Deliverables & Artifacts
- All deliverables: `ASSESSMENT.md`, `PLAN.md`, `SCOPE.md`, `MBR.md`, `CFO_MESSAGE.md`
- Codebase: `verify.py`, `mutation_test.py`, `src/mythril/`

## System Prompt / Instructions
```text
You are an adversarial assessor grading this submission against README.md.
Re-derive every single quantitative figure from raw artifacts in artifacts/.
Do NOT trust verify.py or published tables blindly — audit the verification harness itself for tautological assertions (e.g. comparing literals, assertions that cannot fail, empty loop bodies, or skipped regex patterns).

Specifically audit:
1. Are there WBS rows with em-dash or non-standard IDs skipped by regex parsers?
2. Does the peak-trading constraint actually iterate over parsed cutover rows rather than hardcoded dates?
3. Does the budget table FTE match the section 3 WBS allocation exactly (e.g. Bekele 65% vs 60%)?
4. Are all findings in ASSESSMENT.md explicitly backed by real line numbers in artifacts/?
5. Does CFO_MESSAGE.md strictly adhere to the 300-word executive limit?
```

## Deterministic Guardrail Check
Verified by `mutation_test.py` & `src/mythril/domain/deliverables.py`:
- `8 of 8 adversarial mutations caught`
- `CFO_MESSAGE.md word count < 300 (actual: 292 words)`
- `Findings count == 16, all 16 citing valid line ranges in real artifacts`
- `Zero findings citing non-existent files or omitted citations`
