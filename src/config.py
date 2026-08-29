"""Project paths and experimentally justified default parameters."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
DATA_ORIGINAL = DATA_DIR / "original"
DATA_ROTATION = DATA_DIR / "rotation"
DATA_SCALE = DATA_DIR / "scale"
DATA_VIEWPOINT = DATA_DIR / "viewpoint"
DATA_ILLUMINATION = DATA_DIR / "illumination"

RESULTS_DIR = ROOT / "results"
DIR_KEYPOINTS = RESULTS_DIR / "keypoints"
DIR_INITIAL_MATCHES = RESULTS_DIR / "initial_matches"
DIR_RANSAC_MATCHES = RESULTS_DIR / "ransac_matches"
DIR_HOMOGRAPHIES = RESULTS_DIR / "homographies"
DIR_WARPED = RESULTS_DIR / "warped"
DIR_PANORAMAS = RESULTS_DIR / "panoramas"
DIR_TABLES = RESULTS_DIR / "tables"

PRIMARY_IMAGES = ["boat1.jpg", "boat2.jpg", "boat3.jpg"]
VIEWPOINT_WIDE_IMAGES = ["boat1.jpg", "boat4.jpg"]

# Working resolution. Source photos are 3888x2592 (~10 MP). Detecting
# features at native resolution is unnecessarily slow for this study and
# produces thousands of redundant keypoints on water/sky. Longest side
# 1200 px keeps structure visible while making experiments reproducible
# on a laptop.
MAX_DIM = 1200

# SIFT nfeatures=0 keeps every detected keypoint. ORB is capped because
# the detector itself requires a budget; 4000 is large enough to be
# competitive without exploding matching cost.
SIFT_NFEATURES = 0
ORB_NFEATURES = 4000

# Lowe ratio: 0.75 is the conventional compromise between the original
# 0.8 (more matches, more outliers) and a stricter 0.7.
LOWE_RATIO = 0.75

# Reprojection threshold in pixels at the working resolution. 5 px is
# large enough to tolerate discretisation and mild non-planarity of a
# distant outdoor scene, and small enough to reject gross mismatches.
RANSAC_REPROJ_THRESH = 5.0
RANSAC_MAX_ITERS = 2000
MIN_MATCHES_FOR_HOMOGRAPHY = 8

# Qualitative panorama-quality criteria used in the report.
QUALITY_CRITERIA = [
    "visual_continuity",
    "alignment_accuracy",
    "visible_seams",
    "ghosting",
    "distortion",
    "missing_regions",
    "successful_overlap",
    "structural_consistency",
]


def ensure_result_dirs() -> None:
    for path in (
        DIR_KEYPOINTS,
        DIR_INITIAL_MATCHES,
        DIR_RANSAC_MATCHES,
        DIR_HOMOGRAPHIES,
        DIR_WARPED,
        DIR_PANORAMAS,
        DIR_TABLES,
        DATA_ROTATION,
        DATA_SCALE,
        DATA_VIEWPOINT,
        DATA_ILLUMINATION,
    ):
        path.mkdir(parents=True, exist_ok=True)
