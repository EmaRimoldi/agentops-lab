# Experiment Catalog

This catalog lists the experiment bundles currently preserved in the repository.
It separates completed evidence from historical context.

| Folder | Type | Approximate scale | Evidence preserved | Status / contents | Main limitation |
| --- | --- | ---: | --- | --- | --- |
| [`01_baseline/`](01_baseline/) | calibration | 161 controlled evaluations | summary README, CSV/JSON tables, public figures | future agent workflows should start from the same calibrated `train.py` | not an agent experiment |
| [`02_evaluation_protocol_calibration/`](02_evaluation_protocol_calibration/) | methodology | evaluator determinism checks, CPU scaling at N=1/2/4/8, fixed-step pair benchmark | summary, archived evaluator appendix, raw tables, generated figures | comparisons must use fixed-step deterministic evaluation, not fixed wall-clock training budgets | CPU-only evidence for the contention component |
| [`03_agent_memory_ablation/`](03_agent_memory_ablation/) | agent workflow ablation | 11 valid trials, 247 training attempts | canonical README, trial table, statistical summary, public figures | shared memory stabilizes exploratory agents and reduces catastrophic regressions | one execution per trial |
| [`04_swarm_baselines/`](04_swarm_baselines/) | historical context | four preserved two-agent swarm model comparisons plus partial parallel baseline | summary, JSON/CSV tables, historical analysis figures, public figures | blackboard coordination was promising in earlier swarm experiments | raw swarm run directories not included |
| [`05_autoresearch_model_routing/`](05_autoresearch_model_routing/) | imported processed results | 270 processed routing/accounting records | accounting CSV/JSON, figure outputs, config snapshot, source campaign README | imported from `NeurIPS_2026`; raw live-run tree excluded | source raw runs and balanced symlink tree are not included |
| [`06_humaneval_decomposition_cost/`](06_humaneval_decomposition_cost/) | imported smoke bundle | 9 HumanEval smoke instances | PROGRESS/DIAGNOSTIC notes, metrics JSON, real-smoke logs, prompts, oracles, runners, artifacts | imported decomposition-cost smoke bundle from `NeurIPS_2026` | not a full HumanEval run |
| [`07_swebench_experimental_scaffold/`](07_swebench_experimental_scaffold/) | scaffold | 100-instance input slice plus orchestration code | neutral study config, prompt templates, input slice, implementation code | scaffold only; no SWE-bench results transferred | not an evidence bundle yet |

## How To Read The Evidence

The strongest current experimental story is:

1. [`01_baseline/`](01_baseline/) chooses a fair starting task.
2. [`02_evaluation_protocol_calibration/`](02_evaluation_protocol_calibration/) explains
   why evaluator noise and hardware-dependent training budgets must be controlled.
3. [`03_agent_memory_ablation/`](03_agent_memory_ablation/) shows the current agentic
   signal: exploratory search without memory degrades; shared memory reduces the
   damage and finds occasional improvements.
4. [`04_swarm_baselines/`](04_swarm_baselines/) gives historical context for a richer
   blackboard implementation.
5. [`05_autoresearch_model_routing/`](05_autoresearch_model_routing/) and
   [`06_humaneval_decomposition_cost/`](06_humaneval_decomposition_cost/) preserve
   imported processed results from the NeurIPS workspace.
6. [`07_swebench_experimental_scaffold/`](07_swebench_experimental_scaffold/)
   preserves future SWE-bench scaffold material without importing historical
   results.
7. The theoretical framing remains in `docs/research/`; it is supporting
   context, not a standalone experiment bundle in this public tree.
