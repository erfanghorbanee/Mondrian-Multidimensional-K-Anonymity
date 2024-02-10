import statistics
from typing import Dict

import pandas as pd

# Read data from data/dataset.csv file and store it in a pandas DataFrame
data_df = pd.read_csv('data/dataset.csv')

# Remove 'id' column
data_df = data_df.drop("id", axis=1)


def frequency_set(partition: pd.DataFrame, dimention: str) -> Dict[str, int]:
    # counts all unique value in partition
    frequency = partition[dimention].value_counts().to_dict()
    return frequency


def normalize_range(partition: pd.DataFrame) -> Dict[str, float]:
    """Calculate the normalized range for each numerical column (dimension)
    in the partition and return as a dictionary."""

    normalized_ranges: Dict[str, float] = {}

    # Find maximum and minimum values across all numerical dimensions
    max_value = partition.select_dtypes(include=["int64", "float64"]).max().max()
    min_value = partition.select_dtypes(include=["int64", "float64"]).min().min()

    # For each numerical column, calculate normalized ranges
    for column in partition.select_dtypes(include=["int64", "float64"]).columns:

        column_range = partition[column].max() - partition[column].min()

        # Avoid division by zero
        if max_value != min_value:
            normalized_range = column_range / (max_value - min_value)
        else:
            normalized_range = 0

        normalized_ranges[column] = round(normalized_range, 5)
        sorted_normalized_ranges = dict(
            sorted(normalized_ranges.items(), key=lambda item: item[1], reverse=True)
        )

    return sorted_normalized_ranges


# def choose_dimension(normalized_ranges: Dict[str, float]) -> str:
#     """Return the dimension with the largest normalized range."""

#     return max(normalized_ranges, key=normalized_ranges.get)


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
        return partition


def anonymize_over_dimensions(partition, dimensions, k):
    """for widest dimension, anonymize the partition and when not possible to cut,
    anonymize the resulted partiotion with the next dimension
    till all dimensions are anonymized.
    """

    for dimension in dimensions:
        partition = anonymize(partition, dimension, k)
        print(dimension)
        print(partition)
        print("-------------------")
    return partition


dimensions = normalize_range(data_df)
anonymize_over_dimensions(data_df, dimensions, 2)
