"""Generate simple figures for the starting-model calibration study.

The study directory keeps the historical name `baseline_headroom`, but the
public-facing figures avoid internal shorthand such as q*, q3, BP, and
candidate IDs. Raw IDs remain in the CSV/JSON artifacts for provenance.
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
SELECTED_ID = "width30_lr_low"
TARGET_LOSS = 0.824


STARTING_MODEL_NAMES = {
    "weak_regularization_no_schedule": "already strong;\nlittle room",
    "width30_lr_low": "selected:\nwidth 30 + lower LR",
    "narrow_lr_low": "narrower model",
    "sgd_baseline": "SGD optimizer",
    "fc96_lr_low": "smaller head",
    "dropout005_lr_low": "dropout added",
    "width28_lr_low": "width 28 + lower LR",
    "width24_lr_mid": "width 24 + mid LR",
    "small_fc_lr_low": "very small head",
    "no_batchnorm_lr_low": "batch norm removed",
    "overregularized_lr_low": "too much regularization",
}

EDIT_NAMES = {
    "lr_1e3": "raise learning rate\nto 0.001",
    "lr_1p5e3": "raise learning rate\nto 0.0015",
    "adamw_1e3": "switch optimizer\nto AdamW",
    "schedule_on": "turn on\nLR schedule",
    "width32": "make model\nslightly wider",
    "batch192": "use batch\nsize 192",
    "batch256": "use batch\nsize 256",
}

FAMILY_NAMES = {
    "data_batch": "batch size",
    "optimizer_lr": "learning rate / optimizer",
    "normalization_capacity": "model capacity",
    "scheduler": "schedule",
    "optimizer_scheduler": "schedule",
    "regularization": "regularization",
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
            "axes.titlesize": 17,
            "axes.labelsize": 12,
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "legend.frameon": False,
        }
    )


def _load() -> tuple[pd.DataFrame, pd.DataFrame]:
    starts = pd.read_csv(TABLES / "baseline_summary.csv")
    trials = pd.read_csv(TABLES / "trial_results.csv")

    for col in [
        "fixed_steps",
        "baseline_val_bpb",
        "raw_wins",
        "edit_count",
        "raw_win_rate",
        "category_count",
    ]:
        starts[col] = pd.to_numeric(starts[col], errors="coerce")
    for col in ["fixed_steps", "val_bpb", "total_seconds"]:
        trials[col] = pd.to_numeric(trials[col], errors="coerce")
    trials["is_baseline"] = trials["is_baseline"].astype(str).str.lower().eq("true")
    return starts, trials


def _selected(starts: pd.DataFrame, trials: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    row = starts[(starts["run_id"] == SELECTED_RUN) & (starts["baseline_id"] == SELECTED_ID)].iloc[0]
    edit_rows = trials[
        (trials["run_id"] == SELECTED_RUN)
        & (trials["baseline_id"] == SELECTED_ID)
        & (~trials["is_baseline"])
        & (trials["status"] == "success")
    ].copy()
    edit_rows["improvement"] = float(row["baseline_val_bpb"]) - edit_rows["val_bpb"]
    edit_rows["edit_name"] = edit_rows["id"].map(lambda x: EDIT_NAMES.get(x.split("__")[-1], x))
    edit_rows["family_name"] = edit_rows["category"].map(lambda x: FAMILY_NAMES.get(x, x))
    return row, edit_rows


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGURES / name, dpi=180)
    plt.close(fig)


def _caption(fig: plt.Figure, text: str, *, width: int = 112) -> None:
    fig.text(0.08, 0.025, textwrap.fill(text, width=width), color="#475569", fontsize=11.5)


def figure_01_task_definition() -> None:
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    ax.set_title("What is the task?", pad=18)

    boxes = [
        ("1", "Start from one\ntrain.py", "same starting point\nfor every future agent"),
        ("2", "Agent edits\ntrain.py", "changes architecture,\noptimizer, or training choices"),
        ("3", "Run the evaluator", "train for 1170 optimizer\nupdates, then measure validation loss"),
        ("4", "Score the result", "lower validation loss\nmeans a better candidate"),
    ]

    positions = [(0.08, 0.58), (0.54, 0.58), (0.08, 0.28), (0.54, 0.28)]
    for (x, y), (num, title, body) in zip(positions, boxes):
        rect = plt.Rectangle((x, y), 0.38, 0.22, facecolor="#eff6ff", edgecolor="#93c5fd", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + 0.025, y + 0.165, num, fontsize=18, fontweight="bold", color="#1d4ed8")
        ax.text(x + 0.085, y + 0.165, title, fontsize=14.5, fontweight="bold", va="top", color="#111827")
        ax.text(x + 0.025, y + 0.075, body, fontsize=11.2, va="top", color="#475569")

    ax.text(
        0.08,
        0.16,
        "Why choose the starting point first? If it is too easy, every workflow looks good. "
        "If it is too hard, every workflow looks bad. A fair comparison needs a controlled middle.",
        fontsize=13,
        color="#111827",
        wrap=True,
    )
    ax.text(
        0.08,
        0.08,
        "Metric used here: validation loss, named val_bpb in the logs. There is no separate Q metric in this report.",
        fontsize=12,
        color="#475569",
    )
    _save(fig, "figure-01-baseline-screen-overview.png")


def figure_02_why_1170_updates(starts: pd.DataFrame) -> None:
    grouped = (
        starts.assign(screen=np.where(starts["fixed_steps"] == 585, "585 updates", "1170 updates"))
        .groupby("screen")
        .agg(
            mean_success=("raw_win_rate", "mean"),
            too_easy=("raw_win_rate", lambda values: (values >= 0.85).mean()),
            n=("raw_win_rate", "size"),
        )
        .reindex(["585 updates", "1170 updates"])
    )

    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    x = np.arange(len(grouped))
    bars = ax.bar(x, grouped["mean_success"], color=["#94a3b8", "#2563eb"], width=0.55)
    ax.set_title("Why use 1170 training updates?")
    ax.set_ylabel("Average share of edits that improved")
    ax.set_xticks(x)
    ax.set_xticklabels(grouped.index)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="x", visible=False)

    for bar, (_, row) in zip(bars, grouped.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.04,
            f"{bar.get_height():.0%}\naverage",
            ha="center",
            va="bottom",
            fontsize=12,
            color="#111827",
        )
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            0.07,
            f"{int(row['n'])} starting\nmodels tested",
            ha="center",
            va="bottom",
            fontsize=11,
            color="#f8fafc" if bar.get_height() > 0.35 else "#475569",
        )

    _caption(
        fig,
        "The shorter screen was mostly a debugging screen: edits won too often. "
        "The 1170-update screen keeps improvements available while preserving failures.",
        width=90,
    )
    _save(fig, "figure-02-gate-diagnostics.png")


def figure_03_starting_model_choice(starts: pd.DataFrame) -> None:
    keep = [
        ("weak_regularization_no_schedule", "extended_fixed1170"),
        (SELECTED_ID, SELECTED_RUN),
        ("narrow_lr_low", "default_fixed1170"),
        ("sgd_baseline", "extended_fixed1170"),
        ("width28_lr_low", "refinement_fixed1170"),
        ("small_fc_lr_low", "extended_fixed1170"),
        ("no_batchnorm_lr_low", "default_fixed1170"),
    ]
    rows = []
    for candidate_id, run_id in keep:
        rows.append(starts[(starts["baseline_id"] == candidate_id) & (starts["run_id"] == run_id)].iloc[0])
    data = pd.DataFrame(rows)
    data["name"] = data["baseline_id"].map(lambda x: STARTING_MODEL_NAMES.get(x, x))
    data["selected"] = (data["baseline_id"] == SELECTED_ID) & (data["run_id"] == SELECTED_RUN)
    data = data.sort_values("raw_win_rate")

    fig, ax = plt.subplots(figsize=(11, 6.8))
    colors = np.where(data["selected"], "#f97316", "#2563eb")
    y = np.arange(len(data))
    ax.barh(y, data["raw_win_rate"], color=colors, alpha=0.9)
    ax.axvspan(0.35, 0.70, color="#dcfce7", alpha=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(data["name"])
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Share of tested edits that improved")
    ax.set_title("Pick a starting model that is neither too hard nor too easy")
    ax.grid(axis="y", visible=False)

    verdicts = []
    for row in data.itertuples(index=False):
        if row.selected:
            verdict = "chosen"
        elif row.raw_win_rate < 0.30:
            verdict = "too little room"
        elif row.raw_win_rate > 0.85:
            verdict = "too easy"
        else:
            verdict = "backup / diagnostic"
        verdicts.append(verdict)
    for idx, (row, verdict) in enumerate(zip(data.itertuples(index=False), verdicts)):
        ax.text(
            min(row.raw_win_rate + 0.03, 0.98),
            idx,
            f"{int(row.raw_wins)}/{int(row.edit_count)} edits worked · {verdict}",
            va="center",
            fontsize=10.5,
            color="#374151",
        )

    _caption(
        fig,
        "This chart uses normalized edit success rate, so screens with different trial counts can be compared.",
        width=96,
    )
    _save(fig, "figure-03-category-improvement-heatmap.png")


def figure_04_selected_edits(starts: pd.DataFrame, trials: pd.DataFrame, name: str, *, title: str) -> None:
    selected_row, edits = _selected(starts, trials)
    edits = edits.sort_values("val_bpb", ascending=False)
    colors = np.where(edits["val_bpb"] <= TARGET_LOSS, "#16a34a", "#dc2626")
    y = np.arange(len(edits))

    fig, ax = plt.subplots(figsize=(11.2, 6.5))
    ax.barh(y, edits["val_bpb"], color=colors, alpha=0.9)
    ax.axvline(float(selected_row["baseline_val_bpb"]), color="#111827", linestyle=":", linewidth=1.5, label="starting loss")
    ax.axvline(TARGET_LOSS, color="#2563eb", linestyle="--", linewidth=1.8, label="future target")
    ax.set_yticks(y)
    ax.set_yticklabels(edits["edit_name"])
    ax.set_xlim(0.76, 0.89)
    ax.set_xlabel("Validation loss after the edit (lower is better)")
    ax.set_title(title)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper right", ncol=2)

    for idx, row in enumerate(edits.itertuples(index=False)):
        ax.text(
            row.val_bpb + 0.003,
            idx,
            f"{row.val_bpb:.3f}",
            va="center",
            fontsize=10.5,
            color="#374151",
        )

    _caption(
        fig,
        "Green edits beat the future target. Red edits are useful negative controls: they show that not every change wins.",
        width=100,
    )
    _save(fig, name)


def figure_05_result_card(starts: pd.DataFrame) -> None:
    selected = starts[(starts["baseline_id"] == SELECTED_ID) & (starts["run_id"] == SELECTED_RUN)].iloc[0]

    fig, ax = plt.subplots(figsize=(10.5, 7.4))
    ax.axis("off")
    ax.set_title("Selected starting point for future agent runs", pad=18)

    cards = [
        ("Starting loss", f"{selected['baseline_val_bpb']:.3f}", "validation loss before any agent edit"),
        ("Target loss", f"{TARGET_LOSS:.3f}", "future agent runs must go below this"),
        ("Edits that worked", f"{int(selected['raw_wins'])}/{int(selected['edit_count'])}", "not too easy, not impossible"),
        ("Edit families", f"{int(selected['category_count'])}", "batch size, learning rate, model capacity"),
    ]
    positions = [(0.08, 0.54), (0.54, 0.54), (0.08, 0.25), (0.54, 0.25)]
    for (x, y), (label, value, note) in zip(positions, cards):
        rect = plt.Rectangle((x, y), 0.36, 0.22, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + 0.025, y + 0.17, label, fontsize=11.5, color="#475569", va="top")
        ax.text(x + 0.025, y + 0.115, value, fontsize=25, fontweight="bold", color="#111827", va="top")
        ax.text(x + 0.15, y + 0.11, "\n".join(textwrap.wrap(note, 28)), fontsize=10.5, color="#475569", va="top")

    ax.text(
        0.07,
        0.10,
        "Why this matters: all future workflows should start from the same controlled file, "
        "otherwise a comparison between agents is not meaningful.",
        fontsize=13,
        color="#111827",
        wrap=True,
    )
    _save(fig, "figure-05-presentation-baseline-choice.png")


def figure_06_family_summary(starts: pd.DataFrame, trials: pd.DataFrame) -> None:
    _, edits = _selected(starts, trials)
    family_best = (
        edits.assign(family=edits["family_name"])
        .groupby("family", as_index=False)
        .agg(best_loss=("val_bpb", "min"), best_edit=("edit_name", lambda values: list(values)[0]))
        .sort_values("best_loss", ascending=False)
    )
    colors = np.where(family_best["best_loss"] <= TARGET_LOSS, "#16a34a", "#dc2626")
    y = np.arange(len(family_best))

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.barh(y, family_best["best_loss"], color=colors, alpha=0.9)
    ax.axvline(TARGET_LOSS, color="#2563eb", linestyle="--", linewidth=1.8, label="future target")
    ax.set_yticks(y)
    ax.set_yticklabels(family_best["family"])
    ax.set_xlim(0.76, 0.89)
    ax.set_xlabel("Best validation loss in each edit family")
    ax.set_title("Three different edit families can beat the target")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right")

    for idx, row in enumerate(family_best.itertuples(index=False)):
        ax.text(row.best_loss + 0.003, idx, f"{row.best_loss:.3f}", va="center", fontsize=10.5, color="#374151")

    _caption(
        fig,
        "The chosen task is not solved by one narrow trick: batch size, learning rate, and capacity each have a winning edit.",
        width=100,
    )
    _save(fig, "figure-06-presentation-width30-detail.png")


def main() -> None:
    _style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    starts, trials = _load()
    figure_01_task_definition()
    figure_02_why_1170_updates(starts)
    figure_03_starting_model_choice(starts)
    figure_04_selected_edits(
        starts,
        trials,
        "figure-04-recommended-baseline-detail.png",
        title="What happened when simple edits were tested?",
    )
    figure_05_result_card(starts)
    figure_06_family_summary(starts, trials)


if __name__ == "__main__":
    main()
