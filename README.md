# Agent Workflow

Agent Workflow tells teams whether a more complex AI-agent workflow is worth the
extra cost.

It gives Claude Code a reproducible way to spawn isolated sub-agents, run the
same task in parallel, and compare whether memory, swarm coordination, or merge
synthesis actually improved the result.

![Agent Workflow experiment map](docs/assets/experiments/experiment-map.png)

## Why It Matters

AI-agent teams often add parallelism, memory, or swarm coordination before they
know whether those features improve results. Agent Workflow gives them a way to
measure that tradeoff before trusting agents with expensive or long-running work.

The built-in benchmark is `autoresearch/`: agents edit a CIFAR-10 `train.py`,
run evaluations, and try to reduce `val_bpb` validation loss. Lower is better.

## Current Signal

The strongest result so far is from the memory ablation experiment:

| Condition | Attempts | Best `val_bpb` | Mean `val_bpb` |
|---|---:|---:|---:|
| Exploratory search, no memory | 21 | 0.933 | 1.816 |
| Exploratory search, shared memory | 41 | 0.914 | 1.049 |

The narrow takeaway: shared memory did not solve the task, but it made
exploratory agents much less destructive on this benchmark.

## Evidence

| Evidence | What it proves | Start here |
|---|---|---|
| Baseline calibration | The starting task is neither trivial nor impossible. | [`experiments/01_baseline/`](experiments/01_baseline/) |
| Evaluation protocol | Fixed-step deterministic evaluation avoids hardware-dependent conclusions. | [`experiments/02_evaluation_protocol_calibration/`](experiments/02_evaluation_protocol_calibration/) |
| Memory ablation | Shared memory can stabilize exploratory agents in this substrate. | [`experiments/03_agent_memory_ablation/`](experiments/03_agent_memory_ablation/) |
| Swarm baseline | Historical blackboard runs are promising context for richer coordination. | [`experiments/04_swarm_baselines/`](experiments/04_swarm_baselines/) |

## Quick Demo

```bash
uv sync --dev
uv run agent-workflow doctor
PYTHONPATH=src python -m pytest tests -q
PYTHONPATH=src python -m agent_workflow.cli --help
```

For the shortest guided walkthrough, read [`docs/demo_script.md`](docs/demo_script.md).
For the full evidence path, read [`docs/demo_walkthrough.md`](docs/demo_walkthrough.md).

## CLI

```bash
uv run agent-workflow --help
uv run agent-workflow parallel --help
uv run agent-workflow parallel-shared --help
uv run agent-workflow single-long --help
uv run agent-workflow single-memory --help
uv run agent-workflow swarm --help
uv run agent-workflow merge --help
uv run agent-workflow certified-time --help
uv run agent-workflow baseline-calibration --help
uv run agent-workflow doctor
```

Live agent runs require Claude Code authentication and a clean workspace. See
[`docs/reproducibility.md`](docs/reproducibility.md).

## What Is Included

- A runnable `agent-workflow` CLI.
- Claude Code project instructions, sub-agent templates, and a preflight
  `doctor` command.
- The controlled `autoresearch/` benchmark task.
- Execution modes for single-agent, parallel, shared-memory, swarm, and merge
  workflows.
- Shared-memory/blackboard primitives, certified-time analysis, diversity
  metrics, snapshots, reasoning traces, and reporting utilities.
- Curated experiment summaries, tables, and figures.

## Limits

- This is not a general benchmark for all agent tasks.
- The current strongest evidence is one controlled memory-ablation comparison.
- Historical live-agent runs are not bit-for-bit reproducible because model
  services and agent decisions can change over time.

## More

- [`experiments/README.md`](experiments/README.md) - experiment map
- [`experiments/catalog.md`](experiments/catalog.md) - compact evidence catalog
- [`docs/reviewer_checklist.md`](docs/reviewer_checklist.md) - what is built, proven, and still open
- [`docs/reproducibility.md`](docs/reproducibility.md) - local and Claude Code setup
- [`docs/product/claude_code_orchestration.md`](docs/product/claude_code_orchestration.md) - product wedge and Claude Code orchestration setup
