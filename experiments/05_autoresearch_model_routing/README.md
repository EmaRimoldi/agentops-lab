# AutoResearch Model Routing

This bundle preserves processed results from the `NeurIPS_2026` AutoResearch
campaign. It is an imported evidence bundle, not a raw run archive.

## What Was Transferred

- Processed accounting tables and JSON reports under `results/accounting/`.
- Paper-facing figures under `results/figures/`.
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

## What Is Not Included

- Raw `runs/` directories.
- `runs_balanced_n30/` symlinks.
- Cluster logs and Slurm output.
- Provider transcripts or live-agent workspaces.

Those files are either large, environment-bound, or known to contain broken
absolute symlinks in the inspected workspace.

## Read First

- `results/accounting/threeworker_balanced_n30_frontier_summary.csv`
- `results/accounting/threeworker_threshold_summary.csv`
- `results/accounting/threeworker_router_gain_summary.csv`
- `source/campaign_README.md`
