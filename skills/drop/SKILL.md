---
name: drop
description: >-
  Publish agent deliverables to a live review URL and pull human
  feedback back into the loop. Fires on three branches: the user
  wants an artifact, prototype, report, or file bundle shared for
  someone to review online ("send this to the team", "get eyes on
  this", "publish for review"); an agent loop needs a human
  verdict before continuing (approve / request-changes gating);
  and checking or acting on review feedback for an already
  published drop. Building the artifact itself is htmlize's job;
  reviewing a workspace locally without publishing anything is
  docent's. A drop is published the moment it exists -- anything
  too sensitive for a link that travels stays local.
---

# drop

A drop is a live, expiring, revocable URL wrapping a bundle of
static files, with a review surface a human can annotate and a
feedback API the agent reads back. It closes the loop that
publish-only tools leave open: publish -> human reviews -> agent
reads structured feedback -> revise -> republish, same link.

The interface is MCP-only: four tools from the drop MCP server.
Configure once:

```json
{
  "mcpServers": {
    "drop": {
      "command": "npx",
      "args": ["-y", "@agentdrop/mcp"],
      "env": { "AGENTDROP_URL": "https://<your-drop-service>" }
    }
  }
}
```

## Step 1 -- Gate

Publishing is the exception, not the default exit for every
artifact. Publish when a human other than the requester must see
it, when review needs to happen on another machine or async, or
when an agent loop must block on a human verdict. Stay local when:

| Signal | Route |
|---|---|
| The artifact carries secrets, client code, PII, unreleased work | Keep local -- a capability URL is a publication; treat it like posting the file |
| The requester will review in this same session | Just give the file path; a URL adds nothing |
| The user wants to browse a whole workspace, not one deliverable | docent serves it locally, nothing leaves the machine |
| The deliverable itself still needs building | htmlize first; drop is transport, not authoring |

State what is in the bundle before publishing. If any row above
matches, say which and stop.

## Step 2 -- Publish

Bundle rules: one directory, `index.html` at its root, every
subresource referenced relatively and included. Self-contained
htmlize artifacts already pass. Limits: 25 MiB/file, 100 MiB,
1000 files.

Call `drop_publish {dir, title}`. It returns:

- `url` -- the artifact, live
- `review_url` -- the review surface; this is what the human gets
- `drop_id` + `upload_token` -- returned ONCE; keep both for the
  drop's whole life (feedback, revisions, revoke). Losing the
  token orphans the drop until it expires.

Hand the human `review_url` with one line on what to look at and
what happens on approve. Unclaimed drops expire in ~72 h; say so
when review may wait past a weekend.

## Step 3 -- Feedback

`drop_feedback {drop_id, upload_token}` returns verdicts
(`approve` / `request_changes`) and annotations, each pinned to
the revision the reviewer actually saw -- feedback on r1 after
you shipped r2 is history, not instruction. In a gated loop,
poll with backoff (30 s is plenty; reviews take minutes to
days), and treat `request_changes` + annotations as the work
queue: each annotation carries an anchor (css path, quote, bbox)
into the exact element the reviewer clicked.

## Step 4 -- Revise

Act on the feedback, then `drop_publish {dir, drop_id,
upload_token}` again. That appends an immutable revision N+1 on
the SAME review link -- never create a fresh drop for a revision;
the reviewer's link and the annotation history are the thread.
Old revisions keep serving, so "what did they approve" always has
an answer. When the drop should die early: `drop_revoke`.

## Check

- Bundle self-contained: opening `url` renders with no broken
  subresources.
- The human got `review_url`, not `url` -- the artifact link has
  no verdict bar.
- `upload_token` retained by the agent (memory, scratchpad, or
  task state), never pasted into the artifact or chat.
- Revisions of one deliverable share one drop_id.
- Nothing published that Step 1 would have stopped; when in
  doubt the answer was docent.

## Lineage

Built as the outward half of htmlize -- same privacy doctrine
("a file shared by link is published"), turned into product
defaults: ephemeral, noindex, revocable.
