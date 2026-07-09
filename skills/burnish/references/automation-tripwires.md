# Automation tripwires — green is not alive

Case, 2026-06/07, thevibeworks/claude-code-docs: a scheduled
docs-fetch workflow ran green 4x/day for three weeks while
producing nothing. An unpinned action (`claude-code-action@main`)
changed its argument parsing; the permission rule `Bash(gh pr:*)`
split on its space into two invalid rules; the agent could still
commit and push (`Bash(git:*)` survived) but every `gh pr create`
was silently denied. Result: 31 orphan branches, zero PRs, daily
success notifications, three weeks of stale main — every run
"successful". The failure was invisible precisely because every
component reported success: exit codes checked, artifacts didn't.

## Rules

1. **Assert the outcome artifact, not the exit code.** A pipeline
   whose job is to open PRs must fail when no PR exists. End every
   scheduled workflow with a verification step that checks the
   thing the pipeline exists to produce: PR opened, commit landed,
   post published, file changed. Pattern:

   ```yaml
   - name: Verify outcome
     run: |
       BRANCH=$(git branch --show-current)
       [ -z "$(git status --porcelain)" ] || { echo "::error::uncommitted changes left"; exit 1; }
       if [ "$BRANCH" != "main" ] && [ -n "$BRANCH" ]; then
         [ "$(gh pr list --head "$BRANCH" --json number --jq length)" != "0" ] \
           || { echo "::error::branch pushed but no PR"; exit 1; }
       fi
   ```

2. **Notify after proof, never before.** Success notifications fire
   only once the artifact URL exists and is non-empty. Failure
   notifies louder than success. A notification without an
   artifact behind it trains humans to ignore notifications.
3. **Pin moving refs.** `@main` on a third-party action is an
   outage on a timer. Pin exact tags/SHAs; upgrade deliberately.
   (This applies to base images, GitHub Actions, and any remote
   prompt/config an agent pipeline loads at runtime.)
4. **Permissions live in parse-proof files.** Agent tool
   permissions passed as CLI strings die on parser changes;
   permissions in JSON config (`.claude/settings.json`,
   `permissions.allow`) survive. Any rule containing a space is a
   parser bug waiting to happen.
5. **Watch the freshness signal, not the run history.** For any
   automated repo, the health check is "when did the OUTCOME last
   change" (last commit to main, last release, last post), never
   "are the runs green". Wire this into the groundskeeper sweep.
6. **Repo settings as rot prevention.** Auto-delete merged
   branches. 390 branches on one repo was this incident made
   visible — each orphan a silent failure nobody saw.
7. **Dry-run the failure.** After instrumenting, break the
   pipeline deliberately (deny a permission, point at a bogus
   remote) and confirm the run turns red and the failure
   notification fires. A tripwire that has never fired is a
   hypothesis, not a tripwire.

## Agent-pipeline specifics

When the automation is an LLM agent (claude-code-action or
similar):

- The agent completing its turn is not success; agents exit 0
  after being denied every tool they needed. Check
  `permission_denials_count` in logs, and always check the
  artifact.
- Give the agent an explicit failure protocol in its prompt: what
  to do, and what to notify, when a step is denied or errors —
  otherwise it improvises optimistic behavior (barking success
  after a failed PR).
- Prompts that say "always notify when creating X" become "always
  notify" under failure. Write "notify only after X exists".
