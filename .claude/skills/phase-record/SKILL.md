---
name: phase-record
description: >-
  Acknowledges a hardware project phase explicitly declared by a human engineer
  and, only when requested, records it in README.md.
  Use when the user declares DRAFT, PRELIMINARY, CHECK, or RELEASE.
  Does not evaluate readiness, create state files, or perform Git release actions.
argument-hint: "DRAFT | PRELIMINARY | CHECK | RELEASE"
---

# Phase Record

Record only a phase explicitly declared by the human engineer. A recorded phase
is project context, not evidence of verification, approval, or release.

## Accepted phases
- `DRAFT`
- `PRELIMINARY`
- `CHECK`
- `RELEASE`

## Record
1. Accept a phase only when the human states one of the accepted values.
2. If persistence is not explicitly requested, acknowledge the declaration in
   conversation only and make no file changes.
3. If the human explicitly asks to update `README.md`, use an existing
   `Project Status` section when present. Otherwise add one concise section:

   ```markdown
   ## Project Status

   - Current Phase: CHECK
   - Declared By: Human Engineer
   ```

4. Replace an existing phase record without duplicating status sections;
   preserve unrelated README content.
5. Add a date or note only when the user requests it and supplies it, or when
   a reliable current date is available in the active session.

## Boundaries
- Never infer, validate, advance, or reject a phase from project files, ERC,
  DRC, document presence, Git state, or a GitHub release.
- Do not create `PHASE.md`, JSON state, a database, or other phase records.
- `RELEASE` never authorizes a commit, tag, push, pull request, or GitHub
  release.
- Do not generate, open, read, parse, or assess PDF documents.
- Keep KiCad files and libraries read-only.

## Output
- State the declared phase and whether it was acknowledged only or recorded in
  `README.md`.
- Identify missing prerequisites for a requested README update without creating
  another file automatically.
