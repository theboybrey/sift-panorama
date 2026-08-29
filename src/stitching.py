"""Geometric warping and multi-image panorama construction.

The middle image is the reference frame. Homographies map the left and
right images into that frame. A global translation then shifts every
transform so that all warped corners lie in the positive quadrant of a
shared canvas.

Composition for sequential interpretation:

    left  --H_left-->  mid  <--H_right--  right
                         |
                    translation T
                         |
                      canvas

So the canvas maps are T @ H_left, T, and T @ H_right.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class StitchResult:
    panorama: np.ndarray | None
    warped_images: list[np.ndarray]
    masks: list[np.ndarray]
    canvas_size: tuple[int, int]
    overlap_mae: float | None
    status: str
    message: str = ""


def _image_corners(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    return np.float32([[0, 0], [width, 0], [width, height], [0, height]]).reshape(-1, 1, 2)


def _translation_for_corners(corner_sets: list[np.ndarray]) -> tuple[np.ndarray, int, int]:
    all_corners = np.concatenate(corner_sets, axis=0).reshape(-1, 2)
    xmin, ymin = np.floor(all_corners.min(axis=0)).astype(int)
    xmax, ymax = np.ceil(all_corners.max(axis=0)).astype(int)
    translation = np.array(
        [[1.0, 0.0, float(-xmin)], [0.0, 1.0, float(-ymin)], [0.0, 0.0, 1.0]],
        dtype=np.float64,
    )
    return translation, int(xmax - xmin), int(ymax - ymin)


def warp_to_canvas(image: np.ndarray, homography: np.ndarray, width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    warped = cv2.warpPerspective(image, homography, (width, height))
    mask = cv2.warpPerspective(np.ones(image.shape[:2], dtype=np.uint8) * 255, homography, (width, height))
    mask = (mask > 0).astype(np.uint8)
    return warped, mask


def _feather_blend(warped_images: list[np.ndarray], masks: list[np.ndarray]) -> np.ndarray:
    """Distance-transform feathering. Overlap pixels take a weighted average.

    This is not multi-band blending. Seams can remain if exposure differs.
    """
    height, width = warped_images[0].shape[:2]
    accum = np.zeros((height, width, 3), dtype=np.float64)
    weight_sum = np.zeros((height, width, 1), dtype=np.float64)

    for image, mask in zip(warped_images, masks):
        binary = (mask > 0).astype(np.uint8)
        if binary.max() == 0:
            continue
        dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
        weight = dist[:, :, None]
        accum += image.astype(np.float64) * weight
        weight_sum += weight

    weight_sum = np.maximum(weight_sum, 1e-6)
    blended = np.clip(accum / weight_sum, 0, 255).astype(np.uint8)
    coverage = (weight_sum[:, :, 0] > 1e-6).astype(np.uint8) * 255
    # Crop to the bounding box of valid pixels so the canvas is not mostly black.
    ys, xs = np.where(coverage > 0)
    if len(xs) == 0:
        return blended
    return blended[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]


def overlap_mae(warped_images: list[np.ndarray], masks: list[np.ndarray]) -> float | None:
    """Mean absolute intensity difference on pairwise overlaps. Lower is better."""
    errors = []
    for i in range(len(warped_images)):
        for j in range(i + 1, len(warped_images)):
            overlap = (masks[i] > 0) & (masks[j] > 0)
            if overlap.sum() < 100:
                continue
            a = cv2.cvtColor(warped_images[i], cv2.COLOR_BGR2GRAY).astype(np.float64)
            b = cv2.cvtColor(warped_images[j], cv2.COLOR_BGR2GRAY).astype(np.float64)
            errors.append(float(np.mean(np.abs(a[overlap] - b[overlap]))))
    if not errors:
        return None
    return float(np.mean(errors))


def stitch_with_homographies(
    images: list[np.ndarray],
    homographies_to_ref: list[np.ndarray],
    max_canvas: int = 8000,
) -> StitchResult:
    """Warp every image by its map-to-reference homography onto one canvas.

    `homographies_to_ref[i]` must map image i into the reference image's
    coordinates. The reference image itself should use the identity.
    """
    if len(images) != len(homographies_to_ref):
        raise ValueError("images and homographies must be the same length")
    if any(H is None for H in homographies_to_ref):
        return StitchResult(None, [], [], (0, 0), None, "missing_homography", "One or more homographies are None.")

    corner_sets = [
        cv2.perspectiveTransform(_image_corners(image), H)
        for image, H in zip(images, homographies_to_ref)
    ]
    translation, canvas_w, canvas_h = _translation_for_corners(corner_sets)
    if canvas_w <= 0 or canvas_h <= 0 or canvas_w > max_canvas or canvas_h > max_canvas:
        return StitchResult(
            None,
            [],
            [],
            (canvas_w, canvas_h),
            None,
            "invalid_canvas",
            f"Rejected canvas {canvas_w}x{canvas_h}. Homography is likely unstable.",
        )

    warped_images = []
    masks = []
    for image, H in zip(images, homographies_to_ref):
        warped, mask = warp_to_canvas(image, translation @ H, canvas_w, canvas_h)
        warped_images.append(warped)
        masks.append(mask)

    mae = overlap_mae(warped_images, masks)
    panorama = _feather_blend(warped_images, masks)
    return StitchResult(
        panorama=panorama,
        warped_images=warped_images,
        masks=masks,
        canvas_size=(canvas_w, canvas_h),
        overlap_mae=mae,
        status="ok",
    )


def stitch_pair(src: np.ndarray, dst: np.ndarray, H_src_to_dst: np.ndarray) -> StitchResult:
    identity = np.eye(3, dtype=np.float64)
    return stitch_with_homographies([src, dst], [H_src_to_dst, identity])


def stitch_three(
    left: np.ndarray,
    mid: np.ndarray,
    right: np.ndarray,
    H_left_to_mid: np.ndarray,
    H_right_to_mid: np.ndarray,
) -> StitchResult:
    identity = np.eye(3, dtype=np.float64)
    return stitch_with_homographies(
        [left, mid, right],
        [H_left_to_mid, identity, H_right_to_mid],
    )
