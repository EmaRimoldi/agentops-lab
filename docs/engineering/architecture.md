# AgentOps Lab Architecture

AgentOps Lab exposes one runtime package, `agentops_lab`. The architecture is
split between experiment modes, coordination primitives, instrumentation,
evaluation tooling, and curated experiment evidence.

## Canonical Runtime Shape

```text
agentops CLI
  -> modes.parallel       -> agentops_lab.launcher.main_parallel
  -> parallel-shared      -> agentops_lab.launcher.main_parallel_shared
  -> modes.single_long    -> agentops_lab.launcher.main_single_long
  -> single-memory        -> agentops_lab.launcher.main_single_memory
  -> modes.merge          -> agentops_lab.merger.MergeOrchestrator
  -> modes.swarm          -> blackboard surface and swarm runtime
  -> certified-time       -> agentops_lab.instrumentation.certified_time
  -> baseline-calibration -> agentops_lab.baseline_calibration

agentops_lab.communication
  -> SharedMemory blackboard
  -> coordinator helpers

agentops_lab.analysis
  -> H_prior / H_post diversity metrics

agentops_lab.instrumentation
  -> snapshotting
  -> reasoning traces
  -> certified time
```

## Configuration

There is one canonical config surface:

```python
from agentops_lab.config import AgentConfig, ExperimentConfig
```

`AgentConfig` and `ExperimentConfig` live directly in `agentops_lab.config`.

## Orchestration

There is one canonical orchestrator surface:

```python
from agentops_lab.orchestrator import Orchestrator
```

The orchestrator owns process spawning, git worktree isolation, worker
integration, output collection, and report generation.

## Modes

| Mode | Module | Current integration status |
|---|---|---|
| `parallel` | `agentops_lab.modes.parallel` | Independent agents running concurrently |
| `parallel-shared` | `agentops_lab.launcher.main_parallel_shared` | Parallel agents with shared-memory coordination |
| `single_long` | `agentops_lab.modes.single_long` | Single-agent long-budget baseline |
| `single-memory` | `agentops_lab.launcher.main_single_memory` | Single-agent baseline with external memory |
| `merge` | `agentops_lab.modes.merge` | Post-hoc merge over candidate outputs |
| `swarm` | `agentops_lab.modes.swarm` | Shared-blackboard swarm runtime |

## Integrated Components

### Blackboard Communication

`src/agentops_lab/communication/blackboard.py` provides:

- append-only JSONL shared memory
- file locking via `fcntl`
- claim/dedup/release flow
- best-result sidecar
- context filtering for "other agents" reads

### Swarm Coordinator

`src/agentops_lab/communication/coordinator.py` imports the canonical
blackboard module and exposes local coordination helpers for shared-memory
agent workflows.

### Diversity Metrics

`src/agentops_lab/analysis/diversity.py` consolidates H_prior/H_post-style
analysis. Lightweight trajectory DTW is dependency-free; embedding and
weight-space metrics import heavy ML dependencies lazily.

### Instrumentation

`src/agentops_lab/instrumentation/` consolidates:

- snapshotting
- reasoning traces
- certified-time analysis

## Output And Reporting

The reporting pipeline lives under `src/agentops_lab/outputs/` plus mode-level
collector and reporter calls. Merge and swarm workflows write through the same
summary schema where possible.
