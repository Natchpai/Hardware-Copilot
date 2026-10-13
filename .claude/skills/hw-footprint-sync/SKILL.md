---
name: hw-footprint-sync
description: >-
  Synchronizes project-local KiCad footprint libraries: aligns 3D model folders
  with footprint libraries, repoints local 3D model paths in footprints, aligns
  fp-lib-table with the footprint folders, and fixes mismatched library
  nicknames in schematic Footprint properties.
  Use when the user asks to organize local 3D models, relink 3D models, or make
  fp-lib-table / schematic footprint references consistent with the footprint
  library folders.
  Edits only with explicit engineer authorization; does not touch connectivity,
  values, net names, or geometry.
---

# Footprint Sync

Footprint scope only. Symbol libraries and `sym-lib-table` belong to
`hw-symbol-sync`.

Keep the footprint libraries, the local 3D model folders, `fp-lib-table`, and
schematic Footprint references consistent.

## Locate the project layout first
Do not assume paths. Find them, then use them for the rest of the task:
- **Project dir:** the folder with the `.kicad_pro` and `fp-lib-table`
  (this is what `${KIPRJMOD}` expands to).
- **Footprint root:** the folder holding the `*.pretty` directories, taken from
  the `uri` entries in `fp-lib-table`.
- **Local 3D root:** the folder holding project 3D models, taken from existing
  `(model "${KIPRJMOD}/...` paths in `.kicad_mod` files, or confirmed by the
  user if there is none yet.
- **Naming prefix:** a shared prefix on `.pretty` names (such as `0_`), if the
  project uses one. If none, the 3D folder name equals the `.pretty` name.

## Authorization
- Follow the project's own rules first (for example `CLAUDE.md`, rule files).
  Native KiCad files and libraries are often read-only by default. Edit only
  after the engineer explicitly authorizes it in the current conversation.
- Never edit hooks or permission settings to gain access. If a hook or deny rule
  blocks an authorized edit, report the blocker and let the human adjust it. Do
  not bypass it with shell commands.
- Do not stage, commit, or push without separate approval.

## Conventions
- Local 3D folder: `<3D root>/<Name>/`, where `<Name>` is the `.pretty` name
  without the naming prefix, with identical letter case.
- Local model path in `.kicad_mod`: `${KIPRJMOD}/<relative path to 3D root>/<Name>/<file>`,
  using the same letter case as the real folders (matters on case-sensitive
  systems).
- Footprints whose model path uses a global variable (for example
  `${KICAD10_3DMODEL_DIR}`) are left unchanged.
- Library nickname = `.pretty` folder name without extension. Nicknames are
  case-sensitive.

## Procedure
1. **Inspect (read-only).** List the `*.pretty` folders (use `ls`; Glob does not
   match directories), list the local 3D root, and grep `(model "${KIPRJMOD}`
   in the `.kicad_mod` files. Re-list before every edit step: the human may
   rename folders in parallel.
2. **Rename 3D folders** to match the `.pretty` names. For case-only renames on
   Windows, move through a temporary name in two steps. Do not move or modify
   the `.step/.stp/.wrl` files themselves.
3. **Repoint local models.** For each `${KIPRJMOD}` model path, edit only that
   path string so it matches the actual file location and folder case.
4. **Report missing local 3D.** If a footprint references a local model whose
   file does not exist, do not edit it. Report footprint, referenced path, and
   expected folder. Never create 3D files.
5. **Align `fp-lib-table`.** Make `name` and `uri` of every `lib` entry match
   the `.pretty` folders exactly (no extra, no missing entries).
6. **Check schematics.** Grep `(property "Footprint" "...")` in `*.kicad_sch`
   and compare each nickname with `fp-lib-table`. Fix only the nickname text in
   the Footprint property, and only when the human asks. Do not alter any other
   field.
7. **Verify.** Re-grep model paths and confirm each local path resolves to an
   existing file. Search `.kicad_sch/.kicad_pcb/.kicad_pro` for old nicknames
   affected by a rename.

## Report
- List each change as `file: old -> new`.
- List missing local 3D files and unresolved mismatches.
- State `NOT_VERIFIED` for anything not confirmed in KiCad itself (library
  reload, model rendering). Remind the human to reopen the project, and to close
  schematic/PCB editors holding unsaved copies before external edits.
- Update any README in the 3D folder only if asked.
