# Demo Walkthrough

This repository is easiest to read as an evidence trail, not as a UI demo.
The concrete task is AutoResearch: agents edit one CIFAR-10 training script,
run evaluations, and try to reduce validation loss.

## The Task

`autoresearch/` is the benchmark substrate used by the runtime:

- `autoresearch/train.py` is the file agents are allowed to edit.
- `autoresearch/prepare.py` owns data loading and evaluation.
- `val_bpb` is the reported validation-loss proxy; lower is better.
- Agent modes differ only in how search is coordinated: single long run,
  parallel independent runs, private/shared memory, swarm blackboard, or merge.

This gives the repo a concrete experimental question:

> Which agent workflow finds better `train.py` edits per unit of wall time,
> cost, and coordination overhead?

## Fastest Reading Path

1. Read the selected benchmark baseline:
   [`studies/baseline_headroom/README.md`](../studies/baseline_headroom/README.md).

   The current baseline was chosen after 161 controlled non-agentic evaluations.
   The selected starting model is "width 30, lower learning rate" (internal ID
   `width30_lr_low`), with `val_bpb = 0.841354` and future agent target
   `target_val_bpb = 0.824`.

2. Read the strongest agent-workflow finding:
   [`studies/bp_probe_ablation/results/probe_ablation_summary.md`](../studies/bp_probe_ablation/results/probe_ablation_summary.md).

   The most informative comparison is P11 vs P12:

   | Probe | Meaning | Runs | Best `val_bpb` | Mean `val_bpb` |
   |---|---|---:|---:|---:|
   | P11 | high-temperature exploration, no memory | 21 | 0.934 | 1.816 |
   | P12 | high-temperature exploration with shared memory | 41 | 0.914 | 1.049 |

   The interpretation is that exploration without routing correction behaves
   like a random walk, while shared memory reduces catastrophic repeats.

3. Read why the task had to be calibrated:
   [`studies/calibration_design/results/calibration_design_summary.md`](../studies/calibration_design/results/calibration_design_summary.md).

   This study made evaluation deterministic. Five consecutive baseline runs
   produced identical `val_bpb = 0.811222`, which means differences can be
   attributed to agent edits rather than training noise.

4. Read the earliest pilot only as historical context:
   [`studies/bp_implementation/results/implementation_pilot_summary.md`](../studies/bp_implementation/results/implementation_pilot_summary.md).

   This study built the instrumentation, but it also exposed estimator and task
   design weaknesses that later studies fixed.

## What To Look At Visually

The most useful result figures are:

- [`studies/baseline_headroom/results/figures/figure-04-recommended-baseline-detail.png`](../studies/baseline_headroom/results/figures/figure-04-recommended-baseline-detail.png)
- [`studies/bp_probe_ablation/results/ablation__bp-4term-probing__active/figures/design_audit/figure-04-task-ceiling.png`](../studies/bp_probe_ablation/results/ablation__bp-4term-probing__active/figures/design_audit/figure-04-task-ceiling.png)
- [`studies/calibration_design/results/calibration__2x2-diversity-memory__superseded/figures/figure-01-main-comparison.png`](../studies/calibration_design/results/calibration__2x2-diversity-memory__superseded/figures/figure-01-main-comparison.png)

## Runnable Surface

The current public CLI is:

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

The repository does not include raw private run logs or local datasets. Curated
summaries and figures are checked in under `studies/`; new full runs write to
`runs/`.
