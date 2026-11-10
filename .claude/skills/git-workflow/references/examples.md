# Git Workflow Examples

## Proposal template
Use one block for every state-changing request. Omit lines that do not apply.

```
Proposed actions
1. <action: branch / stage / commit / push / PR>
2. ...

Paths:     <exact paths to stage>
Excluded:  <flagged or unrelated paths left out, and why>
Message:   <commit subject, or PR title>
Not verified: <checks not run, or "none">
Risks:     <protected branch, secrets flagged, behind upstream, or "none">

Approve these actions?
```

Example:

```
Proposed actions
1. Create branch fix/parser-empty-input
2. Stage and commit
3. Push with upstream

Paths:     src/parser.c, tests/parser_test.c
Excluded:  .env (credentials, not staged)
Message:   fix(parser): handle empty input
Not verified: tests not run
Risks:     none identified

Approve these actions?
```

## Commit messages
```
feat(uart): add configurable baud rate
fix(parser): handle empty input
docs(readme): document build steps
refactor(config): split loader from validator
chore: ignore local editor settings
```

With body and breaking change:

```
refactor(api): rename init to open

The old name conflicted with the driver entry point.

BREAKING CHANGE: callers must use open() instead of init().
```
