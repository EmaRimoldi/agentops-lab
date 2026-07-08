# Imported From NeurIPS_2026

This note records the transfer scope from:

```text
engaging:/home/erimoldi/openclaw_remote/projects/NeurIPS_2026
```

The import is intentionally selective. Agent Workflow remains the canonical
repository; the NeurIPS workspace is treated as a source of processed results,
smoke evidence, and scaffold material.

## Imported

| Destination | Imported material |
| --- | --- |
| `05_autoresearch_model_routing/` | Processed AutoResearch accounting results, paper figures, config snapshot, campaign README, and figure/export helper scripts. |
| `06_humaneval_decomposition_cost/` | HumanEval smoke progress notes, diagnostics, artifacts, metrics, real-smoke logs, prompts, oracles, runners, profile, block config, and smoke subset inputs. |
| `07_swebench_experimental_scaffold/` | Neutral SWE-bench study scaffold, fixed 100-instance input slice, prompts, configs, and orchestration implementation code. |

## Excluded

| Source material | Reason |
| --- | --- |
| `Archive/stateful_query_engine/` | Archived benchmark only; no preserved result bundle was found during audit. |
| AutoResearch raw `runs/` | Large, environment-bound live-run tree. |
| AutoResearch `runs_balanced_n30/` | The inspected workspace contained broken absolute symlinks. |
| SWE-bench historical result studies | Results intentionally not transferred in this phase. |
| SWE-bench generated `runs/`, `evaluations/`, `slurm/` | Generated run output; scaffold import only. |
| `paper_overleaf/` | Paper submodule, not part of the product repository import. |
| `tmp/`, cache folders, egg-info, cluster logs | Local/generated artifacts. |
