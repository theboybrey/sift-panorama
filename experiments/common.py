"""Shared helpers for saving pair evidence and running method loops."""

from __future__ import annotations

from pathlib import Path

from src.config import (
    DIR_INITIAL_MATCHES,
    DIR_KEYPOINTS,
    DIR_PANORAMAS,
    DIR_RANSAC_MATCHES,
    DIR_WARPED,
)
from src.pipeline import PairPipelineResult, save_homography_matrix, default_homography_path
from src.visualization import (
    save_before_after_matches,
    save_bgr,
    save_keypoints,
    save_matches,
    save_side_by_side,
)


def save_pair_evidence(result: PairPipelineResult, tag: str, save_warped: bool = True) -> None:
    method = result.method.lower()
    stem = f"{method}_{tag}"
    save_keypoints(
        DIR_KEYPOINTS / f"{stem}_{Path(result.image_a).stem}.png",
        result.color_a,
        result.features_a.keypoints,
        f"{result.method} keypoints — {result.image_a} ({result.features_a.num_keypoints})",
    )
    save_keypoints(
        DIR_KEYPOINTS / f"{stem}_{Path(result.image_b).stem}.png",
        result.color_b,
        result.features_b.keypoints,
        f"{result.method} keypoints — {result.image_b} ({result.features_b.num_keypoints})",
    )
    save_matches(
        DIR_INITIAL_MATCHES / f"{stem}_initial.png",
        result.color_a,
        result.features_a.keypoints,
        result.color_b,
        result.features_b.keypoints,
        result.match_result.initial_matches,
        f"{result.method} initial matches — {tag} (n={result.match_result.num_initial_matches})",
    )
    save_before_after_matches(
        DIR_RANSAC_MATCHES / f"{stem}_before_after.png",
        result.color_a,
        result.features_a.keypoints,
        result.color_b,
        result.features_b.keypoints,
        result.match_result.initial_matches,
        result.homography_result.inlier_mask,
        f"{result.method} {tag}",
    )
    save_homography_matrix(
        default_homography_path(result.method, result.image_a, result.image_b, tag),
        result.homography_result.homography,
        f"{result.method} homography mapping {result.image_a} -> {result.image_b} [{tag}]",
    )
    if save_warped and result.stitch is not None and result.stitch.status == "ok":
        if result.stitch.warped_images:
            save_bgr(DIR_WARPED / f"{stem}_warped_src.png", result.stitch.warped_images[0])
        save_bgr(DIR_PANORAMAS / f"{stem}_pair.png", result.stitch.panorama)


def save_originals(images: list, titles: list[str], path: Path) -> None:
    save_side_by_side(path, images, titles, "Input images (working resolution)")
