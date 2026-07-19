from pytrends.request import TrendReq
from pathlib import Path
import pandas as pd
import time

pytrends = TrendReq(hl='en-US', tz=330)

TIMEFRAME = "2024-01-01 2024-06-04"

party_groups = [
    ["BJP", "INC", "AAP", "TMC", "DMK"],
    ["BJP", "AIADMK", "TDP", "BJD", "SP"],
    ["BJP", "RJD", "Shiv Sena", "NCP", "BRS"]
]

BASE_DIR = Path(__file__).resolve().parents[2]

output_folder = BASE_DIR / "data" / "raw" / "google_trends"
output_folder.mkdir(parents=True, exist_ok=True)

merged_df = None

for i, parties in enumerate(party_groups, start=1):

    print(f"Downloading Group {i}")

    pytrends.build_payload(
        kw_list=parties,
        timeframe=TIMEFRAME,
        geo="IN"
    )

    df = pytrends.interest_by_region(
        resolution="REGION",
        inc_low_vol=True
    )

    # Remove the duplicate BJP column after the first group
    if merged_df is None:
        merged_df = df
    else:
        df = df.drop(columns=["BJP"])
        merged_df = merged_df.join(df)

    time.sleep(10)

# Save one CSV
merged_df.to_csv(
    output_folder / "Google_Trends_2024.csv"
)

print("Saved Google_Trends_2024.csv")