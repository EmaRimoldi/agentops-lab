# Reviewer Checklist

This checklist is for a technical reviewer who has only a few minutes and wants
to know whether Agent Workflow Evaluation Lab is real, inspectable, and honest about its limits.

## Product Clarity

| Question | Where to verify | Status |
|---|---|---|
| What is this? | `README.md` | Benchmark harness for comparing AI-agent workflow modes on one controlled ML task. |
| What concrete task does it run? | `autoresearch/README.md`, `autoresearch/train.py` | Agents optimize CIFAR-10 validation loss by editing one training script. |
| What is the user-facing surface? | `src/agentops_lab/cli.py`, `README.md` | One CLI: `agentops`. |
| What should a reviewer read first? | `docs/demo_script.md`, `docs/demo_walkthrough.md` | Short demo path and evidence path are explicit. |

## Built System

| Capability | Where to verify | Status |
|---|---|---|
| Single-agent and parallel modes | `src/agentops_lab/modes/`, `src/agentops_lab/launcher.py` | Implemented. |
| Shared memory / blackboard | `src/agentops_lab/communication/`, `src/agentops_lab/swarm/` | Implemented and tested. |
| Claude Code runner | `src/agentops_lab/agents/claude_agent_runner.py` | Implemented; requires local Claude Code auth for live runs. |
| Certified hitting-time analysis | `src/agentops_lab/instrumentation/certified_time.py` | Implemented and tested. |
| Diversity metrics | `src/agentops_lab/analysis/diversity.py` | Implemented and tested. |
| Snapshot and reasoning traces | `src/agentops_lab/instrumentation/` | Implemented and tested. |
| Baseline calibration | `src/agentops_lab/baseline_calibration.py` | Implemented and tested. |

## Evidence

| Claim | Evidence | Status |
|---|---|---|
| The benchmark starting model was calibrated before agent claims. | `experiments/01_baseline/README.md` | 161 controlled evaluations; 1170-update runs are the decision evidence. |
| Evaluation protocol confounds are documented. | `experiments/02_evaluation_protocol_calibration/README.md` | Fixed-step determinism and fixed-time compute contention are both covered. |
| Shared memory can reduce destructive exploration in this substrate. | `experiments/03_agent_memory_ablation/README.md` | `T07` beats `T06` on best and mean `val_bpb`, with `p < 0.001`. |

## Reproducibility

| Check | Command or file | Status |
|---|---|---|
| Install dependencies | `uv sync --dev` | Documented. |
| Run tests | `PYTHONPATH=src python -m pytest tests -q` | Passing locally. |
| Inspect CLI | `PYTHONPATH=src python -m agentops_lab.cli --help` | Passing locally. |
| Prepare benchmark data | `docs/reproducibility.md` | Documented. |
| Run live agent experiments | `docs/reproducibility.md` | Requires Claude Code and isolated workspace. |

## Honest Limits

- This is not a general-purpose agent benchmark yet.
- The current empirical result is strongest for one substrate and one trial
  comparison, not every agent workflow.
- Historical live-agent runs are not bit-for-bit reproducible because external
  model services and agent choices can change.
- The BP theory is not presented as fully validated.
- No production deployment story is claimed yet; the repo is an evaluation lab.

## Next Stronger Proof Points

1. Replicate the `T06`/`T07` result across multiple seeds and model families.
2. Run the calibrated `width30_lr_low` benchmark with fixed-step, logged settings.
3. Add a lightweight hosted or recorded demo generated from a fresh run.
4. Add CI for tests and public-surface smoke checks.
5. Choose and publish an explicit license before asking external users to adopt
   the repo.
