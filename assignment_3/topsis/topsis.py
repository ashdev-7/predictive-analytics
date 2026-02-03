import sys
import pandas as pd
import numpy as np
import os

def main():
    # Check parameters
    if len(sys.argv) != 5:
        print("Error: Wrong number of parameters.")
        print("Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>")
        print('Example: python topsis.py data.csv "1,1,1,2" "+,+,-,+" result.csv')
        sys.exit(1)

    input_file = sys.argv[1]
    weights_input = sys.argv[2]
    impacts_input = sys.argv[3]
    output_file = sys.argv[4]

    # Validate file existence
    if not os.path.exists(input_file):
        print("Error: File not found")
        sys.exit(1)

    # Read CSV
    try:
        df = pd.read_csv(input_file)
    except:
        print("Error: Unable to read input file. Ensure it is a valid CSV.")
        sys.exit(1)

    # Validate column count
    if df.shape[1] < 3:
        print("Error: Input file must contain three or more columns")
        sys.exit(1)

    # Validate numeric data
    try:
        data = df.iloc[:, 1:].astype(float)
    except ValueError:
        print("Error: From 2nd to last columns must contain numeric values only")
        sys.exit(1)

    weights = weights_input.split(',')
    impacts = impacts_input.split(',')

    # Validate lengths
    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        print("Error: Number of weights, impacts and columns (from 2nd to last) must be same")
        sys.exit(1)

    # Validate weights are numeric
    try:
        weights = np.array(weights, dtype=float)
    except ValueError:
        print("Error: Weights must be numeric values separated by commas")
        sys.exit(1)

    # Validate impacts format
    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be either '+' or '-'")
        sys.exit(1)

    # Vector Normalization
    rss = np.sqrt((data ** 2).sum())
    
    # Check for zero columns
    if (rss == 0).any():
        print("Error: One of the columns contains all zeros. Cannot proceed with normalization.")
        sys.exit(1)

    normalized = data / rss
    weighted = normalized * weights

    # Ideal Best and Worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Euclidean Distance
    d_plus = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Performance Score
    denom = d_plus + d_minus
    score = np.divide(d_minus, denom, out=np.zeros_like(d_minus), where=denom!=0)

    # Output
    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    try:
        df.to_csv(output_file, index=False)
        print(f"Success: Result file saved as {output_file}")
    except PermissionError:
        print(f"Error: Permission denied. Close {output_file} if it is open.")

if __name__ == "__main__":
    main()