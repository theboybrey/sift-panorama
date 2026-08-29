# CSCD608 Requirements Audit

Status is PASS only where source and/or generated evidence already exists.

| Requirement | Evidence | Status |
| --- | --- | --- |
| 3+ overlapping images | `data/original/boat1.jpg`, `boat2.jpg`, `boat3.jpg`; `results/panoramas/original_triplet.png`; `results/tables/dataset_inventory.json` | PASS |
| Different viewpoints | Left / centre / right waterfront sequence; `boat4.jpg` for wider baseline | PASS |
| Image preprocessing | `src/preprocessing.py` (`prepare_image`, resize max dim 1200, grayscale) | PASS |
| Feature detection | `src/features.py` `detect_and_describe`; `results/keypoints/` | PASS |
| Feature descriptors | SIFT 128-D float, ORB 32-byte binary in `results/tables/sift_vs_orb.csv` | PASS |
| Feature matching | `src/matching.py` BFMatcher + Lowe 0.75; L2 for SIFT, Hamming for ORB | PASS |
| Initial correspondences visualization | `results/matches/sift_initial_matches.png`, `orb_initial_matches.png`; `results/initial_matches/` | PASS |
| RANSAC | `src/homography.py` `cv2.findHomography(..., method=RANSAC, ransacReprojThreshold=5.0)` | PASS |
| Homography estimation | `results/homography/homography_results.txt`; `results/homographies/` | PASS |
| Image warping | `src/stitching.py` `warp_to_canvas`; `results/warped/`; `results/panoramas/*_warped_components.png` | PASS |
| Image alignment | Pair and three-image stitches in `results/panoramas/` | PASS |
| Panorama construction | `src/stitching.py` `stitch_three`; feather blend | PASS |
| 3-image panorama | `results/panoramas/final_panorama.png`, `sift_three_image.png`, `orb_three_image.png` | PASS |
| Before-RANSAC visualization | Top panel of `results/matches/sift_before_after_ransac.png` and `orb_before_after_ransac.png` | PASS |
| After-RANSAC visualization | Bottom panel of the same before/after figures | PASS |
| SIFT implementation | `src/features.py` `cv2.SIFT_create` | PASS |
| ORB implementation | `src/features.py` `cv2.ORB_create` | PASS |
| Keypoint counts | `results/experiments/feature_comparison.csv` columns `keypoints_a`, `keypoints_b` | PASS |
| Initial match counts | same file, `initial_matches` | PASS |
| RANSAC inlier counts | same file, `ransac_inliers` | PASS |
| Inlier ratio | `ransac_inliers / initial_matches` stored as `inlier_ratio` | PASS |
| Processing time | `feature_time_sec`, `match_time_sec`, `ransac_time_sec`, `total_time_sec` | PASS |
| Panorama quality comparison | overlap MAE + qualitative figures; SIFT 12.60 vs ORB 13.70 on the three-image mosaic | PASS |
| Rotation experiment | `experiments/rotation_experiment.py`; `results/experiments/rotation.csv`; `results/panoramas/*rot*` | PASS |
| Scale experiment | `experiments/scale_experiment.py`; `results/experiments/scale.csv`; `results/panoramas/*scale*` | PASS |
| Viewpoint experiment | `experiments/viewpoint_experiment.py`; `results/experiments/viewpoint.csv`; `results/failures/` | PASS |
| Illumination experiment | `experiments/illumination_experiment.py`; `results/experiments/illumination.csv`; `results/panoramas/*illum*` | PASS |
| Failure cases/results | wide baseline 5 inliers; `results/failures/` | PASS |
| Complete source code | `main.py`, `src/`, `experiments/` | PASS |
| Requirements/dependencies | `requirements.txt` (opencv-python, numpy, matplotlib, pandas) | PASS |
| README/execution instructions | `README.md` | PASS |

## Checklist

```text
CSCD608 REQUIREMENTS AUDIT

[PASS] 3+ overlapping images
[PASS] Different viewpoints
[PASS] Image preprocessing
[PASS] Feature detection
[PASS] Feature descriptors
[PASS] Feature matching
[PASS] Initial correspondences visualization
[PASS] RANSAC
[PASS] Homography estimation
[PASS] Image warping
[PASS] Image alignment
[PASS] Panorama construction
[PASS] 3-image panorama
[PASS] Before-RANSAC visualization
[PASS] After-RANSAC visualization
[PASS] SIFT implementation
[PASS] ORB implementation
[PASS] Keypoint counts
[PASS] Initial match counts
[PASS] RANSAC inlier counts
[PASS] Inlier ratio
[PASS] Processing time
[PASS] Panorama quality comparison
[PASS] Rotation experiment
[PASS] Scale experiment
[PASS] Viewpoint experiment
[PASS] Illumination experiment
[PASS] Failure cases/results
[PASS] Complete source code
[PASS] Requirements/dependencies
[PASS] README/execution instructions
```

Counts: PASS 31 · PARTIAL 0 · MISSING 0
