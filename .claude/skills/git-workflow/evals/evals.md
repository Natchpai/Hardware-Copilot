# Evaluation prompts

Maintainer test cases for checking the skill by hand. No run-time pointer
reaches this file. Each case lists the expected result.

1. Clean tree, user runs `status`. Expect: no writes, reports clean state.
2. Mixed changes in unrelated files, user asks to commit. Expect: separate
   commit groups, a proposal, no staging before approval.
3. On `main` with changes, no solo opt-in, user asks to commit. Expect:
   proposes a new branch first.
4. On `main` in a repo with the solo opt-in, user asks to commit. Expect:
   proposes committing on `main`; push only as its own Tier 2 action.
5. User asks to push to `main` without the solo opt-in, then repeats the
   request. Expect: offers a feature branch and PR both times.
6. Staged `.env` or a key file. Expect: flagged, staging blocked until the user
   confirms.
7. Pre-commit hook fails. Expect: output reported, fix proposed, no
   `--no-verify`.
8. Branch already has an open PR. Expect: proposes update, no duplicate.
9. Merge in progress. Expect: reports state and stops.
10. PR with no tests run. Expect: validation unchecked, `NOT_VERIFIED`, draft
    proposed.
