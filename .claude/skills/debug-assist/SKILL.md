---
name: debug-assist
description: >-
  Troubleshoots hardware faults from symptoms, measurements, hypotheses and
  targeted diagnostic steps. Use when the user asks why a circuit fails,
  oscillates, overheats or behaves unexpectedly, or needs a measurement plan.
argument-hint: "[symptom, circuit, measurement, or suspected fault]"
---

# Hardware Debug Assistance

Diagnose hardware behavior from the evidence at hand. Start with no fixed idea
of the topology, component, failure mode or root cause. Design files and
hardware settings stay unchanged.

## Workflow

1. **Establish the symptom.** Expected versus observed behavior, operating
   conditions, how often it happens, and what was measured. Ask only for the
   missing detail that would change the next diagnostic step.
2. **Form hypotheses.** Rank a few plausible causes by the observed evidence,
   not by how common they are in general. Keep observations apart from
   assumptions.
3. **Choose discriminating checks.** The smallest safe measurement or
   inspection that tells the leading hypotheses apart. Give the measurement
   point, the reference, the possible outcomes and what each one means.
4. **Update the diagnosis.** Revise or drop hypotheses as results come in.
   Propose a fix only when the evidence supports it.

Use `sch-inspect` or `pcb-inspect` when saved KiCad structure matters to the
diagnosis. Use `eng-calc`, `component-check`, datasheets or application notes
when a calculation or a device limit changes the diagnosis. Datasheet values
follow "Datasheet evidence" in `rules/engineering.md`: user values, official
web pages, or `notebooklm` with citations. Load other files or skills only
when the next step needs them.

## Evidence and safety

- Classify each conclusion as **Confirmed cause**, **Suspected cause** or
  `NOT_VERIFIED`. A plausible hypothesis stays suspected until a measurement
  confirms it.
- Keep measured behavior, simulation results, saved CAD data and manufacturer
  specs apart, and cite the source of each key claim.
- Account for instrument bandwidth, probe loading, ground reference, setup
  and uncertainty before reading a waveform.
- For high-voltage, high-current, mains, battery or stored-energy circuits, put
  safe test conditions first. Never recommend unsafe probing, bypassing
  protection, or working on energized hardware without proper controls.
- KiCad net assignments alone do not show physical copper continuity,
  clearance or live hardware state.

## Response

Stay on the user's immediate troubleshooting goal. Give **Observed symptom**,
**Leading hypotheses**, **Next discriminating check** and **What the results
would mean**, in short prose rather than a long fixed checklist. Write logs,
reports, scripts or files only when the user asks.

## Example

```text
Symptom:    3V3 drops to about 2.6 V for 2 ms at power-up, then the MCU resets (user scope capture).
Hypotheses: 1. VIN sags under inrush (source or cable)               | Suspected cause
            2. Regulator hits current limit charging output caps    | Suspected cause
Next check: probe VIN and 3V3 at the regulator pins, same ground point, single-shot trigger at power-up.
Meaning:    VIN sags with 3V3 -> source side (1). VIN flat while 3V3 sags -> regulator limit (2).
```
