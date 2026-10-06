# TWINS Gas Sensing — Analysis Scripts

This repository contains the code for the manuscript **"Quantitative multi-analyte detection of volatile organic
compounds using mid-infrared birefringent common-path interferometry"**. The manuscript is in `../Manuscript/`.

The TWINS spectrometer is a birefringent FTIR spectrometer. It measures mixtures of isopropanol and ethanol in a
10 cm gas cell. Two PIDs give the reference concentrations. The notebooks change the measured spectra into
calibrated concentration predictions. The notebooks also make all the figures in the manuscript.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

In VS Code, run the notebooks with the `.venv` interpreter. This interpreter has the kernel name "TWINS Gas Sensing".
The system Python cannot load the pickled models correctly, because it has an older version of scikit-learn.

## Run

```bash
python notebook_runner.py       # runs all notebooks in sequence and saves the outputs in the notebook files
```

The sequence of the notebooks is important, because some notebooks read data that other notebooks write to
`models/` and `results/`.

`setup.py` is the **configuration file**. The variable `configuration` in this file selects the datasets that the
notebooks use.

**Because Figure 5 and Table 2 compare two resolutions, run the pipeline two times:**

1. Run the pipeline with `configuration = "t1"`.
2. Run the pipeline with `configuration = "t2"`.

Then, `05-02` reads the results of the two configurations.

**Table S4** is about the ratio of synthetic training spectra. No file contains the data for this table. To get
these data, do these steps for each of these values of `synthetic_sample_ratio`: 0, 0.05, 0.1, 0.2 and 0.5.

1. Set `synthetic_sample_ratio` to the value.
2. Run `00-02`, `00-03` and `04` again, in this sequence.

## Notebooks and figures

The number at the start of the notebook name is the figure number. The `00-` notebooks do the preprocessing. These
notebooks have no figure.

| Notebook | Figure | Content |
|---|---|---|
| `00-01-calibrate-sensors` | – | Uses NIST spectra to calibrate the PID reference sensors |
| `00-02-train-model` | – | Trains the ridge regression model |
| `00-03-train-filter` | – | Sets the parameters of the Kalman filter |
| `00-04-test-model` | – | Checks the model and the filter with the testing dataset |
| `02-basic-characterization` | **2** | Shows interferograms and spectra. Compares the absorbance with NIST spectra. |
| `03-testing-characterization` | **3** | Compares the predicted concentrations with the reference concentrations for a period of 16 h |
| `04-sensitivity-characterization` | **4** and **Table 2** | Shows sensitivity, selectivity, bias, LOD and drift |
| `05-01-dynamic-characterization` | – | Calculates the response times and the LOD for different filter times. Writes them to `results/`. The response times in Table 2 come from this notebook. |
| `05-02-dynamic-characterization` | **5** | Shows the step response and the LOD for different response times. Compares 20 cm⁻¹ with 50 cm⁻¹. |
| `s02-sensor-calibration` | **S2** | Shows the PID calibration, the validation with ethylene and the saturation |
| `s03-training-characterization` | **S3** | Shows the training data, the noise covariance and the model weights |

The notebooks save the figures to `../Figures/<notebook>-<configuration>.svg`. But `05-02` writes its figure to
`05-dynamic-characterization-t1-t2.svg`.

The panel letters, the titles and the labels in the plots are added by hand to the files `../Figures/<name>.svg`.
Examples of these labels are "Analysis window" and "Fitting range". The names of these files have no suffix. The
Word draft uses these files.

These items do not come from the code:

- Figure 1, which is a drawing
- The photograph of the setup (`s01-setup`)
- Table 1, which is a qualitative comparison
- Table S3, which gives detection limits from the literature

*In the Word draft, the SI items have continuous numbers. These are the names in the Word draft:*

- *S1 is "Figure S6".*
- *S2 is "Figure S7".*
- *S3 is "Figure S8".*
- *The SI tables are "Table S3" and "Table S4".*

## Pipeline

1. **Calibrate the reference** (`00-01`). Because the PIDs saturate, fit a Beer–Lambert saturation model. The NIST
   coefficients and the path length of 10 cm set the absolute scale of this model. This step also gives a
   **cutoff concentration**. PID readings above this concentration are discarded.
2. **Train** (`00-02`). A ridge regression calculates the two concentrations from the absorbance.
   - The spectral range of the absorbance is 850–1450 cm⁻¹.
   - Each spectrum is mean-centred.
   - A 5-fold cross-validation selects λ.
   - Approximately 20% of the samples are synthetic. To make these samples, measured correlated noise is added to
     NIST spectra.
   - The samples get new weights to make the concentration distribution flat. These new weights give the synthetic
     samples approximately 70% of the training weight.
3. **Filter** (`00-03`). The filter is a Kalman filter with a constant gain. This filter is the same as an
   exponential moving average. The target rise time sets the gain.
4. **Evaluate** (`02`–`05`, `s02`–`s03`). Use the model and the filter on the held-out testing dataset.

The pipeline uses only *settled* spectra. It also removes the samples above the cutoff concentration. The result is
the "screened testing dataset" of the manuscript.

## Files and folders

| Path | Description |
|---|---|
| `setup.py` | Configuration file. It selects the datasets and sets the spectral range and the hyperparameters. **Start here.** |
| `processing.py` | Helper functions that different notebooks use: settling detection, spectral broadening, and scaling between PID and cell |
| `notebook_runner.py` | Runs all notebooks in the correct sequence |
| `datasets/` | Measurements in `.npz` and `.yaml` files. They were recorded outside this repository. The size is approximately 400 MB. The notebooks use only 62F, 64F, 66F and 71F–76F. |
| `NIST/` | Reference absorption spectra |
| `PID/` | PID calibration with ethylene |
| `models/` | The notebooks `00-01` to `00-03` write to this folder. |
| `results/` | `05-01` writes to this folder. `05-02` reads from this folder. |

The software `grasp-twins` calculated the spectra in `datasets/` before this pipeline. It used `TWINS.to_spectrum`
with Happ–Genzel apodization. The "resolution" Δν is equal to 1/(2L). L is the one-sided maximum of the optical path
difference. The FWHM of the line shape is approximately 1.8 Δν.

## Configurations

| | Resolution | Measured range | Time for each spectrum | |
|---|---|---|---|---|
| **`t1`** | 20 cm⁻¹ | 550–2500 cm⁻¹ | 64 s | **Main configuration of the manuscript** |
| **`t2`** | 50 cm⁻¹ | 550–2500 cm⁻¹ | 26 s | Configuration with low resolution. Figure 5b and Table 2 compare it with `t1`. |
| `t3` | 20 cm⁻¹ | 700–1400 cm⁻¹ | 37–38 s | Configuration to examine a smaller range. The manuscript does not use it. |
| `t4` | 20 cm⁻¹ | 700–1400 cm⁻¹ | 19–20 s | Configuration to examine bandlimited sampling. The manuscript does not use it. |
