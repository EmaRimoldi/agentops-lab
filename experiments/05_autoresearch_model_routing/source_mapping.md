# Source Mapping

| Original source | New location | Status | Reason |
| --- | --- | --- | --- |
| `autoresearch/campaigns/h20_delta005_20260505/accounting/` | `results/accounting/` | preserved | Processed result tables and JSON reports. |
| `autoresearch/paper_figures/current/` | `results/figures/` | preserved | Existing figure outputs associated with processed results. |
| `autoresearch/campaigns/h20_delta005_20260505/config_snapshot/` | `source/config_snapshot/` | preserved | Captures configs and prompts used by the source campaign. |
| `autoresearch/campaigns/h20_delta005_20260505/README.md` | `source/campaign_README.md` | preserved | Source campaign description and caveats. |
| `autoresearch/scripts/reproduce_main_figures_from_processed.py` | `source/scripts/reproduce_main_figures_from_processed.py` | preserved | Figure regeneration helper from processed JSON. |
| `autoresearch/scripts/make_neurips2026_artifact.py` | `source/scripts/make_neurips2026_artifact.py` | preserved | Reference export script; not wired into Agent Workflow yet. |
| `autoresearch/campaigns/h20_delta005_20260505/runs/` | not imported | excluded | Raw live-run tree is large and environment-bound. |
| `autoresearch/campaigns/h20_delta005_20260505/runs_balanced_n30/` | not imported | excluded | The inspected tree contained broken absolute symlinks. |
| `Archive/stateful_query_engine/` | not imported | excluded | Archived benchmark only; no preserved result bundle found. |
