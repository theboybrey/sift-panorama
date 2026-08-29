"""RANSAC outlier rejection and homography estimation.

A homography H is a 3x3 projective transform relating corresponding
points on two planes (or two views of an approximately planar distant
scene) in homogeneous coordinates:

    p' ~ H p,   p = [x, y, 1]^T

Four point correspondences determine H up to scale. Feature matches
always contain outliers, so a least-squares fit on all matches is
unreliable. RANSAC repeatedly samples a minimal set, estimates a
candidate H, and counts inliers whose reprojection error is below a
threshold. The model with the largest consensus set is retained and
then refined on the inliers.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import cv2
import numpy as np

from src.config import MIN_MATCHES_FOR_HOMOGRAPHY, RANSAC_MAX_ITERS, RANSAC_REPROJ_THRESH


@dataclass
class HomographyResult:
    homography: np.ndarray | None
    inlier_mask: np.ndarray | None
    num_initial: int
    num_inliers: int
    num_outliers: int
    inlier_ratio: float
    reproj_thresh: float
    elapsed_sec: float
    status: str


def estimate_homography(
    pts_src: np.ndarray,
    pts_dst: np.ndarray,
    reproj_thresh: float = RANSAC_REPROJ_THRESH,
    max_iters: int = RANSAC_MAX_ITERS,
) -> HomographyResult:
    """Estimate H mapping src points into the dst coordinate system."""
    start = time.perf_counter()
    num_initial = int(len(pts_src))
    if num_initial < MIN_MATCHES_FOR_HOMOGRAPHY:
        return HomographyResult(
            homography=None,
            inlier_mask=None,
            num_initial=num_initial,
            num_inliers=0,
            num_outliers=num_initial,
            inlier_ratio=0.0,
            reproj_thresh=reproj_thresh,
            elapsed_sec=time.perf_counter() - start,
            status="too_few_matches",
        )

    homography, mask = cv2.findHomography(
        pts_src,
        pts_dst,
        method=cv2.RANSAC,
        ransacReprojThreshold=reproj_thresh,
        maxIters=max_iters,
        confidence=0.995,
    )
    if mask is None or homography is None:
        return HomographyResult(
            homography=None,
            inlier_mask=None,
            num_initial=num_initial,
            num_inliers=0,
            num_outliers=num_initial,
            inlier_ratio=0.0,
            reproj_thresh=reproj_thresh,
            elapsed_sec=time.perf_counter() - start,
            status="estimation_failed",
        )

    mask = mask.ravel().astype(bool)
    num_inliers = int(mask.sum())
    num_outliers = num_initial - num_inliers
    ratio = (num_inliers / num_initial) if num_initial else 0.0
    return HomographyResult(
        homography=homography.astype(np.float64),
        inlier_mask=mask,
        num_initial=num_initial,
        num_inliers=num_inliers,
        num_outliers=num_outliers,
        inlier_ratio=float(ratio),
        reproj_thresh=reproj_thresh,
        elapsed_sec=time.perf_counter() - start,
        status="ok" if num_inliers >= MIN_MATCHES_FOR_HOMOGRAPHY else "few_inliers",
    )


def mean_reprojection_error(
    pts_src: np.ndarray,
    pts_dst: np.ndarray,
    homography: np.ndarray,
    mask: np.ndarray | None = None,
) -> float | None:
    """Mean Euclidean error ||p' - pi(H p)|| on the selected correspondences."""
    if homography is None or len(pts_src) == 0:
        return None
    if mask is not None:
        pts_src = pts_src[mask]
        pts_dst = pts_dst[mask]
    if len(pts_src) == 0:
        return None
    projected = cv2.perspectiveTransform(pts_src.reshape(-1, 1, 2), homography)
    diff = projected.reshape(-1, 2) - pts_dst.reshape(-1, 2)
    return float(np.mean(np.linalg.norm(diff, axis=1)))
