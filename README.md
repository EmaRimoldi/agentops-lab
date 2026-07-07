# AgentOps Lab

AgentOps Lab is a benchmark harness for measuring whether AI-agent workflows
actually improve search quality, cost, and auditability on a concrete ML
optimization task.

The built-in benchmark is `autoresearch/`: agents edit a CIFAR-10 `train.py`,
run evaluations, and try to reduce `val_bpb` (validation loss; lower is better).
The repo then compares whether the search works better as one long-running
agent, independent parallel agents, memory-augmented agents, a blackboard swarm,
or a post-hoc merge.

## 60-Second Review Path

If you are reviewing this repository quickly:

1. Read [`docs/demo_script.md`](docs/demo_script.md) for the short product demo.
2. Read [`docs/demo_walkthrough.md`](docs/demo_walkthrough.md) for the concrete
   result path.
3. Read [`docs/reviewer_checklist.md`](docs/reviewer_checklist.md) to verify
   what is built, what is evidence, and what is still open.
4. Use [`studies/README.md`](studies/README.md) for the study-by-study map.
5. Use [`docs/reproducibility.md`](docs/reproducibility.md) for local and
   Claude Code setup.

## What This Is For

Most agent demos answer "can an agent do the task?" AgentOps Lab asks whether a
workflow is worth running:

- Does parallelization improve quality, or only spend more tokens?
- When does swarm communication create signal instead of coordination overhead?
- Which workflow reaches a target quality threshold fastest?
- What is the cost to hit a reviewer-defined quality level?
- Are improvements caused by better search, better coordination, or evaluator
  noise?
- Can an agent run be replayed, inspected, and defended?

The narrow product wedge is AI-agent evaluation for teams that need to decide
whether a more complex agent workflow is worth the extra cost before trusting it
with long-running or expensive work.

## Concrete Evidence In This Repo

The checked-in `studies/` directory is the demo surface. It contains curated
summaries, figures, and result tables from agent-workflow experiments.

Key examples:

| Evidence | What it shows | Start here |
|---|---|---|
| Baseline headroom | 161 controlled non-agentic evaluations selected the starting `train.py`: validation loss `val_bpb = 0.841354`, future agent target `target_val_bpb = 0.824` | [`studies/baseline_headroom/README.md`](studies/baseline_headroom/README.md) |
| Shared memory effect | P12 shared-memory exploration found better and more stable results than P11 high-temperature exploration without memory: best `0.914` vs `0.934`, mean `1.049` vs `1.816` | [`studies/bp_probe_ablation/results/probe_ablation_summary.md`](studies/bp_probe_ablation/results/probe_ablation_summary.md) |
| Deterministic evaluator | Five baseline runs produced identical `val_bpb = 0.811222`, removing training noise as the main explanation | [`studies/calibration_design/results/calibration_design_summary.md`](studies/calibration_design/results/calibration_design_summary.md) |
| Early pilot | First 2x2 pilot built the instrumentation and exposed why the task and estimators needed redesign | [`studies/bp_implementation/results/implementation_pilot_summary.md`](studies/bp_implementation/results/implementation_pilot_summary.md) |

## What Works Today

- A runnable Python package and `agentops` CLI.
- Isolated AutoResearch workspaces where agents edit one controlled `train.py`.
- Execution modes for single-agent, parallel, shared-memory, swarm, and merge
  workflows.
- Blackboard/shared-memory primitives with tests.
- Certified-time, diversity, snapshotting, reasoning-trace, and calibration
  utilities.
- Curated study evidence with figures and result tables.

## What This Does Not Claim Yet

- It is not a general benchmark for all agent tasks.
- It does not claim the BP theory is fully empirically validated.
- It does not claim shared memory always helps; current evidence says it reduces
  harmful exploration in a specific probe.
- Historical runs are not bit-for-bit reproducible because model services and
  agent decisions can change over time.

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

## What Is `autoresearch/`?

`autoresearch/` is the benchmark task used by the agent runtime. It is not a
separate product.

- `autoresearch/train.py`: the file agents are allowed to modify.
- `autoresearch/prepare.py`: data loading and evaluation harness.
- `autoresearch/program.md`: task instructions given to agents.
- `val_bpb`: the validation-loss proxy parsed by the runtime.

The point of this substrate is controlled comparison: all modes optimize the
same file under the same evaluator, so differences can be attributed to the
agent workflow rather than to changing tasks.

## Repository Layout

```text
src/
  agentops_lab/              public package surface and CLI

docs/
  research/                     BP decomposition and experiment protocols
  engineering/                  architecture and runtime design
  evals/                        certified time, calibration, capacity docs
  demo_script.md                60-second demo narrative and evidence path
  demo_walkthrough.md           guided reading path through concrete results
  reviewer_checklist.md         what a reviewer can verify quickly
  reproducibility.md            local setup and Claude Code reproduction notes

studies/
  swarm_baselines/              blackboard coordination evidence
  bp_implementation/            BP substrate implementation evidence
  theory_validation/            theorem/protocol validation evidence
  calibration_design/           evaluator and design calibration evidence
  bp_probe_ablation/            BP four-term probing evidence
  baseline_headroom/            baseline headroom calibration evidence

autoresearch/
  CIFAR-10 train.py optimization task used by the agents

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
- [Reproducibility setup](docs/reproducibility.md)

## Repository Scope

AgentOps Lab keeps the runnable runtime, evaluation protocols, curated study
summaries, and AutoResearch substrate in one repository. Raw run logs, local
data, transient agent workspaces, and private process notes are intentionally
out of scope.
