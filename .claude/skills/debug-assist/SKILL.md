---
name: debug-assist
description: >-
  Troubleshoot hardware faults using symptoms, measurements, hypotheses, and
  targeted diagnostic steps. Use when the user asks why a circuit fails,
  oscillates, overheats, behaves unexpectedly, or needs a measurement plan.
argument-hint: "[symptom, circuit, measurement, or suspected fault]"
---

# Hardware Debug Assistance

Help diagnose hardware behavior through engineering reasoning. Do not assume a
specific circuit topology, component, failure mode, or root cause. The engineer
retains final judgment; do not modify design files or hardware settings.

## Workflow

1. **Establish the symptom.** Identify expected versus observed behavior,
   operating conditions, reproducibility, and available measurements. Ask for
   only the missing detail that would materially change the next diagnostic step.
2. **Form hypotheses.** Rank a small set of plausible causes by observed
   evidence, not by generic frequency. Separate observations from assumptions.
3. **Choose discriminating checks.** Recommend the smallest safe measurements or
   inspections that distinguish competing hypotheses. State the measurement
   point, reference, expected alternatives, and what each outcome would imply.
4. **Update the diagnosis.** Revise or reject hypotheses as results arrive.
   Propose a corrective action only when the supporting evidence is adequate.

Use `sch-inspect` or `pcb-inspect` only when saved KiCad structural evidence is
needed. Use `eng-calc`, `component-check`, datasheets, or application notes only
when calculations or device-specific constraints affect the diagnosis;
datasheet content comes from user values, official web pages, or `notebooklm`
(never a PDF opened directly). Avoid
loading unrelated files or invoking other skills by default.

## Evidence and safety

- Classify conclusions as **Confirmed cause**, **Suspected cause**, or
  **NOT_VERIFIED**. Do not treat a plausible hypothesis as a confirmed fault.
- Distinguish measured behavior, simulated results, saved CAD data, and
  manufacturer specifications; cite the source of material claims.
- Consider instrument bandwidth, probe loading, ground-reference choice,
  measurement setup, and uncertainty before interpreting waveforms.
- For high-voltage, high-current, mains, battery, or stored-energy circuits,
  prioritize safe test conditions. Do not recommend unsafe probing, bypassing
  protection, or working on energized hardware without appropriate controls.
- Do not infer physical copper continuity, clearance, or live hardware state
  from KiCad net assignments alone.

## Response

Keep responses focused on the user's immediate troubleshooting goal. Summarize
**Observed symptom**, **Leading hypotheses**, **Next discriminating check**, and
**What the results would mean**. Use concise prose rather than a lengthy fixed
checklist. Do not create persistent logs, reports, scripts, or files unless the
user explicitly requests them.
