# Source Mapping

| Original source | New location | Status | Reason |
| --- | --- | --- | --- |
| `autoresearch/campaigns/h20_delta005_20260505/accounting/` | `results/accounting/` | preserved | Processed result tables and JSON reports. |
| `autoresearch/paper_figures/current/` | `results/figures/` | preserved | Existing figure outputs associated with processed results. |
| `autoresearch/campaigns/h20_delta005_20260505/runs/worker_confirmation/*/{config_resolved.yaml,run_manifest.json,baseline_verification.json,interactive_initial_prompt.txt,interactive_session.json,evaluations.jsonl,run_summary.json}` | `raw/worker_confirmation/` | preserved | Minimal raw files for 250 available live runs. |
| `autoresearch/campaigns/h20_delta005_20260505/runs_balanced_n30/MANIFEST.csv` | `raw/manifests/balanced_n30_manifest.csv` | preserved | Balanced `n=30` mapping from cell/trial to source run path. |
| `autoresearch/campaigns/h20_delta005_20260505/config_snapshot/` | `source/config_snapshot/` | preserved | Captures configs and prompts used by the source campaign. |
| `autoresearch/campaigns/h20_delta005_20260505/README.md` | `source/campaign_README.md` | preserved | Source campaign description and caveats. |
| `autoresearch/scripts/reproduce_main_figures_from_processed.py` | `source/scripts/reproduce_main_figures_from_processed.py` | preserved | Figure regeneration helper from processed JSON. |
| `autoresearch/scripts/make_neurips2026_artifact.py` | `source/scripts/make_neurips2026_artifact.py` | preserved | Reference export script; not wired into Agent Workflow yet. |
| `distribution-aware-orchestration/autoresearch/benchmark/cifar10/` | `autoresearch/benchmark/cifar10/` | integrated | Live CIFAR-10 benchmark, workload templates, verifier wrapper, metadata, and source-validation logic needed to reproduce AutoResearch runs. |
| `distribution-aware-orchestration/autoresearch/analysis/` | `autoresearch/analysis/` | integrated | Pilot, threshold, routing, workload-accounting, and z-signal analysis modules needed to regenerate experiment accounting from future run directories. |
| `distribution-aware-orchestration/autoresearch/configs/` | `autoresearch/configs/` | integrated | Current H=20 AutoResearch configs using `gpt_5_3_codex`, `gpt_5_4`, and `gpt_5_4_mini`; these match the processed result worker aliases. |
| `distribution-aware-orchestration/autoresearch/prompts/` | `autoresearch/prompts/` | integrated | Canonical AutoResearch generation, router, and allocation-router prompts. |
| `distribution-aware-orchestration/autoresearch/scripts/` | `autoresearch/scripts/` | integrated | Plotting, artifact, Slurm, and campaign helper scripts. |
| `distribution-aware-orchestration/src/vao/` | `src/vao/` | integrated | Compatibility runtime used by the imported AutoResearch harness. Kept under its original namespace to avoid changing historical run code paths. |
| `distribution-aware-orchestration/configs/models.yaml` | `configs/models.yaml` | integrated | Backend alias catalog required by AutoResearch configs and tests. |
| `distribution-aware-orchestration/configs/profiles.yaml` | `configs/profiles.yaml` | integrated | Profile split catalog required by the compatibility runtime. |
| `distribution-aware-orchestration/tests/` | `tests/vao_runtime/` | integrated | Fast runtime tests for the compatibility layer. |
| `distribution-aware-orchestration/autoresearch/tests/` | `tests/autoresearch_reproduction/` | integrated | Fast AutoResearch benchmark tests. |
| `autoresearch/campaigns/h20_delta005_20260505/runs/worker_pilot/` | not imported | missing in source workspace | The balanced `n=30` manifest references 90 `worker_pilot` runs, but that directory was not present in the inspected remote workspace. |
| `autoresearch/campaigns/h20_delta005_20260505/runs/` full tree | not imported | excluded | Intermediate workspaces, verifier raw trees, proposed solutions, and cluster-bound artifacts are large and environment-bound. |
| `autoresearch/campaigns/h20_delta005_20260505/runs_balanced_n30/` symlink tree | not imported | excluded | The inspected tree contained broken absolute symlinks; the CSV manifest was preserved instead. |
| `Archive/stateful_query_engine/` | not imported | excluded | Archived benchmark only; no preserved result bundle found. |
| `distribution-aware-orchestration/autoresearch/legacy/` | not imported | excluded | Historical/debugging material, not part of the live AutoResearch reproduction surface. |
| `distribution-aware-orchestration/autoresearch/paper_figures/current/` | not imported | duplicate | All 78 figure files are byte-identical to `results/figures/`; only the Agent Workflow figure README is additional. |
