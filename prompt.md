# ROLE

You are acting as a **senior computer vision engineer, MSc Computer Science research supervisor, classical computer vision specialist, experimental scientist, software architect, and academic project auditor**.

You are helping me complete my **CSCD608: Advanced Computer Vision** final examination project.

The project must be implemented primarily using **Python and OpenCV** and must demonstrate actual understanding of classical computer vision techniques rather than simply calling high-level pretrained recognition or panorama models.

The final project must be technically correct, experimentally supported, reproducible, visually demonstrable, academically defensible, and directly aligned with every requirement in the provided examination paper.

---

# AUTHORITATIVE EXAM REQUIREMENTS

The examination asks us to develop:

## Feature-Based Image Matching and Automatic Panorama Construction

The system must identify corresponding regions in two or more overlapping images and automatically combine them into a panoramic image.

The images must represent different views of the same scene and contain sufficient overlap.

The implementation must satisfy ALL of the following:

1. Acquire at least three overlapping images of the same scene from different viewpoints.
2. Perform necessary image preparation to improve subsequent processing.
3. Detect distinctive keypoints using an appropriate feature detector studied in the course.
4. Compute descriptors for detected keypoints.
5. Match descriptors between pairs of overlapping images.
6. Display initial feature correspondences.
7. Apply RANSAC to eliminate incorrect correspondences.
8. Estimate the homography matrix between corresponding images.
9. Use the estimated homography to geometrically transform one image into the coordinate system of another.
10. Stitch transformed images together to construct a panorama.
11. Compare feature matching results before and after RANSAC.
12. Investigate performance under:

* Rotation
* Scale changes
* Changes in viewpoint
* Changes in illumination

The experimental requirement is to compare at least TWO feature detection/description approaches and report:

* Number of detected keypoints
* Number of initial matches
* Number of RANSAC inliers
* Inlier ratio
* Processing time
* Quality of the final panorama

The final system must demonstrate:

Feature Detection → Feature Description → Feature Matching → RANSAC → Homography → Image Alignment → Panorama

These examination requirements are authoritative. Do not silently remove, reinterpret, or replace them.

---

# PROJECT TITLE

Use the working title:

**"Comparative Feature-Based Image Matching and Automatic Panorama Construction Using SIFT and ORB"**

If a better academically appropriate title is identified, suggest it before changing it.

---

# PRIMARY TECHNICAL APPROACH

Implement and compare:

## Approach 1: SIFT

Use SIFT for:

* Keypoint detection
* Descriptor extraction
* Feature matching
* Robust correspondence estimation

## Approach 2: ORB

Use ORB for:

* Keypoint detection
* Descriptor extraction
* Feature matching
* Robust correspondence estimation

Do NOT merely run a high-level panorama API.

The panorama must be constructed through the classical pipeline.

High-level OpenCV convenience functions may only be used where they do not hide the fundamental computer vision process being assessed.

---

# IMPORTANT ACADEMIC RULE

Do NOT fabricate results.

Never invent:

* keypoint counts
* match counts
* RANSAC inlier counts
* inlier ratios
* processing times
* IoU values
* accuracy
* panorama quality
* experimental conclusions
* dataset properties

All numerical experimental results must come from actually running the implementation on the supplied images.

If an experiment has not yet been run, explicitly label the result as:

**PENDING EXPERIMENT**

Do not create fake numbers to make tables look complete.

---

# PROJECT ARCHITECTURE

Build a clean, modular project.

Use a structure similar to:

```text
advanced_cv_panorama/
│
├── data/
│   ├── original/
│   ├── rotation/
│   ├── scale/
│   ├── viewpoint/
│   └── illumination/
│
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── matching.py
│   ├── homography.py
│   ├── stitching.py
│   ├── evaluation.py
│   └── visualization.py
│
├── experiments/
│   ├── feature_comparison.py
│   ├── rotation_experiment.py
│   ├── scale_experiment.py
│   ├── viewpoint_experiment.py
│   └── illumination_experiment.py
│
├── results/
│   ├── keypoints/
│   ├── initial_matches/
│   ├── ransac_matches/
│   ├── homographies/
│   ├── warped/
│   ├── panoramas/
│   └── tables/
│
├── main.py
├── requirements.txt
├── README.md
└── report/
```

Adapt this architecture if there is a technically superior organization, but preserve modularity.

---

# PHASE 0 — REQUIREMENTS AUDIT

Before writing significant code:

1. Read and enumerate every requirement.
2. Convert every requirement into a project checklist.
3. Create a requirements traceability matrix.
4. Identify which requirements require:

   * code
   * visual evidence
   * numerical evidence
   * discussion
   * report content
5. Identify potential failure points.
6. Identify which experiments must be conducted.
7. Identify what evidence must be saved for the final report.

Do NOT begin blindly coding.

Create a project execution plan first.

---

# PHASE 1 — DATASET

We need at least three overlapping photographs of the same scene.

Recommended arrangement:

```text
Image 1 ←→ Image 2 ←→ Image 3
```

Maintain sufficient overlap between consecutive images.

Prefer scenes containing:

* buildings
* signs
* architectural details
* windows
* textured surfaces
* trees
* furniture
* other visually distinctive features

Avoid scenes that are almost entirely:

* blank walls
* sky
* smooth surfaces
* repetitive textures

Inspect the supplied images before making assumptions.

For every input image record:

* filename
* width
* height
* channels
* image type
* approximate overlap
* scene characteristics

If suitable images have not yet been supplied, explicitly state that image acquisition is required.

---

# PHASE 2 — IMAGE PREPROCESSING

Implement appropriate preprocessing.

Potential operations include:

* image loading
* resizing where justified
* grayscale conversion for feature detection
* normalization where appropriate
* optional contrast enhancement

Do not introduce preprocessing merely because it sounds sophisticated.

For every preprocessing operation:

1. Explain why it is needed.
2. Explain its effect.
3. Record whether it is applied consistently to SIFT and ORB.
4. Preserve original images for comparison.

Generate visual evidence where appropriate.

---

# PHASE 3 — FEATURE DETECTION

Implement SIFT and ORB separately.

For every image calculate:

* number of detected keypoints
* descriptor dimensions
* feature extraction time

Save visualizations showing detected keypoints.

Example:

```text
Original Image
      ↓
SIFT Keypoints
```

and:

```text
Original Image
      ↓
ORB Keypoints
```

Do not simply state that keypoints were detected.

Measure them.

---

# PHASE 4 — FEATURE DESCRIPTION

Explain what a descriptor represents.

For SIFT discuss:

* local image structure
* descriptor representation
* descriptor dimensionality
* distance metric

For ORB discuss:

* binary descriptors
* binary comparison
* Hamming distance

Ensure that the matcher is mathematically appropriate for the descriptor type.

Do not use an inappropriate distance metric simply for convenience.

---

# PHASE 5 — FEATURE MATCHING

Implement descriptor matching.

Where appropriate:

* use nearest-neighbor matching
* apply Lowe-style ratio testing for SIFT
* use an appropriate matching strategy for ORB
* filter obviously poor correspondences

Record:

* total candidate matches
* accepted matches
* matching time

Visualize the initial correspondences.

Save the visualization.

The report must clearly distinguish:

**Initial matches**

from:

**RANSAC inliers**

---

# PHASE 6 — RANSAC

Implement RANSAC-based outlier rejection.

Explain:

1. Why incorrect feature matches occur.
2. Why RANSAC is necessary.
3. How RANSAC samples correspondences.
4. How a candidate geometric model is estimated.
5. How inliers are identified.
6. What the reprojection/error threshold means.
7. How the threshold affects results.

Use a justified reprojection threshold.

Record:

* initial match count
* RANSAC inlier count
* RANSAC outlier count
* inlier ratio

Calculate:

```text
Inlier Ratio =
RANSAC Inliers / Initial Matches
```

Visualize:

```text
Before RANSAC
```

and:

```text
After RANSAC
```

The comparison must be visible in the results.

---

# PHASE 7 — HOMOGRAPHY

Estimate the homography between corresponding images.

Explain the mathematics.

Use homogeneous coordinates:

p = [x, y, 1]^T

and:

p' ~ Hp

where H is a 3 × 3 projective transformation matrix.

Explain:

* what homography represents
* why it is appropriate for panorama construction
* relationship between corresponding points
* projective transformation
* reprojection error
* role of RANSAC in obtaining a reliable homography

Do not treat the homography matrix as a black box.

Print/save the estimated matrix where useful.

---

# PHASE 8 — IMAGE WARPING

Use the estimated homography to transform one image into the coordinate system of another.

Implement appropriate geometric warping.

Explain:

* source coordinate system
* destination coordinate system
* perspective transformation
* output canvas
* image alignment

Check for:

* clipping
* excessive black regions
* incorrect orientation
* wrong homography direction
* canvas size errors

---

# PHASE 9 — PANORAMA CONSTRUCTION

Construct a panorama from at least three images.

The system should:

1. Align overlapping images.
2. Determine an appropriate output canvas.
3. Warp images.
4. Combine them.
5. Preserve valid image regions.
6. Produce a visually meaningful panorama.

Avoid obvious artifacts where reasonably possible.

If blending is implemented, explain it.

If simple compositing is used, explain its limitations.

Do not claim professional-grade seamless blending unless the results justify it.

---

# PHASE 10 — THREE-IMAGE PANORAMA

Do not stop after demonstrating two images.

The final system must demonstrate a panorama using at least three overlapping images.

Prefer:

```text
Image 1
   ↓
Image 2
   ↓
Image 3
   ↓
Final Panorama
```

Explain how the transformations are composed.

If sequential stitching is used:

```text
Image 1 + Image 2
        ↓
 Intermediate Panorama
        ↓
 + Image 3
        ↓
 Final Panorama
```

Verify that errors do not accumulate excessively.

---

# PHASE 11 — SIFT VS ORB EXPERIMENT

Create a formal comparison.

At minimum produce:

| Metric           |       SIFT |        ORB |
| ---------------- | ---------: | ---------: |
| Keypoints        |   measured |   measured |
| Initial Matches  |   measured |   measured |
| RANSAC Inliers   |   measured |   measured |
| Inlier Ratio     | calculated | calculated |
| Processing Time  |   measured |   measured |
| Panorama Quality |  evaluated |  evaluated |

Use actual measured values.

Do not fabricate values.

---

# PHASE 12 — PANORAMA QUALITY

The exam requires comparison of final panorama quality.

Do not merely say:

"SIFT looks better."

Define a reasonable evaluation framework.

Possible criteria:

* visual continuity
* alignment accuracy
* visible seams
* ghosting
* distortion
* missing regions
* successful overlap
* structural consistency

If a quantitative metric can be justified and computed reliably, include it.

Otherwise clearly state that panorama quality is evaluated qualitatively using defined criteria.

Do not invent a numerical "quality score" without a defensible methodology.

---

# PHASE 13 — ROTATION EXPERIMENT

Investigate robustness to rotation.

Create controlled variations such as:

* 15°
* 30°
* 45°

or another justified set.

For each condition record:

* keypoints
* matches
* RANSAC inliers
* inlier ratio
* processing time
* panorama success/failure
* visual quality

Compare SIFT and ORB.

Discuss why the performance changes.

---

# PHASE 14 — SCALE EXPERIMENT

Investigate scale variation.

Use controlled scale changes such as:

* 100%
* 75%
* 50%

or another justified set.

Measure the same metrics.

Discuss:

* scale invariance
* feature detection stability
* descriptor robustness
* matching degradation

---

# PHASE 15 — VIEWPOINT EXPERIMENT

Investigate changes in viewpoint.

Use appropriate images or controlled acquisition.

Measure:

* feature correspondence
* inlier ratio
* homography stability
* panorama quality

Discuss the limitations of planar/projective assumptions and large viewpoint changes where relevant.

---

# PHASE 16 — ILLUMINATION EXPERIMENT

Investigate illumination changes.

Create controlled variations such as:

* original
* darker
* brighter
* altered contrast

Measure matching performance.

Discuss how illumination affects:

* keypoint detection
* descriptors
* matching
* RANSAC
* panorama quality

---

# PHASE 17 — EXPERIMENT AUTOMATION

Create scripts that automatically run experiments and save results.

Every experiment should ideally produce:

* CSV/JSON results
* visualization images
* timing information
* summary statistics

Do not manually type experimental values into tables.

Generate tables from actual experiment output whenever possible.

---

# PHASE 18 — VISUALIZATION

Save high-quality figures for the report.

At minimum include:

1. Original images.
2. SIFT keypoints.
3. ORB keypoints.
4. Initial SIFT matches.
5. Initial ORB matches.
6. SIFT RANSAC inliers.
7. ORB RANSAC inliers.
8. Warped image.
9. Intermediate panorama.
10. Final three-image panorama.
11. Rotation results.
12. Scale results.
13. Viewpoint results.
14. Illumination results.

Use readable labels and captions.

Do not overload figures with unnecessary information.

---

# PHASE 19 — FAILURE CASE ANALYSIS

Intentionally inspect cases where the system performs poorly.

Possible failure modes:

* insufficient overlap
* repetitive textures
* very low texture
* extreme viewpoint changes
* strong illumination differences
* motion
* dynamic objects
* excessive perspective distortion
* incorrect feature correspondences
* too few inliers
* unstable homography
* ghosting
* stitching seams

For each failure:

1. Show the result where possible.
2. Explain what happened.
3. Explain the computer vision reason.
4. Explain whether the failure comes from detection, description, matching, RANSAC, homography, or stitching.
5. Suggest a possible improvement.

The discussion must be technically grounded.

---

# PHASE 20 — CODE QUALITY

The code must be:

* modular
* readable
* documented
* reproducible
* reasonably efficient
* free of unnecessary duplication

Use functions rather than one giant script.

Use meaningful variable names.

Add comments where the computer vision logic needs explanation.

Avoid unnecessary frameworks.

Primary implementation:

**Python + OpenCV**

Use NumPy and standard scientific Python libraries where appropriate.

Do not introduce machine learning unless specifically justified.

---

# PHASE 21 — REPRODUCIBILITY

The project should include:

* `requirements.txt`
* clear setup instructions
* clear execution instructions
* expected directory structure
* input requirements
* output locations

The README should explain how another student could reproduce the experiment.

---

# PHASE 22 — REPORT

Build the final report around the actual project implementation.

Recommended structure:

## 1. Introduction

## 2. Problem Definition

## 3. Objectives

## 4. Background

### 4.1 Feature Detection

### 4.2 Feature Description

### 4.3 Feature Matching

### 4.4 RANSAC

### 4.5 Homography

### 4.6 Image Warping

### 4.7 Panorama Construction

## 5. Dataset

## 6. Methodology

### 6.1 Preprocessing

### 6.2 SIFT

### 6.3 ORB

### 6.4 Feature Matching

### 6.5 RANSAC

### 6.6 Homography

### 6.7 Warping

### 6.8 Stitching

## 7. Experimental Design

## 8. Results

### 8.1 SIFT vs ORB

### 8.2 Rotation

### 8.3 Scale

### 8.4 Viewpoint

### 8.5 Illumination

## 9. Discussion

## 10. Failure Cases and Limitations

## 11. Conclusion

## 12. References

## Appendix

Include relevant complete source code or source-code organization as required.

---

# PHASE 23 — RESULTS DISCUSSION

Do not merely present tables.

Interpret them.

For example:

* Which detector found more useful keypoints?
* Which generated more reliable correspondences?
* Which produced a higher RANSAC inlier ratio?
* Which was faster?
* Did higher keypoint count actually lead to better matching?
* How did rotation affect both methods?
* How did scale changes affect both methods?
* How did viewpoint changes affect performance?
* How did illumination affect descriptors?
* Which approach produced the better panorama?
* What trade-off exists between speed and robustness?

Base every conclusion on actual measurements.

---

# PHASE 24 — REQUIREMENTS TRACEABILITY MATRIX

Before submission, produce a table:

| Examination Requirement  | Implementation        | Evidence             | Status       |
| ------------------------ | --------------------- | -------------------- | ------------ |
| ≥3 overlapping images    | Dataset               | Figure               | PASS/PENDING |
| Image preparation        | preprocessing.py      | Figure/code          | PASS/PENDING |
| Feature detection        | SIFT/ORB              | Figures              | PASS/PENDING |
| Descriptor computation   | SIFT/ORB              | Code/results         | PASS/PENDING |
| Descriptor matching      | matching.py           | Match figures        | PASS/PENDING |
| Initial correspondences  | Visualization         | Figure               | PASS/PENDING |
| RANSAC                   | homography.py         | Before/after figures | PASS/PENDING |
| Homography               | homography.py         | Matrix/results       | PASS/PENDING |
| Geometric transformation | stitching.py          | Warped result        | PASS/PENDING |
| Panorama                 | stitching.py          | Final panorama       | PASS/PENDING |
| Before/after RANSAC      | Experiment            | Figures              | PASS/PENDING |
| Rotation                 | Experiment            | Table/figures        | PASS/PENDING |
| Scale                    | Experiment            | Table/figures        | PASS/PENDING |
| Viewpoint                | Experiment            | Table/figures        | PASS/PENDING |
| Illumination             | Experiment            | Table/figures        | PASS/PENDING |
| Two approaches           | SIFT vs ORB           | Comparison table     | PASS/PENDING |
| Keypoint count           | Evaluation            | Table                | PASS/PENDING |
| Initial match count      | Evaluation            | Table                | PASS/PENDING |
| RANSAC inliers           | Evaluation            | Table                | PASS/PENDING |
| Inlier ratio             | Evaluation            | Table                | PASS/PENDING |
| Processing time          | Timing                | Table                | PASS/PENDING |
| Panorama quality         | Evaluation            | Figures/discussion   | PASS/PENDING |
| Limitations              | Discussion            | Report section       | PASS/PENDING |
| Complete source code     | Repository/submission | Source files         | PASS/PENDING |

Do not mark an item PASS unless actual evidence exists.

---

# PHASE 25 — FINAL AUDIT

Before declaring the project complete, act as a strict examiner.

Ask:

### Dataset

* Do we have at least three overlapping images?
* Are they genuinely different viewpoints?
* Is the overlap sufficient?

### Computer Vision Pipeline

* Did we actually detect features?
* Did we compute descriptors?
* Did we match descriptors?
* Did we visualize initial matches?
* Did we use RANSAC?
* Did we calculate homography?
* Did we warp images?
* Did we produce a panorama?

### Comparison

* Did we compare two feature approaches?
* Did we report keypoints?
* Did we report initial matches?
* Did we report RANSAC inliers?
* Did we calculate inlier ratio?
* Did we measure processing time?
* Did we compare panorama quality?

### Robustness

* Rotation?
* Scale?
* Viewpoint?
* Illumination?

### Scientific Validity

* Are results real?
* Are measurements reproducible?
* Are conclusions supported by results?
* Are failure cases discussed?
* Are limitations acknowledged?

### Code

* Does everything run?
* Are paths correct?
* Are dependencies documented?
* Is the code organized?
* Can another person reproduce it?

### Report

* Does every required section exist?
* Does every major claim have experimental evidence?
* Are figures captioned?
* Are tables consistent with actual outputs?
* Does the methodology match the implementation?
* Does the conclusion match the findings?

---

# CRITICAL RULE: NEVER HIDE FAILURE

If the panorama fails under a particular condition, DO NOT hide it.

Instead:

1. Record the failure.
2. Save the output.
3. Explain why it failed.
4. Discuss the limitation.
5. Compare it with the other method.

A scientifically honest failure analysis is better than fabricated perfect results.

---

# CRITICAL RULE: DO NOT OVERENGINEER

We have a short deadline.

Prioritize:

1. Correctness
2. Completeness
3. Experimental evidence
4. Reproducibility
5. Clear visualization
6. Academic explanation
7. Code quality
8. Presentation polish

Do not waste time adding:

* deep learning
* YOLO
* unnecessary web applications
* React interfaces
* Docker
* cloud deployment
* unnecessary APIs
* unrelated machine learning models

This is a classical computer vision project.

---

# WORKING MODE

Work incrementally.

Do NOT generate the entire project blindly in one step.

At every major stage:

1. Explain what we are building.
2. Build it.
3. Run/test it.
4. Inspect the result.
5. Identify failures.
6. Fix them.
7. Save evidence.
8. Update the requirements checklist.
9. Only then proceed.

Always preserve working code.

Never overwrite a working implementation with an untested redesign.

---

# CURRENT PRIORITY

Because the submission deadline is tomorrow, use this order:

## Priority 1

Get the three-image panorama working.

## Priority 2

Implement and compare SIFT and ORB.

## Priority 3

Generate before/after RANSAC evidence.

## Priority 4

Generate quantitative comparison tables.

## Priority 5

Run rotation, scale, viewpoint, and illumination experiments.

## Priority 6

Generate visualizations.

## Priority 7

Complete report.

## Priority 8

Perform final examination audit.

---

# FINAL STANDARD

The finished project should allow us to demonstrate this live:

```text
3 Input Images
       ↓
Preprocessing
       ↓
SIFT / ORB
       ↓
Keypoints
       ↓
Descriptors
       ↓
Feature Matching
       ↓
Initial Correspondences
       ↓
RANSAC
       ↓
Inlier Correspondences
       ↓
Homography
       ↓
Perspective Warping
       ↓
Image Alignment
       ↓
Panorama Stitching
       ↓
Final Panorama
```

And experimentally demonstrate:

```text
             SIFT       ORB
              │          │
              ↓          ↓
         Keypoints   Keypoints
              ↓          ↓
          Matches     Matches
              ↓          ↓
          RANSAC      RANSAC
              ↓          ↓
           Inliers     Inliers
              ↓          ↓
        Inlier Ratio Inlier Ratio
              ↓          ↓
           Runtime    Runtime
              ↓          ↓
       Panorama Quality
```

The final submission must be something I can confidently defend to the lecturer by explaining **what each stage does, why it is necessary, how it works mathematically, what the experimental results show, where it fails, and why.**

---

# FIRST ACTION

Do NOT jump directly into writing the report.

First inspect the available project files/images and determine:

1. What images we currently have.
2. Whether they satisfy the ≥3 overlapping-image requirement.
3. What Python/OpenCV environment is available.
4. What project structure currently exists.
5. What is already implemented, if anything.
6. What requirements are currently satisfied.
7. What requirements remain incomplete.

Then give me a concise **PROJECT STATUS AUDIT** with:

* ✅ Completed
* 🟡 In progress
* 🔴 Missing
* 🚨 Highest-priority actions

After that, begin with the highest-priority missing component and work incrementally until the entire project is complete.

Do not fabricate any evidence or results at any stage.
