# HumanEval Decomposition Cost

This bundle preserves a HumanEval mini-smoke experiment from `NeurIPS_2026`.
It studies a decomposed coding-task workflow and records the cost accounting
needed to compare that workflow with a single-agent baseline.

## What Was Transferred

- Progress and diagnostic notes under `source/`.
- Workflow artifacts under `artifacts/`.
- JSON metrics under `results/metrics/`.
- Real-smoke logs under `results/logs/`.
- The prompt, oracle, runner, block, profile, and smoke-data files needed to
  understand the experiment.

## Source

Remote source repository:

```text
engaging:/home/erimoldi/openclaw_remote/projects/NeurIPS_2026
```

Primary source directory:

```text
step1/
```

## Scope

The preserved run is a 9-instance HumanEval smoke test. The experiment decomposes
each coding task into nodes such as specification understanding, planning, test
generation, implementation, repair, and aggregation. The metric files preserve
pass/fail and cost-success accounting; this README does not interpret those
numbers as a general benchmark result.

## What Is Not Included

- Full HumanEval dataset copies.
- Scratch recovery files.
- Non-real or mock smoke logs except where metrics reference them.
- Cluster execution artifacts.

## Read First

- `source/PROGRESS.md`
- `source/DIAGNOSTIC.md`
- `results/metrics/step1_report_smoke_real.json`
- `artifacts/orchestration.md`
