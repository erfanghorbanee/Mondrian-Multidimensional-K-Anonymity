import csv
import random

from faker import Faker

# Initialize the Faker generator
fake = Faker(["it_IT", "en_US"])

# List of diseases
diseases = [
    "Cancer",
    "Diabetes",
    "Alzheimer's Disease",
    "Parkinson's Disease",
    "HIV/AIDS",
    "Tuberculosis",
    "Malaria",
    "Ebola",
    "Zika Virus",
    "Influenza",
    "Common Cold",
    "Coronavirus",
    "Asthma",
    "Hepatitis",
    "Dengue Fever",
    "Cholera",
    "Lyme Disease",
    "Rabies",
    "Measles",
    "Chickenpox",
]

# Open the CSV file for writing
with open("data/dataset.csv", "w", newline="") as csvfile:
    fieldnames = ["id", "name", "age", "sex", "zip_code", "disease"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Generate and write data for 10 entries
    for i in range(10):
        writer.writerow(
            {
                "id": i,
                "name": fake.name(),
                "age": str(random.randint(20, 40)),
                "sex": random.choice(["M", "F"]),
                "zip_code": str(random.randint(10000, 99999)),
                "disease": random.choice(diseases),
            }
        )
