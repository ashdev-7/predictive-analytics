# Statistical Modeling of NO2 Concentration via MLE

This project focuses on the statistical analysis of air quality data, specifically Nitrogen Dioxide (NO2) levels. The objective is to apply a roll-number-based non-linear transformation to the data and estimate the parameters of a custom Probability Density Function (PDF) using Maximum Likelihood Estimation (MLE).

## Project Objectives
* **Data Preprocessing:** Clean and prepare real-world air quality data (source: Kaggle).
* **Variable Transformation:** Apply a parameterized transformation (x -> z) unique to the student's roll number.
* **Parameter Estimation:** Mathematically derive and calculate the optimal parameters (mu, lambda, c) for the dataset.
* **Visualization:** Plot the empirical data distribution against the learned theoretical model.

## Data Transformation Logic
The dataset feature x (NO2) is transformed into a new variable z using a sine-based function derived from the student's unique identifier.

**Student Roll Number:** 102303683

The transformation rules are:
z = x + a_r * sin(b_r * x)

Where the coefficients are calculated as:
* **a_r (Amplitude):** 0.05 * (102303683 mod 7) = 0
* **b_r (Frequency):** 0.3 * ((102303683 mod 5) + 1) = 1.2

Since a_r is 0 for this specific roll number, the transformation simplifies to an identity function (z = x), meaning the original distribution is preserved.

## Mathematical Model (MLE)
We model the probability density of the transformed variable z using the following Gaussian-like function:

p_hat(z) = c * exp(-lambda * (z - mu)^2)

Using Maximum Likelihood Estimation (MLE), the closed-form solutions for the parameters are derived as:
* **Mean (mu):** (1/N) * sum(z_i)
* **Variance (sigma^2):** Var(z)
* **Precision (lambda):** 1 / (2 * sigma^2)
* **Normalization Constant (c):** sqrt(lambda / pi)

## Estimated Parameters
Applying the MLE formulas to the dataset yielded the following optimal parameters:

| Parameter | Symbol | Estimated Value |
| :--- | :---: | :--- |
| **Mean** | mu | 25.8031 |
| **Precision** | lambda | 0.0015 |
| **Normalization** | c | 0.0216 |

## Visualization & Analysis
The plot below overlays the learned PDF (red curve) on top of the normalized histogram of the actual data.

![Distribution Plot](pdf_plot.png)

**Interpretation:**
* The **histogram** shows the empirical frequency of NO2 levels.
* The **red curve** represents the theoretical probability density learned by our model.
* The close alignment confirms that the Gaussian-based model effectively captures the central tendency and spread of the air quality data.

## Repository Structure
* **main.ipynb:** The core Python notebook containing data ingestion, math logic, and plotting.
* **data.csv:** The raw dataset.
* **pdf_plot.png:** The generated visualization output.
* **README.md:** Project documentation.

## Usage
To replicate this analysis:

1.  **Clone the repository:**
    git clone https://github.com/ashdev-7/predictive-analytics.git

2.  **Install requirements:**
    pip install pandas numpy matplotlib

3.  **Run the notebook:**
    Execute `main.ipynb` to regenerate the parameters and plots.
