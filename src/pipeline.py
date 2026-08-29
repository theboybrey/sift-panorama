"""End-to-end pair pipeline: detect → describe → match → RANSAC → warp."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.config import DIR_HOMOGRAPHIES, LOWE_RATIO, RANSAC_REPROJ_THRESH
from src.features import detect_and_describe
from src.homography import estimate_homography, mean_reprojection_error
from src.matching import correspondences_from_matches, match_descriptors
from src.preprocessing import prepare_image, to_gray
from src.stitching import stitch_pair, stitch_three


@dataclass
class PairPipelineResult:
    method: str
    image_a: str
    image_b: str
    condition: str
    color_a: np.ndarray
    color_b: np.ndarray
    features_a: object
    features_b: object
    match_result: object
    homography_result: object
    pts_a: np.ndarray
    pts_b: np.ndarray
    mean_reproj_error: float | None
    stitch: object
    total_time_sec: float

    def metrics_row(self, experiment: str) -> dict:
        h = self.homography_result
        f_a, f_b = self.features_a, self.features_b
        m = self.match_result
        stitch_status = self.stitch.status if self.stitch is not None else "not_run"
        return {
            "experiment": experiment,
            "method": self.method,
            "image_a": self.image_a,
            "image_b": self.image_b,
            "condition": self.condition,
            "keypoints_a": f_a.num_keypoints,
            "keypoints_b": f_b.num_keypoints,
            "descriptor_dim": f_a.descriptor_dim,
            "candidate_matches": m.candidate_matches,
            "initial_matches": m.num_initial_matches,
            "ransac_inliers": h.num_inliers,
            "ransac_outliers": h.num_outliers,
            "inlier_ratio": h.inlier_ratio,
            "mean_reproj_error": self.mean_reproj_error,
            "feature_time_sec": f_a.elapsed_sec + f_b.elapsed_sec,
            "match_time_sec": m.elapsed_sec,
            "ransac_time_sec": h.elapsed_sec,
            "total_time_sec": self.total_time_sec,
            "homography_status": h.status,
            "panorama_status": stitch_status,
            "overlap_mae": None if self.stitch is None else self.stitch.overlap_mae,
            "panorama_success": bool(
                self.stitch is not None
                and self.stitch.status == "ok"
                and self.homography_result.status == "ok"
            ),
        }


def run_pair(
    image_a: np.ndarray,
    image_b: np.ndarray,
    method: str,
    name_a: str,
    name_b: str,
    condition: str = "original",
    stitch: bool = True,
) -> PairPipelineResult:
    """Run the classical pipeline on two already-prepared colour images."""
    started = time.perf_counter()
    method = method.upper()
    gray_a = to_gray(image_a)
    gray_b = to_gray(image_b)
    features_a = detect_and_describe(gray_a, method)
    features_b = detect_and_describe(gray_b, method)
    matches = match_descriptors(
        features_a.descriptors,
        features_b.descriptors,
        features_a.distance_norm,
        ratio=LOWE_RATIO,
    )
    pts_a, pts_b = correspondences_from_matches(
        features_a.keypoints, features_b.keypoints, matches.initial_matches
    )
    homo = estimate_homography(pts_a, pts_b, reproj_thresh=RANSAC_REPROJ_THRESH)
    reproj = mean_reprojection_error(pts_a, pts_b, homo.homography, homo.inlier_mask)
    stitch_result = None
    if stitch and homo.homography is not None:
        stitch_result = stitch_pair(image_a, image_b, homo.homography)
    return PairPipelineResult(
        method=method,
        image_a=name_a,
        image_b=name_b,
        condition=condition,
        color_a=image_a,
        color_b=image_b,
        features_a=features_a,
        features_b=features_b,
        match_result=matches,
        homography_result=homo,
        pts_a=pts_a,
        pts_b=pts_b,
        mean_reproj_error=reproj,
        stitch=stitch_result,
        total_time_sec=time.perf_counter() - started,
    )


def load_working_pair(path_a: Path, path_b: Path):
    color_a, _, rec_a = prepare_image(path_a)
    color_b, _, rec_b = prepare_image(path_b)
    return color_a, color_b, rec_a, rec_b


def save_homography_matrix(path: Path, matrix: np.ndarray | None, header: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if matrix is None:
        path.write_text(f"{header}\nHOMOGRAPHY_UNAVAILABLE\n")
        return
    with path.open("w") as handle:
        handle.write(header + "\n")
        np.savetxt(handle, matrix, fmt="%.8f")


def default_homography_path(method: str, name_a: str, name_b: str, tag: str = "") -> Path:
    stem = f"{method.lower()}_{Path(name_a).stem}_{Path(name_b).stem}"
    if tag:
        stem = f"{stem}_{tag}"
    return DIR_HOMOGRAPHIES / f"{stem}.txt"


def run_three_image_panorama(
    left: np.ndarray,
    mid: np.ndarray,
    right: np.ndarray,
    method: str,
    names: tuple[str, str, str],
) -> tuple[PairPipelineResult, PairPipelineResult, object]:
    """Match left→mid and right→mid, then compose a three-image panorama."""
    left_mid = run_pair(left, mid, method, names[0], names[1], stitch=True)
    right_mid = run_pair(right, mid, method, names[2], names[1], stitch=True)
    h_left = left_mid.homography_result.homography
    h_right = right_mid.homography_result.homography
    if h_left is None or h_right is None:
        from src.stitching import StitchResult

        failed = StitchResult(
            None, [], [], (0, 0), None, "missing_homography",
            "Could not estimate both pairwise homographies.",
        )
        return left_mid, right_mid, failed
    panorama = stitch_three(left, mid, right, h_left, h_right)
    return left_mid, right_mid, panorama
