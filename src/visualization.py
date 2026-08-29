"""Saved figures for the report. Labels stay short and readable."""

from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np


def _bgr_to_rgb(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def save_bgr(path: str | Path, image: np.ndarray) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)


def save_keypoints(path: str | Path, image: np.ndarray, keypoints: list, title: str) -> None:
    canvas = cv2.drawKeypoints(
        image,
        keypoints,
        None,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    )
    _save_figure(path, canvas, title)


def save_matches(
    path: str | Path,
    image_a: np.ndarray,
    keypoints_a: list,
    image_b: np.ndarray,
    keypoints_b: list,
    matches: list,
    title: str,
    max_draw: int = 80,
) -> None:
    drawn = matches[:max_draw]
    canvas = cv2.drawMatches(
        image_a,
        keypoints_a,
        image_b,
        keypoints_b,
        drawn,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    _save_figure(path, canvas, title)


def save_before_after_matches(
    path: str | Path,
    image_a: np.ndarray,
    keypoints_a: list,
    image_b: np.ndarray,
    keypoints_b: list,
    matches: list,
    inlier_mask: np.ndarray | None,
    title: str,
    max_draw: int = 80,
) -> None:
    initial = matches[:max_draw]
    if inlier_mask is None:
        inliers = []
    else:
        inliers = [m for m, keep in zip(matches, inlier_mask) if keep][:max_draw]

    before = cv2.drawMatches(
        image_a, keypoints_a, image_b, keypoints_b, initial, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    after = cv2.drawMatches(
        image_a, keypoints_a, image_b, keypoints_b, inliers, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    axes[0].imshow(_bgr_to_rgb(before))
    axes[0].set_title(f"{title} — before RANSAC ({len(matches)} matches, showing {len(initial)})")
    axes[0].axis("off")
    axes[1].imshow(_bgr_to_rgb(after))
    inlier_count = 0 if inlier_mask is None else int(np.sum(inlier_mask))
    axes[1].set_title(f"{title} — after RANSAC ({inlier_count} inliers, showing {len(inliers)})")
    axes[1].axis("off")
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def save_side_by_side(path: str | Path, images: list[np.ndarray], titles: list[str], main_title: str) -> None:
    fig, axes = plt.subplots(1, len(images), figsize=(5 * len(images), 4))
    if len(images) == 1:
        axes = [axes]
    for axis, image, title in zip(axes, images, titles):
        axis.imshow(_bgr_to_rgb(image))
        axis.set_title(title)
        axis.axis("off")
    fig.suptitle(main_title)
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _save_figure(path: str | Path, image: np.ndarray, title: str) -> None:
    fig, axis = plt.subplots(figsize=(10, 6))
    axis.imshow(_bgr_to_rgb(image))
    axis.set_title(title)
    axis.axis("off")
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
