from typing import Dict

import pandas as pd

data_dict = {
    "id": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "name": [
        "Anthony Bowen",
        "Melissa Brock",
        "Sig.ra Eva Salata",
        "Joshua Vargas",
        "Sig. Ottavio Malaparte",
        "Tina Marinetti",
        "Anthony Rangel",
        "Eva Grifeo",
        "Heather Romero",
        "Patricia Walton",
    ],
    "age": [27, 29, 26, 29, 33, 35, 21, 33, 37, 29],
    "sex": ["F", "F", "F", "M", "M", "M", "M", "F", "F", "M"],
    "zip_code": [26128, 25973, 30792, 28940, 80591, 49346, 56817, 76710, 92459, 78786],
    "disease": [
        "Measles",
        "Diabetes",
        "Measles",
        "Lyme Disease",
        "Malaria",
        "Dengue Fever",
        "Measles",
        "Influenza",
        "Alzheimer's Disease",
        "Cancer",
    ],
}

data_df = pd.DataFrame(data_dict)

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

    return normalized_ranges


def choose_dimension(normalized_ranges: Dict[str, float]) -> str:
    """Return the dimension with the largest normalized range."""

    return max(normalized_ranges, key=normalized_ranges.get)


def find_median(frequencySetData):
    '''calculate the split value which is the median of partition projected on dimension'''

    return sum(frequencySetData.values()) / len(frequencySetData.keys())


def left_hand_side(partition, dimension, splitValue):
    return [i for i in partition[dimension] if i <= splitValue]



def right_hand_side(partition, dimension, splitValue):
    return [i for i in partition[dimension] if i > splitValue]


def anonymize(partition, k):
    normalized_ranges = normalize_range(partition)
    dimension = choose_dimension(normalized_ranges)

    print(is_allowable_to_cut(partition, k, dimension))
    if is_allowable_to_cut(partition, k, dimension):
        frequnceData = frequency_set(partition, dimension)
        splitValue = find_median(frequnceData)
        left = left_hand_side(partition, dimension, splitValue)
        right = right_hand_side(partition, dimension, splitValue)
        anonymize(left, k)
        anonymize(right, k)
    else:
        return partition



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


print(anonymize(data_df, 2))
