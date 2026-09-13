# Data

This directory contains documentation for the external data used in the
empirical component of the tennis serve admissibility study.

## US Open point-by-point data

The empirical analysis uses Grand Slam point-by-point tennis data from the
Jeff Sackmann `tennis_slam_pointbypoint` dataset.

The data are not redistributed in this repository. Users should obtain the
dataset directly from its original source and place the required CSV file
in this directory before running the empirical notebooks.

### Source

Jeff Sackmann  
`tennis_slam_pointbypoint`

Repository:
https://github.com/JeffSackmann/tennis_slam_pointbypoint

### License

The dataset is distributed under the
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
license (CC BY-NC-SA 4.0).

Please consult the original repository and license before using or
redistributing the data.

## Expected file

The empirical notebooks expect the relevant US Open point-by-point CSV
file to be available locally in this directory.

The current analysis was performed using:

`2024-usopen-points.csv`

The raw data file is intentionally not committed to this repository.

## Reproducibility

To reproduce the empirical analysis:

1. Obtain the dataset from the original source.
2. Place the required CSV file in this directory.
3. Open:

   `notebooks/00_usopen_data_audit.ipynb`

4. Run the data-audit notebook first.
5. Continue with:

   `notebooks/09_usopen_empirical_analysis.ipynb`

6. The final computational and empirical synthesis is presented in:

   `notebooks/10_scientific_synthesis.ipynb`

## Important limitation

The point-by-point dataset provides serve-level information such as serve
speed and point outcomes, but it does not provide the full launch-state
variables required by the physical trajectory model, such as contact
position, launch direction, or spin.

Therefore, the empirical analysis is used to provide real-world context for
the modeled serve-speed range. It is not treated as direct validation of
individual simulated trajectories.
