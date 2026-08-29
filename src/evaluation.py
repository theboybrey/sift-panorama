"""Metrics collection and table export. Numbers come only from measured runs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PAIR_COLUMNS = [
    "experiment",
    "method",
    "image_a",
    "image_b",
    "condition",
    "keypoints_a",
    "keypoints_b",
    "descriptor_dim",
    "candidate_matches",
    "initial_matches",
    "ransac_inliers",
    "ransac_outliers",
    "inlier_ratio",
    "mean_reproj_error",
    "feature_time_sec",
    "match_time_sec",
    "ransac_time_sec",
    "total_time_sec",
    "homography_status",
    "panorama_status",
    "overlap_mae",
    "panorama_success",
]


def rows_to_frame(rows: list[dict]) -> pd.DataFrame:
    frame = pd.DataFrame(rows)
    for column in PAIR_COLUMNS:
        if column not in frame.columns:
            frame[column] = None
    return frame[PAIR_COLUMNS]


def write_table(rows: list[dict], csv_path: Path, json_path: Path | None = None) -> pd.DataFrame:
    frame = rows_to_frame(rows)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(csv_path, index=False)
    if json_path is not None:
        json_path.write_text(json.dumps(rows, indent=2, default=_json_default))
    return frame


def _json_default(value):
    if hasattr(value, "tolist"):
        return value.tolist()
    return str(value)


def summarise_method(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    grouped = frame.groupby("method", as_index=False).agg(
        keypoints_a=("keypoints_a", "mean"),
        keypoints_b=("keypoints_b", "mean"),
        initial_matches=("initial_matches", "mean"),
        ransac_inliers=("ransac_inliers", "mean"),
        inlier_ratio=("inlier_ratio", "mean"),
        total_time_sec=("total_time_sec", "mean"),
        overlap_mae=("overlap_mae", "mean"),
        success_rate=("panorama_success", "mean"),
    )
    return grouped
