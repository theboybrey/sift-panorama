"""SIFT vs ORB on the original consecutive pairs and the three-image panorama."""

from __future__ import annotations

from src.config import DATA_ORIGINAL, DIR_PANORAMAS, PRIMARY_IMAGES
from src.pipeline import load_working_pair, run_pair, run_three_image_panorama, save_homography_matrix
from src.preprocessing import prepare_image
from src.visualization import save_bgr, save_side_by_side
from experiments.common import save_originals, save_pair_evidence


def run_feature_comparison() -> list[dict]:
    rows: list[dict] = []
    paths = [DATA_ORIGINAL / name for name in PRIMARY_IMAGES]
    colors = []
    records = []
    for path in paths:
        color, _, record = prepare_image(path)
        record.scene_notes = _scene_note(path.name)
        colors.append(color)
        records.append(record)

    save_originals(colors, PRIMARY_IMAGES, DIR_PANORAMAS / "original_triplet.png")

    pairs = [(0, 1), (1, 2)]
    for method in ("SIFT", "ORB"):
        for i, j in pairs:
            result = run_pair(
                colors[i],
                colors[j],
                method,
                PRIMARY_IMAGES[i],
                PRIMARY_IMAGES[j],
                condition="original",
            )
            tag = f"{PRIMARY_IMAGES[i].split('.')[0]}_{PRIMARY_IMAGES[j].split('.')[0]}"
            save_pair_evidence(result, tag)
            rows.append(result.metrics_row("feature_comparison"))

        left_mid, right_mid, panorama = run_three_image_panorama(
            colors[0], colors[1], colors[2], method, tuple(PRIMARY_IMAGES)
        )
        from src.config import DIR_HOMOGRAPHIES

        save_homography_matrix(
            DIR_HOMOGRAPHIES / f"{method.lower()}_three_left_to_mid.txt",
            left_mid.homography_result.homography,
            f"{method} H mapping boat1 -> boat2",
        )
        save_homography_matrix(
            DIR_HOMOGRAPHIES / f"{method.lower()}_three_right_to_mid.txt",
            right_mid.homography_result.homography,
            f"{method} H mapping boat3 -> boat2",
        )
        if panorama.status == "ok":
            save_bgr(DIR_PANORAMAS / f"{method.lower()}_three_image.png", panorama.panorama)
            if panorama.warped_images:
                save_side_by_side(
                    DIR_PANORAMAS / f"{method.lower()}_warped_components.png",
                    panorama.warped_images,
                    ["left warped", "mid (reference)", "right warped"],
                    f"{method} images on the shared canvas",
                )
        rows.append(
            {
                **left_mid.metrics_row("three_image_left_mid"),
                "panorama_status": panorama.status,
                "overlap_mae": panorama.overlap_mae,
                "panorama_success": panorama.status == "ok",
            }
        )
        rows.append(
            {
                **right_mid.metrics_row("three_image_right_mid"),
                "panorama_status": panorama.status,
                "overlap_mae": panorama.overlap_mae,
                "panorama_success": panorama.status == "ok",
            }
        )
    return rows


def _scene_note(name: str) -> str:
    notes = {
        "boat1.jpg": "Left view: tall ship, embankment, fortress/spire on the right. Overlaps boat2 on the fortress/spire.",
        "boat2.jpg": "Centre view: Peter and Paul Fortress and golden spire dominate. Overlaps both neighbours.",
        "boat3.jpg": "Right view: fortress/spire on the left, bridge and far bank on the right. Overlaps boat2 on the fortress.",
    }
    return notes.get(name, "")


if __name__ == "__main__":
    from src.config import ensure_result_dirs

    ensure_result_dirs()
    print(run_feature_comparison())
