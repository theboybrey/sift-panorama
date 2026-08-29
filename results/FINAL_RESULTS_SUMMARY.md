# Final results summary

All numbers below were produced by `python main.py all` and saved in `results/tables/`. They were not typed by hand.

Times are wall-clock seconds from `time.perf_counter` on the machine that ran the experiment. They will differ on another computer; the ranking is what matters.

Inlier ratio = RANSAC inliers / initial matches.

---

## SIFT vs ORB

Source: `results/experiments/feature_comparison.csv` (copy of `results/tables/sift_vs_orb.csv`).

| Method | Pair | Keypoints A | Keypoints B | Descriptor dim | Initial matches | RANSAC inliers | Inlier ratio | Feature time (s) | Match time (s) | RANSAC time (s) | Total time (s) | Overlap MAE | Panorama |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SIFT | boat1–boat2 | 2495 | 1748 | 128 | 777 | 700 | 0.901 | 0.064 | 0.007 | 0.001 | 0.123 | 16.98 | ok |
| SIFT | boat2–boat3 | 1748 | 1639 | 128 | 582 | 469 | 0.806 | 0.054 | 0.005 | 0.000 | 0.106 | 7.72 | ok |
| ORB | boat1–boat2 | 4000 | 3977 | 32 | 805 | 771 | 0.958 | 0.034 | 0.014 | 0.001 | 0.090 | 16.99 | ok |
| ORB | boat2–boat3 | 3977 | 3993 | 32 | 1110 | 956 | 0.861 | 0.016 | 0.013 | 0.001 | 0.076 | 6.96 | ok |

Three-image overlap MAE (from the composed mosaic rows in `all_results.csv`): SIFT 12.60, ORB 13.70.

---

## Rotation

Source: `results/experiments/rotation.csv`. `boat2` matched to a rotated `boat3`.

| Method | Angle | Keypoints (rotated) | Initial | Inliers | Ratio | Total time (s) | Overlap MAE | Success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SIFT | 15° | 1853 | 554 | 466 | 0.841 | 0.124 | 19.90 | yes |
| ORB | 15° | 4000 | 1050 | 837 | 0.797 | 0.092 | 19.80 | yes |
| SIFT | 30° | 1948 | 591 | 500 | 0.846 | 0.243 | 26.89 | yes |
| ORB | 30° | 4000 | 962 | 778 | 0.809 | 0.111 | 27.56 | yes |
| SIFT | 45° | 1998 | 598 | 487 | 0.814 | 0.191 | 33.75 | yes |
| ORB | 45° | 4000 | 1038 | 896 | 0.863 | 0.116 | 29.34 | yes |

Figures: `results/panoramas/sift_rot15_pair.png` … `sift_rot45_pair.png` and the matching `orb_rot*_pair.png`.

---

## Scale

Source: `results/experiments/scale.csv`. `boat2` matched to a scaled `boat3`.

| Method | Scale | Keypoints (scaled) | Initial | Inliers | Ratio | Total time (s) | Overlap MAE | Success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SIFT | 100% | 1639 | 582 | 469 | 0.806 | 0.100 | 7.72 | yes |
| ORB | 100% | 3993 | 1110 | 956 | 0.861 | 0.077 | 6.96 | yes |
| SIFT | 75% | 1160 | 448 | 379 | 0.846 | 0.076 | 6.86 | yes |
| ORB | 75% | 3612 | 859 | 785 | 0.914 | 0.052 | 8.77 | yes |
| SIFT | 50% | 551 | 242 | 206 | 0.851 | 0.051 | 6.73 | yes |
| ORB | 50% | 2553 | 530 | 489 | 0.923 | 0.032 | 8.53 | yes |

Figures: `results/panoramas/sift_scale50_pair.png`, `orb_scale50_pair.png`, and the 75/100 variants.

---

## Viewpoint

Source: `results/experiments/viewpoint.csv`.

| Method | Condition | Initial | Inliers | Ratio | Reproj (px) | Overlap MAE | Homography | Success |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| SIFT | adjacent (boat1–boat2) | 777 | 700 | 0.901 | 0.33 | 16.98 | ok | yes |
| ORB | adjacent (boat1–boat2) | 805 | 771 | 0.958 | 1.06 | 16.99 | ok | yes |
| SIFT | wide (boat1–boat4) | 27 | 5 | 0.185 | 0.62 | 47.33 | few_inliers | **no** |
| ORB | wide (boat1–boat4) | 21 | 5 | 0.238 | 0.14 | 72.62 | few_inliers | **no** |

Failure figures: `results/failures/sift_wide_baseline_failure.png`, `results/failures/orb_wide_baseline_failure.png`.

---

## Illumination

Source: `results/experiments/illumination.csv`. `boat2` matched to photometric variants of `boat3`.

| Method | Condition | Keypoints (variant) | Initial | Inliers | Ratio | Overlap MAE | Success |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| SIFT | original | 1639 | 582 | 469 | 0.806 | 7.72 | yes |
| ORB | original | 3993 | 1110 | 956 | 0.861 | 6.96 | yes |
| SIFT | darker | 721 | 309 | 229 | 0.741 | 41.95 | yes |
| ORB | darker | 2918 | 817 | 667 | 0.816 | 41.99 | yes |
| SIFT | brighter | 2169 | 508 | 421 | 0.829 | 64.43 | yes |
| ORB | brighter | 4000 | 951 | 821 | 0.863 | 64.54 | yes |
| SIFT | low contrast | 721 | 309 | 229 | 0.741 | 12.94 | yes |
| ORB | low contrast | 2918 | 817 | 667 | 0.816 | 12.91 | yes |
| SIFT | high contrast | 3214 | 408 | 340 | 0.833 | 24.31 | yes |
| ORB | high contrast | 4000 | 592 | 536 | 0.905 | 26.49 | yes |

The large overlap MAE on darker/brighter variants is mostly photometric (the pixels were deliberately re-exposed), not a collapsed alignment.

---

## Final panorama

Strongest valid three-image result (SIFT; lower combined overlap MAE):

`results/panoramas/final_panorama.png`

(copy of `results/panoramas/sift_three_image.png`)

ORB three-image result:

`results/panoramas/final_panorama_orb.png`

(copy of `results/panoramas/orb_three_image.png`)

Inputs used: `data/original/boat1.jpg`, `boat2.jpg`, `boat3.jpg`. Middle image (`boat2`) is the reference frame.

---

## Known limitations

- Wide-baseline pair boat1–boat4 fails for both methods (5 inliers). The mosaic is unusable. This is kept in `results/failures/`.
- A single homography approximates a wide outdoor scene by a plane, so the three-image mosaic has a slightly bowed horizon and empty canvas corners.
- Feather blending is single-band; seams can remain after rotation or exposure change.
- Open water and sky produce few useful keypoints.
- ORB’s 4000-keypoint cap and SIFT’s unlimited count make raw keypoint totals not strictly comparable.
- Times are machine-specific.
- Overlap percentages in the dataset inventory are visual estimates, not measured IoU.
