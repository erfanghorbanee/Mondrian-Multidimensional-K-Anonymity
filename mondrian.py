import statistics
import warnings
from typing import Dict

import pandas as pd

# Read data from data/dataset.csv file and store it in a pandas DataFrame
#data_df = pd.read_csv("data/dataset.csv")
data_df = pd.read_csv("data/adult.csv")
# data_df.to_csv("D:/UniGe/DataProtection/Mondrian-Multidimensional-K-Anonymity/data.csv", index=False)

# Remove 'id' column
#data_df = data_df.drop("id", axis=1)


def frequency_set(partition: pd.DataFrame, dimension: str) -> Dict[str, int]:
    # counts all unique value in partition
    frequency = partition[dimension].value_counts().to_dict()
    return frequency
    



def normalize_data(df):
    """Normalize the data and return mappings of original to normalized values."""

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


def choose_dimension(partition, map):
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


def generalize(partition, exclude_columns):
    # Categorical generalize
    for dimension in partition.select_dtypes(include=["object", "string"]).columns:
        if dimension not in exclude_columns:
            unique_values = partition[dimension].unique()
            generalized_value = "-".join(unique_values)
            partition.loc[:, dimension] = generalized_value

    # Numerical generalize
    for dimension in partition.select_dtypes(include=["int64", "float64"]).columns:
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


# Calculate mapping for normalization so we can set it by default in anonymize function
mapping = normalize_data(data_df)


def anonymize(partition, k, exclude_columns=[], map=mapping):
    dimension = choose_dimension(partition, map)

    if is_allowable_to_cut(partition, k, dimension):
        frequnceData = frequency_set(partition, dimension)
        splitValue = find_median(frequnceData)
        left = left_hand_side(partition, dimension, splitValue)
        right = right_hand_side(partition, dimension, splitValue)
        return pd.concat(
            [anonymize(left, k, exclude_columns), anonymize(right, k, exclude_columns)]
        )

    else:
        return generalize(partition, exclude_columns)


#print(anonymize(data_df, 2, exclude_columns=["name", "disease"]))
print(anonymize(data_df , 2 , exclude_columns = ["class"]))
