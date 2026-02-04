"""
v12_mca_lib

Lab-course-experiment 12: alpha spectroscopy with a surface-barrier-counter.

This file is a library with useful functions for data analysis.
"""

import sys
import os
import re
import numpy
#from matplotlib import pyplot as plt
#from scipy.signal import find_peaks
#from scipy.optimize import curve_fit


def check_files(filepath: str):
    """Check if data files are valid.

    Args:
        filepath (str): relative path to either the *.asc or *.mcd file.

    Returns:
        tuple[str,str]: ["/abs/path/to/data.asc", "/abs/path/to/metadata.mcd"]
    """
    (pathname, ext) = os.path.splitext(filepath)
    if ext not in [".asc", ".mcd"]:
        print("Error. Wrong file!")
    data_file = os.path.abspath(pathname + ".asc")
    metadata_file = os.path.abspath(pathname + ".mcd")

    if not os.path.isfile(data_file):
        print(f"Error. File not found: {data_file}")
        sys.exit()
    if not os.path.isfile(metadata_file):
        print(f"Error. File not found: {metadata_file}")
        sys.exit()

    return data_file, metadata_file


def load_asc_file(filepath: str):
    """Loads the histogram data into a numpy ndarray

    Args:
        filepath (str): path to .asc file, as given by the first return value of check_files()

    Returns:
        NDArray: The full histogram as 1D-array
    """
    data = numpy.loadtxt(filepath, dtype=numpy.uint32)
    return data


def load_mcd_file(filepath: str):
    """Retrieve the necessary metadata from the .mcd file.

    Args:
        filepath (str): path to .mcd file, as given by the second return value of check_files()

    Returns:
        dict[str,float]: Metadata
        | Key       | Value  | Unit |
        | :-------  | :----  | :--- |
        | livetime  | float  |  seconds  |
    """
    metadata = {}
    with open(filepath, "r") as mcd_file:
        for line in mcd_file:
            if "LIVETIME:" in line:
                # Regex catch group matches a string containing a floating point number like 123.456
                match = re.search(r"(?:\d+\.\d+)", line)
                if match:
                    metadata["livetime"] = float(match.group())
    return metadata


def gauss_func(x, a, mu, sigma):
    return a * numpy.exp(-((x - mu) ** 2) / (2 * sigma**2))


def lin_func(x, m, b):
    return m * x + b


def calib_func(chan, m, b):
    return (chan - b) / m
