# Export and round-trip

An interactive artifact is a loop, not a destination. The user
manipulates state in the browser; the result must come back to
the agent or land in a durable file. An editor without an export
is a dead end -- the work done in it evaporates.

## The contract

Every artifact where the user manipulates state ends with a
visible export control. Design the leaving data before the UI:
decide what crosses back to the agent and in what format -- the
interface is whatever produces that payload.

Match the format to the user's next action:

| Next action | Export |
|---|---|
| Paste back to the agent to act on | Copy as prompt -- natural language with the decisions inline |
| Another session parses it | Copy as JSON -- stable keys, no prose |
| Commit to docs / notes | Copy as markdown -- ready to paste into the file |
| Apply to config | Copy as diff -- only the changed keys |

Scope follows the next action too. A board the user works
through one item at a time wants a copy control on each card; a
config editor wants the changed keys, never the full dump. Offer
two scopes at most; a panel of five export buttons is a puzzle,
not a feature.

## Clipboard mechanics

`navigator.clipboard.writeText` rejects in sandboxed artifact
iframes (Permissions Policy blocks clipboard-write) and when the
document has lost focus -- both common situations for artifacts.
Always wrap it. `document.execCommand('copy')` is deprecated but
retained by every browser as exactly this fallback; do not let a
cleanup pass remove it.

```js
async function copyText(text, btn) {
  let ok = false;
  try {
    await navigator.clipboard.writeText(text);
    ok = true;
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    ok = document.execCommand('copy');
    ta.remove();
  }
  const old = btn.textContent;
  btn.textContent = ok ? 'Copied' : 'Copy failed -- select the text manually';
  setTimeout(() => { btn.textContent = old; }, 1500);
}
```

Honest feedback is part of the contract -- a button that gives no
confirmation gets clicked three times and trusted zero times, and
a button that says "Copied" when both paths failed is worse.

## Embedding the task data

Pre-populating with real data has a sharp edge: the data lives
inside a `<script>` element, and if any string in it contains
`</script>` -- a diff touching HTML, a code sample, a log line --
the document truncates at that point. Embed as JSON in a
non-executing block, escaping `</` as `<\/` (a legal JSON escape
that `JSON.parse` resolves back to `/` for free):

```html
<script id="task-data" type="application/json">
  {"diff": "...content with <\/script> safely escaped..."}
</script>
<script>
  const data = JSON.parse(
    document.getElementById('task-data').textContent
  );
</script>
```

This also keeps data and behavior separated, which makes the
artifact auditable: anyone can read exactly what data it carries.

## Unexported state is one closed tab from gone

With `localStorage` banned, an editor's state lives only in
memory -- thirty triaged tickets vanish on an accidental Cmd-W.
Guard it:

```js
let dirty = false;  // set on any edit, cleared by export
addEventListener('beforeunload', (e) => {
  if (dirty) e.preventDefault();
});
```

Flip `dirty` on every mutation and clear it when an export
fires. This is the replacement for the persistence localStorage
would have provided: not saving the work, but making losing it
a deliberate act.

## Markdown stays the source of truth

When an artifact touches durable project state -- a plan that
will be tracked, a config that lives in the repo, notes the team
maintains -- the HTML is a generated view, never the record:

1. The durable content is written to (or already lives in) a
   markdown file that git can diff.
2. The artifact renders or edits that content.
3. The export produces the updated markdown (or a patch to it),
   labeled with which file it belongs to.
4. After the user acts, the markdown gets updated -- by them
   pasting, or by the agent on the next turn.

This resolves the co-authoring objection to HTML artifacts:
humans and git keep the medium they can edit and diff; HTML
provides the reading and manipulation surface. If you find
yourself versioning `.html` files to track content changes, the
record is in the wrong layer.

## What this skill deliberately does not do

There is a richer pattern where the artifact POSTs results to a
local listener and the agent is notified without any paste --
implemented in
[f-labs-io/agent-html-skills](https://github.com/f-labs-io/agent-html-skills)
with a per-session server, monitor wiring, and helper skills. It
is genuinely better UX and genuinely heavier machinery, and it
only works in harnesses with shell access and background
monitors. This skill takes the portable subset: clipboard out,
paste back. One copy-paste per round trip is the cost of working
identically in every agent harness.
