import pandas as pd

df = pd.read_csv(r"data\times_articles_with_sentiment.csv")

print("Category counts:")
print(df["category"].value_counts(dropna=False))

print("\nCheck 'Sports Arena' articles:")
mask = df["title"].str.contains("Sports Arena", case=False, na=False)
print(df.loc[mask, ["title", "category"]])
