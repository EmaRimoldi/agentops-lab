# Experiment Catalog

This catalog lists the experiment bundles currently preserved in the repository.
It separates completed evidence from historical context.

| Folder | Type | Approximate scale | Evidence preserved | Core claim supported | Main limitation |
| --- | --- | ---: | --- | --- | --- |
| [`01_baseline/`](01_baseline/) | calibration | 161 controlled evaluations | summary README, CSV/JSON tables, public figures | future agent workflows should start from the same calibrated `train.py` | not an agent experiment |
| [`02_evaluation_protocol_calibration/`](02_evaluation_protocol_calibration/) | methodology | evaluator determinism checks, CPU scaling at N=1/2/4/8, fixed-step pair benchmark | summary, archived evaluator appendix, raw tables, generated figures | comparisons must use fixed-step deterministic evaluation, not fixed wall-clock training budgets | CPU-only evidence for the contention component |
| [`03_agent_memory_ablation/`](03_agent_memory_ablation/) | agent workflow ablation | 11 valid trials, 247 training attempts | canonical README, trial table, statistical summary, public figures | shared memory stabilizes exploratory agents and reduces catastrophic regressions | one execution per trial |
| [`04_swarm_baselines/`](04_swarm_baselines/) | historical context | four preserved two-agent swarm model comparisons plus partial parallel baseline | summary, JSON/CSV tables, historical analysis figures, public figures | blackboard coordination was promising in earlier swarm experiments | raw swarm run directories not included |

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
5. The theoretical framing remains in `docs/research/`; it is supporting
   context, not a standalone experiment bundle in this public tree.
