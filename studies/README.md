# Studies

This directory is the empirical spine of AgentOps Lab. Each study should be read
with the same rhythm:

1. What question was being tested?
2. What was actually run?
3. What did the run show?
4. What caveat or failure did it expose?
5. Which file should a reviewer read first?

The public tree keeps curated summaries, result tables, and figures. Raw run
directories, transient agent workspaces, and large local logs are intentionally
left out.

## Vocabulary

- **Study**: a complete evidence bundle under `studies/`.
- **Pilot**: an early feasibility study used to build instrumentation or expose
  design problems.
- **Probe**: one configuration inside the probe ablation matrix. Labels such as
  `P11` and `P12` are retained because they identify exact experimental cells.
- **Wave**: an execution batch inside a study. It is scheduling metadata, not a
  public milestone.
- **Reviewer-grade run**: a run that uses fixed-step evaluation, preserved logs,
  and a pre-registered success threshold.

## Reading Order

Read the studies in this order if you want the cleanest narrative:

1. [`baseline_headroom/`](baseline_headroom/) - current starting model calibration.
2. [`bp_probe_ablation/`](bp_probe_ablation/) - strongest current agentic signal.
3. [`calibration_design/`](calibration_design/) - deterministic evaluator and
   design audit that motivated the probe redesign.
4. [`theory_validation/`](theory_validation/) - theorem, estimator, and protocol
   audit.
5. [`bp_implementation/`](bp_implementation/) - first implementation study and
   instrumentation pilot.
6. [`swarm_baselines/`](swarm_baselines/) - historical swarm context.

## Study Map

### `baseline_headroom/`

**Status**: active starting model calibration.

**Question**: which `autoresearch/train.py` should every future agent workflow
start from?

**What was run**: 161 controlled non-agentic evaluations across baseline/edit
panels at fixed evaluator lengths, including the selected 1170-update screen.

**Main result**: the selected starting model is "width 30, lower learning
rate" (internal ID `width30_lr_low`): `val_bpb = 0.841354`, with future agent
target `target_val_bpb = 0.824`. It preserves multiple useful improvement
categories while keeping negative controls.

**Caveat**: This is not an agent result. It chooses the common starting point so
later agent comparisons are fair.

**Read first**:
[`baseline_headroom/README.md`](baseline_headroom/README.md).

### `bp_probe_ablation/`

**Status**: active signal-detection study.

**Question**: With the known confounds controlled, do the BP terms produce a
measurable empirical pattern?

**What was run**: 16 executed probes, 293 valid training runs, sequential
execution to remove CPU contention, and a matrix varying parallelism,
temperature diversity, shared memory, private memory, seeding, and budget.

**Main result**: The clearest signal is shared memory as variance reduction.
P12, the high-temperature shared-memory probe, beat P11 high-temperature
exploration without memory: best `val_bpb = 0.914` vs `0.934`, mean `1.049` vs
`1.816`, Mann-Whitney `p < 0.001`.

**Caveat**: This is one replicate per probe, so it is a probing study rather
than a confirmatory benchmark. It also exposed that the task ceiling was still
tight: only 1.9 percent of non-baseline runs beat baseline.

**Read first**:
[`bp_probe_ablation/results/probe_ablation_summary.md`](bp_probe_ablation/results/probe_ablation_summary.md).

### `calibration_design/`

**Status**: superseded by `bp_probe_ablation/`, but still important.

**Question**: Can the evaluator be made deterministic, and is the memory/no
memory contrast large enough to justify a full 2x2 study?

**What was run**: deterministic fixed-step evaluation, five baseline
verification runs, and 5 replicates each of `d00` and `d10`.

**Main result**: Five unmodified baseline runs produced identical
`val_bpb = 0.811222`, proving the evaluator could remove training noise. The
`d00` vs `d10` calibration was measurable, but the effect went the wrong way:
memory was worse on best-of-rep (`Cohen's d = 0.66` against d10).

**Caveat**: The study found design problems rather than a final result:
run-count thresholds, memory anchoring, training-time confounds, and a task
ceiling. Those findings directly motivated the probe ablation study.

**Read first**:
[`calibration_design/results/calibration_design_summary.md`](calibration_design/results/calibration_design_summary.md).

### `theory_validation/`

**Status**: theory and protocol audit, not an empirical success claim.

**Question**: Does the BP decomposition theorem and its estimators survive a
close audit against the pilot evidence?

**What was run**: formal theorem review, estimator refactor, mode-label
coverage audit, repeated incumbent evaluations, Jensen-gap checks, verifier
noise analysis, and context-pressure feasibility analysis.

**Main result**: The original claim was too broad. The current defensible
position is a narrower single-axis theorem with explicit assumptions and a
Jensen remainder. The protocol is cleaner, but the empirical validation remains
insufficient.

**Caveat**: The retained PDFs are source theory artifacts. Intermediate text
extractions and stale TeX were removed because they duplicated the PDFs and made
the reading path unclear.

**Read first**:
[`theory_validation/results/README.md`](theory_validation/results/README.md).

### `bp_implementation/`

**Status**: archived first study.

**Question**: Can a 2x2 agent experiment be instrumented end-to-end, and can the
BP decomposition be measured on real LLM-driven AutoResearch runs?

**What was run**: an early 2x2 pilot over single, memory, parallel, and
parallel-shared modes; 3 reps per cell; token and wall-clock accounting;
mode-labeling; decomposition estimates; trajectory plots.

**Main result**: The infrastructure worked and produced the first evidence
bundle, but the estimators were too brittle and the task/noise setup was not
strong enough for a rigorous claim.

**Caveat**: Treat this as historical implementation evidence. It explains why
the later deterministic evaluator, baseline calibration, and probe ablation were
needed.

**Read first**:
[`bp_implementation/results/implementation_pilot_summary.md`](bp_implementation/results/implementation_pilot_summary.md).

### `swarm_baselines/`

**Status**: historical context.

**Question**: How did earlier blackboard-style swarm coordination behave before
the current AgentOps Lab package was unified?

**What was run**: archived analyses of two-agent swarm runs, model comparisons,
and swarm-vs-parallelisation comparisons from the earlier swarm codebase.

**Main result**: The artifacts are useful for understanding the blackboard
coordination design: shared claims, pull-best behavior, cross-agent influence,
and model comparison under a historical task setup.

**Caveat**: These are not normalized `d00` / `d10` / `d01` / `d11` rows for the
current BP decomposition. They are context for the swarm implementation and
should not be mixed directly with the current calibrated studies.

**Read first**:
[`swarm_baselines/results/README.md`](swarm_baselines/results/README.md).
