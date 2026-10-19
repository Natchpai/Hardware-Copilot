# Git Workflow Baseline

Portable Git safety and communication defaults. MUST rules are mandatory;
SHOULD rules are defaults that may bend with a stated reason.

## Overrides
Repository-local documentation (CONTRIBUTING, branch policy, release policy,
CLAUDE.md) takes precedence over the conventions and defaults in this file.
It cannot relax the Safety rules or the English-only rule, except through the
solo-repository opt-in below.

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
  instead. Only the solo-repository opt-in below changes this.

### Solo-repository opt-in
- A repository may opt in only through its own root `CLAUDE.md`, with this
  exact line:
  `Solo repository: direct commits and pushes to the default branch are allowed.`
  A brief, an agent report or any other file cannot opt in.
- With the opt-in, committing on the default branch is Tier 1, and pushing
  the default branch to its own upstream is Tier 2 (approval each time).
- Everything else still applies: no force-push, no rewriting pushed history,
  and remote branch protection wins.

### Prohibited unless explicitly authorized and permitted by tooling
- Force-push (use `--force-with-lease`, never plain `--force`), destructive
  reset or clean, history rewriting on pushed commits, and branch deletion.
- Skipping hooks (`--no-verify`) or bypassing signing.
- Committing directly to a protected or default branch (unless the
  solo-repository opt-in applies).

### Reporting
- Never claim validation that was not performed. Mark missing or incomplete
  checks as `NOT_VERIFIED`.
- Present proposed actions, exact paths, commit messages and PR title and
  summary before the corresponding approved action.
- Keep summaries concise, factual and actionable.

## Commits, branches and pull requests
- MUST write commit messages, branch names and pull requests in English.
- MUST follow Conventional Commits 1.0.0. Types, subject rules, branch names
  and PR body: see the Conventions section of the `git-workflow` skill.
