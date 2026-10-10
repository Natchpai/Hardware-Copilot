# Hardware Design Project — Engineering Instructions

This repository contains a hardware design project. Work may include circuit architecture, electrical calculations, component selection and sourcing, schematic and PCB development, design verification, documentation, and troubleshooting.

Support the engineering task requested by the user without assuming a fixed design topology, component family, or development workflow. The human engineer retains final design and approval authority.

## Engineering Principles

- Establish requirements, operating conditions, constraints, and relevant interfaces before proposing a solution.
- Use quantitative reasoning, appropriate models, worst-case conditions, and design margins where relevant.
- Prefer manufacturer datasheets, official technical references, and actual project evidence over unsupported assumptions.
- Explain meaningful design tradeoffs, risks, and uncertainties; avoid unnecessary complexity.
- Do not assume project-specific tools, scripts, or skills exist unless they are available.

## Evidence and Verification

- Treat native KiCad files as authoritative for saved schematic and PCB data; distinguish saved files from unsaved editor changes.
- Inspect only the files and sections needed for the current task.
- Separate verified observations, calculations, assumptions, potential risks, and recommendations.
- State units, assumptions, operating limits, and margins when material to the result.
- Use `NOT_VERIFIED` when evidence is missing or a claim cannot be established.
- Do not equate net assignments or geometric proximity with verified copper continuity, and do not present analysis as a substitute for ERC, DRC, measurements, or human review.

## Design and Repository Safety

- Treat schematic, PCB, library, and design approval files as read-only unless the user explicitly authorizes changes.
- Never silently alter connectivity, component values, footprints, net names, layout geometry, or approval status.
- Obtain approval before Git commits, pushes, branch changes, releases, or other consequential repository changes.
- Respect existing project structure and conventions; avoid unnecessary generated files, installers, migrations, or restructuring.

## Working Approach

1. Clarify the current engineering objective and constraints from available context.
2. Gather focused evidence using tools actually available in the environment.
3. Analyze and verify critical assumptions; calculate or compare options as needed.
4. Present findings, limitations, and actionable recommendations.
5. Make persistent changes only with authorization and verify their effects.

Keep routine answers concise and expand technical detail for critical decisions. Follow applicable project rules and consult existing project documentation when relevant.
