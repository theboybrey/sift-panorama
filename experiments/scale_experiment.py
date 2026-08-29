"""Controlled scale changes of the second image of the centre pair."""

from __future__ import annotations

import cv2

from src.config import DATA_ORIGINAL, DATA_SCALE, PRIMARY_IMAGES
from src.pipeline import run_pair
from src.preprocessing import prepare_image, scale_image
from experiments.common import save_pair_evidence


SCALES = (1.00, 0.75, 0.50)


def run_scale_experiment() -> list[dict]:
    ref, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[1])
    moving, _, _ = prepare_image(DATA_ORIGINAL / PRIMARY_IMAGES[2])
    rows: list[dict] = []
    for factor in SCALES:
        scaled = scale_image(moving, factor)
        percent = int(round(factor * 100))
        cv2.imwrite(str(DATA_SCALE / f"boat3_scale{percent}.jpg"), scaled)
        for method in ("SIFT", "ORB"):
            result = run_pair(
                ref,
                scaled,
                method,
                PRIMARY_IMAGES[1],
                f"boat3_scale{percent}.jpg",
                condition=f"scale_{percent}",
            )
            save_pair_evidence(result, f"scale{percent}")
            rows.append(result.metrics_row("scale"))
    return rows


if __name__ == "__main__":
    from src.config import ensure_result_dirs

    ensure_result_dirs()
    print(run_scale_experiment())
