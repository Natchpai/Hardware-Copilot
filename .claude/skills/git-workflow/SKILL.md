---
name: git-workflow
description: >-
  Git and GitHub work: status and diffs, branches, Conventional Commits and
  pull requests. Use when the user asks what changed, or wants to commit,
  create or switch a branch, or open a PR.
argument-hint: "status | branch [name] | commit [scope] | pr [base]"
---

# Git Workflow

Shared safety policy (approval tiers, default-branch rules, solo-repository
opt-in, secrets, `NOT_VERIFIED`) lives in `~/.claude/rules/git-workflow.md`,
which is always loaded; follow it. This skill adds the conventions and the
procedure. If that rule is not in your context, treat every state-changing
action as needing its own approval, and push only feature branches.

Read `references/examples.md` when drafting a proposal, commit message or PR
body.

## Local safeguards
- Read repository-local instructions (CONTRIBUTING, CLAUDE.md, branch rules);
  they override the defaults here.
- Change only Git state. Source files, generated artifacts and repository
  configuration stay as they are unless the user asks for that edit
  separately.

## Execution gate
- Read-only inspection needs no approval.
- Before any state-changing action, present one **proposal** (template in
  `references/examples.md`) listing every action with exact paths, then stop.
- Apply the rules' approval tiers to the actions in the proposal. Any later
  action or change of scope needs a new proposal.
- Show the proposal even when the user gave advance or blanket approval ("no
  need to ask again"). Approval covers only the listed actions.
- For a request to push to the default or a protected branch, offer the
  allowed route: push a feature branch and open a PR. Keep that answer when
  the request is repeated. The only exception is the solo-repository opt-in.
- After each approved action, verify the real result (`git status`,
  `git log -1`, or the tool output) and report it. An exit code alone is not
  proof of success.

## Conventions
- Commits follow Conventional Commits 1.0.0: `<type>(<scope>): <description>`.
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`, `build`,
  `ci`. A repository that defines its own types or scopes overrides this list.
- Use lowercase types, imperative wording and a subject of at most 72
  characters; use `BREAKING CHANGE:` for incompatible interfaces.
- Keep each commit to one logical change. Add a body when rationale or impact
  needs explanation.
- Prefer a new commit to amending; never amend or rewrite a pushed commit.
- Reuse scopes and issue-reference style already present in history.
- Branches: `<type>/<short-kebab-description>` using the types above.
- PRs: Conventional Commit-style title. The body summarizes purpose, affected
  areas, impact, risks and only the validation actually performed. Open as
  draft when validation is `NOT_VERIFIED`.

## Dispatch
Interpret `$ARGUMENTS` as one of:
- `status`: inspect only.
- `branch [name]`: propose creating or switching a branch.
- `commit [scope]`: propose and, after approval, create focused commit(s).
  `scope` is an optional commit-scope hint (for example `uart`), not a path.
- `pr [base]`: propose and, after approval, push and open a PR.
- No argument: infer the command from the user's request. If it is unclear,
  list these choices and change nothing.
- Tag, release, merge, rebase, reset and deletion requests each get their own
  proposal, separate from any commit or PR workflow.

## Shared inspection
1. Establish repository root, branch, upstream and working-tree state
   (`git status --short --branch`). Untracked files count as candidates for
   "my changes".
2. Separate staged, unstaged and untracked changes (`git diff --stat`,
   `git diff --cached --stat`); open only relevant diffs.
3. Read recent history (`git log --oneline -n 20`) and follow the repo's
   existing conventions for scopes, language and issue references, unless
   they conflict with the rules.
4. For binary or non-reviewable files, report path and metadata, not a diff.
5. Flag unrelated files, caches and generated artifacts; propose leaving them
   out.
6. Secrets and large files (see rules): check staged and candidate paths and
   diffs for credential files (`.env`, key and certificate files), tokens or
   private keys in content, and unusually large files. Inspect secret files
   by key names only; never print their values. Block staging until the user
   explicitly confirms each flagged item, and list flagged items as
   "Excluded" in the proposal. Suggesting a `.gitignore` entry is fine; editing
   it needs its own request.
7. If inspection fails, report the failure and change nothing. Report evidence
   you could not get as `NOT_VERIFIED`.

Done when branch, upstream and any state from "Repository states" are known,
and every changed path (staged, unstaged, untracked) is either a candidate or
listed as Excluded with a reason.

## Repository states
Detect these during inspection and adapt the proposal:
- **Merge, rebase, cherry-pick or bisect in progress**: report it and stop.
  Commit or switch branches only after the user decides how to proceed.
- **Detached HEAD**: propose a new branch before committing.
- **On the default or a protected branch**:
  - With the solo-repository opt-in (default branch only): propose committing
    on it, and propose the push as its own Tier 2 action.
  - Otherwise: propose a new feature branch first and deliver through a PR.
    Commit on the default or protected branch itself only if the user
    explicitly asks; push only the feature branch.
- **No upstream**: note it; propose `git push -u origin <branch>` in the PR
  flow.
- **No remote**: report that pushing and PRs are not possible yet. Adding a
  remote changes repository configuration and needs its own proposal.
- **Dirty tree when switching branches**: creating a new branch carries the
  changes by default; switching to an existing branch may conflict, so
  propose carrying or stashing. Stash is a mutation and needs approval.
- **Empty repository (no commits)**: say so; the first commit is a normal
  commit proposal.
- **Behind the base or upstream**: report it; propose a merge or rebase
  only as a separate proposal.

## status
Report branch, upstream, clean/dirty state, and logical change groups,
distinguishing staged, unstaged and untracked paths, plus any state from
"Repository states". Suggest a commit or branch name only when useful. Done
when every changed path appears in exactly one group.

## branch
1. Inspect current branch and ahead/behind state.
2. Propose `<type>/<short-kebab-description>` using a type from Conventions.
3. After approval, create or switch (`git switch -c <name>` or
   `git switch <name>`). Deleting, renaming or force-moving a branch is a
   separate Tier 2 proposal.

## commit
1. Inspect staged and unstaged diffs, including pre-existing staged content.
2. Group changes by purpose, one commit per logical group. Splitting is at
   path level (interactive staging is unsupported); flag files that mix
   concerns and ask how to proceed. Propose the split by default; the user may
   ask for a single commit. Name a new branch after the primary group's type.
3. Draft each message per Conventions.
4. Present the proposal. Stop for approval.
5. After approval, stage only the listed paths (`git add -- <paths>`), recheck
   `git diff --cached`, and stop if it differs materially from the proposal.
6. Commit. Amend only with explicit Tier 2 approval and an unpushed commit.
7. If a hook fails, report its output and propose a fix. Hooks stay enabled.
8. Report the hash and remaining changes. Push only if the user separately
   approved it.

## pr
1. Determine the base branch; inspect branch, upstream and ahead/behind.
2. Check whether a PR already exists for the branch
   (`gh pr list --head <branch>`); if so, propose updating it instead of
   creating a duplicate.
3. Review the whole range (`git log <base>..HEAD`,
   `git diff <base>...HEAD --stat`); separate committed work from local
   changes. Done when every commit in the range is reflected in the summary.
4. Fill the repository PR template (`.github/pull_request_template.md` or
   `pull_request_template.md`), preserving its sections:
   - **Summary**: purpose and why, from the whole range, not just the last
     commit.
   - **Type of Change** and **Affected Areas**: check only from the diff and
     changed paths (a docs-only diff means Documentation).
   - **Validation Performed**: check only checks actually run and put their
     results under "Results / evidence"; otherwise leave unchecked and write
     `NOT_VERIFIED`.
   - **Related Issues**: add `Closes #n` only when the branch name, commits or
     user supply the issue.
5. Use a Conventional Commit-style title. Propose a draft PR when validation
   is `NOT_VERIFIED`.
6. Present base/head, required push, title, body, impact and risks as one
   proposal.
7. After approval, push the feature branch (`git push -u origin <branch>`)
   and create the PR (`gh pr create`) only if `gh` is available and
   authenticated.
8. Report the PR URL only if the tool returned one. Merging is left to the
   user.

## Platform notes
Line-ending warnings (LF/CRLF) are informational; do not report them as risks
or change settings unless asked.
Commands are shown in POSIX form. On Windows PowerShell, quote arguments
containing spaces or special characters, and pass multi-line commit messages
or PR bodies with a here-string or a message file outside the repository
rather than relying on shell escapes. Use forward slashes in paths.

## Output
Keep logs, reports and temporary files outside the repository unless asked.
