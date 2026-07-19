import pandas as pd
from pathlib import Path

#Find the Project Folder
BASE_DIR = Path(__file__).resolve().parents[2]

#Locate the Raw Data Folder
RAW_DIR = BASE_DIR / "data" / "raw" / "election_results"

#Locate the Processed Folder
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "election_results"

#Create the Folder if It Doesn't Exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Read Raw Datasets
# --------------------------------------------------

print("Reading Election Result Datasets...")

winner2019 = pd.read_csv(
    RAW_DIR / "2019_Results_Winning_Candidate.csv"
)

result2019 = pd.read_csv(
    RAW_DIR / "2019_Results.csv",
    encoding="latin1"
)

result2024 = pd.read_csv(
    RAW_DIR / "2024_Results new.csv"
)

# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------

print("\n========== 2019 WINNER DATASET ==========")
print(winner2019.head())

print("\nShape :", winner2019.shape)

print("\nColumns :")
print(winner2019.columns.tolist())


print("\n========== 2019 RESULTS DATASET ==========")
print(result2019.head())

print("\nShape :", result2019.shape)

print("\nColumns :")
print(result2019.columns.tolist())


print("\n========== 2024 RESULTS DATASET ==========")
print(result2024.head())

print("\nShape :", result2024.shape)

print("\nColumns :")
print(result2024.columns.tolist())


print(result2019["Candidate Won"].unique())



# --------------------------------------------------
# Standardize 2019 Winner Dataset
# --------------------------------------------------

winner2019 = winner2019.rename(columns={
    "Votes": "Total Votes",
    "Percentage": "% of Votes"
})

# Add Result column
winner2019["Result"] = "Won"

# Keep only required columns
winner2019 = winner2019[
    [
        "State",
        "Constituency",
        "Candidate",
        "Party",
        "Total Votes",
        "% of Votes",
        "Result"
    ]
]

# --------------------------------------------------
# Standardize 2019 Result loser Dataset
# --------------------------------------------------

result2019 = result2019.rename(columns={
    "Candidate Won": "Result"
})

# Convert loss -> Lost
result2019["Result"] = result2019["Result"].replace({
    "loss": "Lost"
})

# Keep only required columns
result2019 = result2019[
    [
        "State",
        "Constituency",
        "Candidate",
        "Party",
        "Total Votes",
        "% of Votes",
        "Result"
    ]
]


# --------------------------------------------------
# Merge 2019 Winner + Loser Datasets
# --------------------------------------------------

merged2019 = pd.concat(
    [winner2019, result2019],
    ignore_index=True
)

print("\nMerged 2019 Dataset Shape:")
print(merged2019.shape)


# --------------------------------------------------
# Standardize 2024 Dataset
# --------------------------------------------------

result2024 = result2024[
    [
        "State",
        "Constituency",
        "Candidate",
        "Party",
        "Total Votes",
        "% of Votes",
        "Result"
    ]
]


# --------------------------------------------------
# Save Processed Files
# --------------------------------------------------

merged2019.to_csv(
    PROCESSED_DIR / "Election_Results_2019.csv",
    index=False
)

result2024.to_csv(
    PROCESSED_DIR / "Election_Results_2024.csv",
    index=False
)

print("\nCleaning Completed Successfully!")

print("\nSaved Files:")

print(PROCESSED_DIR / "Election_Results_2019.csv")

print(PROCESSED_DIR / "Election_Results_2024.csv")


#removing duplicates
merged2019 = merged2019.drop_duplicates()
result2024 = result2024.drop_duplicates()

##removing extra spaces
for col in ["State", "Constituency", "Candidate", "Party"]:
    merged2019[col] = merged2019[col].str.strip()
    result2024[col] = result2024[col].str.strip()


##rename BRS->TRS
merged2019["Party"] = merged2019["Party"].replace({
    "TRS": "BRS"
})

##convert votes column to numeric
merged2019["Total Votes"] = pd.to_numeric(
    merged2019["Total Votes"],
    errors="coerce"
)

merged2019["% of Votes"] = pd.to_numeric(
    merged2019["% of Votes"],
    errors="coerce"
)

##checking missing values
print(merged2019.isnull().sum())
print(result2024.isnull().sum())


#save the processed data
merged2019.to_csv(
    PROCESSED_DIR / "Election_Results_2019.csv",
    index=False
)

result2024.to_csv(
    PROCESSED_DIR / "Election_Results_2024.csv",
    index=False
)




print("Duplicate rows in 2019:", merged2019.duplicated().sum())
print("Duplicate rows in 2024:", result2024.duplicated().sum())

print("\n2019 Result Counts")
print(merged2019["Result"].value_counts())

print("\n2024 Result Counts")
print(result2024["Result"].value_counts())