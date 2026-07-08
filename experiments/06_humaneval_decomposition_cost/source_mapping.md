# Source Mapping

| Original source | New location | Status | Reason |
| --- | --- | --- | --- |
| `step1/PROGRESS.md` | `source/PROGRESS.md` | preserved | Main experiment log and milestone notes. |
| `DIAGNOSTIC.md` | `source/DIAGNOSTIC.md` | preserved | Cost-accounting and handoff diagnostic notes. |
| `step1/artifact/` | `artifacts/` | preserved | Workflow artifact, DAG candidate, and routing calibration. |
| `step1/metrics/*.json` | `results/metrics/` | preserved | Report and adaptation-curve outputs. |
| `step1/logs/*_smoke_real.jsonl` | `results/logs/` | preserved | Real-smoke traces used by the preserved metrics. |
| `step1/profile/` | `source/profile/` | preserved | Task profile used to build the smoke subset. |
| `step1/prompts/` | `source/prompts/` | preserved | Prompt templates for the decomposed workflow. |
| `step1/oracles/` | `source/oracles/` | preserved | Oracle/checking code used by the workflow. |
| `step1/runners/` | `source/runners/` | preserved | Runner code for reproduction and inspection. |
| `step1/blocks/` | `source/blocks/` | preserved | Node library configuration. |
| `step1/data/*smoke_stratified*` | `source/data/` | preserved | Smoke subset inputs only. |
| `step1/data/humaneval_public.jsonl` | not imported | excluded | Full dataset copy is not required for the preserved bundle. |
| `step1/data/humaneval_verifier.jsonl` | not imported | excluded | Full verifier dataset copy is not required for the preserved bundle. |
| `step1/logs/` other files | not imported | excluded | Scratch, mock, or recovery logs outside the selected real-smoke evidence. |
