# START-HERE — project resumption protocol [PROJECT NAME]

> You are a new assistant session and you are to continue this project?
> Read the WHOLE file and follow the steps in order. The project owner
> knows this file and directs you with the words: "start from
> START-HERE.md".
>
> Last updated: [DATE] · reason: [WHAT CHANGED]

## About the project in three sentences

1. [Project goal and audience.]
2. [State: what works, what is built, where the technical documentation lives.]
3. [Project memory: where the conversation log and the work log are.]

## Repo map

| path | contents |
|---|---|
| `START-HERE.md` | this file — the starting point of a new session |
| [FOLDER/] | [description] |
| [FOLDER/] | [description] |

## Resumption protocol (step by step)

**Step 0 — access.** The repo is [private/public]. The user pastes a
PAT (permissions for this repo). [Where to get a token / where to keep
it.] Secrets NEVER inside file contents.

**Step 1 — context.** Read in order: the work log (the banner at the
top!), the conversation-log map, the indicated sections. Key
non-negotiable decisions: [3–5 project decisions]. The same ritual
applies after a mid-session context compression (a shortened
conversation = a new session: repeat this step from the top).

**Step 2 — environment recovery.** [Environment: what to initialize,
which commands, how to verify it works. Include the lesson:
environments sometimes fall apart partially between sessions — do not
panic, the files in the repo are the source of truth.]

**Step 3 — protocols.** After every task: a work-log entry. After
important changes: a full background save. [Commands.]

**Step 4 — unbreakable rules.**
- secrets only in the environment, never in the repo,
- [platform dependencies: what works only here, what works everywhere],
- language and tone with the user: [e.g. direct, concrete, no jargon].

## What is currently waiting

- [Task 1 — status.]
- [Task 2 — status.]

## For the Human (when you read this alone)

- Starting a new session — write exactly this:
  *"We are continuing the project [NAME]. Everything is in the repo
  [USER/REPO] on GitHub — start from START-HERE.md in the root. PAT:
  [paste token]."*
- Lost the PAT? GitHub → Settings → Developer settings → Personal
  access tokens → generate a new one (revoke the old). The key is the
  GitHub account, not any single token.
- The assistant suddenly "forgets" arrangements or changes form (e.g.
  switches to formal address after always being direct)? That is most
  often a symptom of context compression, not ill will. Say: "refresh
  yourself from the repo (start file → work log)" — the start ritual
  will be repeated and the context will return.
- [What is deliberately NOT archived and why — e.g. a database that
  rebuilds automatically.]
