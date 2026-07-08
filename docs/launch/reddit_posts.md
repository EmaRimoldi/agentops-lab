# Reddit Drafts

Use these only where they fit the community. Do not cross-post the same text
unchanged everywhere.

## r/programming

```text
I built an open-source harness for evaluating Claude Code agent workflows.

The problem I am trying to solve: spawning more agents is now easy, but it is
hard to tell whether parallelism, shared memory, or coordination actually
improved the result.

Agent Workflow lets you define one agent or N agents, run them in isolated
workspaces, keep evaluation fixed-step, and preserve configs/logs/trajectories
for later review.

Repo:
https://github.com/EmaRimoldi/agent-workflow

I would appreciate feedback on the CLI/API surface and what evidence you would
want before trusting a multi-agent coding workflow.
```

## r/MachineLearning

```text
I built Agent Workflow, an open-source evaluation harness for Claude Code
agent teams.

The checked-in benchmark is an AutoResearch task where agents edit a CIFAR-10
training file and try to reduce validation bits-per-byte. The current strongest
signal is a memory ablation: shared memory did not solve the task, but it made
exploratory agents less destructive on this benchmark.

The repo includes fixed-step evaluation, agent trajectories, snapshots, logs,
and experiment summaries.

Repo:
https://github.com/EmaRimoldi/agent-workflow

I am interested in feedback on the evaluation protocol and whether this is a
useful substrate for reproducible agent-workflow experiments.
```

## r/ClaudeAI or agent-specific communities

```text
I built a small open-source harness for testing Claude Code agent teams:

- define one agent or N agents
- assign roles/models/memory modes/devices
- run isolated workers
- compare single, parallel, shared-memory, swarm, and merge workflows

Repo:
https://github.com/EmaRimoldi/agent-workflow

I would love feedback from people using Claude Code worktrees or subagents in
real projects.
```
