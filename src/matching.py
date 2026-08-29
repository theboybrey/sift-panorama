"""Nearest-neighbour descriptor matching with a Lowe-style ratio test.

SIFT descriptors are 128-D float vectors compared with Euclidean (L2)
distance. ORB descriptors are 256-bit binary strings compared with
Hamming distance. Using the wrong norm would make the matcher
mathematically inappropriate for the descriptor.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import cv2
import numpy as np

from src.config import LOWE_RATIO


@dataclass
class MatchResult:
    candidate_matches: int
    initial_matches: list
    num_initial_matches: int
    ratio: float
    elapsed_sec: float


def match_descriptors(
    descriptors_a: np.ndarray | None,
    descriptors_b: np.ndarray | None,
    norm_type: int,
    ratio: float = LOWE_RATIO,
) -> MatchResult:
    """k-NN matching (k=2) followed by Lowe's ratio test.

    The ratio test is well-known for SIFT. It is also a reasonable
    filter for ORB: a match is kept only when the nearest neighbour is
    distinctly closer than the second nearest, which removes many
    ambiguous correspondences before RANSAC.
    """
    start = time.perf_counter()
    if descriptors_a is None or descriptors_b is None:
        return MatchResult(0, [], 0, ratio, time.perf_counter() - start)
    if len(descriptors_a) < 2 or len(descriptors_b) < 2:
        return MatchResult(0, [], 0, ratio, time.perf_counter() - start)

    matcher = cv2.BFMatcher(norm_type, crossCheck=False)
    knn = matcher.knnMatch(descriptors_a, descriptors_b, k=2)

    candidate = 0
    good: list = []
    for pair in knn:
        if len(pair) < 2:
            continue
        candidate += 1
        best, second = pair
        if second.distance == 0:
            continue
        if best.distance < ratio * second.distance:
            good.append(best)

    good.sort(key=lambda m: m.distance)
    return MatchResult(
        candidate_matches=candidate,
        initial_matches=good,
        num_initial_matches=len(good),
        ratio=ratio,
        elapsed_sec=time.perf_counter() - start,
    )


def correspondences_from_matches(
    keypoints_a: list,
    keypoints_b: list,
    matches: list,
) -> tuple[np.ndarray, np.ndarray]:
    """Return Nx2 point arrays in image A and image B."""
    if not matches:
        return np.empty((0, 2), np.float32), np.empty((0, 2), np.float32)
    pts_a = np.float32([keypoints_a[m.queryIdx].pt for m in matches])
    pts_b = np.float32([keypoints_b[m.trainIdx].pt for m in matches])
    return pts_a, pts_b
