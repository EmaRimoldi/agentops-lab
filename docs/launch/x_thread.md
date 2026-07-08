# X Thread Draft

```text
1/ I built Agent Workflow: an open-source harness for testing Claude Code agent teams before scaling them.

The question is simple:

Do N agents actually beat one?
```

```text
2/ Spawning agents is easy now.

Measuring whether parallelism, shared memory, or swarm coordination improved the result is the harder part.
```

```text
3/ Agent Workflow lets you define a custom roster:

- explorer
- optimizer
- regularizer
- any N your quota/compute supports

Each agent can have its own role, model, memory mode, and device assignment.
```

```text
4/ The harness gives each agent an isolated workspace, runs fixed-step evaluation, and preserves configs, logs, trajectories, snapshots, metrics, and reports.
```

```text
5/ The checked-in benchmark is AutoResearch:

Claude Code agents edit a CIFAR-10 train.py and try to reduce validation bits-per-byte.

Lower val_bpb is better.
```

```text
6/ Current strongest signal:

Shared memory did not solve the task, but it made exploratory agents less destructive.

No memory: best 0.933, mean 1.816
Shared memory: best 0.914, mean 1.049
```

```text
7/ Quick start:

git clone https://github.com/EmaRimoldi/agent-workflow.git
cd agent-workflow
uv run agent-workflow doctor
```

```text
8/ Repo:

https://github.com/EmaRimoldi/agent-workflow

I am looking for feedback from people building Claude Code, agent worktree, and multi-agent coding workflows.
```
