import pandas as pd
import numpy as np
import sys
import os


def validate_input(input_file, weights, impacts):
    if not os.path.exists(input_file):
        print("Error: Input file not found")
        sys.exit(1)

    try:
        dataframe = pd.read_csv(input_file)
    except:
        print("Error: Cannot read input file")
        sys.exit(1)

    if dataframe.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns")
        sys.exit(1)

    try:
        decision_matrix = dataframe.iloc[:, 1:].astype(float)
    except:
        print("Error: From 2nd column onward, values must be numeric")
        sys.exit(1)

    weights = np.array(weights, dtype=float)
    impacts = np.array(impacts)

    if len(weights) != decision_matrix.shape[1] or len(impacts) != decision_matrix.shape[1]:
        print("Error: Weights, impacts and criteria count must match")
        sys.exit(1)

    if not all(weights > 0):
        print("Error: Weights must be positive")
        sys.exit(1)

    for impact in impacts:
        if impact not in ['+', '-']:
            print("Error: Impacts must be '+' or '-'")
            sys.exit(1)

    return dataframe, decision_matrix, weights, impacts


def apply_topsis(dataframe, decision_matrix, weights, impacts):
    # STEP 1: Normalize decision matrix
    normalized_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))

    # STEP 2: Weighted normalized matrix
    weighted_normalized_matrix = normalized_matrix * weights

    # STEP 3: Positive & Negative Ideal Solutions
    positive_ideal_solution = []
    negative_ideal_solution = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            positive_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].max())
            negative_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].min())
        else:
            positive_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].min())
            negative_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].max())

    positive_ideal_solution = np.array(positive_ideal_solution)
    negative_ideal_solution = np.array(negative_ideal_solution)

    # STEP 4: Separation measures
    distance_from_pis = np.sqrt(((weighted_normalized_matrix - positive_ideal_solution) ** 2).sum(axis=1))
    distance_from_nis = np.sqrt(((weighted_normalized_matrix - negative_ideal_solution) ** 2).sum(axis=1))

    # STEP 5: Relative closeness
    topsis_score = distance_from_nis / (distance_from_pis + distance_from_nis)

    # STEP 6: Ranking
    rank = topsis_score.rank(ascending=False, method='dense').astype(int)

    result = dataframe.copy()
    result["Topsis Score"] = topsis_score
    result["Rank"] = rank

    return result


def main():
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <inputfile> <weights> <impacts> <outputfile>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    dataframe, decision_matrix, weights, impacts = validate_input(
        input_file, weights, impacts
    )

    result = apply_topsis(dataframe, decision_matrix, weights, impacts)
    result.to_csv(output_file, index=False)

    print("TOPSIS result saved to", output_file)


if __name__ == "__main__":
    main()
