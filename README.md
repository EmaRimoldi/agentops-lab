# Agent Workflow

[![Tests](https://github.com/EmaRimoldi/agent-workflow/actions/workflows/tests.yml/badge.svg)](https://github.com/EmaRimoldi/agent-workflow/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-workflow%20evaluation-111827)

Build N Claude Code agents, run them safely, and measure whether they actually beat a single agent.

![Agent Workflow demo](docs/assets/product/demo.gif)

Agent Workflow is an open-source harness for testing agent architectures before
you spend serious time, quota, or compute on them. Define one agent or N agents,
choose roles, models, memory mode, and CPU/GPU assignment, then compare
single-agent, parallel, shared-memory, swarm, and merge workflows on the same
task.

The framework runs locally. Live Claude Code capacity depends on your
subscription, provider quota, rate limits, and available compute.

## Quick Start

```bash
git clone https://github.com/EmaRimoldi/agent-workflow.git
cd agent-workflow
uv run agent-workflow doctor
```

Run a custom three-agent roster:

```bash
uv run agent-workflow parallel-shared --config configs/agent_roster_example.yaml
```

Run four similar workers from the CLI:

```bash
uv run agent-workflow parallel \
  --n-agents 4 \
  --model claude-haiku-4-5-20251001 \
  --cuda-devices 0,1,2,3 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --experiment-id four_agent_smoke
```

## Why This Exists

Spawning more agents is easy. Knowing whether parallelism, shared memory, or
coordination improved the result is the hard part.

Agent Workflow gives each agent an isolated workspace, keeps evaluation budgets
fixed, records trajectories and snapshots, and writes comparable reports. It is
designed for developers and researchers who want to experiment with agent teams
without needing frontier-lab infrastructure.

The built-in benchmark is `autoresearch/`: Claude Code agents edit a CIFAR-10
`train.py`, run evaluations, and try to reduce `val_bpb` validation loss. Lower
is better.

## Build Your Own Agent Team

Use YAML when each agent should have a different job:

```yaml
agents:
  use_shared_memory: true
  roster:
    - id: explorer
      role: broad architecture and hyperparameter search
      model: claude-sonnet-4-6
      temperature: 1.2  # search-style directive; Claude CLI has no native temperature flag
      cuda_device: "0"
    - id: optimizer
      role: conservative refinement of the best known candidate
      model: claude-haiku-4-5-20251001
      temperature: 0.3  # lower values ask the agent to make smaller edits
      cuda_device: "1"
```

`N` is intentionally not hardcoded. You can test as many agents as your
subscription, provider rate limits, evaluator concurrency, and local CPU/GPU
resources can support.

## How It Compares

| Approach | Spawn agents | Isolate workspaces | Configure N-agent rosters | Fixed-step evaluation | Evidence bundle |
|---|---:|---:|---:|---:|---:|
| Ad hoc Claude Code worktrees | Yes | Partial | Manual | No | No |
| Agent template collections | Yes | Varies | Varies | No | No |
| Observability dashboards | No | No | No | No | Yes |
| Agent Workflow | Yes | Yes | Yes | Yes | Yes |

Agent Workflow is not trying to replace Claude Code, agent templates, or
observability tools. It sits before scale-up: run the workflow, collect evidence,
then decide whether the more complex agent team is worth using.

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
- Configurable agent rosters for custom roles, models, temperatures, and device
  assignment.
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
- A public license still needs to be chosen before broad external adoption.

## More

- [`docs/index.html`](docs/index.html) - minimal GitHub Pages landing page
- [`docs/launch/`](docs/launch/) - launch checklist and copy
- [`experiments/README.md`](experiments/README.md) - experiment map
- [`experiments/catalog.md`](experiments/catalog.md) - compact evidence catalog
- [`docs/reviewer_checklist.md`](docs/reviewer_checklist.md) - what is built, proven, and still open
- [`docs/reproducibility.md`](docs/reproducibility.md) - local and Claude Code setup
- [`docs/product/claude_code_orchestration.md`](docs/product/claude_code_orchestration.md) - product wedge and Claude Code orchestration setup
