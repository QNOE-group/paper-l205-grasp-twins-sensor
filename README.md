# TWINS Gas Sensing — Analysis Scripts

Code for the manuscript **"Quantitative multi-analyte detection of volatile organic
compounds using birefringent common-path interferometry"** (`../Manuscript/`).

A TWINS birefringent FTIR spectrometer measures isopropanol/ethanol mixtures in a 10 cm
gas cell; two PIDs give reference concentrations. These notebooks turn the measured
spectra into calibrated concentration predictions and produce every figure in the paper.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Run

```bash
python notebook_runner.py       # runs all notebooks in order, in place
```

Notebooks pass data through `models/` and `results/`, so the order matters.
`setup.py` is the **config file** — `configuration` there selects which datasets are used.

**Figure 5 and Table 1 compare two resolutions, so run the pipeline twice:** once with
`configuration = "t1"`, once with `"t2"`. `05-02` then reads both results.

## Notebooks → figures

The leading number is the figure. `00-` notebooks are preprocessing and map to no figure.

| Notebook | Figure | Content |
|---|---|---|
| `00-01-calibrate-sensors` | – | Calibrate the PID reference sensors against NIST spectra |
| `00-02-train-model` | – | Train the ridge regression model |
| `00-03-train-filter` | – | Configure the Kalman filter |
| `00-04-test-model` | – | Check model + filter on the testing dataset |
| `02-basic-characterization` | **2** | Interferograms, spectra, absorbance vs. NIST |
| `03-testing-characterization` | **3** | Predicted vs. reference concentrations over 16 h |
| `04-sensitivity-characterization` | **4** + **Table 1** | Sensitivity, selectivity, bias, LOD, drift |
| `05-01-dynamic-characterization` | – | Response times and LOD → `results/` |
| `05-02-dynamic-characterization` | **5** | Step response, LOD vs. response time (20 vs. 50 cm⁻¹) |
| `s02-sensor-calibration` | **S2** | PID calibration, ethylene validation, saturation |
| `s03-training-characterization` | **S3** | Training data, noise covariance, model weights |

Figures are saved to `../Figures/<notebook>-<configuration>.svg`.
Figure 1 and S1 are drawings, not code.
*The Word draft numbers SI figures continuously, so S2 → "Figure S7" and S3 → "Figure S8".*

## Pipeline

1. **Calibrate reference** (`00-01`) — PIDs saturate, so fit a Beer–Lambert saturation
   model with the absolute scale set by NIST coefficients and the 10 cm path length.
   Also yields a **cutoff concentration** above which PID readings are discarded.
2. **Train** (`00-02`) — Ridge regression maps absorbance (850–1450 cm⁻¹) to both
   concentrations; λ by 5-fold CV. ~20% of samples are synthetic (NIST spectra + measured
   correlated noise), and samples are reweighted to flatten the concentration distribution.
3. **Filter** (`00-03`) — Kalman filter with constant gain, i.e. an exponential moving
   average, set by the target rise time.
4. **Evaluate** (`02`–`05`, `s02`–`s03`) — Apply to the held-out testing dataset.

Only *settled* spectra are used, and samples above the PID cutoff are dropped — the
"screened testing dataset" of the paper.

## Layout

| Path | Role |
|---|---|
| `setup.py` | Config: dataset selection, spectral range, hyperparameters. **Start here.** |
| `processing.py` | Shared helpers: settling detection, spectral broadening, PID↔cell scaling |
| `notebook_runner.py` | Runs all notebooks in order |
| `datasets/` | Raw measurements (`.npz` + `.yaml`), acquired elsewhere, ~400 MB |
| `NIST/`, `PID/` | Reference absorption spectra; ethylene PID calibration |
| `models/`, `results/` | Written by the `00-` and `05-01` notebooks |

## Configurations

| | Resolution | Acquired range | |
|---|---|---|---|
| **`t1`** | 20 cm⁻¹ | 550–2500 cm⁻¹ | **Main configuration of the paper** |
| **`t2`** | 50 cm⁻¹ | 550–2500 cm⁻¹ | Low-resolution comparison (Fig. 5b, Table 1) |
| `t3` | 20 cm⁻¹ | 700–1400 cm⁻¹ | Exploratory: narrowed range. Not in the manuscript |
| `t4` | 20 cm⁻¹ | 700–1400 cm⁻¹ | Exploratory: bandlimited sampling. Not in the manuscript |
