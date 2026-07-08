# Agent Workflow Claude Code Guide

Agent Workflow is a measurement harness for Claude Code agent workflows. The
goal is to test whether a more complex workflow, such as parallel agents,
shared memory, swarm coordination, or merge synthesis, is worth the extra cost.

## Default Behavior

- Prefer read-only inspection unless the user explicitly asks for edits.
- Do not start live Claude Code agent experiments unless the user explicitly
  asks for a live run.
- Before any live run, execute `uv run agent-workflow doctor`.
- Use fixed-step evaluation for comparable claims:
  `--train-max-steps 1170 --serialized-evaluator`.
- Keep generated run artifacts under `runs/` and preserve `config.json`,
  logs, trajectory files, snapshots, and reports.

## Product Surface

- CLI: `uv run agent-workflow --help`
- Setup check: `uv run agent-workflow doctor`
- Single-agent baseline: `uv run agent-workflow single-long`
- Independent parallel agents: `uv run agent-workflow parallel`
- Shared-memory parallel agents: `uv run agent-workflow parallel-shared`
- Blackboard swarm: `uv run agent-workflow swarm`
- Post-run synthesis: `uv run agent-workflow merge`

## Safety Boundary

Live runs invoke the local `claude` binary and can edit files inside isolated
workspaces. Run them from a clean clone or disposable worktree, not from a
directory containing secrets or unrelated personal files.

Use the project subagents in `.claude/agents/` for planning, execution, and
analysis. They should report concise evidence and file paths rather than broad
claims.
