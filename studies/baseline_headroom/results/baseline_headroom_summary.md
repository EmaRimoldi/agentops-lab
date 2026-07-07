# Starting Model Calibration

**Status**: Active
**Period**: April 14, 2026
**Objective**: choose one controlled `autoresearch/train.py` starting point before comparing agent workflows.

## Task Context

Future agents will edit `autoresearch/train.py`, run the training evaluator,
and try to lower validation loss. The logs call this metric `val_bpb`; lower is
better.

The target for later agent runs is `val_bpb <= 0.824`.

## Research Question

The next agent studies need a shared starting point. If it is too weak, almost
any edit wins. If it is already too strong, no edit works and the comparison
mostly measures noise.

**Can we choose a starting `train.py` where several distinct edit families can
improve validation loss, without making the task too easy?**

This study is deliberately non-agentic: a script applied predefined edits, not
an AI agent choosing what to try.

## What Changed

This study added a controlled starting-point calibration tool:

- fixed-step evaluator support with `AUTOSEARCH_MAX_STEPS`;
- isolated workspaces for every baseline/edit trial;
- starting-point and edit panels covering optimizer, learning rate, schedule, capacity, regularization, and batch size;
- JSON/CSV/Markdown outputs for calibration screens;
- cost and hitting-time instrumentation from the preceding protocol work.

The working `autoresearch/train.py` starting point was updated to the selected candidate:

```text
DEPTH = 3
BASE_CHANNELS = 30
FC_HIDDEN = 128
OPTIMIZER = adam
LEARNING_RATE = 5e-4
WEIGHT_DECAY = 1e-4
DROPOUT_RATE = 0.0
USE_LR_SCHEDULE = False
BATCH_SIZE = 128
AUTOSEARCH_MAX_STEPS = 1170
```

## Experiments

| screen | training updates | trials | purpose |
| --- | ---: | ---: | --- |
| `baseline_headroom_calibration_fixed1170` | 1170 | 43 | initial screen over plausible starting points |
| `baseline_headroom_calibration_extended_targeted_fixed1170` | 1170 | 38 | broader model / optimizer / regularization screen |
| `baseline_refinement_custom_fixed585` | 585 | 40 | shorter-step refinement screen |
| `baseline_refinement_custom_fixed1170` | 1170 | 40 | intermediate-width / head / mild-dropout refinement |

Total controlled evaluations summarized here: **161**.

Trial counts differ because each screen tested a different candidate/edit panel,
and no-op edits were skipped. Compare normalized edit win rate
(`successful_edits / tested_edits`), not raw trial count.

## Key Figures

![Task definition](figures/figure-01-baseline-screen-overview.png)

**Figure 1** explains the task. There is no separate `Q` metric in this report:
the quality score is validation loss, `val_bpb`, and lower is better.

![Training update choice](figures/figure-02-gate-diagnostics.png)

**Figure 2** explains why the study uses 1170 optimizer updates. At 585 updates,
edits won too often, so that screen was mostly useful for debugging.

![Starting point choice](figures/figure-03-category-improvement-heatmap.png)

**Figure 3** compares candidate starting points. The selected one is in the
middle: not too hard, not too easy.

![Recommended baseline detail](figures/figure-04-recommended-baseline-detail.png)

**Figure 4** shows the seven edits tested on the selected starting point. Green
bars beat the future target; red bars are useful failures.

## Decision

Selected starting point:

```text
starting_model = width 30, lower learning rate
internal_id = width30_lr_low
run = refinement_fixed1170
starting val_bpb = 0.841354
target val_bpb = 0.824
```

Edits that beat the target:

| category | best trial | best val_bpb | improvement |
| --- | --- | ---: | ---: |
| data_batch | `width30_lr_low__data_batch__batch256` | 0.784812 | 0.056542 |
| normalization_capacity | `width30_lr_low__normalization_capacity__width32` | 0.823338 | 0.018016 |
| optimizer_lr | `width30_lr_low__optimizer_lr__lr_1p5e3` | 0.800896 | 0.040458 |

Useful failed edits:

| trial | category | val_bpb | delta vs baseline |
| --- | --- | ---: | ---: |
| `width30_lr_low__scheduler__schedule_on` | scheduler | 0.845433 | -0.004079 |

## Candidate Comparison

| starting point | screen | training updates | starting val_bpb | edits that worked | winning categories | target loss |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| narrow_lr_low | default_fixed1170 | 1170 | 0.864447 | 4/8 | data_batch, normalization_capacity, optimizer_lr | 0.832826 |
| sgd_baseline | extended_fixed1170 | 1170 | 0.884132 | 3/6 | data_batch, optimizer_lr, regularization | 0.872697 |
| width30_lr_low | refinement_fixed1170 | 1170 | 0.841354 | 4/7 | data_batch, normalization_capacity, optimizer_lr | 0.823338 |
| mild_dropout_no_schedule | extended_fixed1170 | 1170 | 1.065839 | 4/7 | data_batch, optimizer_lr, optimizer_scheduler, regularization | 1.035120 |
| overregularized_lr_low | default_fixed1170 | 1170 | 0.966298 | 5/8 | data_batch, normalization_capacity, optimizer_lr, regularization | 0.899594 |
| no_batchnorm_lr_low | default_fixed1170 | 1170 | 1.078067 | 5/8 | data_batch, normalization_capacity, optimizer_lr | 0.963829 |
| fc96_lr_low | refinement_fixed1170 | 1170 | 0.851718 | 5/7 | data_batch, normalization_capacity, optimizer_lr | 0.834426 |
| dropout005_lr_low | refinement_fixed1170 | 1170 | 0.868005 | 5/7 | data_batch, optimizer_lr, regularization | 0.830335 |

## Why 1170 Updates

The 585-update screens were too easy: almost every reasonable edit won. That is
useful for debugging, but weak for comparing agent workflows. At 1170 updates,
the task remains learnable while retaining failed edits.

## Next Step

Run a small agent pilot on `width30_lr_low`:

```text
fixed-length evaluator
AUTOSEARCH_MAX_STEPS = 1170
serialized evaluator
target_val_bpb = 0.824
separate agent_deliberation_wall_time and evaluator_wall_time
true independent replicates
```

## Artifacts

- Summary table: `tables/baseline_summary.csv`
- Trial table: `tables/trial_results.csv`
- Machine-readable summary: `tables/baseline_headroom_summary.json`
- Legacy raw-table note: the `q3` column means the target loss implied by the
  third winning edit family. In prose, this summary calls the selected target
  `target_val_bpb`.
- Source calibration reports remain under `runs/baseline_*`.
