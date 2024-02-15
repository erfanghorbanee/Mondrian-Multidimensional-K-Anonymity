import argparse
import statistics
import time
import warnings
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd


def frequency_set(partition: pd.DataFrame, dimension: str) -> Dict[str, int]:
    # Counts all unique dimension values in a given partition (example: {40: 2, 45: 1, 50: 1} for age dimension)
    frequency = partition[dimension].value_counts().to_dict()
    return frequency


def normalize_data(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Normalize the data using Min-Max Normalization method and return mappings of original to normalized values."""

    mapping = {}

    for dimension in df.select_dtypes(include=["int64", "float64"]).columns:
        max_value = df[dimension].max()
        min_value = df[dimension].min()

        # Add to mapping
        unique_values = df[dimension].unique()
        mapping[dimension] = {
            original: round((original - min_value) / (max_value - min_value), 4)
            for original in unique_values
        }

    return mapping


def choose_dimension(partition: pd.DataFrame, map: Dict[str, Dict[str, float]]) -> str:
    """Return the dimension with the largest normalized range."""

    max_range = -1
    choosen_dimension = ""

    for dimension in partition.select_dtypes(include=["int64", "float64"]).columns:
        max_value = partition[dimension].max()
        min_value = partition[dimension].min()

        # get normalized values from map and calculate their range
        normalize_max_value = map[dimension][max_value]
        normalize_min_value = map[dimension][min_value]
        range = normalize_max_value - normalize_min_value

        if range > max_range:
            max_range = range
            choosen_dimension = dimension

    return choosen_dimension


def find_median(frequencySetData) -> float:
    """calculate the split value which is the median of partition projected on dimension.
    The median is the central number of a data set. Arrange data points from smallest to largest
    and locate the central number. This is the median.
    """
    return statistics.median(frequencySetData)


def left_hand_side(
    partition: pd.DataFrame, dimension: str, splitValue: float
) -> pd.DataFrame:
    return partition[partition[dimension] <= splitValue]


def right_hand_side(
    partition: pd.DataFrame, dimension: str, splitValue: float
) -> pd.DataFrame:
    return partition[partition[dimension] > splitValue]


def is_allowable_to_cut(partition: pd.DataFrame, k: int, dimension: str) -> bool:
    frequnceData = frequency_set(partition, dimension)
    splitValue = find_median(frequnceData)
    if (
        len(left_hand_side(partition, dimension, splitValue)) >= k
        and len(right_hand_side(partition, dimension, splitValue)) >= k
    ):
        return True
    else:
        return False


def generalize(partition: pd.DataFrame, exclude_columns: List[str]) -> pd.DataFrame:
    # Categorical generalize
    for dimension in partition.select_dtypes(include=["object", "string"]).columns:
        if dimension not in exclude_columns:
            unique_values = partition[dimension].unique()
            generalized_value = "-".join(unique_values)
            partition.loc[:, dimension] = generalized_value

    # Numerical generalize
    for dimension in partition.select_dtypes(include=["int64", "float64"]).columns:
        if dimension not in exclude_columns:
            min_value = partition[dimension].min()
            max_value = partition[dimension].max()

            if min_value == max_value:
                continue
            else:
                generalized_value = f"{min_value} - {max_value}"

                warnings.filterwarnings("ignore", category=FutureWarning)
                partition.loc[:, dimension] = generalized_value
                warnings.filterwarnings("default", category=FutureWarning)

    return partition


total_equivalence_classes = 0
discernability_penalty = 0


def anonymize(
    partition: pd.DataFrame,
    k: int,
    map: Dict[str, Dict[str, float]],
    exclude_columns=[],
):
    global total_equivalence_classes
    global discernability_penalty

    dimension = choose_dimension(partition, map)

    if is_allowable_to_cut(partition, k, dimension):
        frequnceData = frequency_set(partition, dimension)
        splitValue = find_median(frequnceData)
        left = left_hand_side(partition, dimension, splitValue)
        right = right_hand_side(partition, dimension, splitValue)
        return pd.concat(
            [
                anonymize(left, k, map, exclude_columns),
                anonymize(right, k, map, exclude_columns),
            ]
        )

    else:
        total_equivalence_classes += 1
        discernability_penalty += len(partition) ** 2

        return generalize(partition, exclude_columns)


# ===========Main Program=================

start_time = time.time()

parser = argparse.ArgumentParser(
    description="An application of 'Mondrian Multidimensional K-Anonymity' article in Python"
)

# Explicit Identifiers
parser.add_argument(
    "--ei",
    metavar="Explicit Identifier",
    type=str,
    nargs="+",
    default=[],
    help="Explicit Identifiers to be removed from dataset (example: --ei id name)",
)

# Sensitive Data
parser.add_argument(
    "--sensitive-data",
    metavar="Sensitive Data",
    type=str,
    nargs="+",
    default=[],
    help="Sensitive Data you don't want to anonymize to maintain utility (example: --sensitive-data salary)",
)

# K
parser.add_argument(
    "--k", type=int, default=2, help="The k value for k-anonymity (default: 2)"
)

parser.add_argument(
    "--input",
    type=str,
    default="data/adult.csv",
    help="Input csv file path (default: data/adult.csv)",
)

parser.add_argument(
    "--test",
    action="store_true",
    help="Draws an illustration of c-avg metric for different k values using data/adult.csv file.",
)


args = parser.parse_args()


# Read data from data/*.csv file and store it in a pandas DataFrame
data_directory = args.input
data_df = pd.read_csv(data_directory)


# Drop Explicit Identifiers if exist in the dataset
column_names = data_df.columns.tolist()

for e in args.ei:
    if e in column_names:
        data_df = data_df.drop(e, axis=1)
    else:
        print(f"{e} explicit identifier was not found in data columns")
        exit()


print("⏳ Anonymizing data, it may take a while...\n")

# Calculate mapping for normalization
mapping = normalize_data(data_df)

# Anonymize and save the result in data/output.csv
anonymized_data = anonymize(
    data_df, args.k, map=mapping, exclude_columns=args.sensitive_data
)

print(f"🛡️  K value for anonymity: {args.k}")

# Calculate normalized average equivalence class metric
total_records = len(data_df)
c_avg = (total_records / total_equivalence_classes) / args.k

print(f"📊 Total Records: {total_records}")
print(f"📊 Total Equivalence Classes: {total_equivalence_classes}")
print(f"📊 Normalized Average Equivalence Class Metric: {c_avg:.2f}")
print(f"Discernability Penalty: {discernability_penalty}")


# Save anonymized data to data/output.csv
anonymized_data.to_csv("data/output.csv", index=False)

# Calculate execution time
end_time = time.time()
execution_time = end_time - start_time
print(f"⏱️  Execution Time: {execution_time:.2f} seconds\n")

print("\n✅ Process finished successfully.")
print("📁 Anonymized data is saved in data/output.csv")


# illustrate a figure if --test flag is set with predefined data.
if args.test:
    print("\nCreating the figure for data/adult.csv ...")
    data_df = pd.read_csv("data/adult.csv")
    total_records = len(data_df)
    mapping = normalize_data(data_df)

    k_values = [5, 20, 40, 60, 80, 100]
    c_avg_list = []

    for k in k_values:
        total_equivalence_classes = 0
        anonymize(data_df, k, map=mapping, exclude_columns=["class"])

        c_avg = (total_records / total_equivalence_classes) / k
        c_avg_list.append(c_avg)

    plt.plot(k_values, c_avg_list, marker="^", color="blue", label="Mondrian")
    plt.xlabel("k")
    plt.ylabel("Normalized Average Equivalence Class Metric")
    plt.title("Comparison of c-avg for different k values")

    plt.legend()
    plt.show()
