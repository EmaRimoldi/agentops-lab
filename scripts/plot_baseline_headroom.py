"""Generate readable figures for the baseline-headroom study.

The figures are presentation artifacts. They intentionally avoid dense point
labels and internal candidate IDs where possible; the raw IDs remain available
in the CSV/JSON tables under the study directory.
"""

from __future__ import annotations

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "baseline_headroom"
TABLES = STUDY / "results" / "tables"
FIGURES = STUDY / "results" / "figures"

SELECTED_RUN = "refinement_fixed1170"
SELECTED_BASELINE = "width30_lr_low"
TARGET_LOSS = 0.824


BASELINE_LABELS = {
    "lr_low_no_schedule": "low learning rate,\nno schedule",
    "lr_very_low_no_schedule": "very low learning rate",
    "narrow_lr_low": "narrow model,\nlow learning rate",
    "no_batchnorm_lr_low": "batch norm removed",
    "overregularized_lr_low": "too much regularization",
    "mild_dropout_no_schedule": "mild dropout,\nno schedule",
    "sgd_baseline": "SGD optimizer",
    "shallow_lr_low": "shallower model",
    "small_fc_lr_low": "very small classifier head",
    "weak_regularization_no_schedule": "weak regularization",
    "dropout005_lr_low": "dropout 0.05,\nlow learning rate",
    "fc96_lr_low": "classifier head 96",
    "width24_lr_mid": "width 24,\nmedium learning rate",
    "width28_lr_low": "width 28,\nlow learning rate",
    "width30_lr_low": "selected: width 30,\nlow learning rate",
}

CATEGORY_LABELS = {
    "data_batch": "Batch size",
    "normalization_capacity": "Model capacity",
    "optimizer_lr": "Learning rate /\noptimizer",
    "optimizer_scheduler": "Schedule",
    "scheduler": "Schedule",
    "regularization": "Regularization",
}

EDIT_LABELS = {
    "lr_1e3": "Raise learning rate to 0.001",
    "lr_1p5e3": "Raise learning rate to 0.0015",
    "adamw_1e3": "Switch optimizer to AdamW",
    "schedule_on": "Turn on learning-rate schedule",
    "cosine_schedule_on": "Turn on learning-rate schedule",
    "width32": "Make model slightly wider",
    "batch192": "Use batch size 192",
    "batch256": "Use batch size 256",
}


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": "#111827",
            "axes.titlecolor": "#111827",
            "axes.grid": True,
            "grid.color": "#e5e7eb",
            "grid.linewidth": 0.8,
            "font.size": 12,
            "axes.titlesize": 18,
            "axes.labelsize": 13,
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "legend.frameon": False,
        }
    )


def _load() -> tuple[pd.DataFrame, pd.DataFrame]:
    baselines = pd.read_csv(TABLES / "baseline_summary.csv")
    trials = pd.read_csv(TABLES / "trial_results.csv")

    numeric_baseline_cols = [
        "fixed_steps",
        "baseline_val_bpb",
        "raw_wins",
        "edit_count",
        "raw_win_rate",
        "category_count",
        "q3",
    ]
    for col in numeric_baseline_cols:
        baselines[col] = pd.to_numeric(baselines[col], errors="coerce")

    for col in ["fixed_steps", "val_bpb", "total_seconds"]:
        trials[col] = pd.to_numeric(trials[col], errors="coerce")
    trials["is_baseline"] = trials["is_baseline"].astype(str).str.lower().eq("true")
    return baselines, trials


def _baseline_label(value: str) -> str:
    return BASELINE_LABELS.get(value, value.replace("_", " "))


def _short_edit_label(trial_id: str) -> str:
    suffix = trial_id.split("__")[-1]
    return EDIT_LABELS.get(suffix, suffix.replace("_", " "))


def _wrap_labels(labels: list[str], width: int = 18) -> list[str]:
    return ["\n".join(textwrap.wrap(label, width=width)) for label in labels]


def _selected_trials(baselines: pd.DataFrame, trials: pd.DataFrame) -> tuple[float, pd.DataFrame]:
    selected_row = baselines[
        (baselines["run_id"] == SELECTED_RUN)
        & (baselines["baseline_id"] == SELECTED_BASELINE)
    ].iloc[0]
    base_loss = float(selected_row["baseline_val_bpb"])
    selected = trials[
        (trials["run_id"] == SELECTED_RUN)
        & (trials["baseline_id"] == SELECTED_BASELINE)
        & (~trials["is_baseline"])
        & (trials["status"] == "success")
    ].copy()
    selected["improvement"] = base_loss - selected["val_bpb"]
    selected["label"] = selected["id"].map(_short_edit_label)
    selected["category_label"] = selected["category"].map(
        lambda value: CATEGORY_LABELS.get(value, value.replace("_", " "))
    )
    selected = selected.sort_values("improvement", ascending=True)
    return base_loss, selected


def figure_01_candidate_map(baselines: pd.DataFrame) -> None:
    data = baselines.copy()
    data["is_selected"] = (
        (data["run_id"] == SELECTED_RUN) & (data["baseline_id"] == SELECTED_BASELINE)
    )
    data["step_label"] = np.where(data["fixed_steps"] == 585, "585 updates", "1170 updates")
    colors = np.where(data["fixed_steps"] == 585, "#94a3b8", "#2563eb")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(
        data["raw_win_rate"],
        data["baseline_val_bpb"],
        s=70 + data["category_count"].fillna(0) * 45,
        c=colors,
        alpha=0.75,
        linewidths=0.8,
        edgecolors="white",
    )

    selected = data[data["is_selected"]].iloc[0]
    ax.scatter(
        [selected["raw_win_rate"]],
        [selected["baseline_val_bpb"]],
        marker="*",
        s=420,
        color="#f97316",
        edgecolors="#7c2d12",
        linewidths=1.2,
        zorder=5,
        label="selected starting point",
    )

    ax.axhline(TARGET_LOSS, color="#0f766e", linestyle="--", linewidth=1.5, label="future target loss")
    ax.axvspan(0.0, 0.2, color="#fee2e2", alpha=0.45)
    ax.axvspan(0.85, 1.02, color="#fef3c7", alpha=0.55)
    ax.text(0.04, 0.97, "too few edits work", transform=ax.transAxes, va="top", color="#991b1b")
    ax.text(0.79, 0.97, "too easy", transform=ax.transAxes, va="top", color="#92400e")

    ax.set_title("Baseline calibration: choose a useful starting point")
    ax.set_xlabel("Share of tested edits that improved the starting model")
    ax.set_ylabel("Starting validation loss, val_bpb (lower is better)")
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(data["baseline_val_bpb"].max() + 0.04, data["baseline_val_bpb"].min() - 0.04)

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#2563eb", markersize=9, label="1170 training updates"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#94a3b8", markersize=9, label="585 training updates"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="#f97316", markeredgecolor="#7c2d12", markersize=16, label="selected"),
        plt.Line2D([0], [0], color="#0f766e", linestyle="--", label="target loss"),
    ]
    ax.legend(handles=handles, loc="lower left", ncol=2)
    fig.text(
        0.08,
        0.02,
        "Each dot is a possible starting train.py. Dot size shows how many edit families improved it.",
        color="#475569",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIGURES / "figure-01-baseline-screen-overview.png", dpi=180)
    plt.close(fig)


def figure_02_difficulty_diagnostic(baselines: pd.DataFrame) -> None:
    data = baselines[baselines["fixed_steps"] == 1170].copy()
    data = data.sort_values(["raw_win_rate", "category_count"], ascending=[True, True])
    labels = [_baseline_label(value) for value in data["baseline_id"]]
    y = np.arange(len(data))
    selected_mask = (
        (data["run_id"] == SELECTED_RUN) & (data["baseline_id"] == SELECTED_BASELINE)
    ).to_numpy()
    colors = np.where(selected_mask, "#f97316", "#2563eb")

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.barh(y, data["raw_win_rate"], color=colors, alpha=0.86)
    ax.axvspan(0.25, 0.75, color="#dcfce7", alpha=0.45, label="useful calibration range")
    ax.axvline(0.5, color="#64748b", linewidth=1, linestyle=":")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, 1.08)
    ax.set_xlabel("Share of tested edits that improved the starting model")
    ax.set_title("Task difficulty at 1170 training updates")
    ax.grid(axis="y", visible=False)

    for idx, row in enumerate(data.itertuples(index=False)):
        ax.text(
            min(float(row.raw_win_rate) + 0.025, 1.02),
            idx,
            f"{int(row.category_count)} edit families",
            va="center",
            ha="left",
            fontsize=10,
            color="#475569",
        )

    fig.text(
        0.08,
        0.02,
        "The selected baseline is neither saturated nor trivial: 4 of 7 edits worked, across 3 different edit families.",
        color="#475569",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIGURES / "figure-02-gate-diagnostics.png", dpi=180)
    plt.close(fig)


def figure_03_category_heatmap(baselines: pd.DataFrame, trials: pd.DataFrame) -> None:
    data = baselines[baselines["fixed_steps"] == 1170].copy()
    trial_data = trials[(trials["fixed_steps"] == 1170) & (~trials["is_baseline"])].copy()
    merged = trial_data.merge(
        data[["run_id", "baseline_id", "baseline_val_bpb"]],
        on=["run_id", "baseline_id"],
        how="inner",
    )
    merged["improvement"] = merged["baseline_val_bpb"] - merged["val_bpb"]
    merged["public_category"] = merged["category"].replace(
        {"optimizer_scheduler": "scheduler"}
    )
    category_order = ["data_batch", "optimizer_lr", "scheduler", "normalization_capacity", "regularization"]
    rows = []
    row_labels = []
    for row in data.sort_values("baseline_val_bpb").itertuples(index=False):
        candidate_trials = merged[
            (merged["run_id"] == row.run_id) & (merged["baseline_id"] == row.baseline_id)
        ]
        values = []
        for category in category_order:
            category_trials = candidate_trials[candidate_trials["public_category"] == category]
            values.append(category_trials["improvement"].max() if not category_trials.empty else np.nan)
        rows.append(values)
        row_labels.append(_baseline_label(row.baseline_id))

    matrix = np.array(rows, dtype=float)
    vmax = np.nanmax(np.abs(matrix))
    fig, ax = plt.subplots(figsize=(12, 9))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(np.arange(len(category_order)))
    ax.set_xticklabels(
        [CATEGORY_LABELS.get(category, category.replace("_", " ")) for category in category_order],
        rotation=0,
    )
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels)
    ax.set_title("Which edit families create headroom?")
    ax.set_xlabel("Edit family")
    ax.set_ylabel("Starting model")
    ax.grid(False)

    selected_indices = [
        idx
        for idx, row in enumerate(data.sort_values("baseline_val_bpb").itertuples(index=False))
        if row.run_id == SELECTED_RUN and row.baseline_id == SELECTED_BASELINE
    ]
    for idx in selected_indices:
        ax.axhline(idx - 0.5, color="#f97316", linewidth=2)
        ax.axhline(idx + 0.5, color="#f97316", linewidth=2)

    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label("Best validation-loss improvement in that family")
    fig.text(
        0.08,
        0.02,
        "Green means that at least one edit in the family lowered validation loss. Blank cells were not tested in that screen.",
        color="#475569",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIGURES / "figure-03-category-improvement-heatmap.png", dpi=180)
    plt.close(fig)


def _plot_selected_detail(path: Path, *, presentation: bool = False) -> None:
    baselines, trials = _load()
    base_loss, selected = _selected_trials(baselines, trials)
    target_improvement = base_loss - TARGET_LOSS
    colors = np.where(selected["improvement"] >= 0, "#16a34a", "#dc2626")
    y = np.arange(len(selected))

    height = 6.8 if presentation else 6.2
    fig, ax = plt.subplots(figsize=(11.5, height))
    ax.barh(y, selected["improvement"], color=colors, alpha=0.88)
    ax.axvline(0, color="#111827", linewidth=1)
    ax.axvline(
        target_improvement,
        color="#2563eb",
        linestyle="--",
        linewidth=1.5,
        label=f"target improvement: {target_improvement:.3f}",
    )
    ax.set_yticks(y)
    ax.set_yticklabels(_wrap_labels(selected["label"].tolist(), width=26))
    ax.set_xlabel("Validation-loss improvement vs selected starting model")
    ax.set_title(
        "Selected baseline: which simple edits actually help?"
        if presentation
        else "Detailed outcomes for the selected baseline"
    )
    ax.grid(axis="y", visible=False)

    for idx, row in enumerate(selected.itertuples(index=False)):
        ha = "left" if row.improvement >= 0 else "right"
        offset = 0.004 if row.improvement >= 0 else -0.004
        ax.text(
            row.improvement + offset,
            idx,
            f"loss {row.val_bpb:.3f}",
            va="center",
            ha=ha,
            fontsize=10,
            color="#374151",
        )

    xmin = min(-0.045, float(selected["improvement"].min()) - 0.025)
    xmax = max(0.07, float(selected["improvement"].max()) + 0.04)
    ax.set_xlim(xmin, xmax)
    ax.legend(loc="lower right")
    fig.text(
        0.08,
        0.02,
        "Positive bars are useful edits. The blue line is the minimum improvement needed to beat the future target loss.",
        color="#475569",
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, dpi=180)
    plt.close(fig)


def figure_05_presentation_choice(baselines: pd.DataFrame) -> None:
    data = baselines[baselines["fixed_steps"] == 1170].copy()
    data["is_selected"] = (
        (data["run_id"] == SELECTED_RUN) & (data["baseline_id"] == SELECTED_BASELINE)
    )

    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    base_colors = np.where(data["raw_win_rate"] >= 0.9, "#94a3b8", "#2563eb")
    ax.scatter(
        data["raw_win_rate"],
        data["category_count"],
        s=140,
        color=base_colors,
        alpha=0.8,
        edgecolors="white",
        linewidths=1,
    )
    selected = data[data["is_selected"]].iloc[0]
    ax.scatter(
        [selected["raw_win_rate"]],
        [selected["category_count"]],
        marker="*",
        s=520,
        color="#f97316",
        edgecolors="#7c2d12",
        linewidths=1.2,
        zorder=5,
    )
    ax.axhline(3, color="#334155", linestyle="--", linewidth=1.2)
    ax.axvspan(0.25, 0.75, color="#dcfce7", alpha=0.5)
    ax.axvspan(0.9, 1.02, color="#fef3c7", alpha=0.55)
    ax.annotate(
        "selected\n4/7 edits worked\n3 edit families",
        xy=(selected["raw_win_rate"], selected["category_count"]),
        xytext=(0.34, 4.55),
        arrowprops={"arrowstyle": "->", "color": "#7c2d12"},
        color="#7c2d12",
        fontsize=12,
        ha="left",
    )
    ax.set_title("Why this starting model?")
    ax.set_xlabel("Share of tested edits that improved it")
    ax.set_ylabel("Number of edit families that improved it")
    ax.set_xlim(0, 1.04)
    ax.set_ylim(0.5, 5.4)
    ax.text(0.91, 5.15, "too easy", color="#92400e")
    ax.text(0.26, 0.82, "useful range", color="#166534")
    fig.text(
        0.08,
        0.02,
        "This view normalizes by trial count, so screens with different numbers of edits can be compared.",
        color="#475569",
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(FIGURES / "figure-05-presentation-baseline-choice.png", dpi=180)
    plt.close(fig)


def main() -> None:
    _style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    baselines, trials = _load()
    figure_01_candidate_map(baselines)
    figure_02_difficulty_diagnostic(baselines)
    figure_03_category_heatmap(baselines, trials)
    _plot_selected_detail(FIGURES / "figure-04-recommended-baseline-detail.png")
    figure_05_presentation_choice(baselines)
    _plot_selected_detail(
        FIGURES / "figure-06-presentation-width30-detail.png",
        presentation=True,
    )


if __name__ == "__main__":
    main()
