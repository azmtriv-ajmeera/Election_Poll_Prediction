import pandas as pd
from pathlib import Path

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parents[2]

# locate the raw data folder(input directory)
RAW_DIR = BASE_DIR / "data" / "raw" / "google_trends"

# locate the processed data folder(output directory)
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "google_trends"

# Create output directory if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load Google Trends datasets
trends2019 = pd.read_csv(RAW_DIR / "Google_Trends_2019.csv")
trends2024 = pd.read_csv(RAW_DIR / "Google_Trends_2024.csv")


##displays dataset shape
print("=" * 60)
print("GOOGLE TRENDS 2019")
print("=" * 60)
print("Shape:", trends2019.shape)

print("\n")

print("=" * 60)
print("GOOGLE TRENDS 2024")
print("=" * 60)
print("Shape:", trends2024.shape)


##displays first 5 rows
print("\nFirst 5 Rows of 2019 Dataset")
print(trends2019.head())

print("\nFirst 5 Rows of 2024 Dataset")
print(trends2024.head())

print("\nLast 5 Rows of 2019 Dataset")
print(trends2019.tail())

print("\nLast 5 Rows of 2024 Dataset")
print(trends2024.tail())


##display column names
print("\nColumns in Google Trends 2019:")
print(trends2019.columns.tolist())

print("\nColumns in Google Trends 2024:")
print(trends2024.columns.tolist())


##Display Dataset Information
print("\nInformation - Google Trends 2019")
print(trends2019.info())

print("\nInformation - Google Trends 2024")
print(trends2024.info())


##Display Summary Statistics
print("\nSummary Statistics - 2019")
print(trends2019.describe(include="all"))

print("\nSummary Statistics - 2024")
print(trends2024.describe(include="all"))

##check missing values
print("=" * 60)
print("MISSING VALUES - GOOGLE TRENDS 2019")
print("=" * 60)
print(trends2019.isnull().sum())

print("\n")

print("=" * 60)
print("MISSING VALUES - GOOGLE TRENDS 2024")
print("=" * 60)
print(trends2024.isnull().sum())


##check duplicate rows
print("=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)

print("2019 :", trends2019.duplicated().sum())
print("2024 :", trends2024.duplicated().sum())


##rename columns
trends2019.rename(
    columns={
        "geoName": "State",
        "TRS": "BRS"
    },
    inplace=True
)

trends2024.rename(
    columns={
        "geoName": "State"
    },
    inplace=True
)


##verifying columns names
print(trends2019.columns)
print(trends2024.columns)


##validate search interest values
print("=" * 60)
print("VALUE RANGE CHECK")
print("=" * 60)

print("\n2019")
print(trends2019.describe())

print("\n2024")
print(trends2024.describe())


##verify state names
print("=" * 60)
print("STATE NAMES - 2019")
print("=" * 60)

print(trends2019["State"].sort_values().tolist())

print("\n")

print("=" * 60)
print("STATE NAMES - 2024")
print("=" * 60)

print(trends2024["State"].sort_values().tolist())



##final validation
print("=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print("2019 Shape :", trends2019.shape)
print("2024 Shape :", trends2024.shape)

print("\n2019 Missing Values")
print(trends2019.isnull().sum().sum())

print("\n2024 Missing Values")
print(trends2024.isnull().sum().sum())

print("\n2019 Duplicate Rows :", trends2019.duplicated().sum())
print("2024 Duplicate Rows :", trends2024.duplicated().sum())



##saving cleaned datasets
trends2019.to_csv(
    PROCESSED_DIR / "Google_Trends_2019.csv",
    index=False
)

trends2024.to_csv(
    PROCESSED_DIR / "Google_Trends_2024.csv",
    index=False
)

print("\nCleaned Google Trends datasets saved successfully.")




#verifying saved files
verify2019 = pd.read_csv(PROCESSED_DIR / "Google_Trends_2019.csv")
verify2024 = pd.read_csv(PROCESSED_DIR / "Google_Trends_2024.csv")

print("\nProcessed 2019 Shape :", verify2019.shape)
print("Processed 2024 Shape :", verify2024.shape)