"""SIFT and ORB keypoint detection plus descriptor extraction."""

from __future__ import annotations

import time
from dataclasses import dataclass

import cv2
import numpy as np

from src.config import ORB_NFEATURES, SIFT_NFEATURES


@dataclass
class FeatureResult:
    method: str
    keypoints: list
    descriptors: np.ndarray | None
    num_keypoints: int
    descriptor_dim: int
    descriptor_dtype: str
    distance_norm: int
    elapsed_sec: float


def create_detector(method: str):
    method = method.upper()
    if method == "SIFT":
        return cv2.SIFT_create(nfeatures=SIFT_NFEATURES)
    if method == "ORB":
        return cv2.ORB_create(nfeatures=ORB_NFEATURES)
    raise ValueError(f"Unsupported method: {method}")


def detector_norm(method: str) -> int:
    """Distance metric that matches the descriptor type."""
    method = method.upper()
    if method == "SIFT":
        return cv2.NORM_L2
    if method == "ORB":
        return cv2.NORM_HAMMING
    raise ValueError(f"Unsupported method: {method}")


def detect_and_describe(gray: np.ndarray, method: str) -> FeatureResult:
    """Detect keypoints and compute descriptors. Time only this stage."""
    method = method.upper()
    detector = create_detector(method)
    start = time.perf_counter()
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    elapsed = time.perf_counter() - start

    if keypoints is None:
        keypoints = []
    descriptor_dim = 0 if descriptors is None else int(descriptors.shape[1])
    descriptor_dtype = "none" if descriptors is None else str(descriptors.dtype)

    return FeatureResult(
        method=method,
        keypoints=list(keypoints),
        descriptors=descriptors,
        num_keypoints=len(keypoints),
        descriptor_dim=descriptor_dim,
        descriptor_dtype=descriptor_dtype,
        distance_norm=detector_norm(method),
        elapsed_sec=elapsed,
    )
