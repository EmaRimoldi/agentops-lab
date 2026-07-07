# Reproducibility Setup

This repo can be used at three levels:

1. Inspect checked-in study summaries, tables, and figures without running agents.
2. Run local smoke tests for the runtime and analysis code.
3. Re-run agent experiments with Claude Code and the AutoResearch substrate.

Historical study summaries are preserved evidence bundles. New agent runs will
not be bit-for-bit identical because Claude Code, model routing, service
versions, and stochastic agent decisions can change over time. For reviewer-grade
reruns, pin the model, use fixed-step evaluation, and keep the generated run
directory.

## Requirements

- Python 3.10 or newer.
- `uv`.
- Git.
- `claude` CLI from Claude Code, authenticated and available on `PATH`.
- Network access for the first CIFAR-10 data download.

Install Python dependencies:

```bash
uv sync --dev
```

Prepare the AutoResearch data:

```bash
cd autoresearch
uv run python prepare.py
cd ..
```

Run local smoke checks:

```bash
PYTHONPATH=src python -m pytest tests -q
PYTHONPATH=src python -m agentops_lab.cli --help
```

## Claude Code Setup

AgentOps Lab invokes Claude Code headlessly through the `claude` binary. The
current runner builds commands in this shape:

```bash
claude \
  --print \
  --output-format json \
  --dangerously-skip-permissions \
  --model <model> \
  --system-prompt <system-prompt> \
  "<turn message>"
```

The exact call site is `src/agentops_lab/agents/claude_agent_runner.py`.

Install Claude Code using Anthropic's current setup instructions:

- Official setup docs: <https://code.claude.com/docs/en/setup>
- CLI reference: <https://code.claude.com/docs/en/cli-reference>

Common install paths as of July 2026:

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# macOS with Homebrew stable channel
brew install --cask claude-code
```

Verify the install and auth state:

```bash
claude --version
claude doctor
claude auth status
```

If not authenticated, run:

```bash
claude auth login
```

## Safety Boundary

The runtime uses `--dangerously-skip-permissions` because experiments need
unattended file edits and shell commands inside isolated agent workspaces. Do not
run reviewer experiments from a directory containing secrets, production config,
or unrelated personal files.

Recommended practice:

- Run from a clean clone or disposable worktree.
- Keep `.env` local and never commit credentials.
- Review generated `runs/` artifacts before sharing.
- Do not grant Claude Code access to parent directories that are not part of the
  experiment.

## Minimal Agent Smoke Run

After local tests succeed and Claude Code is authenticated, start with a short run:

```bash
uv run agentops single-long \
  --config configs/experiment.yaml \
  --time-budget 10 \
  --train-budget 120 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --experiment-id smoke_single_long
```

For a matched parallel run:

```bash
uv run agentops parallel \
  --config configs/experiment.yaml \
  --time-budget 10 \
  --train-budget 120 \
  --n-agents 2 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --experiment-id smoke_parallel
```

For shared-memory parallel mode:

```bash
uv run agentops parallel-shared \
  --config configs/experiment.yaml \
  --time-budget 10 \
  --train-budget 120 \
  --n-agents 2 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --experiment-id smoke_parallel_shared
```

The swarm command currently has a separate surface:

```bash
uv run agentops swarm --blackboard-dir /tmp/agentops-blackboard
uv run agentops swarm --run --config configs/experiment.yaml --time-budget 10 --train-budget 120 --n-agents 2
```

## Reviewer-Grade Settings

Use these settings when the output will support a claim:

- `--train-max-steps 1170` so the evaluator is fixed-step rather than
  time-based.
- `--serialized-evaluator` when multiple agents share a machine.
- A pinned Claude model in `configs/experiment.yaml`.
- A pre-registered `--target-val-bpb` when computing certified hitting time.
- A clean `--experiment-id` that names the study and date.

Example:

```bash
uv run agentops parallel \
  --config configs/experiment.yaml \
  --time-budget 30 \
  --train-budget 300 \
  --n-agents 2 \
  --train-max-steps 1170 \
  --serialized-evaluator \
  --target-val-bpb 0.824 \
  --success-confidence 0.80 \
  --experiment-id study06_parallel_d01
```

## Output To Preserve

Agent runs write under `runs/` by default. Preserve at least:

- `config.json`
- per-agent `logs/`
- `results/trajectory.jsonl`
- `results/results.tsv`
- `results/training_runs.jsonl`
- `results/snapshots/`
- aggregate reports

These files are what make later certified-time, diversity, and decomposition
analysis auditable.
