---
name: hardware-specification
description: >-
  Gathers, refines and documents hardware and PCB requirements with beginner
  and general specification templates. Use when the user asks to collect
  stakeholder needs, draft or update a hardware specification, turn beginner
  requirements into an engineering spec, or analyze requirements and PCB
  constraints. Not for task tracking (use hardware-checklist).
argument-hint: "beginner | general | translate | update"
---

# Hardware Specification

Support power electronics, MCU, FPGA, analog, digital, mixed-signal, and PCB projects.

Human engineers retain authority over requirements, design decisions, and approvals. Keep specification development progressive, evidence-based, and context-efficient.

## Specification Templates

Select the template according to the user's intent:

- **Beginner:** `assets/beginner_requirements_template.md`
  - Gather project needs from non-engineers, stakeholders, or beginners.
  - Use accessible language without requiring circuit-level knowledge.
  - Allow incomplete or unknown answers.

- **General Hardware Specification:** `assets/GENERAL_HARDWARE_SPEC_TEMPLATE.md`
  - Develop engineering requirements for hardware and PCB design.
  - Adapt the technical depth to the project's actual complexity.
  - Do not require every section to be completed.

### Template Loading

- Load only the template relevant to the current task.
- Do not load both templates unless translation or comparison requires them.
- Treat templates as adaptable structures, not mandatory checklists.
- Preserve confirmed requirements, identifiers, units, constraints, and verification criteria.
- Do not invent requirements to populate incomplete sections.
- Do not modify source templates during normal specification work.

## Workflow Selection

- **Beginner:** Gather intended use, functions, operating environment, available power, interfaces, size, quantity, budget, and constraints in accessible language. Accept unknown answers.
- **General:** Define measurable functional, electrical, interface, PCB, mechanical, and manufacturing requirements based on confirmed information.
- **Translate:** Preserve user intent and provenance when converting beginner requirements into an engineering specification. Transfer confirmed information, mark unresolved values as `TBD`, and identify proposals requiring human confirmation.
- **Update:** Inspect the existing specification before editing. Modify only authorized sections, preserve requirement IDs and unrelated content, and report conflicts without silently resolving them.

## Procedure

1. Establish project purpose, scope, intended use, and constraints from user input or permitted project data.
2. Select the relevant template and gather the most important missing information.
3. Separate user needs, confirmed requirements, assumptions, proposed implementations, and verification results.
4. Organize confirmed information into the appropriate sections.
5. Identify conflicts, ambiguities, and unresolved requirements without inventing values or approvals.
6. Draft or update files only when explicitly requested.
7. Preserve existing requirement IDs, values, units, tolerances, constraints, and unrelated content.
8. Keep the resulting specification proportional to the project's actual requirements.

## Requirements Quality

- Use `shall` for confirmed mandatory requirements, `should` for preferences, and `may` for optional capabilities.
- Assign stable unique IDs to engineering requirements when useful.
- Include units, tolerances, operating conditions, and verification criteria where relevant.
- Use `TBD` for unresolved requirements and `NOT_VERIFIED` for claims lacking sufficient evidence.
- Distinguish design targets from measured or verified results.
- ERC/DRC results or file presence do not establish design correctness or approval.

## Keep It Short

- Define the status defaults once in a conventions block at the top (for example: every requirement is `NOT_VERIFIED` unless stated, and `TBD` means open). Do not repeat `NOT_VERIFIED` or `TBD` in every row when a default covers it.
- State each fact once. A requirement lives in one place. Other sections refer to it by ID (for example "see PWR-001"). Do not repeat the same value in the register, the topic tables, the architecture text, and the decisions.
- Put each numeric limit in one topic table (for example the electrical table). The register and the decisions table refer to it by ID. Decisions keep the topic, the date, and the owner, not a second copy of the value.
- Keep tables and their template columns, even when cells are `TBD`. Do not replace a table with a sentence or a list.
- Do not fill a template table with placeholder rows. Add rows only for real requirements.
- Table format: pad the first column of every table to the width of its longest cell (header included), so the source lines up. Match the dashes in the separator row to that width. Leave the other columns unpadded.
- Remove template sections that do not apply. Fold the verification plan into the Verification column when it would only repeat it.
- Do not copy usage notes, template guidance, or maintainer comments into the specification.

## Writing Style

- Write simple, direct English, like one engineer talking to another. Use everyday words, short sentences, and active voice.
- Avoid fancy words, marketing phrases, and AI-style filler.
- Keep standard engineering terms and exact identifiers. Do not simplify a term if it loses accuracy.
- Do not use the em dash (`—`). Use a period, comma, colon, or parentheses.
- Use `TBD` for open values. Do not mix it with other spellings such as "TO BE DECIDED".
- Do not reword existing text that is already clear and correct.
- Priority: technical accuracy, then clarity, then brevity, then style.

## Boundaries

- Do not open, parse, assess, generate, or review PDF content.
- Keep KiCad design and library files read-only.
- Do not infer, validate, or change hardware project phases.
- Do not invent electrical specifications, component ratings, manufacturing capabilities, or test results.
- Do not assume specific hardware architectures, components, suppliers, PCB stackups, or fabrication processes.
- Do not create unnecessary logs, manifests, reports, Skills, scripts, or Git operations.
- Do not modify source templates unless explicitly requested.

## Suggested Output Names

- `HARDWARE_BRIEF.md` : Beginner stakeholder requirements.
- `HARDWARE_SPEC.md` : General hardware engineering specification.

For an execution checklist that tracks work and evidence against the specification, use the `hardware-checklist` skill.

Preserve existing project naming conventions and documentation. Human engineers remain responsible for confirming requirements and approving design decisions.
