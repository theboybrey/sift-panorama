"""Controlled in-plane rotation of the second image of the centre pair."""

from __future__ import annotations

import cv2

from src.config import DATA_ORIGINAL, DATA_ROTATION, PRIMARY_IMAGES
from src.pipeline import run_pair
from src.preprocessing import prepare_image, rotate_image
from experiments.common import save_pair_evidence


ANGLES = (15, 30, 45)


def run_rotation_experiment() -> list[dict]:
    ref, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[1])
    moving, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[2])
    rows: list[dict] = []
    for angle in ANGLES:
        rotated = rotate_image(moving, angle)
        cv2.imwrite(str(DATA_ROTATION / f"boat3_rot{angle}.jpg"), rotated)
        for method in ("SIFT", "ORB"):
            result = run_pair(
                ref,
                rotated,
                method,
                PRIMARY_IMAGES[1],
                f"boat3_rot{angle}.jpg",
                condition=f"rotation_{angle}",
            )
            save_pair_evidence(result, f"rot{angle}")
            rows.append(result.metrics_row("rotation"))
    return rows


if __name__ == "__main__":
    from src.config import ensure_result_dirs

    ensure_result_dirs()
    print(run_rotation_experiment())
