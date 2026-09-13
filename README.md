# The Serve Admissibility Envelope

## How Speed and Spin Constrain Legal Tennis Serves

A computational study of nonlinear tennis-ball flight, service-box constraints, admissible launch regions, sensitivity to speed and spin, uncertainty, and professional serve-speed data.

---

## Overview

A tennis serve is simultaneously a mechanical, aerodynamic, geometric, and constrained dynamical system.

A server chooses an initial launch state consisting of quantities such as:

- launch speed,
- launch direction,
- launch height,
- spin magnitude,
- spin axis,
- and target direction.

Once the ball leaves the racket, however, the trajectory is no longer freely controlled.

Gravity accelerates the ball downward. Aerodynamic drag reduces its forward speed. Spin generates a Magnus force that bends the trajectory. At the same time, the serve must satisfy geometric constraints imposed by the tennis court:

1. the ball must clear the net,
2. the first landing point must occur between the net and the service line,
3. the first landing point must lie inside the correct service box.

This project asks:

> **Given a serve speed, what set of launch conditions can physically produce a legal tennis serve, and how does this feasible set change with speed, spin, launch direction, and uncertainty?**

Rather than treating a serve as a single trajectory, this project treats legality as a **constrained nonlinear dynamical-system problem**.

The central object is the **serve admissibility envelope**:

\[
\mathcal{A}(v,\omega,h)
\]

the set of launch conditions that produce trajectories satisfying all modeled service constraints for a given serve speed \(v\), spin state \(\omega\), and contact height \(h\).

The project combines:

- numerical integration,
- analytical verification,
- aerodynamic drag,
- three-dimensional Magnus acceleration,
- court geometry,
- nonlinear boundary solving,
- continuation-style parameter sweeps,
- sensitivity analysis,
- uncertainty analysis,
- statistical inference,
- and empirical analysis of professional serve speeds.

---

# Research Question

The primary research question is:

> **How do serve speed and spin constrain the set of launch conditions that can produce a legal tennis serve?**

This can be decomposed into several computational questions:

1. How does the legal launch-angle interval change with serve speed?
2. How does spin alter the net-clearance and service-line boundaries?
3. How does the admissible angular width vary with spin?
4. How does lateral launch direction interact with spin?
5. Which modeled uncertainties most strongly affect serve legality?
6. How does the modeled admissible region compare with the empirical distribution of professional serve speeds?
7. What can be concluded from the comparison, and what cannot?

---

# Scientific Contribution

This project is not intended to claim the first physical model of a tennis ball, the first use of drag or Magnus forces in tennis, or the first three-dimensional trajectory model.

Those areas have substantial prior literature.

The contribution here is instead the formulation and systematic analysis of **serve legality as an admissibility-envelope problem**.

Many trajectory studies ask a question such as:

> Given a measured or estimated launch state, what trajectory does the ball follow?

This project asks a complementary forward question:

> Given a serve speed, spin state, and court geometry, **which launch states are physically admissible at all?**

The resulting object is a constrained region in launch-condition space rather than a single trajectory.

The project therefore connects:

**initial conditions**

\[
\longrightarrow
\]

**nonlinear ball dynamics**

\[
\longrightarrow
\]

**court constraints**

\[
\longrightarrow
\]

**admissible launch region**

and then studies how that region changes as the physical parameters change.

---

# Physical Model

The ball is modeled as a particle subject to gravity, aerodynamic drag, and Magnus lift.

The governing equation is

\[
m\dot{\mathbf v}
=
m\mathbf g
-
\frac12\rho A C_D
\|\mathbf v\|\mathbf v
+
\frac12\rho A C_L
\|\mathbf v\|^2
\left(
\hat{\boldsymbol\omega}
\times
\hat{\mathbf v}
\right)
\]

where:

- \(m\) is ball mass,
- \(\mathbf v\) is ball velocity,
- \(\mathbf g\) is gravitational acceleration,
- \(\rho\) is air density,
- \(A\) is ball cross-sectional area,
- \(C_D\) is the drag coefficient,
- \(C_L\) is the lift coefficient,
- \(\boldsymbol\omega\) is angular velocity,
- \(\hat{\mathbf v}\) is the velocity direction,
- \(\hat{\boldsymbol\omega}\) is the spin-axis direction.

The aerodynamic terms are nonlinear because they depend on the ball speed.

---

## Physical Parameters

The baseline model uses:

| Parameter | Value | Units |
|---|---:|---|
| Ball mass | 0.0575 | kg |
| Ball diameter | 0.067 | m |
| Ball radius | 0.0335 | m |
| Air density | 1.21 | kg/m³ |
| Drag coefficient | 0.55 | dimensionless |
| Gravity | 9.81 | m/s² |
| Nominal contact height | 3.0 | m |
| Nominal serve speed | 200 | km/h |

The drag coefficient is treated as a **provisional modeling parameter**, not as a universal constant for every tennis ball and condition.

Real tennis-ball aerodynamics depend on factors including speed, ball condition, surface texture, and spin.

---

# Aerodynamic Drag

Quadratic drag is modeled as

\[
\mathbf a_D
=
-
\frac{1}{2m}
\rho A C_D
\|\mathbf v\|\mathbf v
\]

so the drag acceleration always acts opposite to the instantaneous velocity vector.

This produces a nonlinear reduction in forward velocity and therefore affects:

- flight time,
- landing distance,
- launch angle requirements,
- and the allowable region of legal serves.

The aerodynamic implementation is contained in:

```text
src/aerodynamics.py
```

and reused by the trajectory model.

---

# Magnus Effect

Spin is modeled through a Magnus acceleration perpendicular to both the spin axis and velocity direction.

The implementation uses the provisional lift-coefficient relationship

\[
C_L =
\frac{1}
{2+v/v_{\mathrm{spin}}}
\]

where

\[
v_{\mathrm{spin}}=r\omega.
\]

The Magnus direction is determined by

\[
\hat{\boldsymbol\omega}
\times
\hat{\mathbf v}.
\]

The current implementation accepts angular velocity in radians per second.

RPM is converted before entering the core physical model:

\[
\omega_{\mathrm{rad/s}}
=
\omega_{\mathrm{rpm}}
\frac{2\pi}{60}.
\]

### Important modeling limitation

The lift relationship is a provisional computational model rather than a claim that the coefficient law is universally valid for tennis balls.

The project therefore interprets spin-dependent results as **results of the stated model**, rather than as universal empirical laws.

---

# Court Geometry

The court is represented in a coordinate system in which:

- \(x\) is the direction from the server toward the net and service line,
- \(y\) is the lateral direction,
- \(z\) is vertical.

The modeled geometry uses:

| Quantity | Value |
|---|---:|
| Net distance from baseline | 11.885 m |
| Net center height | 0.914 m |
| Net post height | 1.07 m |
| Net-to-service-line distance | 6.40 m |
| Singles court width | 8.23 m |
| Half-width | 4.115 m |

The official tennis rules specify a 23.77 m court, an 8.23 m singles width, a service line 6.40 m from the net, and a net height of 0.914 m at center and 1.07 m at the posts.

The model places the server's nominal contact point at

\[
x=-11.885\text{ m}
\]

relative to the net.

---

# Service Constraints

A simulated serve is considered legal only if it satisfies all modeled constraints.

## 1. Net clearance

At the location where the trajectory crosses the net plane,

\[
x=0,
\]

the ball must satisfy

\[
z_{\mathrm{net}}
>
h_{\mathrm{net}}(y_{\mathrm{net}}).
\]

The model uses the net center and post heights to represent the lateral variation in net height.

---

## 2. Service depth

The first landing point must occur between the net and service line:

\[
0<x_{\mathrm{land}}<6.40.
\]

This is an important distinction.

A trajectory landing beyond the service line is not a valid serve even if it is inside the lateral boundaries.

---

## 3. Service-box width

For the deuce side:

\[
0\le y_{\mathrm{land}}\le4.115.
\]

For the ad side:

\[
-4.115\le y_{\mathrm{land}}\le0.
\]

Thus a legal serve is determined by the intersection of aerodynamic trajectory dynamics with court geometry.

---

# The Admissibility Envelope

For a fixed speed and spin state, different launch angles and azimuths produce different trajectories.

Some trajectories:

- hit the net,
- land short,
- land long,
- land outside the service box,
- or satisfy all constraints.

The admissible set is therefore

\[
\mathcal A
=
\{
\theta,\phi:
\text{trajectory satisfies all legal constraints}
\}.
\]

Here:

- \(\theta\) is launch elevation angle,
- \(\phi\) is launch azimuth.

The boundary of this set is determined by the transition between legal and illegal trajectories.

This boundary is the primary computational object studied in the project.

---

# Numerical Methods

The project uses numerical integration to solve the nonlinear equations of motion.

The numerical workflow is:

1. define physical constants,
2. construct the initial velocity vector,
3. integrate the equations of motion,
4. locate the net crossing,
5. determine the first landing point,
6. evaluate service constraints,
7. classify the trajectory as legal or illegal,
8. solve for admissibility boundaries,
9. repeat across speed, spin, azimuth, and uncertainty conditions.

The numerical solver is implemented using SciPy.

---

# Numerical Verification

Before studying tennis serves, the numerical machinery was independently verified.

## Projectile-motion verification

The gravity-only numerical trajectory was compared with the analytical projectile solution.

The maximum discrepancies were approximately:

```text
x error: 3.55 × 10^-14 m
z error: 6.66 × 10^-15 m
```

These errors are at numerical floating-point precision.

---

## RK4 convergence

A nonlinear benchmark problem,

\[
y'=-y^2,
\]

was used to test fourth-order Runge-Kutta convergence.

Observed convergence orders were approximately:

```text
3.8674
3.9671
3.9937
3.9984
```

with an average observed order of approximately:

```text
3.9567
```

which is consistent with fourth-order RK4 convergence.

---

# Aerodynamic Verification

The drag implementation was independently checked against expected force and trajectory behavior.

For the baseline model:

- initial drag magnitude was approximately 3.62 N,
- horizontal drag component was approximately -3.60 N,
- vertical drag component was approximately -0.38 N.

An artificial high-speed trajectory test demonstrated a substantial reduction in range when drag was enabled.

For the benchmark:

```text
No-drag range:   86.90 m
Drag range:      48.13 m
Range reduction: 44.61%
```

The final speed was reduced by approximately 60.57% relative to the corresponding no-drag benchmark.

A monotonicity test also confirmed that increasing the drag coefficient reduced landing distance in the modeled trajectory.

---

# Magnus Verification

The three-dimensional Magnus implementation was tested using:

- principal-axis spin configurations,
- known cross-product directions,
- zero-spin behavior,
- and controlled trajectory comparisons.

For a representative velocity of

\[
\mathbf v=[55.5556,0,0]\text{ m/s}
\]

and angular velocity

\[
\boldsymbol\omega=[0,100,0]\text{ rad/s},
\]

the resulting Magnus acceleration was directed vertically downward in the adopted coordinate convention.

The implementation was also tested for:

- top-down trajectory displacement,
- side-view trajectory displacement,
- zero-spin behavior,
- and orthogonal spin axes.

These tests are intended to verify the numerical implementation and coordinate conventions rather than establish an empirical spin classification.

---

# Main Computational Experiments

The project is organized into a sequence of computational experiments.

## V1 — Projectile verification

Establishes that the numerical integration framework reproduces known analytical projectile motion and exhibits expected RK4 convergence.

---

## V2 — Aerodynamic drag

Introduces quadratic drag and evaluates its effect on trajectory and range.

---

## V3 — Three-dimensional Magnus dynamics

Introduces spin-dependent lift and verifies the three-dimensional force direction and trajectory response.

---

## V4 — Court geometry and constraints

Implements:

- net geometry,
- service line,
- service-box boundaries,
- net-clearance constraint,
- legal landing region.

---

## V5 — Two-dimensional admissibility envelope

Computes the legal launch-angle interval for a fixed serve speed and lateral target.

For the baseline 200 km/h, zero-spin case:

```text
Net boundary:       -8.675886°
Service boundary:   -7.152987°
Admissible width:    1.522899°
```

The width is the difference between the upper and lower admissibility boundaries.

---

# Speed Dependence

The speed-dependent analysis evaluates the admissible angular width at speeds from 160 to 220 km/h.

For the baseline zero-spin model:

| Speed | Net boundary | Service boundary | Width |
|---:|---:|---:|---:|
| 160 km/h | -7.960° | -5.944° | 2.016° |
| 170 km/h | -8.187° | -6.327° | 1.860° |
| 180 km/h | -8.377° | -6.648° | 1.729° |
| 190 km/h | -8.538° | -6.920° | 1.618° |
| 200 km/h | -8.676° | -7.153° | 1.523° |
| 210 km/h | -8.794° | -7.353° | 1.441° |
| 220 km/h | -8.897° | -7.527° | 1.370° |

Across this modeled range, the admissible width decreases by approximately:

```text
32.05%
```

The average modeled width change is approximately:

```text
-0.1077° per 10 km/h
```

A quadratic response fit over the modeled speed range produced:

```text
R² = 0.9997647
```

with a maximum residual of approximately:

```text
0.00405°
```

### Interpretation

The results indicate that, under the baseline model, faster serves produce a narrower angular window of launch conditions that remain legal.

This is a **model-response result**, not a universal physical law.

The quadratic fit is descriptive of the simulated parameter range and should not be extrapolated outside it.

---

# Spin Dependence

Spin produces a substantially different response.

At 200 km/h, the modeled admissible width changes as follows:

| Spin | Net boundary | Service boundary | Width |
|---:|---:|---:|---:|
| -2500 rpm | -10.313° | -9.752° | 0.561° |
| -2000 rpm | -10.056° | -9.348° | 0.708° |
| -1500 rpm | -9.770° | -8.897° | 0.873° |
| -1000 rpm | -9.449° | -8.389° | 1.060° |
| -500 rpm | -9.087° | -7.813° | 1.275° |
| 0 rpm | -8.676° | -7.153° | 1.523° |
| 500 rpm | -8.264° | -6.493° | 1.771° |
| 1000 rpm | -7.902° | -5.915° | 1.987° |
| 1500 rpm | -7.581° | -5.406° | 2.175° |
| 2000 rpm | -7.295° | -4.953° | 2.342° |
| 2500 rpm | -7.038° | -4.548° | 2.490° |

Across the modeled range from -2500 to +2500 rpm, the admissible width changes by approximately:

```text
343.87%
```

Over the tested range, the relationship is approximately linear, although the project does not interpret that as a universal law.

---

# Spin-Reversal Check

The implementation was also tested for approximate symmetry under spin reversal.

The maximum observed boundary mismatch was approximately:

```text
0.00625°
```

This provides a useful numerical consistency check for the adopted coordinate conventions and force model.

---

# Spin–Azimuth Interaction

The project also evaluates the joint dependence of admissibility on spin and lateral launch direction.

The resulting two-dimensional parameter space is visualized using a spin–azimuth heatmap.

The corrected computation produced:

```text
98 / 98 valid parameter combinations
98 / 98 positive-width envelopes
```

At zero azimuth, the corrected boundary calculations reproduced the independently computed one-dimensional spin boundaries with errors below approximately:

```text
3.8 × 10^-7 degrees
```

for the net boundary and

```text
9.3 × 10^-8 degrees
```

for the service boundary.

This cross-check is important because it tests consistency between two different computational pathways.

---

# Robustness and Uncertainty

A nominal serve was selected and subjected to controlled perturbations in:

- serve speed,
- launch angle,
- azimuth,
- contact height,
- spin.

The nominal modeled state was:

```text
Speed:          200 km/h
Contact height: 3.0 m
Launch angle:   -7.914436°
Azimuth:         6.883538°
Spin:            0 rpm
```

The nominal trajectory produced:

```text
Net y-position:     1.434778 m
Net height:         1.060158 m
Net clearance:      0.091766 m
Landing x:          5.158320 m
Landing y:          2.057500 m
```

and was classified as legal.

A full factorial perturbation experiment produced:

```text
Total cases:       243
Legal cases:       199
Illegal cases:      44
Robustness rate:  81.89%
```

All 44 illegal cases in this perturbation design failed because of net clearance.

The modeled net-clearance landscape had:

```text
Worst case: -0.089589 m
Best case:   0.272247 m
```

The largest marginal effects in this particular perturbation experiment were associated with:

| Parameter | Approximate marginal effect |
|---|---:|
| Contact height | 54.32 percentage points |
| Launch angle | 33.33 percentage points |
| Spin | 11.11 percentage points |
| Speed | 1.23 percentage points |
| Azimuth | 1.23 percentage points |

These values should be interpreted as **effects within the specified perturbation design**, not as global variance decompositions or universal sensitivity coefficients.

---

# Empirical Professional Serve-Speed Analysis

The computational model is complemented by an empirical analysis of professional tennis serve speeds.

The analysis uses Grand Slam point-by-point data from the Jeff Sackmann tennis dataset.

The dataset provides serve-level information useful for studying empirical speed distributions, but it does not contain the complete launch-state information required to reconstruct each physical trajectory.

The raw data are therefore not treated as direct trajectory-validation data.

---

## Dataset

The analysis used:

```text
2024-usopen-points.csv
```

The working dataset contained:

```text
45,289 rows
```

including:

```text
44,783 serve-point rows
506 metadata rows
```

The analysis identified:

```text
ServeNumber = 0:  2,509 rows
ServeNumber = 1: 25,909 rows
ServeNumber = 2: 16,365 rows
```

The current dataset does not contain the player-name/gender information required for a player-level or gender-level analysis.

---

# Serve-Speed Results

Valid first-serve speeds:

```text
n = 25,528
```

Summary:

| Statistic | First serve |
|---|---:|
| Mean | 171.12 km/h |
| Median | 172 km/h |
| Standard deviation | 20.59 km/h |
| Minimum | 96 km/h |
| Maximum | 230 km/h |

Valid second-serve speeds:

```text
n = 16,074
```

Summary:

| Statistic | Second serve |
|---|---:|
| Mean | 140.32 km/h |
| Median | 140 km/h |
| Standard deviation | 15.68 km/h |
| Minimum | 98 km/h |
| Maximum | 214 km/h |

The median difference between first- and second-serve speed was:

```text
32 km/h
```

with a bootstrap 95% confidence interval of approximately:

```text
[31, 32] km/h
```

The standardized difference was large:

```text
Cohen's d = 1.63
```

A two-sample KS test also showed a strong distributional difference:

```text
D = 0.607
p < 0.001
```

---

# First-Serve Speed Distribution

Among valid first-serve observations:

```text
160–220 km/h: 70.96%
≤200 km/h:     92.59%
95th percentile: 202 km/h
99th percentile: 210 km/h
```

The empirical distribution provides context for the computational speed range used in the admissibility analysis.

Importantly, these values should not be interpreted as saying that serves above 220 km/h are illegal.

They simply describe the observed speeds in this dataset.

---

# Serve Speed and Point Outcome

A logistic model was also used to examine the relationship between serve speed and server point outcome.

Using 170 km/h as the reference point:

```text
Intercept:          0.8174
Coefficient / 10km: 0.1264
Odds ratio / 10km:  1.1347
```

Predicted server-win probabilities from the model were approximately:

| Speed | Predicted server-win probability |
|---:|---:|
| 150 km/h | 63.75% |
| 160 km/h | 66.62% |
| 170 km/h | 69.37% |
| 180 km/h | 71.99% |
| 190 km/h | 74.46% |
| 200 km/h | 76.79% |
| 210 km/h | 78.97% |
| 220 km/h | 80.99% |

A quadratic specification improved AIC over the linear model across the full modeled range:

```text
ΔAIC = -6.62
Likelihood-ratio p = 0.0033
```

However, after restricting the analysis to 120–220 km/h:

```text
ΔAIC = -0.40
Likelihood-ratio p = 0.121
```

Therefore, the evidence for curvature is not treated as robust.

This analysis is descriptive and observational. It does not establish that increasing serve speed causally increases point-winning probability.

---

# Computational–Empirical Connection

One purpose of the project is to connect two different types of information.

### Computational model

Answers:

> **What launch conditions are physically compatible with a legal serve under the specified model?**

### Empirical dataset

Answers:

> **What serve speeds are actually observed in professional competition?**

The two datasets are therefore complementary rather than interchangeable.

The empirical dataset does not contain sufficient information to reconstruct each serve's full initial state.

Conversely, the physical model does not predict player behavior, strategy, or point outcomes.

The comparison is therefore intentionally limited to the **serve-speed dimension**.

---

# What This Project Does Not Claim

Several limitations are important.

## 1. It is not a complete biomechanical serve model

The model begins at ball launch/contact.

It does not model:

- racket mechanics,
- player biomechanics,
- joint torques,
- racket deformation,
- ball-racket collision,
- pronation,
- body rotation,
- or energy transfer from the player.

---

## 2. It does not reconstruct professional trajectories

The US Open point-by-point data do not provide the full launch state needed for trajectory reconstruction.

The empirical analysis therefore does not validate individual simulated trajectories.

Recent professional-tracking research has demonstrated that full trajectory reconstruction is possible when detailed spatiotemporal tracking data are available. The present project addresses a different problem: characterizing the forward admissibility region under a specified physical model.

---

## 3. Aerodynamic coefficients are simplified

The model uses:

```text
Cd = 0.55
```

and a provisional lift-coefficient relationship.

Real tennis-ball aerodynamics can vary with:

- Reynolds number,
- spin parameter,
- ball condition,
- surface texture,
- and velocity.

Experimental wind-tunnel studies have demonstrated variation in tennis-ball aerodynamic behavior, including differences associated with ball condition.

---

## 4. Environmental effects are not fully modeled

The current model does not explicitly incorporate:

- wind,
- temperature,
- humidity,
- altitude,
- air-pressure variation,
- or detailed court-specific environmental conditions.

---

## 5. The net model is simplified

The current implementation represents net height using the center and post heights with a simplified lateral interpolation.

The model is intended for computational study rather than centimeter-level officiating.

---

## 6. Numerical admissibility is not human serving probability

An admissible angular width is not the same thing as the probability that a player will make the serve.

A player does not randomly sample launch angles uniformly.

Human motor variability, strategy, spin generation, biomechanics, and targeting behavior are outside the present model.

Therefore:

> **Admissible-envelope width is a geometric/physical quantity, not a serve-success probability.**

---

# Reproducibility

The project is designed to be reproducible.

The computational workflow is divided between reusable Python modules and Jupyter notebooks.

The reusable model is contained in:

```text
src/
```

The experiments are contained in:

```text
notebooks/
```

The automated tests are contained in:

```text
tests/
```

The rendered figures are contained in:

```text
figures/
```

The external-data provenance documentation is contained in:

```text
data/README.md
```

---

# Running the Project

## 1. Clone the repository

Clone the repository to a local machine.

## 2. Create a Python environment

A virtual environment is recommended.

For example:

```bash
python -m venv .venv
```

Activate the environment according to your operating system.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The current dependency set includes:

```text
numpy
scipy
matplotlib
pandas
jupyter
```

## 4. Run the automated tests

From the repository root:

```bash
python -m pytest -q
```

The current test suite contains:

```text
37 tests
```

The verified result is:

```text
37 passed
```

## 5. Run the notebooks

The recommended sequence is:

```text
00_usopen_data_audit.ipynb
01_projectile_verification.ipynb
02_aerodynamic_drag.ipynb
03_magnus_3d.ipynb
04_court_geometry.ipynb
05_admissibility_envelope.ipynb
06_speed_dependent_envelope.ipynb
07_spin_dependent_envelope.ipynb
08_robustness_uncertainty.ipynb
09_usopen_empirical_analysis.ipynb
10_scientific_synthesis.ipynb
```

The empirical notebook requires the appropriate external dataset to be obtained separately and placed in the expected location.

See:

```text
data/README.md
```

for data provenance and reproduction instructions.

---

# Repository Structure

```text
tennis-serve-admissibility/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── README.md
│
├── figures/
│   ├── main/
│   │   ├── 01_admissibility_envelope.png
│   │   ├── 02_speed_dependent_envelope.png
│   │   ├── 03_spin_dependent_envelope.png
│   │   ├── 04_spin_azimuth_heatmap.png
│   │   ├── 05_robustness_landscape.png
│   │   ├── 06_usopen_speed_distribution.png
│   │   └── 07_empirical_computational_synthesis.png
│   │
│   └── supporting/
│       └── [supporting validation and analysis figures]
│
├── notebooks/
│   ├── 00_usopen_data_audit.ipynb
│   ├── 01_projectile_verification.ipynb
│   ├── 02_aerodynamic_drag.ipynb
│   ├── 03_magnus_3d.ipynb
│   ├── 04_court_geometry.ipynb
│   ├── 05_admissibility_envelope.ipynb
│   ├── 06_speed_dependent_envelope.ipynb
│   ├── 07_spin_dependent_envelope.ipynb
│   ├── 08_robustness_uncertainty.ipynb
│   ├── 09_usopen_empirical_analysis.ipynb
│   └── 10_scientific_synthesis.ipynb
│
├── src/
│   ├── __init__.py
│   ├── constants.py
│   ├── aerodynamics.py
│   ├── trajectory.py
│   ├── constraints.py
│   ├── continuation.py
│   ├── sensitivity.py
│   ├── inference.py
│   └── validation.py
│
├── tests/
│   ├── test_aerodynamics.py
│   ├── test_constraints.py
│   ├── test_trajectory.py
│   └── test_validation.py
│
└── .github/
    └── workflows/
        └── tests.yml
```

---

# Main Figures

## Serve admissibility envelope

The central result of the project is the modeled region of launch conditions that produce legal serves.

See:

```text
figures/main/01_admissibility_envelope.png
```

## Speed-dependent admissibility

This figure shows how the modeled admissible region changes with serve speed.

See:

```text
figures/main/02_speed_dependent_envelope.png
```

## Spin-dependent admissibility

This figure shows how spin changes the modeled launch-angle window.

See:

```text
figures/main/03_spin_dependent_envelope.png
```

## Spin–azimuth interaction

This heatmap shows the joint response of admissibility to spin and lateral launch direction.

See:

```text
figures/main/04_spin_azimuth_heatmap.png
```

## Robustness landscape

This visualization shows how perturbations in the launch state affect modeled net clearance.

See:

```text
figures/main/05_robustness_landscape.png
```

## Professional serve-speed distribution

This figure provides empirical context for the modeled serve-speed range.

See:

```text
figures/main/06_usopen_speed_distribution.png
```

## Computational–empirical synthesis

The final synthesis figure combines the modeled admissibility response with the empirical serve-speed distribution.

See:

```text
figures/main/07_empirical_computational_synthesis.png
```

---

# Research Workflow

The project follows the following computational pipeline:

```text
                    Physical constants
                           │
                           ▼
                 Initial serve state
                           │
                           ▼
              Nonlinear equations of motion
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Gravity                  Aerodynamics
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                            Drag                  Magnus
                              │                     │
                              └──────────┬──────────┘
                                         │
                                         ▼
                                Numerical trajectory
                                         │
                                         ▼
                                  Net intersection
                                         │
                                         ▼
                                  First landing
                                         │
                                         ▼
                                Court constraints
                                         │
                           ┌─────────────┴─────────────┐
                           │                           │
                        Illegal                      Legal
                           │                           │
                           └─────────────┬─────────────┘
                                         │
                                         ▼
                              Admissibility boundary
                                         │
                                         ▼
                         Parameter continuation / sweeps
                                         │
                   ┌─────────────────────┼────────────────────┐
                   │                     │                    │
                 Speed                  Spin              Azimuth
                   │                     │                    │
                   └─────────────────────┼────────────────────┘
                                         │
                                         ▼
                                Robustness analysis
                                         │
                                         ▼
                            Empirical speed comparison
                                         │
                                         ▼
                              Scientific synthesis
```

---

# Validation Philosophy

The project distinguishes between three different forms of evidence.

## 1. Numerical verification

Does the implementation behave correctly for problems with known answers?

Examples:

- analytical projectile motion,
- RK4 convergence,
- zero-spin behavior,
- cross-product direction checks.

## 2. Internal consistency

Do independently computed quantities agree?

Examples:

- one-dimensional and two-dimensional boundary calculations,
- spin-reversal checks,
- endpoint perturbation tests,
- consistency of admissibility classifications.

## 3. Empirical context

Do modeled parameter ranges overlap with physically observed tennis behavior?

The professional serve-speed dataset provides empirical context.

It is not treated as direct trajectory validation because the required launch-state information is unavailable.

---

# Interpretation of the Main Findings

The computational results support several conclusions within the stated model.

### Finding 1 — Speed narrows the admissible launch-angle window

At fixed contact height and zero spin, increasing serve speed from 160 to 220 km/h reduces the modeled admissible angular width by approximately 32%.

### Finding 2 — Spin strongly modifies admissibility

Across the modeled spin range from -2500 to +2500 rpm, the admissible width changes by several hundred percent.

Thus speed and spin should not be treated as interchangeable parameters.

### Finding 3 — The two legal boundaries have different physical meanings

One boundary is controlled by the need to clear the net.

The other is associated with reaching the service region before crossing the service line.

The admissible serve region therefore emerges from the interaction of multiple constraints rather than from a single "correct" launch angle.

### Finding 4 — Robustness is not identical to legality

A trajectory can be legal while remaining close to an admissibility boundary.

The uncertainty experiment demonstrates why margin matters.

A nominally legal serve with a small clearance margin can become illegal under modest perturbations.

### Finding 5 — Professional serve speeds provide useful empirical context

The empirical first-serve distribution is concentrated in a range that overlaps substantially with the modeled 160–220 km/h computational experiments.

This makes the modeled parameter sweep relevant to realistic professional serving conditions.

However, the empirical dataset does not provide sufficient information to infer each player's launch angle, spin, or trajectory.

---

# Limitations and Future Work

Several extensions would substantially improve the model.

## Aerodynamic refinement

Future work could replace the provisional aerodynamic coefficients with experimentally calibrated functions of:

- Reynolds number,
- spin parameter,
- ball condition,
- and velocity.

## Wind

A future model could include a wind vector and calculate aerodynamic forces using the velocity relative to the surrounding air:

\[
\mathbf v_{\mathrm{rel}}
=
\mathbf v_{\mathrm{ball}}
-
\mathbf v_{\mathrm{air}}.
\]

This would allow study of how crosswinds and headwinds deform the admissibility envelope.

## Contact-height distribution

The current model uses a nominal contact height and perturbations around it.

Future work could use measured serving contact-height distributions.

## Full launch-state distributions

The strongest future empirical extension would combine:

- launch speed,
- launch angle,
- azimuth,
- spin magnitude,
- spin axis,
- contact position,
- and landing location

from professional tracking systems.

This would permit direct comparison between the modeled admissibility envelope and the empirical distribution of actual launch states.

## Ball-condition modeling

The aerodynamic model could incorporate changing ball condition during a match.

Experimental literature indicates that ball condition can influence aerodynamic behavior, making this an important potential extension.

## Optimization

A future optimization layer could solve questions such as:

> What launch state maximizes margin to all legal boundaries for a specified serve speed and spin?

or

> What serve speed maximizes a chosen objective while maintaining a prescribed robustness margin?

This would transform the current descriptive envelope into an optimization framework.

---

# Relationship to Prior Research

The physics of tennis-ball flight has been studied extensively.

Experimental work has measured drag and lift on spinning and non-spinning tennis balls and demonstrated that aerodynamic behavior depends on ball condition and other physical parameters.

More recent work has used professional spatiotemporal tracking data to reconstruct tennis trajectories from launch parameters and aerodynamic properties. In particular, Eassom, Robertson, and Reid (2026) demonstrated trajectory reconstruction using tracking data from 8,654 serves at the 2022 Australian Open, reporting a median pre-bounce trajectory MAE of 4.8 mm.

The present project should therefore be understood as complementary.

Rather than attempting to reconstruct observed professional trajectories, it investigates the **forward constrained dynamics of legal serve generation** and maps the resulting admissible launch region as a function of model parameters.

---

# References

The project draws on the following categories of sources.

### Tennis rules and court geometry

International Tennis Federation / World Tennis:

**Rules of Tennis**

The official rules define the court dimensions, service-line location, and net geometry used as the basis for the computational court model.

### Tennis-ball aerodynamics

Goodwill, S. R., Chin, S. B., & Haake, S. J.

**Aerodynamics of spinning and non-spinning tennis balls.**

Journal of Wind Engineering and Industrial Aerodynamics, 92(11), 2004.

DOI:

```text
10.1016/j.jweia.2004.05.004
```

### Professional trajectory reconstruction

Eassom, A., Robertson, S., & Reid, M.

**Tennis ball trajectory decomposition based on spatiotemporal tracking data.**

Sports Engineering, 29, 19, 2026.

DOI:

```text
10.1007/s12283-026-00547-6
```

This work provides an important reference point for trajectory reconstruction using professional spatiotemporal tracking data.

### Empirical tennis data

Jeff Sackmann.

**tennis_slam_pointbypoint**

Grand Slam point-by-point tennis data used for the empirical serve-speed analysis.

The dataset is distributed under its stated Creative Commons Attribution-NonCommercial-ShareAlike terms. See:

```text
data/README.md
```

for provenance and reproduction instructions.

---

# Reproducibility Statement

All central computational conclusions in this project are generated from code contained in the repository.

The repository separates:

- reusable physical models,
- numerical methods,
- constraints,
- analysis procedures,
- validation tests,
- notebooks,
- figures,
- and external-data documentation.

The current automated test suite contains 37 tests and has been verified to pass:

```text
37 passed
```

The project also includes continuous integration through GitHub Actions so that computational tests can be rerun automatically when the repository changes.

---

# Important Distinction Between Model Results and Empirical Results

Throughout this repository, results are classified into two categories.

### Model-derived

These depend on the stated physical assumptions, including:

- ball mass,
- ball dimensions,
- air density,
- drag coefficient,
- lift model,
- contact height,
- court geometry,
- and numerical integration.

Examples:

- admissible angular widths,
- speed-dependent boundaries,
- spin-dependent boundaries,
- robustness rates,
- net-clearance landscapes.

### Data-derived

These depend on the external professional point-by-point dataset.

Examples:

- first-serve speed distribution,
- second-serve speed distribution,
- speed percentiles,
- first/second serve differences,
- serve-speed/outcome statistical models.

The two should not be conflated.

---

# Summary

This project develops a computational framework for studying tennis serve legality as a constrained nonlinear dynamical-system problem.

The central result is the **serve admissibility envelope**: the set of launch conditions that allow a ball, under a specified physical model, to clear the net and land inside the legal service region.

The analysis demonstrates that:

1. increasing serve speed narrows the modeled admissible angular region;
2. spin can substantially reshape the admissible region;
3. the interaction between spin and lateral launch direction creates a multidimensional admissibility landscape;
4. nominal legality does not imply robustness to launch-state perturbations;
5. professional serve-speed data provide empirical context for the modeled speed range;
6. the available point-by-point data are insufficient for direct trajectory-level validation.

The broader goal is to demonstrate how **physics, numerical computation, geometry, uncertainty analysis, and empirical data can be integrated into one reproducible computational-engineering framework**.

---

# Status

**Research computation:** Complete

**Numerical verification:** Complete

**Physical model:** Complete for the stated assumptions

**Admissibility analysis:** Complete

**Speed analysis:** Complete

**Spin analysis:** Complete

**Robustness analysis:** Complete

**Empirical analysis:** Complete

**Automated tests:** 37/37 passing

**Figures:** 29

**Reproducibility documentation:** Complete

**Formal research paper:** Planned as a subsequent stage
