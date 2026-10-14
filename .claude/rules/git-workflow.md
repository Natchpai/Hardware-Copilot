# Git Workflow Baseline

Portable Git safety and communication defaults. MUST rules are mandatory;
SHOULD rules are defaults that may bend with a stated reason.

## Overrides
Repository-local documentation (CONTRIBUTING, branch policy, release policy,
CLAUDE.md) takes precedence over the conventions and defaults in this file.
It cannot relax the Safety rules or the English-only rule.

## Hardware overrides (KiCad projects)
These add to, and never relax, the rules below. Hardware workflow phases and
engineering policy live in `hardware-workflow.md` and `engineering.md`.
- Git inspection is not permission to edit engineering files. Staging an
  existing change is distinct from writing the design and still needs approval
  for the exact paths.
- Native KiCad files (schematics, PCB layouts, symbol and footprint libraries,
  project files) and libraries remain subject to configured protections. Never
  modify them solely to prepare Git history.
- Never infer a project phase (DRAFT, PRELIMINARY, CHECK, RELEASE) from Git
  status, files or history. Do not tag, release or open a release PR unless the
  human declares the phase and approves that Git action separately.
- Do not open, read or assess PDF documents while inspecting changes; report
  their paths and metadata only. Mark ERC/DRC or document checks that were not
  run as `NOT_VERIFIED`.
- In commit and PR text, describe design changes, impact and risks factually.
  Do not claim a design is correct, safe or approved based on ERC/DRC results.

## Safety (MUST)

### Scope
- Preserve existing user changes, staged content, repository history,
  protected branches and review state.
- Git inspection is not permission to edit files. Never modify project files
  solely to prepare Git history. Editing `.gitignore`, a changelog or
  formatting is a content change and needs its own request.
- Never commit secrets, credentials, private keys or local environment files.
  Flag them and exclude them unless the user explicitly confirms.

### Approval tiers
- **Read-only** (status, diff, log, show, branch listing): no approval.
- **Tier 1, local and reversible**: staging, committing, creating or
  switching a branch, stashing. One explicit approval of a proposal that
  lists the exact actions and paths covers them.
- **Tier 2, remote or hard to reverse**: pushing, creating/updating/closing
  pull requests, tags, releases, merging, rebasing, reset/restore/clean,
  amending or rewriting commits, renaming or deleting branches. Each action
  needs its own explicit approval, even when shown in the same proposal as
  Tier 1 actions.
- Approval covers only what was listed. Do not infer it from an earlier
  request, a drafted message or a tool permission prompt.
- Never merge a pull request automatically.

### Never (no approval overrides these)
- Push directly to a protected or default branch (`main`, `master`, or the
  repository default), including refspecs such as `HEAD:main` and
  `git push origin main`. Push a feature branch and open a pull request
  instead.

### Prohibited unless explicitly authorized and permitted by tooling
- Force-push (use `--force-with-lease`, never plain `--force`), destructive
  reset or clean, history rewriting on pushed commits, and branch deletion.
- Skipping hooks (`--no-verify`) or bypassing signing.
- Committing directly to a protected or default branch.

### Reporting
- Never claim validation that was not performed. Mark missing or incomplete
  checks as `NOT_VERIFIED`.
- Present proposed actions, exact paths, commit messages and PR title and
  summary before the corresponding approved action.
- Keep summaries concise, factual and actionable.

## Commits
- MUST write commit messages, branch names and pull requests in English.
- MUST follow Conventional Commits 1.0.0: `<type>(<scope>): <description>`.
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`, `build`,
  `ci`. A repository that defines its own types or scopes overrides this list.
- MUST use lowercase types, imperative wording and a subject of at most 72
  characters; use `BREAKING CHANGE:` for incompatible interfaces.
- SHOULD keep each commit to one logical change; do not mix unrelated changes.
- SHOULD add a body when rationale or impact needs explanation.
- SHOULD prefer a new commit to amending; do not amend or rewrite a commit
  once it is pushed.
- SHOULD reuse scopes and issue-reference style already present in history.

## Branches and pull requests
- SHOULD name branches `<type>/<short-kebab-description>` using the commit
  types above.
- SHOULD use a Conventional Commit-style PR title.
- PR body SHOULD summarize purpose, affected areas, impact, risks and only
  the validation actually performed.
- SHOULD open a PR as draft when validation is `NOT_VERIFIED`.
