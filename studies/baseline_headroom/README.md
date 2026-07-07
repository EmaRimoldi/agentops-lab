# Baseline Headroom Study

**Status**: Active
**Period**: April 14, 2026
**Objective**: Find a healthy but non-trivial AutoResearch baseline before running the reviewer-grade BP 2x2.

## Short Version

**Task**: agents will edit `autoresearch/train.py`, run the training evaluator,
and try to lower validation loss. The evaluator reports `val_bpb`; lower is
better.

**Question**: which starting `train.py` should future agent runs optimize?

**What was run**: 161 controlled evaluator runs. These were non-agentic: a
script applied predefined edits, not an AI agent choosing what to try.

**Main result**: the selected starting model has `val_bpb = 0.841354`. It is
credible, but still improvable through batch size, learning rate, and model
capacity.

**Target for later agents**: `target_val_bpb = 0.824`. Older protocol notes call
this `q*`: it is just the validation-loss threshold an agent must beat.

**Caveat**: this study calibrates the task. It does not yet prove that agents
can solve it better than scripts or humans.

## Terms

- **Baseline / starting model**: the initial `train.py` that agents will edit.
- **`val_bpb`**: validation loss reported by the training script; lower is
  better. This is the main quality metric in this study.
- **`q*`**: older shorthand for the target validation loss. Here, `q* = 0.824`
  means `target_val_bpb = 0.824`.
- **Training update / step**: one optimizer gradient update inside
  `autoresearch/train.py`.
- **1170 training updates**: the evaluator length chosen for the benchmark. It
  is not a magic number: the shorter 585-update screen was too easy because
  nearly every reasonable edit improved validation loss.
- **Edit family**: a class of edits, such as batch size, learning rate, model
  capacity, schedule, or regularization.

## Research Question

The next agent studies need a task that is neither trivial nor saturated. If the
starting model is too weak, almost any edit wins. If it is too strong, no edit
works and the agent comparison measures noise.

This study asks:

**Can we choose a starting `train.py` where several distinct edit families can
improve validation loss, without making the task trivially easy?**

## Protocol

The calibration script did the following:

1. Create candidate starting versions of `autoresearch/train.py`.
2. For each candidate, run a fixed-length training evaluation.
3. Apply simple predefined edits, one at a time.
4. Re-run the evaluator and record whether validation loss improved.
5. Prefer a candidate where multiple edit families help, but not every edit
   wins.

The selected starting model uses:

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
| initial 1170-update screen | 1170 | 43 | broad scan over plausible starting models |
| extended 1170-update screen | 1170 | 38 | additional optimizer, regularization, and capacity checks |
| 585-update refinement | 585 | 40 | shorter training screen used as a stress test |
| 1170-update refinement | 1170 | 40 | final comparison among intermediate candidates |

Total controlled evaluations summarized here: **161**.

Trial counts differ because each screen tested a different candidate/edit panel,
and no-op edits were skipped. For cross-screen comparisons, use normalized edit
win rate (`successful_edits / tested_edits`) rather than raw trial count.

## Key Figures

![Baseline screen overview](results/figures/figure-01-baseline-screen-overview.png)

**Figure 1**: each dot is a candidate starting `train.py`. The x-axis shows the
normalized edit success rate; the y-axis shows starting validation loss. The
orange star is the chosen starting model.

![Gate diagnostics](results/figures/figure-02-gate-diagnostics.png)

**Figure 2**: 1170-update candidates ranked by normalized edit success rate.
The selected model is useful because 4 of 7 tested edits worked across 3 edit
families: enough headroom, but not a free win.

![Category improvement heatmap](results/figures/figure-03-category-improvement-heatmap.png)

**Figure 3**: which edit families helped which starting model. Green means an
edit family lowered validation loss; red means it hurt.

![Recommended baseline detail](results/figures/figure-04-recommended-baseline-detail.png)

**Figure 4**: the seven simple edits tested on the selected starting model.
Positive bars lower validation loss. The blue dashed line is the improvement
needed to beat `target_val_bpb = 0.824`.

![Presentation baseline choice](results/figures/figure-05-presentation-baseline-choice.png)

**Figure 5**: presentation version of the selection logic. It compares 1170-
update candidates by normalized edit success rate and number of edit families.

![Presentation width30 detail](results/figures/figure-06-presentation-width30-detail.png)

**Figure 6**: presentation version of the selected-baseline edit outcomes.

## Decision

Recommended baseline:

```text
starting_model = width 30, lower learning rate
internal_id = width30_lr_low
run = refinement_fixed1170
starting val_bpb = 0.841354
target_val_bpb = 0.824  # old shorthand: q*
```

Edits that beat the target:

| edit family | best edit | best val_bpb | improvement |
| --- | --- | ---: | ---: |
| Batch size | use batch size 256 | 0.784812 | 0.056542 |
| Learning rate / optimizer | raise learning rate to 0.0015 | 0.800896 | 0.040458 |
| Model capacity | make the model slightly wider | 0.823338 | 0.018016 |

Negative / near-negative controls:

| edit | family | val_bpb | effect |
| --- | --- | ---: | ---: |
| turn on learning-rate schedule | Schedule | 0.845433 | worse by 0.004079 |
| raise learning rate to 0.001 | Learning rate / optimizer | 0.847634 | worse by 0.006280 |
| switch optimizer to AdamW | Learning rate / optimizer | 0.878075 | worse by 0.036721 |

## Candidate Comparison Snapshot

| candidate | starting val_bpb | edits that worked | verdict |
| --- | ---: | ---: | --- |
| selected: width 30, lower learning rate | 0.841354 | 4/7 | chosen: credible but improvable |
| narrow model, low learning rate | 0.864447 | 4/8 | valid backup, but more obviously weakened |
| SGD optimizer | 0.884132 | 3/6 | useful diagnostic, less representative |
| weak regularization | 0.810496 | 1/6 | too strong/narrow; little headroom |
| width 28, low learning rate | 0.879400 | 7/7 | too easy |
| width 24, medium learning rate | 0.862439 | 7/7 | too easy |
| very small classifier head | 0.889742 | 7/7 | too easy |
| batch norm removed | 1.078067 | 5/8 | too obviously damaged |

## Why 1170 Updates

The 585-update screen created broad headroom, but almost every reasonable edit
won. That is useful for debugging, but weak for an agent benchmark.

At 1170 training updates, the task still has real improvements available, but
also keeps negative controls. That makes it a better benchmark for later claims
about agent search quality.

## Next Step

Run a small agentic pilot on `width30_lr_low` before the full 2x2:

```text
fixed-step evaluator
AUTOSEARCH_MAX_STEPS = 1170
serialized evaluator
target_val_bpb = 0.824
separate agent_deliberation_wall_time and evaluator_wall_time
true independent replicates
```

## Artifacts

- Summary table: `results/tables/baseline_summary.csv`
- Trial table: `results/tables/trial_results.csv`
- Machine-readable summary: `results/tables/baseline_headroom_summary.json`
- Legacy raw-table note: the `q3` column means the target loss implied by the
  third winning edit family. In prose, this README calls the selected threshold
  `target_val_bpb`.
- Source calibration reports remain under `runs/baseline_*`.
