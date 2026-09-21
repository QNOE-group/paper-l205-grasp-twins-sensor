from pathlib import Path

# Plotting
violet = "#785ef0"
blue = "#648fff"
green = "#007d79"
yellow = "#ffb000"
orange = "#fe6100"
red = "#dc267f"
white = "#ffffff"
gray = "#cccccc"
black = "#000000"
colors = [blue, yellow]
plot_style = "seaborn-v0_8"

# Datasets
filepath = Path("datasets")

configuration = "t1"
labels = {
    "t1": {
        "calibration": ["GRASP26_62F"],
        "training": ["GRASP26_71F"],
        "testing": ["GRASP26_72F"],
    },
    "t2": {
        "calibration": ["GRASP26_62F"],
        "training": ["GRASP26_66F"],
        "testing": ["GRASP26_64F"],
    },
    "t3": {
        "calibration": ["GRASP26_62F"],
        "training": ["GRASP26_75F"],
        "testing": ["GRASP26_76F"],
    },
    "t4": {
        "calibration": ["GRASP26_62F"],
        "training": ["GRASP26_73F"],
        "testing": ["GRASP26_74F"],
    },
}
calibration_labels = labels[configuration]["calibration"]
training_labels = labels[configuration]["training"]
testing_labels = labels[configuration]["testing"]

# Measurement
spectral_range = (850, 1450)  # (cm^-1)

absorption_path_length = 0.1  # (m)

gas_cell_volume = 132  # (ml)

rise_time = 60  # (s)

settling_times = {
    "t1": {
        "calibration": 300,
        "training": 600,
        "testing": 600,
    },
    "t2": {
        "calibration": 300,
        "training": 600,
        "testing": 600,
    },
    "t3": {
        "calibration": 300,
        "training": 600,
        "testing": 600,
    },
    "t4": {
        "calibration": 300,
        "training": 600,
        "testing": 600,
    },
}  # (s)
calibration_settling_time = settling_times[configuration]["calibration"]
training_settling_time = settling_times[configuration]["training"]
testing_settling_time = settling_times[configuration]["testing"]

# Calibration
calibration_type = "pid"  # "pid" or "flowrate"

pid_response_factors = {"isopropanol": 0.444, "ethanol": 1.222}  # ethylene equiv.

# Regression
predictor_type = "absorbance"  # "absorbance" or "neg-log-spectrum"

concentration_bin_width = 10  # None or (ppm) - good: 10

synthetic_sample_ratio = 1 / 5  # good: 1/5

number_folds = 5

random_seed = 42
