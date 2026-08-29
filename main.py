#!/usr/bin/env python3
"""Run the CSCD608 feature-matching and panorama experiments."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import DATA_ORIGINAL, DIR_TABLES, PRIMARY_IMAGES, ensure_result_dirs
from src.evaluation import summarise_method, write_table
from src.preprocessing import prepare_image


def inventory_dataset() -> list[dict]:
    rows = []
    notes = {
        "boat1.jpg": (
            "Leftmost waterfront view. Tall ship and embankment on the left; "
            "fortress/spire enter from the right. Consecutive overlap with boat2."
        ),
        "boat2.jpg": (
            "Centre view. Peter and Paul Fortress and golden spire are dominant. "
            "Overlaps boat1 on the left of the fortress and boat3 on the right."
        ),
        "boat3.jpg": (
            "Rightward view. Fortress/spire sit on the left; a long bridge and "
            "the opposite bank appear on the right. Consecutive overlap with boat2."
        ),
        "boat4.jpg": (
            "Further-right viewpoint used only for the wide-baseline experiment. "
            "Less overlap with boat1 than the adjacent pair."
        ),
    }
    for path in sorted(DATA_ORIGINAL.glob("*.jpg")):
        _, _, record = prepare_image(path)
        record.scene_notes = notes.get(path.name, "")
        overlap = "consecutive ~40-60% (visual)" if path.name in PRIMARY_IMAGES else "wide baseline vs boat1"
        row = record.to_dict()
        try:
            row["path"] = str(path.resolve().relative_to(ROOT))
        except ValueError:
            row["path"] = str(path)
        row["approximate_overlap"] = overlap
        row["image_type"] = "JPEG photograph"
        rows.append(row)
        print(
            f"  {record.filename:12s}  native {record.width}x{record.height}x{record.channels}  "
            f"working {record.working_width}x{record.working_height}  scale={record.scale:.3f}"
        )
    DIR_TABLES.mkdir(parents=True, exist_ok=True)
    (DIR_TABLES / "dataset_inventory.json").write_text(json.dumps(rows, indent=2))
    return rows


def run_selected(which: str) -> list[dict]:
    from experiments.feature_comparison import run_feature_comparison
    from experiments.illumination_experiment import run_illumination_experiment
    from experiments.rotation_experiment import run_rotation_experiment
    from experiments.scale_experiment import run_scale_experiment
    from experiments.viewpoint_experiment import run_viewpoint_experiment

    runners = {
        "compare": [("feature_comparison", run_feature_comparison)],
        "rotation": [("rotation", run_rotation_experiment)],
        "scale": [("scale", run_scale_experiment)],
        "viewpoint": [("viewpoint", run_viewpoint_experiment)],
        "illumination": [("illumination", run_illumination_experiment)],
        "all": [
            ("feature_comparison", run_feature_comparison),
            ("rotation", run_rotation_experiment),
            ("scale", run_scale_experiment),
            ("viewpoint", run_viewpoint_experiment),
            ("illumination", run_illumination_experiment),
        ],
    }
    if which not in runners:
        raise SystemExit(f"Unknown target: {which}")

    rows: list[dict] = []
    for name, fn in runners[which]:
        print(f"\n=== {name} ===")
        produced = fn()
        print(f"  recorded {len(produced)} result rows")
        rows.extend(produced)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="CSCD608 SIFT/ORB panorama experiments")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=["all", "compare", "rotation", "scale", "viewpoint", "illumination", "inventory"],
    )
    args = parser.parse_args()

    ensure_result_dirs()
    print("Dataset inventory")
    inventory_dataset()
    if args.target == "inventory":
        return

    rows = run_selected(args.target)
    frame = write_table(rows, DIR_TABLES / "all_results.csv", DIR_TABLES / "all_results.json")
    summary = summarise_method(frame)
    summary.to_csv(DIR_TABLES / "method_summary.csv", index=False)
    split_names = {
        "feature_comparison": "sift_vs_orb.csv",
        "rotation": "rotation.csv",
        "scale": "scale.csv",
        "viewpoint": "viewpoint.csv",
        "illumination": "illumination.csv",
    }
    for experiment, filename in split_names.items():
        subset = frame[frame["experiment"] == experiment]
        if not subset.empty:
            subset.to_csv(DIR_TABLES / filename, index=False)
    print("\n=== method summary (means over recorded rows) ===")
    print(summary.to_string(index=False))
    print(f"\nWrote {DIR_TABLES / 'all_results.csv'}")


if __name__ == "__main__":
    main()
