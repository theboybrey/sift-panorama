"""Image loading and the modest preparation used before feature extraction.

Operations are kept minimal on purpose. Each step has a concrete reason:
the exam asks for preparation, not a decorative enhancement pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path

import cv2
import numpy as np

from src.config import MAX_DIM


@dataclass
class ImageRecord:
    filename: str
    path: str
    width: int
    height: int
    channels: int
    dtype: str
    working_width: int
    working_height: int
    scale: float
    scene_notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def load_bgr(path: str | Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def resize_max_dim(image: np.ndarray, max_dim: int = MAX_DIM) -> tuple[np.ndarray, float]:
    """Downscale so the longest side is `max_dim`, preserving aspect ratio."""
    height, width = image.shape[:2]
    longest = max(height, width)
    if longest <= max_dim:
        return image.copy(), 1.0
    scale = max_dim / float(longest)
    new_size = (int(round(width * scale)), int(round(height * scale)))
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized, scale


def to_gray(image: np.ndarray) -> np.ndarray:
    """Convert BGR to grayscale. Both SIFT and ORB operate on intensity."""
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def prepare_image(path: str | Path, max_dim: int = MAX_DIM) -> tuple[np.ndarray, np.ndarray, ImageRecord]:
    """Load, resize if needed, and produce a grayscale working copy.

    Colour originals are preserved for visualisation and stitching.
    """
    path = Path(path)
    original = load_bgr(path)
    working, scale = resize_max_dim(original, max_dim=max_dim)
    gray = to_gray(working)
    record = ImageRecord(
        filename=path.name,
        path=str(path),
        width=int(original.shape[1]),
        height=int(original.shape[0]),
        channels=int(original.shape[2]) if original.ndim == 3 else 1,
        dtype=str(original.dtype),
        working_width=int(working.shape[1]),
        working_height=int(working.shape[0]),
        scale=float(scale),
    )
    return working, gray, record


def rotate_image(image: np.ndarray, angle_deg: float) -> np.ndarray:
    """Rotate about the image centre, expanding the canvas to avoid clipping."""
    height, width = image.shape[:2]
    center = (width / 2.0, height / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])
    new_w = int(height * sin + width * cos)
    new_h = int(height * cos + width * sin)
    matrix[0, 2] += (new_w / 2.0) - center[0]
    matrix[1, 2] += (new_h / 2.0) - center[1]
    return cv2.warpAffine(image, matrix, (new_w, new_h), flags=cv2.INTER_LINEAR)


def scale_image(image: np.ndarray, factor: float) -> np.ndarray:
    if factor <= 0:
        raise ValueError("scale factor must be positive")
    height, width = image.shape[:2]
    new_size = (max(1, int(round(width * factor))), max(1, int(round(height * factor))))
    interpolation = cv2.INTER_AREA if factor < 1.0 else cv2.INTER_LINEAR
    return cv2.resize(image, new_size, interpolation=interpolation)


def adjust_illumination(image: np.ndarray, mode: str) -> np.ndarray:
    """Create a controlled photometric variant of a colour image."""
    if mode == "original":
        return image.copy()
    if mode == "darker":
        return cv2.convertScaleAbs(image, alpha=0.55, beta=0)
    if mode == "brighter":
        return cv2.convertScaleAbs(image, alpha=1.35, beta=25)
    if mode == "low_contrast":
        return cv2.convertScaleAbs(image, alpha=0.55, beta=40)
    if mode == "high_contrast":
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        return cv2.cvtColor(cv2.merge((l_channel, a_channel, b_channel)), cv2.COLOR_LAB2BGR)
    raise ValueError(f"Unknown illumination mode: {mode}")
