# Branch Protection Verification

Verification of the ruleset that protects `main` in the public repository.

## Ruleset (portfolio repository)

| Rule | Setting |
|---|---|
| Target | Default branch (`main`) |
| Enforcement | Active |
| Restrict deletions | On |
| Block force pushes | On |
| Require a pull request before merging | On (0 approvals required) |
| Require status checks to pass | On, check `test`, branches must be up to date |
| Bypass list | Empty |

## Test performed on 18 Nov 2026

A throwaway private repository was created with the same ruleset, then changed to public, because
GitHub does not enforce rulesets on private repositories on the free plan.

1. A commit was created locally on `main` of the throwaway repository.
2. `git push origin main` was attempted directly.

Result: the push was rejected.

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
remote: - Required status check "test" is expected.
! [remote rejected] main -> main (push declined due to repository rule violations)
```

The throwaway repository was deleted afterwards.

## Conclusion

Direct pushes to `main` are blocked, and changes must go through a pull request with the `test` check passing.
All changes merged into `main` in November 2026 (PRs #12 to #19) went through this path.
