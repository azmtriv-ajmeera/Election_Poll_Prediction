import pandas as pd
import torch
from transformers import pipeline
from tqdm import tqdm


##loading the dataset
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


## Process all 2024 tweets

labels = []
scores = []

tweets = twitter2024["Clean_Text"].fillna("").tolist()

BATCH_SIZE = 32

for i in tqdm(
        range(0, len(tweets), BATCH_SIZE),
        desc="Processing 2024 Tweets"):

    # Select one batch
    batch = tweets[i:i+BATCH_SIZE]

    # Predict sentiment for the whole batch
    predictions = sentiment_model(
        batch,
        batch_size=BATCH_SIZE,
        truncation=True,
        max_length=512
    )

    # Store results
    for prediction in predictions:

        labels.append(prediction["label"])
        scores.append(prediction["score"])

twitter2024["Sentiment"] = labels
twitter2024["Confidence"] = scores

twitter2024.to_csv(
    "data/processed/twitter/Twitter_2024_Sentiment.csv",
    index=False
)

print("2024 Sentiment Analysis Completed!")     