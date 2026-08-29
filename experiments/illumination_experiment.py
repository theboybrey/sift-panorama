"""Photometric robustness: darker, brighter, and contrast-altered copies."""

from __future__ import annotations

import cv2

from src.config import DATA_ILLUMINATION, DATA_ORIGINAL, PRIMARY_IMAGES
from src.pipeline import run_pair
from src.preprocessing import adjust_illumination, prepare_image
from experiments.common import save_pair_evidence


MODES = ("original", "darker", "brighter", "low_contrast", "high_contrast")


def run_illumination_experiment() -> list[dict]:
    ref, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[1])
    moving, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[2])
    rows: list[dict] = []
    for mode in MODES:
        variant = adjust_illumination(moving, mode)
        cv2.imwrite(str(DATA_ILLUMINATION / f"boat3_{mode}.jpg"), variant)
        for method in ("SIFT", "ORB"):
            result = run_pair(
                ref,
                variant,
                method,
                PRIMARY_IMAGES[1],
                f"boat3_{mode}.jpg",
                condition=mode,
            )
            save_pair_evidence(result, f"illum_{mode}")
            rows.append(result.metrics_row("illumination"))
    return rows


if __name__ == "__main__":
    from src.config import ensure_result_dirs

    ensure_result_dirs()
    print(run_illumination_experiment())
