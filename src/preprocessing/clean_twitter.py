import pandas as pd
from pathlib import Path


##finding project folder
BASE_DIR = Path(__file__).resolve().parents[2]


##locate the raw data folder
RAW_DIR = BASE_DIR / "data" / "raw" / "twitter"

##locate the processed data folder
PROCESSED_DIR = BASE_DIR / "data" / "processed" / "twitter"

##create the output directory if it doesnt exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

twitter2019=pd.read_csv(RAW_DIR / "IndianElection19TwitterData.csv")
twitter2024=pd.read_csv(RAW_DIR / "Election_2024_Tweets.csv")


##displays the first 5 rows
print(twitter2019.head())
print(twitter2024.head())


#displays the shape of the datasets
print("shape:" ,twitter2019.shape)
print("shape:" ,twitter2024.shape)


#columns of the both datasets
print("="*60)
print("\n COLUMNS")
print("="*60)
print(twitter2019.columns.tolist())
print(twitter2024.columns.tolist())


##displays last 5 rows
print("="*60)
print("\n TWITTER2019 LAST 5 ROWS")
print("="*60)
print(twitter2019.tail())
print("="*60)
print("\n TWITTER2024 LAST 5 ROWS")
print("="*60)
print(twitter2024.tail())


#information of 2019 and 2024 datasets
print("="*60)
print("\nInformation of 2019")
print("="*60)
print(twitter2019.info())
print("="*60)
print("\nInformation of 2024")
print("="*60)
print(twitter2024.info())


##summary statistics for both 2019 and 2024 datasets
print("="*60)
print("\nSummary Statistics of 2019")
print("="*60)
print(twitter2019.describe(include="all"))
print("="*60)
print("\nSummary Statistics of 2019")
print("="*60)
print(twitter2024.describe(include="all"))


##check missing values
print("=" * 60)
print("MISSING VALUES - TWITTER 2019")
print("=" * 60)
print(twitter2019.isnull().sum())

print("\n")

print("=" * 60)
print("MISSING VALUES - TWITTER 2024")
print("=" * 60)
print(twitter2024.isnull().sum())

##removing the missing values
twitter2024.dropna(subset=["text"], inplace=True)

##verifying missing values
print(twitter2019.isnull().sum())
print(twitter2024.isnull().sum())


##checking duplicate values
print("=" * 60)
print("DUPLICATE ROWS - TWITTER 2019")
print("=" * 60)
print(twitter2019.duplicated().sum())

print()

print("=" * 60)
print("DUPLICATE ROWS - TWITTER 2024")
print("=" * 60)
print(twitter2024.duplicated().sum())

##remove unnecessary columns
twitter2019.drop(columns=["Unnamed: 0"], inplace=True)
twitter2024.drop(columns=["link"], inplace=True)


##rename columns
twitter2019.rename(columns={
    "Date": "Date",
    "User": "User",
    "Tweet": "Text"
}, inplace=True)

twitter2024.rename(columns={
    "date": "Date",
    "text": "Text"
}, inplace=True)

##removing missing tweets
twitter2024.dropna(subset=["Text"], inplace=True)


##converting  2024 dates
print(twitter2024["Date"].head(10)) 

twitter2024["Date"] = (
    twitter2024["Date"]
    .str.replace("·", "", regex=False)
    .str.replace("UTC", "", regex=False)
    .str.strip()
)

twitter2024["Date"] = pd.to_datetime(
    twitter2024["Date"],
    format="%b %d, %Y %I:%M %p",
    errors="coerce"
)
print(twitter2024["Date"].isnull().sum())

twitter2024["Date"] = pd.to_datetime(twitter2024["Date"])

print(twitter2024["Date"].head())
print(twitter2024["Date"].isnull().sum())
##convert dates
twitter2019["Date"] = pd.to_datetime(twitter2019["Date"])

twitter2019["Date"] = twitter2019["Date"].dt.tz_localize(None)

##add year
twitter2019["Year"] = 2019
twitter2024["Year"] = 2024

print(twitter2019.info())
print(twitter2024.info())



print(twitter2019['Date'].head())


##ADDING TWEET TEXT CLEANING
import re
def clean_tweet(text):

    if pd.isna(text):
        return text

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Remove only #
    text = re.sub(r"#", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


twitter2019["Clean_Text"] = twitter2019["Text"].apply(clean_tweet)

twitter2024["Clean_Text"] = twitter2024["Text"].apply(clean_tweet)

print(repr(twitter2019.loc[0, "Clean_Text"]))


print(twitter2019[["Text","Clean_Text"]].head())

print()

print(twitter2024[["Text","Clean_Text"]].head())


##confirming the final validaitons
print("=" * 60)
print("Twitter 2019")
print("=" * 60)
print(twitter2019.info())
print()
print(twitter2019.isnull().sum())
print()
print("Duplicates:", twitter2019.duplicated().sum())

print()

print("=" * 60)
print("Twitter 2024")
print("=" * 60)
print(twitter2024.info())
print()
print(twitter2024.isnull().sum())
print()
print("Duplicates:", twitter2024.duplicated().sum())


##knowing which are the duplicate rows
print(
    twitter2024.loc[
        twitter2024.duplicated(subset=["Clean_Text"], keep=False),
        ["Date", "Text", "Clean_Text", "No_of_likes", "No_of_comments"]
    ]
)

duplicate_rows = twitter2024[twitter2024.duplicated()]

print(duplicate_rows)


##removing those duplicates
twitter2024.drop_duplicates(inplace=True)

##again verifying those duplicates removed or not
print("Duplicates:", twitter2024.duplicated().sum())
print("Shape:", twitter2024.shape)


##save the cleaned datasets
twitter2019.to_csv(
    PROCESSED_DIR / "Twitter_2019_Cleaned.csv",
    index=False
)

twitter2024.to_csv(
    PROCESSED_DIR / "Twitter_2024_Cleaned.csv",
    index=False
)

print("Twitter preprocessing completed successfully!")