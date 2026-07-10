# AutoResearch Model Routing

This bundle preserves processed results from the `NeurIPS_2026` AutoResearch
campaign. It is an imported evidence bundle, not a raw run archive.

## What Was Transferred

- Processed accounting tables and JSON reports under `results/accounting/`.
- Paper-facing figures under `results/figures/`.
- Minimal raw run files under `raw/`.
- The submitted campaign README and config snapshot under `source/`.
- Figure/artifact helper scripts under `source/scripts/`.

## Source

Remote source repository:

```text
engaging:/home/erimoldi/openclaw_remote/projects/NeurIPS_2026
```

Primary source campaign:

```text
autoresearch/campaigns/h20_delta005_20260505/
```

## Scope

The imported campaign records AutoResearch CIFAR-10 workload-routing outputs for
three workload families and three worker aliases. The preserved processed file
`results/accounting/threeworker_balanced_n30_sensitivity.json` records
`run_count = 270` and `threshold = 0.05`.

## Parameters

- Task: CIFAR-10 training-script optimization. An agent proposes structured
  edits to `solution.py`; the harness applies the edit, runs the verifier, and
  records validation loss.
- Workloads: `mlp_flat`, `cnn_compact`, `resnet_micro`.
- Workers: `gpt_5_3_codex`, `gpt_5_4`, `gpt_5_4_mini`.
- Run horizon: 20 proposal/evaluation steps per run.
- Success threshold: `0.05`, meaning at least 5% relative validation-loss
  improvement versus the unmodified baseline:

  ```text
  relative_improvement = (baseline_loss - best_loss) / baseline_loss
  success = relative_improvement >= 0.05
  ```

- `tau_step`: the first proposal step at which the run reaches the success
  threshold. A lower `tau_step` means the worker found a useful edit earlier.

## Reader-Facing Metrics

Use these metrics when presenting this experiment:

- `success_count` / `success_rate`: how often a worker reaches the 5%
  validation-loss improvement threshold within 20 steps.
- `mean_tau`: average first successful step among successful runs.
- `mean_final_relative_improvement`: average best validation-loss improvement
  by the end of the 20-step run.
- `mean_elapsed_wall_minutes`: observed wall-clock runtime.
- `mean_total_tokens_millions`: token usage reported by the run accounting.

Do not use the imported composite deployment-cost field for product or research
claims in this repository. It is retained only inside source accounting files
for provenance.

## Main Observed Results

- The balanced `n=30` table contains 270 processed records:
  `3 workloads x 3 workers x 30 trials`.
- At threshold `0.05`, the processed table records 263 successes out of 270
  records.
- The raw bundle covers 180 of the 270 balanced records: trials `011`-`030`
  for every workload/worker cell. The missing 90 records are trials `001`-`010`
  in every cell, which point to `worker_pilot` sources that were not present in
  the inspected cluster workspace.

## What Is Not Included

- Full raw `runs/` directories.
- `runs_balanced_n30/` symlink tree.
- Cluster logs and Slurm output.
- Provider transcripts or live-agent workspaces.

The repository keeps a minimal raw bundle instead. The full run tree is larger
and environment-bound, and `runs_balanced_n30/` contained broken absolute
symlinks in the inspected workspace.

Raw coverage is documented in `raw/README.md` and
`raw/manifests/raw_import_summary.json`.

## Cluster Audit For Missing Raw Traces

Checked on `login007` under:

```text
/home/erimoldi/openclaw_remote/projects/NeurIPS_2026/autoresearch/campaigns/h20_delta005_20260505
```

Findings:

- `runs/worker_pilot/` is not present.
- `manifests/worker_pilot_nonspark_tasks.tsv` and
  `manifests/worker_pilot_gpt54mini_tasks.tsv` are present.
- `runs_balanced_n30/MANIFEST.csv` contains 90 references to `worker_pilot`.
- The corresponding `runs_balanced_n30` entries are broken symlinks in the
  inspected workspace.

## Read First

- `results/accounting/threeworker_balanced_n30_frontier_summary.csv`
- `results/accounting/threeworker_threshold_summary.csv`
- `results/accounting/threeworker_router_gain_summary.csv`
- `raw/manifests/raw_run_inventory.csv`
- `source/campaign_README.md`
- `results/figures/README.md`
