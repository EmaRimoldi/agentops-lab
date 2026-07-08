# Show HN Draft

Title:

```text
Show HN: Agent Workflow - build N Claude Code agents and measure if they beat one
```

Body:

```text
Hi HN,

I built Agent Workflow, an open-source harness for evaluating Claude Code agent
workflows before scaling them.

The problem: it is now easy to spawn more agents, but hard to know whether
parallelism, shared memory, or swarm coordination actually improved the result.

Agent Workflow lets you:

- define one agent or N agents with roles, models, memory mode, and CPU/GPU assignment
- run isolated Claude Code workers against the same task
- keep evaluation fixed-step so hardware contention does not distort the comparison
- preserve configs, logs, trajectories, snapshots, and reports

The checked-in benchmark is an AutoResearch task where agents edit a CIFAR-10
training file and try to reduce validation bits-per-byte. The strongest current
signal: shared memory did not solve the task, but it made exploratory agents
much less destructive on this benchmark.

Quick start:

git clone https://github.com/EmaRimoldi/agent-workflow.git
cd agent-workflow
uv run agent-workflow doctor

Repo:
https://github.com/EmaRimoldi/agent-workflow

I would be especially interested in feedback from people running Claude Code,
agent worktrees, or multi-agent coding workflows in practice.
```
