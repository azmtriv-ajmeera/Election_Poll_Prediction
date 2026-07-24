import pandas as pd
import torch
from transformers import pipeline
from tqdm import tqdm

##loading cleaned twitter dataset
twitter2019 = pd.read_csv(
    "data/processed/twitter/Twitter_2019_Cleaned.csv"
)

twitter2024 = pd.read_csv(
    "data/processed/twitter/Twitter_2024_Cleaned.csv"
)



##loading the model
sentiment_model = pipeline(
    task="sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


##lets test on one tweet
tweet = "BJP is doing a good job."

prediction = sentiment_model(tweet)[0]

print(prediction)
##extract label
print(prediction['label'])
print(prediction['score'])



## Process all tweets using batches for 2019 twitter dataset

labels = []
scores = []

# Convert the Clean_Text column into a list
tweets = twitter2019["Clean_Text"].fillna("").tolist()

BATCH_SIZE = 32

for i in tqdm(
        range(0, len(tweets), BATCH_SIZE),
        desc="Processing Tweets"):

    # Select one batch
    batch = tweets[i:i + BATCH_SIZE]

    # Predict sentiment for the whole batch
    predictions = sentiment_model(
        batch,
        batch_size=BATCH_SIZE,
        truncation=True
    )

    # Store results
    for prediction in predictions:

        labels.append(prediction["label"])
        scores.append(prediction["score"])


twitter2019["Sentiment"] = labels
twitter2019["Confidence"] = scores

##saving 2019 twitter sentiment analysis file
twitter2019.to_csv(
    "data/processed/twitter/Twitter_2019_Sentiment.csv",
    index=False
)

print("2019 Sentiment Analysis Completed!")

