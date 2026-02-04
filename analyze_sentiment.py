import pandas as pd
from textblob import TextBlob
from pathlib import Path


def analyze_sentiment(input_path: str, output_path: str):
    df = pd.read_csv(input_path)

    if "text" not in df.columns:
        raise ValueError("CSV must have a 'text' column with article content")

    polarities = []
    subjectivities = []
    labels = []

    for text in df["text"]:
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity      # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1

        if polarity > 0.1:
            label = "positive"
        elif polarity < -0.1:
            label = "negative"
        else:
            label = "neutral"

        polarities.append(polarity)
        subjectivities.append(subjectivity)
        labels.append(label)

    df["sentiment_polarity"] = polarities
    df["sentiment_subjectivity"] = subjectivities
    df["sentiment_label"] = labels

    Path(Path(output_path).parent).mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved sentiment-annotated data to {output_path}")


if __name__ == "__main__":
    input_csv = r"data\times_articles.csv"
    output_csv = r"data\times_articles_with_sentiment.csv"
    analyze_sentiment(input_csv, output_csv)
