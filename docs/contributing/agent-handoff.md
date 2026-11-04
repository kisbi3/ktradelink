# Agent work assignment and handoff

Keep the collaboration record on GitHub, not in agent-local chat history or a
shared continuously edited progress file. Post short status updates as Issue
or PR comments when assigning work, after major independent commits, and at
handoff. **One owner per topic branch**; other agents can review without push.

## Assignment (Issue or PR comment)

```text
Owner: ChatGPT | Claude Code | named contributor
Issue / PR: #...
Base main SHA: <40 hex>
Branch: feat/... (or review-only)
Scope / files: ...
Out of scope: ...
Pending decision or approval: ...
```

## Handoff (Issue or PR comment)

```text
Agent: ChatGPT | Claude Code
Issue / PR: #...
Branch / HEAD: ... / <40 hex>
Completed: ...
Evidence and publisher version/date: ...
Local tests actually run: ...
GitHub CI on exact SHA: links or pending
Unverified / blockers: ...
Next owner and concrete next steps: ...
Merge authorized? No, unless maintainer explicitly approved
```

Independent review should name a **fixed SHA**, give an Approved/Changes
requested verdict, severity/file/line/reproducible findings and explicitly
state any unverified platform or upstream behavior. Record future work on an
Issue rather than modifying a reviewed PR only for notes. A PR comment or
review does not change the SHA; a branch commit ordinarily does.
