"""Generate public figures for the historical swarm baseline study."""

from __future__ import annotations

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies" / "swarm_baselines"
FIGURES = STUDY / "results" / "figures"

BLUE = "#2563eb"
ORANGE = "#f97316"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
GRAY = "#64748b"
LIGHT_GRAY = "#f1f5f9"
DARK = "#111827"
GRID = "#e5e7eb"

MODEL_BASELINE_BPB = 1.1020746984708296

EXPERIMENTS = [
    {
        "key": "independent_parallel_baseline",
        "title": "Independent\nparallel baseline",
        "mode": "parallel",
        "model": "historical",
        "best_bpb": 1.113130,
        "agent0_best": 1.113884,
        "agent1_best": 1.113130,
        "runs": None,
        "duration_min": None,
        "color": GRAY,
        "status": "partial artifact",
    },
    {
        "key": "haiku_swarm_run_1",
        "title": "Haiku\nswarm run 1",
        "mode": "swarm",
        "model": "Haiku 4.5",
        "best_bpb": 1.041477,
        "agent0_best": 1.047929,
        "agent1_best": 1.041477,
        "runs": 27,
        "duration_min": 119.2,
        "color": ORANGE,
        "status": "complete summary",
    },
    {
        "key": "haiku_swarm_run_2",
        "title": "Haiku\nswarm run 2",
        "mode": "swarm",
        "model": "Haiku 4.5",
        "best_bpb": 1.044341,
        "agent0_best": 1.044341,
        "agent1_best": 1.050358,
        "runs": 28,
        "duration_min": 120.0,
        "color": ORANGE,
        "status": "complete summary",
    },
    {
        "key": "sonnet_swarm_run",
        "title": "Sonnet\nswarm run",
        "mode": "swarm",
        "model": "Sonnet 4.6",
        "best_bpb": 1.044216,
        "agent0_best": 1.044662,
        "agent1_best": 1.044216,
        "runs": 29,
        "duration_min": 124.8,
        "color": BLUE,
        "status": "complete summary",
    },
    {
        "key": "opus_swarm_run",
        "title": "Opus\nswarm run",
        "mode": "swarm",
        "model": "Opus 4.6",
        "best_bpb": 1.044304,
        "agent0_best": 1.044304,
        "agent1_best": 1.047083,
        "runs": 22,
        "duration_min": 119.7,
        "color": PURPLE,
        "status": "complete summary",
    },
]


def style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": DARK,
            "axes.titlecolor": DARK,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.color": "#374151",
            "ytick.color": "#374151",
            "legend.frameon": False,
            "savefig.bbox": "tight",
        }
    )


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.png", dpi=220)
    fig.savefig(FIGURES / f"{stem}.pdf")
    plt.close(fig)


def wrap(text: str, width: int = 30) -> str:
    return "\n".join(textwrap.wrap(text, width=width))


def add_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    wh: tuple[float, float],
    title: str,
    body: str,
    color: str,
    title_size: int = 12,
    body_size: int = 10,
) -> None:
    x, y = xy
    w, h = wh
    rect = Rectangle((x, y), w, h, linewidth=1.4, edgecolor=color, facecolor="white")
    ax.add_patch(rect)
    ax.text(
        x + w / 2,
        y + h - 0.08,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=DARK,
    )
    ax.text(
        x + w / 2,
        y + h - 0.26,
        body,
        ha="center",
        va="top",
        fontsize=body_size,
        color="#374151",
        linespacing=1.3,
    )


def arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = GRAY,
    dashed: bool = False,
    both: bool = False,
) -> None:
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="<->" if both else "-|>",
        mutation_scale=16,
        linewidth=1.6,
        linestyle="--" if dashed else "-",
        color=color,
    )
    ax.add_patch(patch)


def figure_experiment_scorecards() -> None:
    fig, axes = plt.subplots(1, 5, figsize=(16, 4.6), constrained_layout=True)
    fig.suptitle(
        "Historical experiments represented in swarm baselines",
        fontsize=16,
        y=1.04,
    )

    for ax, exp in zip(axes, EXPERIMENTS):
        ax.set_axis_off()
        ax.add_patch(
            Rectangle(
                (0.03, 0.03),
                0.94,
                0.94,
                linewidth=1.6,
                edgecolor=exp["color"],
                facecolor="white",
            )
        )
        ax.text(
            0.5,
            0.88,
            exp["title"],
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color=DARK,
        )
        ax.text(0.5, 0.69, f"mode: {exp['mode']}", ha="center", fontsize=10, color="#374151")
        ax.text(0.5, 0.59, f"model: {exp['model']}", ha="center", fontsize=10, color="#374151")
        duration = (
            f"{exp['duration_min']:.1f} min"
            if exp["duration_min"] is not None
            else "not preserved"
        )
        runs = f"{exp['runs']}" if exp["runs"] is not None else "not preserved"
        ax.text(0.5, 0.48, f"duration: {duration}", ha="center", fontsize=10, color="#374151")
        ax.text(0.5, 0.38, f"training attempts: {runs}", ha="center", fontsize=10, color="#374151")
        ax.text(0.5, 0.25, f"best validation BPB\n{exp['best_bpb']:.6f}", ha="center", fontsize=12, color=DARK)
        ax.text(0.5, 0.10, exp["status"], ha="center", fontsize=9, color=GRAY)

    save(fig, "figure-01-experiment-scorecards")


def figure_performance_comparison() -> None:
    fig, ax = plt.subplots(figsize=(10.8, 5.4), constrained_layout=True)
    labels = [e["title"].replace("\n", " ") for e in EXPERIMENTS]
    values = [e["best_bpb"] for e in EXPERIMENTS]
    colors = [e["color"] for e in EXPERIMENTS]
    y = list(range(len(EXPERIMENTS)))

    for idx, value in enumerate(values):
        ax.hlines(idx, xmin=1.035, xmax=value, color="#e5e7eb", linewidth=2.0)
    ax.scatter(values, y, color=colors, s=170, zorder=3, edgecolor="white", linewidth=1.2)
    ax.axvline(MODEL_BASELINE_BPB, color="#94a3b8", linestyle="--", linewidth=1.5, label="model comparison baseline")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Best validation BPB (lower is better)")
    ax.set_title("Swarm runs reached lower validation BPB than the independent-parallel baseline")
    ax.set_xlim(1.035, 1.120)
    ax.grid(axis="y", visible=False)
    ax.legend(loc="lower right")

    for idx, value in enumerate(values):
        ax.text(value + 0.0012, idx, f"{value:.6f}", va="center", fontsize=10, color=DARK)

    save(fig, "figure-02-performance-comparison")


def figure_budget_comparability() -> None:
    swarm = [e for e in EXPERIMENTS if e["mode"] == "swarm"]
    labels = [e["title"].replace("\n", " ") for e in swarm]
    colors = [e["color"] for e in swarm]
    durations = [e["duration_min"] for e in swarm]
    runs = [e["runs"] for e in swarm]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)

    ax = axes[0]
    bars = ax.bar(labels, durations, color=colors, alpha=0.9)
    ax.axhline(120, color="#94a3b8", linestyle="--", linewidth=1.5, label="target budget")
    ax.set_ylabel("Experiment duration (minutes)")
    ax.set_title("A. Model comparison used the same 120 min/agent budget")
    ax.set_ylim(0, 132)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")
    for bar, value in zip(bars, durations):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f"{value:.1f}", ha="center", fontsize=10)

    ax = axes[1]
    bars = ax.bar(labels, runs, color=colors, alpha=0.9)
    ax.set_ylabel("Valid training attempts")
    ax.set_title("B. Faster agents complete more evaluator calls")
    ax.set_ylim(0, 34)
    ax.grid(axis="x", visible=False)
    for bar, value in zip(bars, runs):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.7, str(value), ha="center", fontsize=10)

    for ax in axes:
        ax.tick_params(axis="x", labelrotation=18)

    save(fig, "figure-03-budget-and-throughput")


def figure_swarm_memory_architecture() -> None:
    fig, ax = plt.subplots(figsize=(13.8, 7.0), constrained_layout=True)
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_title("Swarm mode: two isolated Claude Code agents coordinate through one blackboard", fontsize=16, pad=18)

    add_box(
        ax,
        (0.35, 3.35),
        (2.55, 1.35),
        "Agent 0",
        "Claude Code subprocess\nisolated worktree\nGPU 0 worker",
        BLUE,
    )
    add_box(
        ax,
        (7.10, 3.35),
        (2.55, 1.35),
        "Agent 1",
        "Claude Code subprocess\nisolated worktree\nGPU 1 worker",
        ORANGE,
    )
    add_box(
        ax,
        (3.62, 2.72),
        (2.76, 1.74),
        "Shared blackboard",
        "append-only JSONL\nfcntl file locks\nclaim, result, best,\ninsight, hypothesis",
        GREEN,
        body_size=9.5,
    )
    add_box(
        ax,
        (3.70, 0.65),
        (2.60, 1.10),
        "Task",
        "edit train.py\nrun training attempts\nminimize validation BPB",
        GRAY,
        title_size=11,
        body_size=9.5,
    )

    arrow(ax, (2.90, 4.02), (3.62, 3.62), BLUE, both=True)
    arrow(ax, (7.10, 4.02), (6.38, 3.62), ORANGE, both=True)
    arrow(ax, (4.95, 2.72), (4.95, 1.75), GREEN)
    arrow(ax, (1.63, 3.35), (4.00, 1.48), BLUE)
    arrow(ax, (8.37, 3.35), (5.90, 1.48), ORANGE)

    ax.text(
        5.0,
        5.32,
        wrap("Two agents were used because the preserved experiment allocated one GPU per agent: 2 agents, 2 GPUs total, 120 minutes per agent.", 88),
        ha="center",
        va="center",
        fontsize=11,
        color="#374151",
    )
    ax.text(
        5.0,
        0.18,
        "Coordination is explicit: agents reserve hypotheses, publish results, and pull the global best through the blackboard.",
        ha="center",
        fontsize=10.5,
        color="#374151",
    )

    save(fig, "figure-04-swarm-memory-architecture")


def figure_independent_parallel_architecture() -> None:
    fig, ax = plt.subplots(figsize=(13.8, 6.6), constrained_layout=True)
    ax.set_axis_off()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_title("Independent parallel baseline: agents run side-by-side without shared memory", fontsize=16, pad=18)

    add_box(
        ax,
        (0.50, 3.45),
        (2.45, 1.35),
        "Agent 0",
        "Claude Code subprocess\nisolated worktree\nown evaluator worker",
        BLUE,
    )
    add_box(
        ax,
        (7.05, 3.45),
        (2.45, 1.35),
        "Agent 1",
        "Claude Code subprocess\nisolated worktree\nown evaluator worker",
        ORANGE,
    )
    add_box(
        ax,
        (3.75, 1.00),
        (2.50, 1.18),
        "Post-run collector",
        "reads both outputs only\nafter agents finish",
        GRAY,
        title_size=11,
        body_size=9.5,
    )
    add_box(
        ax,
        (3.55, 4.05),
        (2.90, 0.90),
        "No shared channel",
        "no shared context\nno shared files\nno mid-run merge",
        "#ef4444",
        title_size=11,
        body_size=9.2,
    )

    arrow(ax, (1.72, 3.45), (4.25, 2.18), BLUE)
    arrow(ax, (8.27, 3.45), (5.75, 2.18), ORANGE)
    arrow(ax, (2.95, 4.40), (3.55, 4.40), "#ef4444", dashed=True)
    arrow(ax, (7.05, 4.40), (6.45, 4.40), "#ef4444", dashed=True)

    ax.text(
        5.0,
        5.35,
        wrap("This is the control condition: simultaneous agents get the same task but cannot see each other's hypotheses, results, or best code during the run.", 90),
        ha="center",
        va="center",
        fontsize=11,
        color="#374151",
    )
    ax.text(
        5.0,
        0.35,
        "The collector compares final outputs after both processes exit; it does not coordinate the search.",
        ha="center",
        fontsize=10.5,
        color="#374151",
    )

    save(fig, "figure-05-independent-parallel-architecture")


def main() -> None:
    style()
    figure_experiment_scorecards()
    figure_performance_comparison()
    figure_budget_comparability()
    figure_swarm_memory_architecture()
    figure_independent_parallel_architecture()


if __name__ == "__main__":
    main()
