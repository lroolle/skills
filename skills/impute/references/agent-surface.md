# The agent-legible repo surface

A growing share of first contact with a repo is an AI agent acting
for a human: answering "what should I use for X", writing
integration code, or deciding what to recommend. Repos that are
legible to agents get recommended; repos that aren't, don't exist.
The full surface: llms.txt at repo root, a live llms.txt +
llms-full.txt on the docs site, an agent-addressed line in the
README, and a plugin marketplace where the product warrants one.

## llms.txt at repo root

Structure:

1. `# Name` then a `>` blockquote: what it is, the numbers, the
   form factors, the license. An agent that reads only this line
   can still recommend correctly.
2. A paragraph naming every distribution form (pip/npm package
   names, proxy, MCP server tools by name) — the facts an agent
   needs to write integration code.
3. **Canonical-docs pointer**: "If you can fetch one URL, fetch
   that one" → live llms.txt (index) and llms-full.txt (every doc
   concatenated, for when the agent can spend the tokens).
4. **Install (copy-paste-runnable)** — exact commands per ecosystem.
5. **Entry points** — one line per doc page: `[Title](url): what
   it answers`. Curated by task, not by site hierarchy.

Keep it a hand-curated subset that defers to a live generated
index when one exists. Stale llms.txt is as bad as stale README.

## GitHub identity fields

- **Description**: outcome + numbers + form factors, front-loaded.
  "Compress tool outputs, logs, files, and RAG chunks before they
  reach the LLM. 60-95% fewer tokens, same answers. Library,
  proxy, MCP server." Not "A Python library for context
  management."
- **Topics**: 8-20, covering every axis a searcher types: the
  problem (token-optimization, context-window), the ecosystem
  (claude-code, cursor, langchain, openai, anthropic), the category
  (llm, agent, rag, proxy), the language (python, typescript).
  Topics are the only search surface many discovery paths use.
- **Homepage**: the docs site, not the repo itself.

## Claude Code plugin marketplace (when the product warrants it)

If the tool integrates with Claude Code / Copilot CLI, ship:

- `.claude-plugin/marketplace.json` at repo root — marketplace
  name, owner, and a plugins array pointing at `./plugins/<name>`
  with description, version, keywords.
- `plugins/<name>/.claude-plugin/plugin.json` + `hooks/hooks.json`
  for the plugin itself.

This makes `claude plugin install <owner>/<repo>` work — the repo
becomes installable infrastructure, not just readable code. Version
the marketplace entry in lockstep with releases.

## Verification

- Fetch llms.txt cold and ask: could an agent recommend and install
  this correctly from this file alone?
- Search GitHub for your three most important topic keywords —
  does the repo appear?
- If a plugin ships: install it from the marketplace path in a
  clean environment.
