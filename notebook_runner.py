"""Run all notebooks in this folder in order, in place."""

from pathlib import Path

import nbformat
from nbclient import NotebookClient
from jupyter_client.manager import KernelManager


NOTEBOOKS = [
    "00-01-calibrate-sensors.ipynb",
    "00-02-train-model.ipynb",
    "00-03-train-filter.ipynb",
    "00-04-test-model.ipynb",
    "02-basic-characterization.ipynb",
    "03-testing-characterization.ipynb",
    "04-sensitivity-characterization.ipynb",
    "05-01-dynamic-characterization.ipynb",
    "05-02-dynamic-characterization.ipynb",
    "s02-sensor-calibration.ipynb",
    "s03-training-characterization.ipynb",
]

if __name__ == "__main__":
    for filename in NOTEBOOKS:
        filepath = Path(filename)
        print(f"Running {filename} ...")
        nb = nbformat.read(filepath, as_version=4)
        km = KernelManager(kernel_name="python3")
        km.transport_encryption = "auto"
        client = NotebookClient(
            nb, km=km, resources={"metadata": {"path": filepath.parent or "."}}
        )

        client.execute()
        nbformat.write(nb, filepath)
        print(f"Finished {filename}\n")
