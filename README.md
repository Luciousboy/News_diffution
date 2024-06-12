# News_diffution

## Overview

This project contains essential data and functions for analyzing time series and visualizing word clouds. The repository is structured to facilitate easy access to the data and methods required for event detection and analysis.

## Files and Descriptions

### Data

The `Data` folder contains all the necessary information for this project, including time series data and data required for plotting word clouds. Additionally, the file `all_metrics_and_p_values.pkl` within this folder includes the results obtained from the following methods:
- Transfer Entropy
- Mutual Information
- Granger Causality

This data is organized as a source target matrix.

### Event Functions

The file `event_functions.py` includes all the necessary functions for event detection and the identification of event coincidences. This file is crucial for the analysis and interpretation of events within the provided time series data.

### Example Notebook

An example Jupyter Notebook (`example_usage.ipynb`) is included to demonstrate the functionality of these functions and the creation of the Qs and Qa matrices. This notebook provides practical examples and can be used as a reference for understanding how to implement the methods provided in this repository.

