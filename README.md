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
