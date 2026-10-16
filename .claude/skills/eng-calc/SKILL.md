---
name: eng-calc
description: >-
  Perform, verify, or audit engineering calculations for electronic hardware.
  Use when the user asks to calculate component values, power, current, voltage,
  timing, filters, control parameters, losses, thermal behavior, tolerances,
  margins, worst-case conditions, or to check an existing equation or result.
  Apply the appropriate model to the actual problem; do not assume a fixed
  topology, part, or manufacturer.
argument-hint: "[calculation | specifications | equation to verify]"
---

# Engineering Calculations

Provide auditable calculations for hardware design and analysis. This skill
specifies a **calculation method**, not a fixed circuit topology, formula bank,
component value, or part recommendation. The engineer retains final authority.

## Boundaries

- Establish what is being calculated and which physical model applies before
  choosing equations. Do not reuse formulas outside their assumptions (for
  example, ideal converters, steady-state operation, CCM, small-signal models).
- Separate **given**, **derived**, **assumed**, and **datasheet-sourced** values.
  Never invent missing ratings, parasitics, material parameters, or test data.
- Use SI units consistently, convert prefixes explicitly where error-prone,
  and distinguish peak, RMS, average, instantaneous, and rated quantities.
- Treat absolute maximum ratings as limits, not recommended operating points.
  Account for tolerances, derating, temperature, transient behavior, and margins
  when they materially affect the answer.
- Label unsupported parameters or model validity `NOT_VERIFIED`. If assumptions
  materially affect the answer, provide a range or conditional result instead
  of a falsely precise single value.
- Calculated results are **estimates, not hardware verification**. Do not claim
  compliance, electrical safety, thermal adequacy, or design closure without
  the required source data and independent validation.
- Read KiCad files only through approved read-only tools. Do not modify design,
  library, BOM, or project configuration files; do not create persistent outputs
  unless explicitly requested.

## Workflow

1. **Define the target.** Identify the required quantity, operating mode,
   design constraints, available inputs, and appropriate accuracy. Ask only for
   information necessary to avoid a materially misleading answer; otherwise
   state bounded assumptions.
2. **Select and justify the model.** State the relevant equations and the
   assumptions under which they hold. Consider nonideal effects where material.
3. **Normalize inputs.** Show units, prefixes, operating ranges, and which
   values are nominal, worst-case, or manufacturer-specified.
4. **Calculate reproducibly.** Substitute values, perform dimensional checks,
   and use a calculator or local Python for error-prone numerical work, sweeps,
   optimization, matrices, or multiple operating points. Do not present
   unexecuted code as a computed result.
5. **Check the result.** Test limiting cases, signs, dimensions, conservation
   laws, and physical plausibility. Cross-check with an independent method
   when the consequence of error is high.
6. **Evaluate sensitivity.** Examine min/nominal/max conditions, tolerances,
   temperature, losses, derating, and significant parameter uncertainty when
   relevant; identify worst cases rather than assuming they occur at nominal.
7. **Report evidence and limitations.** Distinguish mathematical correctness
   from the validity of the underlying model and from measured performance.
   Flag missing evidence as `NOT_VERIFIED`.

## Coordination

- `design-assist`: use calculations to compare architectures and validate
  design trade-offs; do not select the overall architecture by formula alone.
- `component-select`: translate calculated limits into device requirements;
  do not choose an MPN merely because one calculated parameter fits.
- `stock-select`: check sourcing only after technical suitability is considered.
- `component-check`: verify actual datasheet ratings, tolerance, operating
  conditions, and package-related constraints.
- `sch-inspect`: obtain targeted schematic facts, without treating inferred
  connectivity as independently verified.
- For device-dependent models, consult the applicable current datasheet or
  reference through an allowed source (user values, official web pages, or
  `notebooklm` with citations; never open a PDF directly); do not pretend to
  have checked a source not actually accessed.

## Output

Keep the answer proportional to the request. For substantive calculations use:

1. **Inputs & assumptions** : values with units and relevant operating range.
2. **Model & equations** : applicable formula(s), conditions, and limitations.
3. **Results** : calculated quantities with appropriate precision and units;
   use a compact table for multiple operating points. Label each result
   `ESTIMATED` and state the method and margin (`rules/engineering.md`).
4. **Checks & implications** : sanity checks, margins, sensitivity, and the
   next evidence needed for design decisions. Mark critical unknowns
   `NOT_VERIFIED`.

For a simple arithmetic request, return the result and essential assumptions
without forcing all four sections. If the user supplies an equation for review,
check its derivation and conditions before substituting numbers.
