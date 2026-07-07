# Theory Validation Study

This folder audits the mathematical frame behind AgentOps Lab. It is not a
claim that the theory has been empirically validated.

Current status:

> cleaner theory, upgraded estimators, insufficient empirical validation

## What The Study Did

The study started from an AutoResearch BP theory note and asked whether the
theorem, estimators, and pilot evidence were strong enough to support the agent
workflow claims.

It performed:

- a formal audit of the original theorem;
- a refactor to a narrower single-axis theorem with explicit assumptions;
- protocol upgrades for incumbent re-evaluation and provenance logging;
- corrected mode-labeling and decomposition estimators;
- repeated incumbent evaluations across the four pilot cells;
- Jensen-gap checks for token and wall-clock cost;
- verifier-noise and context-pressure analyses.

## Reading Order

Shortest path to the current conclusion:

1. [`theory_validation_summary.md`](theory_validation_summary.md)
2. [`analysis/final_verdict.md`](analysis/final_verdict.md)
3. [`analysis/reanalysis_summary.md`](analysis/reanalysis_summary.md)
4. [`analysis/formal_theory_audit.md`](analysis/formal_theory_audit.md)
5. [`analysis/estimator_design.md`](analysis/estimator_design.md)

Read the PDFs only if you are auditing the theory source material:

1. [`theory/BP.pdf`](theory/BP.pdf)
2. [`theory/autoresearch_bp.pdf`](theory/autoresearch_bp.pdf)

## Theory Files

- `theory/BP.pdf`: the Beneventano-Poggio source paper used as the theoretical
  reference point for the decomposition.
- `theory/autoresearch_bp.pdf`: the project-specific AutoResearch BP theory
  note that this study audited.

Plain-text PDF extractions and stale TeX intermediates were removed from the
public tree. They duplicated the PDFs, were not the canonical source of truth,
and made the theory folder look more authoritative than it was.

## Folder Structure

### `analysis/`

Human-readable audit and follow-up analysis:

- `final_verdict.md`
- `reanalysis_summary.md`
- `formal_theory_audit.md`
- `theorem_refactor_summary.md`
- `validation_strategy.md`
- `protocol_compliance_audit.md`
- `protocol_upgrade_spec.md`
- `protocol_upgrade_smoke_check.md`
- `estimator_design.md`
- `estimator_validation_note.md`
- `experiment_01_replicated_means.md`
- `experiment_02_cost_variance.md`
- `experiment_03_context_sweep.md`

Machine-readable outputs:

- `noise_assay_interpretation.json`
- `context_pressure_metrics.json`
- `mode_label_coverage.json`
- `protocol_compliance.json`
- `estimator_validation_rep1.json`
- `corrected_decomposition_rep1.json`
- `corrected_decomposition_rep2.json`
- `corrected_decomposition_rep3.json`

### `artifacts/`

Original pilot artifacts preserved for provenance:

- `pilot_summary.md`
- `pilot_raw_data.json`
- `decomposition_rep1.json`
- `decomposition_rep2.json`
- `decomposition_rep3.json`
- `pilot_mapping.json`

### `figures/`

Reviewer-facing figures for replicated means, Jensen gap, corrected
decomposition, noise assay, and context pressure.

## Main Finding

The original AutoResearch BP note was too strong. The defensible result is a
narrower single-axis BP reduction with explicit extra assumptions and a Jensen
remainder. The estimator and protocol layers are now much cleaner, but repeated
incumbent evaluations still show overlapping uncertainty across the main cells,
wall-clock Jensen gaps are large enough to matter, and the pilot does not supply
enough accepted-mode support for stable `phi`, `G`, and `epsilon` estimates.

This is useful research infrastructure, not a finished theorem-to-benchmark
validation.
