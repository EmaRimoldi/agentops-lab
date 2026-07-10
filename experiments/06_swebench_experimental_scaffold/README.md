# SWE-bench Experimental Scaffold

This bundle preserves the SWE-bench orchestration scaffold from `NeurIPS_2026`.
It intentionally does not transfer historical SWE-bench results.

## What Was Transferred

- Neutral 100-instance study inputs under `source/study/`.
- SWE-bench orchestration implementation code under
  `source/implementation/vao_swebench_orchestration/`.
- The source SWE-bench README as `source/swebench_README.md`.

## Source

Remote source repository:

```text
engaging:/home/erimoldi/openclaw_remote/projects/NeurIPS_2026
```

Primary source directories:

```text
swebench/studies/neutral_swebench_trial_100/
swebench/src/vao/swebench_orchestration/
```

## Scope

This is a scaffold for future SWE-bench work in Agent Workflow. It includes
configs, prompts, neutral worker definitions, a fixed 100-instance input slice,
and orchestration code. It does not include previous run outputs, evaluator
reports, Slurm logs, predictions, traces, or historical failure analyses.

The file `source/study/data/verified_100/instances_private_metadata.jsonl` is
preserved as bookkeeping metadata and must not be injected into solver prompts.

## What Is Not Included

- `swebench/studies/open_source_meta_loop_20260607/` result reports.
- `swebench/studies/codex_suite_100_vs_gpt55/`.
- `runs/`, `evaluations/`, and `slurm/` generated-output trees.
- Any resolved/unresolved SWE-bench result counts.

## Read First

- `source/study/README.md`
- `source/study/configs/swebench_meta_design_neutral.yaml`
- `source/implementation/vao_swebench_orchestration/prompt.py`
- `source/implementation/vao_swebench_orchestration/executor.py`
