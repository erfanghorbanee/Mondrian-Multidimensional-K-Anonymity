# Mondrian-Multidimensional-K-Anonymity

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

An application of the "Mondrian Multidimensional K-Anonymity" article in Python.

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/erfanghorbanee/Mondrian-Multidimensional-K-Anonymity.git
cd Mondrian-Multidimensional-K-Anonymity
```

```bash
python3 -m venv venv
. venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

To run the Mondrian anonymization process on your data:

```bash
python3 mondrian.py --input data/adult.csv --sensitive-data class
```

You can also get an illustration of c-avg metric for different k values using [data/adult.csv](https://github.com/erfanghorbanee/Mondrian-Multidimensional-K-Anonymity/blob/main/data/adult.csv) file:

```bash
python3 mondrian.py --test
```

![image](https://github.com/erfanghorbanee/Mondrian-Multidimensional-K-Anonymity/assets/49264993/2d2cfbfa-2b84-431a-9280-733758079b3e)

**Note that this is only an illustration of algorithm quality and will be generated using predefined data and the generated figure is always the same.**

To see the full list of commands run:

```bash
python3 mondrian.py --help
```

```bash
python3 mondrian.py --help

usage: mondrian.py [-h] [--ei Explicit Identifier [Explicit Identifier ...]]
                   [--sensitive-data Sensitive Data [Sensitive Data ...]] [--k K] [--input INPUT] [--test]

An application of 'Mondrian Multidimensional K-Anonymity' article in Python

options:
  -h, --help            show this help message and exit
  --ei Explicit Identifier [Explicit Identifier ...]
                        Explicit Identifiers to be removed from dataset (example: --ei id name)
  --sensitive-data Sensitive Data [Sensitive Data ...]
                        Sensitive Data you don't want to anonymize to maintain utility (example: --sensitive-
                        data salary)
  --k K                 The k value for k-anonymity (default: 2)
  --input INPUT         Input csv file path (default: data/adult.csv)
  --test                Draws an illustration of c-avg metric for different k values using data/adult.csv file.
```

## Resources

### Article

- [Mondrian Multidimensional K-Anonymity by K. LeFevre; D.J. DeWitt; R. Ramakrishnan](https://ieeexplore.ieee.org/abstract/document/1617393)

### Dataset

- [Adults database from the UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/dataset/2/adult)
