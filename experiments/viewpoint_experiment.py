"""Viewpoint change: adjacent pair versus a wider baseline pair."""

from __future__ import annotations

from src.config import DATA_ORIGINAL, DATA_VIEWPOINT, PRIMARY_IMAGES
from src.pipeline import load_working_pair, run_pair
from src.visualization import save_side_by_side
from experiments.common import save_pair_evidence


def run_viewpoint_experiment() -> list[dict]:
    rows: list[dict] = []
    adjacent = (DATA_ORIGINAL / PRIMARY_IMAGES[0], DATA_ORIGINAL / PRIMARY_IMAGES[1])
    wide = (DATA_ORIGINAL / PRIMARY_IMAGES[0], DATA_ORIGINAL / "boat4.jpg")

    conditions = [
        ("adjacent", adjacent[0], adjacent[1]),
        ("wide_baseline", wide[0], wide[1]),
    ]
    for label, path_a, path_b in conditions:
        color_a, color_b, rec_a, rec_b = load_working_pair(path_a, path_b)
        save_side_by_side(
            DATA_VIEWPOINT / f"{label}_pair.png",
            [color_a, color_b],
            [rec_a.filename, rec_b.filename],
            f"Viewpoint condition: {label}",
        )
        for method in ("SIFT", "ORB"):
            result = run_pair(
                color_a,
                color_b,
                method,
                rec_a.filename,
                rec_b.filename,
                condition=label,
            )
            save_pair_evidence(result, f"view_{label}")
            rows.append(result.metrics_row("viewpoint"))
    return rows


if __name__ == "__main__":
    from src.config import ensure_result_dirs

    ensure_result_dirs()
    print(run_viewpoint_experiment())
