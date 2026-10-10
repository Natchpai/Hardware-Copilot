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
- Use authoritative manufacturer datasheets and package drawings where available. Identify the exact device variant, revision, and source.
- A footprint name, pin count, ERC result, or similar-looking package is not proof of compatibility.
- Do not invent datasheet values, stock status, or verification results.

## Workflow
1. Resolve `$ARGUMENTS` or the user's request into a reference, MPN, or pair of MPNs. If a KiCad reference is given, locate its sheet instance and read only relevant component properties from native `.kicad_sch` data. Do not export or load a full-project netlist by default.
2. Resolve the exact manufacturer and orderable MPN, including package and suffix. If ambiguous, report candidate identities instead of selecting one silently.
3. Retrieve the relevant manufacturer datasheet sections and package drawing. Record source/revision when available. If the document cannot be checked, say so.
4. Select checks according to the question:
   - **Identity/BOM:** manufacturer, MPN, value, variants and orderable package.
   - **Electrical:** absolute maximum ratings versus recommended operating conditions, relevant limits, tolerances, and derating.
   - **Symbol:** pin numbers, names, functions, power pins, special/multiplexed pins, and omitted pins.
   - **Footprint:** package variant, pad count/numbers, pin-1 orientation, dimensions and land pattern versus the exact datasheet package.
   - **Substitution:** electrical, functional, pinout, footprint and operating-condition compatibility; flag required design changes.
5. Compare only evidence available for the selected checks. When evaluating a schematic pin-to-net connection, request targeted connectivity evidence from `sch-inspect` if available; do not infer connections solely from nearby text or labels.
6. If PCB pad/net or geometry evidence is necessary, use targeted `pcb-inspect` data when available. Never claim that these companion skills or parsers are implemented merely because they are named.
7. Present concise findings. State the evidence source, the specific mismatch or limitation, and the next recommended action.

## Result format
- **Target:** reference/MPN and inspected scope.
- **Checks:** `PASS`, `FAIL`, `WARNING`, or `NOT_VERIFIED`, each with a short reason. `PASS` applies only to checks supported by evidence.
- **Evidence:** datasheet/document revision, pin/table/page, and relevant CAD references when available.
- **Action:** specific correction to consider or human verification needed.

## Efficiency
- Start with part metadata and only the datasheet sections relevant to the request.
- Do not load entire datasheets, BOMs, symbol libraries, or PCB files by default.
- Use supporting files or deterministic scripts only when they exist and are applicable; do not generate persistent outputs unless asked.
