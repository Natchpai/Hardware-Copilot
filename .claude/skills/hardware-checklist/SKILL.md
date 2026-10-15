---
name: hardware-checklist
description: Create, update, or audit an execution checklist for a hardware or PCB project. Turns specification requirements into gated tasks with owner, status, and required evidence. Use when the user asks for a hardware checklist, work plan, gate list, bring-up plan, or wants to check that every requirement has a task.
argument-hint: "create | update | audit"
---

# Hardware Checklist

Track the work and evidence needed to close each gate of a hardware or PCB project. The checklist is a tracker. It is not an approval record, a verification record, or a phase declaration.

Human engineers keep authority over decisions, approvals, and gate closure.

## Template

- Use `assets/execution_checklist_template.md` when creating a new checklist.
- Adapt gates, columns, and rows to the project. Remove gates and rows that do not apply.
- Do not modify the template during normal work.

## Modes

- **Create:** Read the specification first. Draft one or more tasks for each requirement or open item that needs work or evidence. Show the draft before writing the file, unless the user asked for the file.
- **Update:** Read the existing checklist first. Change only the rows the user names. Keep IDs, order, and unrelated rows. Never reuse a removed ID.
- **Audit:** Read-only. Compare the checklist with the specification and report:
  - requirement IDs with no task
  - tasks with no requirement or reason
  - `DONE` rows without evidence
  - open items without an owner or gate
  - rows that conflict with the specification

## Rules

1. **Source of truth.** Requirements and decisions come from the specification. Do not copy their values into the checklist. Reference the ID (for example `PWR-001`).
2. **Task states.** Use only: `OPEN`, `IN_PROGRESS`, `BLOCKED BY <ID>`, `DEFERRED`, `DONE`, `N/A`. Define them once in a conventions block. Do not put evidence labels in the status column.
3. **Done needs evidence.** Mark `DONE` only when the user states the task is complete and the evidence column names or links the record. A checkbox, file presence, or an ERC/DRC pass is not evidence by itself.
4. **Gates.** Group tasks into gates. Each gate has an exit criterion. Default gates are P0 to P4: requirements, allocation, schematic, PCB and release package, bring-up. Gates are work stages. They are not the project phase (`DRAFT`, `PRELIMINARY`, `CHECK`, `RELEASE`). Never infer or change the project phase.
5. **Owner.** Every row has an owner role (Human owner, Hardware, Software, Fabricator, and so on). Approval and gate-closure rows are owned by the human.
6. **Evidence required.** Say what record closes the row: a table, a log, a review, a measurement. Be specific. Do not invent results.
7. **Deferred work.** Mark non-hardware or later work `DEFERRED` and say who owns it. Say if it does not block the gate.
8. **Open items.** Keep one short register that points to the specification's open-item IDs. Do not copy their descriptions.
9. **Unknowns.** Use `TBD`. Do not guess owners, dates, or evidence.

## Keep it short

- Define status values once. Do not repeat them per row.
- One task per row. Keep the task to one sentence.
- Use tables. Remove a column only if it is empty in every row.
- Do not repeat the same fact in the checkpoint, the gate rows, and the register. State it once.
- Prefer a few specific tasks over many vague ones.

## Writing style

- Write simple, direct English, like one engineer talking to another. Use everyday words, short sentences, and active voice.
- Avoid fancy words, marketing phrases, and AI-style filler.
- Keep standard engineering terms and exact IDs.
- Do not use the em dash (`—`). Use a period, comma, colon, or parentheses.
- Use `TBD` for open values. Do not mix it with other spellings.
- Priority: technical accuracy, then clarity, then brevity, then style.

## Boundaries

- Do not open, parse, assess, or generate PDF content.
- Keep KiCad design and library files read-only.
- Do not run ERC or DRC, claim their results, or treat a pass as proof of correctness.
- Do not mark a task done, approve a gate, or declare a phase for the human.
- Do not stage, commit, or push. Git actions need separate approval.
- Do not create logs, manifests, or other files that were not requested.

## Output

Report the file written, the rows added or changed, and any gap, such as a requirement with no task. Preserve existing project file names.

Suggested name: `HARDWARE_CHECKLIST.md`.
