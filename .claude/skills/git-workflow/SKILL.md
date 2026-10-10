---
name: git-workflow
description: >-
  Assists with Git and GitHub workflows, including repository
  status inspection, change analysis, branch management,
  Conventional Commits, and pull request preparation.
  Use when the user asks to review Git changes, prepare or
  create commits, organize branches, summarize changes,
  or prepare and open GitHub pull requests.
  Requires user approval before repository write operations.
argument-hint: "status | commit [scope] | pr [base]"
---


# Git Workflow

Manage Git changes without modifying engineering design content.

## Source of policy
- Follow `.claude/rules/git-workflow.md` and `.claude/settings.json`.
- For PRs, read `.github/pull_request_template.md` and preserve its sections and checkboxes.
- Respect repository branch protection and tool permissions. This skill does not grant additional permissions.

## Dispatch
Interpret `$ARGUMENTS` as one of:
- `status` — inspect only; never change repository state.
- `commit [scope]` — propose and, after approval, create focused commit(s).
- `pr [base]` — propose and, after approval, push/open a draft PR.
- If omitted or unsupported, show these choices without making changes.

## Shared inspection
1. Check repository root, current branch, working-tree status, and staged/unstaged/untracked changes.
2. Inspect only diffs and files relevant to the requested operation; check for binary KiCad changes with file lists and metadata rather than claiming textual diff coverage.
3. Detect unrelated or potentially sensitive files. Do not stage secrets, caches, generated exports, or unrelated changes.
4. Never modify KiCad design/library files, discard user changes, or alter review/approval state.
5. Report missing evidence as `NOT_VERIFIED`; do not invent ERC/DRC/test results.

## status
- Report branch, upstream if available, clean/dirty state, and concise logical change groups.
- Distinguish staged, unstaged, and untracked files.
- Suggest a next commit or branch name only when useful. Perform no writes.

## commit
1. Inspect staged and unstaged diffs, including any pre-existing staged content.
2. Group changes by purpose; use Conventional Commits 1.0.0 and repository scopes.
3. If a new branch is needed, suggest `feature/`, `fix/`, `docs/`, or `chore/` plus a short descriptive name. Do not create/switch branches silently.
4. Present proposed branch action (if any), exact file paths to stage, commit subject, optional body, and any unverified checks.
5. Obtain explicit user approval before branch changes, staging, or committing; comply with tool permission prompts as well.
6. Stage only approved paths. Recheck the staged diff before committing, and stop if it differs materially from the approved scope.
7. Commit only approved changes. Report the resulting commit hash and any remaining changes. Do not push unless separately requested and approved.

## pr
1. Determine the intended base branch (use the repository default branch unless the user specifies another); inspect the current branch, upstream, and ahead/behind state.
2. Compare the complete proposed PR range against the base, including all commits and changed files; distinguish committed work from uncommitted changes.
3. Propose a Conventional Commit-style PR title and a concise body using the repository PR template.
4. Check only boxes supported by the actual diff or confirmed validation. Explain not-run or inconclusive checks; never infer PASS from an unchecked item.
5. Display base/head, any push needed, PR title/body, impact, risks, and validation status for approval.
6. Obtain explicit approval before push and before PR creation. Do not push directly to a protected branch.
7. Create a **Draft PR** using GitHub tooling only if available and authenticated; otherwise provide the ready-to-paste title and body. Never merge.
8. Report the PR URL only if returned by GitHub tooling. Do not claim PR creation or push succeeded without confirmation.

## Safety
- No force-push, destructive reset/clean, automatic merge, branch deletion, or history rewriting.
- Do not bypass permission prompts or claim approvals from earlier unrelated requests.
- Do not create additional logs, reports, or temporary repository files unless necessary and approved.
- Keep user-facing summaries concise, with enough evidence for review.
