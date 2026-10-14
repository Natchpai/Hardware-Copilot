---
name: hw-symbol-sync
description: >-
  Maintains project-local KiCad symbol libraries: splits a monolithic .kicad_sym
  into a per-symbol .kicad_symdir with kicad-cli, keeps sym-lib-table consistent
  with the symbol folders, and audits each symbol's Footprint link and
  ki_fp_filters against the project's footprint libraries.
  Use when the user asks to convert .kicad_sym to .kicad_symdir, align
  sym-lib-table, or check/fix symbol footprint links and footprint filters.
  Edits only with explicit engineer authorization; does not alter pins, graphics,
  or other symbol content.
disable-model-invocation: true
argument-hint: "[split <lib> | sym-lib-table | footprint-links]"
---

# Symbol Sync

Symbol scope only. Footprint libraries, 3D models, and `fp-lib-table` belong to
`hw-footprint-sync`.

## Locate the project layout first
Do not assume paths. Find them, then use them for the rest of the task:
- **Project dir:** the folder with the `.kicad_pro` and `sym-lib-table`
  (this is what `${KIPRJMOD}` expands to).
- **Symbol root:** the folder holding the `*.kicad_symdir` / `*.kicad_sym`
  libraries, taken from the `uri` entries in `sym-lib-table`.
- **Footprint root:** the folder holding the `*.pretty` directories, taken from
  `fp-lib-table`.
- **kicad-cli:** on PATH, or under the KiCad install (on Windows usually
  `C:/Program Files/KiCad/<ver>/bin/kicad-cli.exe`). Check `--version` and
  `sym upgrade --help` before relying on the splitting behavior below.

## Authorization
- Follow the project's own rules first (for example `CLAUDE.md`, rule files).
  Native KiCad files and libraries are often read-only by default. Act only
  after the engineer explicitly authorizes the conversion, edits, and any
  deletion of a source `.kicad_sym` in the current conversation.
- Never edit hooks or permission settings to gain access. If a hook or deny rule
  blocks an authorized action, report it and let the human adjust it. Do not
  bypass it.
- Do not stage, commit, or push without separate approval; Git actions follow
  `rules/git-workflow.md`.

## Conventions
- A `.kicad_symdir` folder holds one `<Symbol>.kicad_sym` per symbol.
- `sym-lib-table` entry: `name` = folder name without `.kicad_symdir`,
  `uri` = `${KIPRJMOD}/<path to symbol root>/<folder>`, with identical letter
  case.
- Library nicknames are case-sensitive.

## Split a .kicad_sym into a .kicad_symdir
`kicad-cli sym upgrade` splits a library only when the output path is an
**existing directory**. Without the directory it writes a single file named
`.kicad_symdir`, which is wrong. `--force` is required because the file is
usually already in the current format.

1. **Inspect (read-only).** List the symbol root, count source symbols with
   `grep -c '^	(symbol "' <lib>.kicad_sym` (top-level symbols only, one tab),
   and confirm no `<lib>.kicad_symdir` already exists.
2. **Check recoverability.** `git ls-files --error-unmatch <path>`. If the
   source is untracked, deleting it is irreversible: back it up to the scratch
   directory first.
3. **Convert.**
   ```bash
   cd <symbol root>
   mkdir <Lib>.kicad_symdir
   kicad-cli sym upgrade --force -o <Lib>.kicad_symdir <Lib>.kicad_sym
   ```
4. **Verify.** The file count in the new folder equals the source symbol count,
   and a sample file has the same header (`version`, `generator`) as another
   `.kicad_symdir` in the project, if any.
5. **Remove the source** `.kicad_sym` only when the human asked for it, after
   steps 2 and 4 succeed. Never delete before verification.

## Align sym-lib-table
Make `sym-lib-table` contain exactly one `lib` entry per `*.kicad_symdir`
folder (no extra, no missing), with `name` and `uri` matching the folder name
exactly. Keep empty libraries unless the human says to remove them.

## Audit symbol footprint links and ki_fp_filters
Read-only first. Run `hw-link-audit` to classify every symbol's `Footprint` link
and `ki_fp_filters` (its tables define the categories). If it cannot run, read
the `Footprint` and `ki_fp_filters` properties of every
`*.kicad_symdir/*.kicad_sym` (Grep with `-n false`; `grep -L` for files lacking
either) and compare with `*.pretty/*.kicad_mod` (`ls`).

Decide the action for each class:
- **Linked to a project-local footprint, file exists:** correct, except for a
  nickname whose letter case differs from the `.pretty` folder (fix the case).
- **Linked to a global library:** report it. If an equivalent project-local
  footprint exists and the human wants local links, repoint to it.
- **Linked to local, file missing** (or library missing): keep as is and report
  footprint and library.
- **Empty Footprint:** generic parts (R, C, connectors, jumpers) stay as is
  unless the human says otherwise.

`ki_fp_filters` rules:
- Patterns are space-separated globs (`*`, `?`); a space splits a pattern, so
  `SOD 882` is two patterns and does not match `D_SOD-882`.
- Edit a filter only when it does not match the linked footprint name AND that
  footprint file exists. Leave correct filters untouched.
- If a symbol linked to an existing footprint has no filter, add one.
- Whether a pattern without a library prefix is matched against the name only
  or the full `lib:name` is `NOT_VERIFIED`; cite KiCad documentation before
  relying on it.

Edit procedure (these files are easy to break):
1. Make one file at a time, never a batch of edits across files.
2. Property blocks are indented with **tabs** (2 for the property line, 3
   inside). Copy the indentation from the file, not from a line-numbered Read
   view, which adds one extra tab.
3. A new `ki_fp_filters` property copies the block layout of the sibling
   `ki_keywords` property (`at`, `show_name`, `do_not_autoplace`, `hide yes`,
   `effects`), placed right after it.
4. After each file, re-grep the two properties and report the result.

## Check schematics
Grep `(lib_id "..."` in `*.kicad_sch`. For every nickname that refers to a
project-local library, confirm it matches `sym-lib-table` (case-sensitive) and
that the symbol exists in that library. Global libraries (`Device:`, etc.) are
out of scope. Change schematics only when the human asks.

## Report
- List created folders, removed files, and `sym-lib-table` changes.
- State where the backup of any removed untracked file was saved.
- State `NOT_VERIFIED` for anything not confirmed in KiCad itself: no content
  diff of pins/properties was done, and the library table must be reloaded by
  reopening the project.
