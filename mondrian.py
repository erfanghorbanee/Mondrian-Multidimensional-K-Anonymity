import statistics
from typing import Dict

import pandas as pd

# Data as seen in the provided image
data = {
    "id": [0, 1, 2, 3, 4, 5],
    "Age": [25, 25, 26, 27, 27, 28],
    "Sex": ["Male", "Female", "Male", "Male", "Female", "Male"],
    "Zipcode": [53711, 53712, 53711, 53710, 53712, 53711],
    "Disease": ["Flu", "Hepatitis", "Brochitis", "Broken Arm", "AIDS", "Hang Nail"],
}

# Create a DataFrame
data_df = pd.DataFrame(data)

# data_df.to_csv("D:/UniGe/DataProtection/Mondrian-Multidimensional-K-Anonymity/data.csv", index=False)

# Remove 'id' column
data_df = data_df.drop("id", axis=1)


def frequency_set(partition: pd.DataFrame, dimention: str) -> Dict[str, int]:
    # counts all unique value in partition
    frequency = partition[dimention].value_counts().to_dict()
    return frequency


def normalize_data(df):
    """Normalize the data and return mappings of original to normalized values."""
    result = df.copy()
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


def choose_dimension(normalized_ranges: Dict[str, float]) -> str:
    """Return the dimension with the largest normalized range."""

    return max(normalized_ranges, key=normalized_ranges.get)


def find_median(frequencySetData):
    """calculate the split value which is the median of partition projected on dimension.
    The median is the central number of a data set. Arrange data points from smallest to largest
    and locate the central number. This is the median.
    """
    return statistics.median(frequencySetData)


def left_hand_side(partition, dimension, splitValue):
    return partition[partition[dimension] <= splitValue]


def right_hand_side(partition, dimension, splitValue):
    return partition[partition[dimension] > splitValue]


def is_allowable_to_cut(partition, k, dimension):
    frequnceData = frequency_set(partition, dimension)
    splitValue = find_median(frequnceData)
    if (
        len(left_hand_side(partition, dimension, splitValue)) >= k
        and len(right_hand_side(partition, dimension, splitValue)) >= k
    ):
        return True
    else:
        return False


def generalize(partition, dimension):
    min_value = partition[dimension].min()
    max_value = partition[dimension].max()
    if min_value == max_value:
        return partition
    else:
        generalized_value = f"{min_value} - {max_value}"
        partition[dimension] = partition[dimension].apply(lambda x: generalized_value)
        return partition


def anonymize(partition, dimension, k):

    if is_allowable_to_cut(partition, k, dimension):
        frequnceData = frequency_set(partition, dimension)
        splitValue = find_median(frequnceData)
        left = left_hand_side(partition, dimension, splitValue)
        right = right_hand_side(partition, dimension, splitValue)
        return pd.concat(
            [anonymize(left, dimension, k), anonymize(right, dimension, k)]
        )

    else:
        print(dimension)
        print(partition, "\n")
        return partition


def anonymize_over_dimensions(partition, dimensions, k):
    """for widest dimension, anonymize the partition and when not possible to cut,
    anonymize the resulted partiotion with the next dimension
    till all dimensions are anonymized.
    """

    for dimension in dimensions:
        partition = anonymize(partition, dimension, k)
        print(dimension)
        # print(partition)
        # print("-------------------")
    return partition


print(normalize_data(data_df))

# dimensions = normalize_range(data_df)
# anonymize_over_dimensions(data_df, dimensions, 2)
