---
name: component-check
description: >-
  Checks and compares electronic components used in KiCad hardware designs.
  Use when the user asks to verify a part number (MPN), datasheet, component
  ratings, pinout, schematic symbol, footprint, package, pad-to-pin mapping,
  BOM entry, or possible replacement part. Performs targeted, read-only
  verification with evidence and identifies unresolved mismatches.
argument-hint: "[<reference> | <MPN> | compare <MPN1> <MPN2>]"
---

# Component Check

## Scope and safety
- Read-only: never edit KiCad files, libraries, BOMs, or design records.
- Check the specific reference, MPN, or comparison requested; do not scan the whole project by default.
- Use authoritative manufacturer datasheets and package drawings. Identify the exact device variant, revision, and source. Never open or read a PDF directly (`rules/engineering.md`): use user-supplied values, official web pages, or the `notebooklm` skill with its citations, and report `NOT_VERIFIED` when none is available.
- A footprint name, pin count, ERC result, or similar-looking package is not proof of compatibility.
- Do not invent datasheet values, stock status, or verification results.

## Workflow
1. Resolve `$ARGUMENTS` or the user's request into a reference, MPN, or pair of MPNs. If a KiCad reference is given, locate its sheet instance and read only relevant component properties from native `.kicad_sch` data. Do not export or load a full-project netlist by default.
2. Resolve the exact manufacturer and orderable MPN, including package and suffix. If ambiguous, report candidate identities instead of selecting one silently. If the reference is not found, report `NOT_VERIFIED`; you may list similar references as candidates, but do not pick one.
3. Obtain the relevant datasheet sections and package drawing through an allowed source (see Scope). For a PDF, follow the NotebookLM rules in `rules/engineering.md` (ask before using it; the human approves the upload), query it with pinned IDs, and quote the cited table or pin text for the exact MPN. Record source and revision; if the document cannot be checked, say so.
4. Select checks according to the question:
   - **Identity/BOM:** manufacturer, MPN, value, variants and orderable package.
   - **Electrical:** absolute maximum ratings versus recommended operating conditions, relevant limits, tolerances, and derating.
   - **Symbol:** pin numbers, names, functions, power pins, special/multiplexed pins, and omitted pins.
   - **Footprint:** package variant, pad count/numbers, pin-1 orientation, dimensions and land pattern versus the exact datasheet package.
   - **Substitution:** electrical, functional, pinout, footprint and operating-condition compatibility; flag required design changes.
5. Compare only evidence available for the selected checks. When evaluating a schematic pin-to-net connection, request targeted connectivity evidence from `sch-inspect` if available; do not infer connections solely from nearby text or labels.
6. If PCB pad/net or geometry evidence is necessary, use targeted `pcb-inspect` data. For symbol, footprint and 3D-model link consistency across the project, use `hw-link-audit` instead of checking by hand. If a companion skill is not installed, say so and mark the dependent check `NOT_VERIFIED`.
7. Present concise findings. State the evidence source, the specific mismatch or limitation, and the next recommended action.

## Result format
- **Target:** reference/MPN and inspected scope.
- **Checks:** `PASS`, `FAIL`, `WARNING`, or `NOT_VERIFIED`, each with a short reason. `PASS` applies only to checks supported by evidence.
- **Evidence:** datasheet/document revision, pin/table/page, and relevant CAD references when available.
- **Action:** specific correction to consider or human verification needed.

## Example
```text
Target:   U7 (MPN as in BOM), symbol pins 1-8
Checks:   Pinout vs datasheet pin table  PASS   (pins 1-8, via NotebookLM, cited)
          Footprint land pattern         NOT_VERIFIED (package drawing not available)
          Absolute max VIN               WARNING (6 V max; net VIN_5V can reach 5.5 V, margin 0.5 V)
Evidence: datasheet rev C, table 5 and package drawing section; schematic U7 pins
Action:   Provide the package drawing values, then re-run the footprint check.
```

## Efficiency
- Start with part metadata and only the datasheet sections relevant to the request.
- Do not load entire datasheets, BOMs, symbol libraries, or PCB files by default.
- Use supporting files or deterministic scripts only when they exist and are applicable; do not generate persistent outputs unless asked.
