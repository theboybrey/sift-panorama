# Feature-Based Image Matching and Automatic Panorama Construction Using SIFT and ORB

CSCD608 Advanced Computer Vision. Classical Python + OpenCV pipeline. No high-level `Stitcher` API.

**Repository:** https://github.com/theboybrey/sift-panorama

```text
Input Images → Preprocess → SIFT / ORB → Descriptors → Matching
    → Initial Matches → RANSAC → Homography → Warp → Panorama
```

Runnable source lives at the package root (`main.py`, `src/`, `experiments/`) so `data/` and `results/` stay on relative paths.

## Environment

- Python 3.13 recommended (OpenCV wheels were used on 3.13; system 3.14 may not have `cv2`)
- Packages in `requirements.txt`: `opencv-python`, `numpy`, `matplotlib`, `pandas`

## Installation

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows: `py -3.13 -m venv .venv` then `.venv\Scripts\activate`.

## Dataset

`data/original/`

| File | Role |
| --- | --- |
| `boat1.jpg` | Left view |
| `boat2.jpg` | Centre / reference |
| `boat3.jpg` | Right view |
| `boat4.jpg` | Wider baseline (viewpoint experiment only) |

Source note: `data/original/SOURCE.md`. Native size 3888×2592. The pipeline resizes so the longest side is 1200 px before detection.

Rotation, scale, and illumination variants are generated into `data/rotation/`, `data/scale/`, and `data/illumination/` when those experiments run.

## Running the system

From this directory, with the venv active:

```bash
python main.py all
```

That inventories the images, compares SIFT and ORB, builds the three-image panoramas, and runs rotation, scale, viewpoint, and illumination experiments.

Single targets:

```bash
python main.py inventory
python main.py compare
python main.py rotation
python main.py scale
python main.py viewpoint
python main.py illumination
```

## Experiments

| Command | Script | Measured table |
| --- | --- | --- |
| `python main.py compare` | `experiments/feature_comparison.py` | `results/experiments/feature_comparison.csv` |
| `python main.py rotation` | `experiments/rotation_experiment.py` | `results/experiments/rotation.csv` |
| `python main.py scale` | `experiments/scale_experiment.py` | `results/experiments/scale.csv` |
| `python main.py viewpoint` | `experiments/viewpoint_experiment.py` | `results/experiments/viewpoint.csv` |
| `python main.py illumination` | `experiments/illumination_experiment.py` | `results/experiments/illumination.csv` |

## Outputs

| Path | Contents |
| --- | --- |
| `results/panoramas/final_panorama.png` | Three-image SIFT panorama (strongest valid mosaic) |
| `results/panoramas/final_panorama_orb.png` | Three-image ORB panorama |
| `results/keypoints/` | Keypoint figures |
| `results/matches/` | Examiner-named initial and before/after RANSAC copies |
| `results/initial_matches/` | Full initial-match set |
| `results/ransac_matches/` | Full before/after RANSAC set |
| `results/homography/homography_results.txt` | Three-image homography matrices |
| `results/homographies/` | All estimated matrices |
| `results/warped/` | Warped source images |
| `results/failures/` | Wide-baseline collapse (kept on purpose) |
| `results/experiments/` | Measured CSV tables |
| `results/FINAL_RESULTS_SUMMARY.md` | Consolidated measured numbers |
| `results/REQUIREMENTS_AUDIT.md` | Exam-requirement checklist |

## Reproducibility

- Paths are relative to this directory (`src/config.py` sets `ROOT` from the file location).
- Do not invent table values. After a run, read the CSVs.
- A panorama is counted successful only when RANSAC status is `ok` (≥8 inliers).
- The wide-baseline pair (`boat1` vs `boat4`) is an observed failure (5 inliers). That is expected evidence, not a missing file.
- Times will change on another machine; counts should be close if OpenCV versions match.

The written examination report was submitted separately to the LMS and is not required in this code package.
