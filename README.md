# AgentOps Lab

AgentOps Lab is a research-grade framework for measuring when AI agent systems
should run as a single agent, parallel agents, coordinated swarms, or post-hoc
merge workflows.

The goal is practical: make agentic workflows auditable before they are trusted
with expensive or long-running work. The repo focuses on reliability,
evaluation, cost, wall-clock time, coordination, and reproducibility.

## Why This Exists

Most agent demos answer "can an agent do the task?" AgentOps Lab asks harder
operational questions:

- Does parallelization improve quality, or only spend more tokens?
- When does swarm communication create signal instead of coordination overhead?
- Which workflow reaches a target quality threshold fastest?
- What is the cost to hit a reviewer-defined quality level?
- Are improvements caused by better search, better coordination, or evaluator
  noise?
- Can an agent run be replayed, inspected, and defended?

## Core Capabilities

| Capability | What it provides |
|---|---|
| Mode comparison | `single_long`, `parallel`, `swarm`, and `merge` execution surfaces |
| Swarm coordination | Shared JSONL blackboard, claims, deduplication, global-best tracking |
| Certified time | `T_wall` and `T_cost` hitting-time analysis from run logs |
| Baseline headroom | Calibration before confirmatory studies so easy baselines do not dominate |
| Diversity metrics | `H_prior` / `H_post` style prompt, trajectory, and weight-space diversity |
| Reproducible substrate | CPU-oriented AutoResearch task with deterministic fixed-step evaluation |
| Operational traces | Snapshots, reasoning traces, training run logs, collector/reporting pipeline |

## Repository Layout

```text
src/
  agentops_lab/              public package surface and CLI

docs/
  research/                     BP decomposition and experiment protocols
  engineering/                  architecture and workflow design
  evals/                        certified time, calibration, capacity docs
  positioning/                  public narrative for project framing

studies/
  swarm_baselines/              blackboard coordination evidence
  bp_implementation/            BP substrate implementation evidence
  theory_validation/            theorem/protocol validation evidence
  calibration_design/           evaluator and design calibration evidence
  bp_probe_ablation/            BP four-term probing evidence
  baseline_headroom/            baseline headroom calibration evidence

autoresearch/
  deterministic CPU optimization substrate

configs/
  runnable experiment configs

scripts/
  analysis utilities and workflow helpers

tests/
  unit, integration, and public-surface smoke tests
```

## Install

```bash
uv sync --dev
```

Run tests:

```bash
PYTHONPATH=src python -m pytest tests -q
```

## CLI

Canonical public surface:

```bash
uv run agentops --help
uv run agentops parallel --help
uv run agentops parallel-shared --help
uv run agentops single-long --help
uv run agentops single-memory --help
uv run agentops swarm --help
uv run agentops merge --help
uv run agentops certified-time --help
uv run agentops baseline-calibration --help
```

## Public Package Surface

The preferred import path is `agentops_lab`.

```text
agentops_lab/
  cli.py
  config.py
  orchestrator.py
  communication/
    blackboard.py
    coordinator.py
  analysis/
    diversity.py
  instrumentation/
    snapshotting.py
    reasoning_trace.py
    certified_time.py
  modes/
    parallel.py
    single_long.py
    swarm.py
    merge.py
```

The runtime, evaluation tools, reporting pipeline, and public imports live under
one package: `agentops_lab`.

## Research Frame

AgentOps Lab evaluates agentic systems through a decomposition of improvement:

```math
\Delta = \log(\kappa_0 / \kappa) + \phi + G - \epsilon
```

where the terms separate cost/search efficiency, parallel or coordination
effects, gains, and estimator/error penalties. The current empirical substrate
uses a deterministic CPU optimization task with fixed-step evaluation, mode
labeling, calibration gates, and post-hoc decomposition analysis.

Start here:

- [Architecture](docs/engineering/architecture.md)
- [Reviewer-grade evaluation protocol](docs/evals/reviewer_grade_protocol.md)
- [Baseline headroom calibration](docs/evals/baseline_headroom_calibration.md)
- [Experiment protocol](docs/research/experiment_protocol.md)

## Repository Scope

AgentOps Lab keeps the runnable runtime, evaluation protocols, curated study
summaries, and AutoResearch substrate in one repository. Raw run logs, local
data, transient agent workspaces, and private process notes are intentionally
out of scope.
