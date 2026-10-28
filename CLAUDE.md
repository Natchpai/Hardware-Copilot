## Hardware Design Project

This repository contains a hardware engineering project. Work may involve circuit architecture, electrical calculations, component selection and sourcing, schematic and PCB development, design review, documentation, and troubleshooting.

Assist with the engineering task at hand. Do not assume a fixed circuit topology, component family, or project workflow. The human engineer makes final design and approval decisions.

## Project Context

- Use the project's requirements, existing design files, and documentation to understand the current design before making recommendations.
- Locate the KiCad project first: the folder with the `.kicad_pro` file. Its library tables (`fp-lib-table`, `sym-lib-table`) and project-local libraries belong to the design.
- Treat KiCad files as the representation of the **saved** design; unsaved changes in the editor may not be reflected in those files.
- Follow the existing project structure, naming conventions, and design intent. Do not introduce new conventions without a clear need.
- Use only capabilities available in the current environment; do not assume a specific script, skill, or analysis tool exists.

## Protected Files

Native design files and local libraries are protected by the `.claude/hooks/protect_kicad_v2.py` hook. The rules live in `.claude/hooks/protect.json`, and `.claude/settings.json` should stay consistent with them.

- **Default:** inspect and propose changes with justification; do not edit.
- If the hook blocks or asks, report it. Never edit the hook, `protect.json`, or permission settings to gain access, and do not bypass a block with shell commands.
- Never silently alter connectivity, component values, footprints, net names, or geometry.

## Project Instructions

- Follow applicable project-specific instructions in `.claude/rules/` when available.
- Respect existing project conventions, documentation, and workflows.
- Use available tools and capabilities appropriate to the task.
- Do not assume that optional project configurations or tools are installed.
- PDFs: follow `.claude/rules/pdf.md` (project reports may be read and generated; schematic, PCB and datasheet PDFs are not read directly).
- Language: follow the project's convention. If none is stated, write files and commit messages in English and reply in the user's language.

## Working Approach

1. Establish the task objective, relevant constraints, and scope from the available context.
2. Inspect the relevant project data and use suitable calculations, references, or tools as needed.
3. Explain key tradeoffs and distinguish findings from proposed design changes.
4. Present actionable conclusions, open questions, and next steps at a level of detail appropriate to the task.

## Language Rules
- Use English for all files, code, error messages, and git's activity messages.
- Use English for user-facing explanations, conversational text in CLI, unless otherwise specified by the user.
