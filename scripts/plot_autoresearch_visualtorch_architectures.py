"""Generate VisualTorch architecture diagrams for AutoResearch workloads."""

from __future__ import annotations

import sys
from pathlib import Path

import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont
from visualtorch.flow import flow_view


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "autoresearch" / "benchmark" / "cifar10"
OUT = ROOT / "docs" / "assets" / "autoresearch"

sys.path.insert(0, str(BENCHMARK))

from workloads import cnn_compact, mlp_flat, resnet_micro  # noqa: E402


WORKLOADS = [
    {
        "title": "MLP",
        "subtitle": "mlp_flat · flattened image MLP · ~669k parameters",
        "module": mlp_flat,
    },
    {
        "title": "Compact CNN",
        "subtitle": "cnn_compact · two convolutional blocks · ~77k parameters",
        "module": cnn_compact,
    },
    {
        "title": "Micro ResNet",
        "subtitle": "resnet_micro · residual block with skip path · ~2.6k parameters",
        "module": resnet_micro,
    },
]


def font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_workload(module: object) -> Image.Image:
    model = module.CIFAR10Net().eval()
    image = flow_view(
        model,
        input_shape=(2, 3, 32, 32),
        draw_volume=True,
        show_dimension=True,
        spacing=32,
        padding=30,
        scale_z=0.55,
        scale_xy=2.0,
        min_xy=18,
        max_xy=280,
        min_z=12,
        max_z=130,
        type_ignore=[nn.BatchNorm1d, nn.BatchNorm2d, nn.Dropout, nn.Dropout2d],
        palette="tol_muted",
        background_fill="white",
        legend=True,
    )
    return image.convert("RGB")


def label_panel(title: str, subtitle: str, architecture: Image.Image, width: int) -> Image.Image:
    title_font = font(32, bold=True)
    subtitle_font = font(22)
    label_height = 92
    panel = Image.new("RGB", (width, label_height + architecture.height), "white")
    draw = ImageDraw.Draw(panel)
    draw.text((22, 14), title, fill=(17, 24, 39), font=title_font)
    draw.text((22, 54), subtitle, fill=(100, 116, 139), font=subtitle_font)
    x = (width - architecture.width) // 2
    panel.paste(architecture, (x, label_height))
    return panel


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered: list[Image.Image] = []
    for workload in WORKLOADS:
        image = render_workload(workload["module"])
        image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
        rendered.append(image)
        image.save(OUT / f"visualtorch-{workload['title'].lower().replace(' ', '-')}.png")

    width = max(image.width for image in rendered) + 80
    panels = [
        label_panel(workload["title"], workload["subtitle"], image, width)
        for workload, image in zip(WORKLOADS, rendered)
    ]
    title_font = font(42, bold=True)
    subtitle_font = font(24)
    header_height = 112
    gap = 24
    total_height = header_height + sum(panel.height for panel in panels) + gap * (len(panels) - 1) + 36
    canvas = Image.new("RGB", (width, total_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 20), "AutoResearch neural substrates", fill=(17, 24, 39), font=title_font)
    draw.text(
        (24, 72),
        "VisualTorch renderings of the small CIFAR-10 networks agents edit during the experiment.",
        fill=(100, 116, 139),
        font=subtitle_font,
    )
    y = header_height
    for panel in panels:
        canvas.paste(panel, (0, y))
        y += panel.height + gap

    canvas.save(OUT / "autoresearch-visualtorch-architectures.png")


if __name__ == "__main__":
    main()
