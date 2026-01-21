# Predictive Analytics: MLE Parameter Estimation

This repository contains an analysis of **NO₂ (Nitrogen Dioxide)** concentration data. The project involves data cleaning, variable transformation based on a unique identifier (Roll Number), and fitting a custom Probability Density Function (PDF) using **Maximum Likelihood Estimation (MLE)**.

## Project Overview
The goal of this assignment is to estimate parameters ($\mu$, $\lambda$, $c$) for a dataset where the variable $x$ (NO₂ levels) is transformed into $z$ based on specific student parameters.

**Student Roll Number:** `102303683`

### 1. Variable Transformation
The transformation is defined as:
$$z = x + a_r \sin(b_r x)$$

Where parameters are derived from the roll number ($r$):
* $a_r = 0.05 \times (r \pmod 7) = 0.0$
* $b_r = 0.3 \times ((r \pmod 5) + 1) = 1.2$

*(Since $a_r = 0$, the transformation effectively simplifies to $z = x$ for this dataset).*

### 2. Learned PDF Model
We fit the data to the following probability density function:
$$\hat{p}(z) = c \cdot e^{-\lambda(z - \mu)^2}$$

The parameters were estimated as:
* **Mean ($\mu$):** `25.803054`
* **Precision Parameter ($\lambda$):** `0.001459`
* **Normalization Constant ($c$):** `0.021554`

## Results
The plot below shows the empirical histogram of the NO₂ data overlaid with the estimated PDF curve.

![PDF Plot](pdf_plot.png)

## Files in Repository
* `main.ipynb`: Jupyter Notebook containing the data loading, cleaning, math calculations, and plotting code.
* `data.csv`: The source dataset containing air quality measurements.
* `pdf_plot.png`: The generated visualization of the histogram and PDF.
* `readme.md`: Project documentation.

## How to Run
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/ashdev-7/predictive-analytics.git](https://github.com/ashdev-7/predictive-analytics.git)
    cd predictive-analytics
    ```

2.  **Install dependencies**
    ```bash
    pip install pandas numpy matplotlib
    ```

3.  **Run the analysis**
    Open `main.ipynb` in Jupyter Notebook or VS Code and run all cells.
