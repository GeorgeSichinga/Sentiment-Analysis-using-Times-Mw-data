import pandas as pd
import streamlit as st
from pathlib import Path
import altair as alt



DATA_PATH = Path("data") / "times_articles_with_sentiment.csv"


def load_data():
    if not DATA_PATH.exists():
        st.error(f"Data file not found: {DATA_PATH}. Run analyze_sentiment.py first.")
        return None
    return pd.read_csv(DATA_PATH)


def main():
    st.set_page_config(
        page_title="Malawi News Sentiment Dashboard",
        layout="wide",
    )
 # Header with copyright
    st.markdown(
        "<hr><p style='text-align:center; color:#777;'>© George Sichinga</p>",
        unsafe_allow_html=True,
    )
    # Simple color styling
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .stSidebar {
            background-color: #0b3d91;
        }
        .stSidebar > div {
            color: white;
        }
        h1, h2, h3 {
            color: #0b3d91;
        }
        .sentiment-positive {
            color: #2e7d32;
            font-weight: bold;
        }
        .sentiment-neutral {
            color: #616161;
            font-weight: bold;
        }
        .sentiment-negative {
            color: #c62828;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Malawi News Sentiment Dashboard (Times)")

    df = load_data()
    if df is None:
        return

    st.sidebar.header("Filters")

    sources = ["All"] + sorted(df["source"].dropna().unique().tolist())
    selected_source = st.sidebar.selectbox("Source", sources)

    categories = ["All"] + sorted(
        [c for c in df["category"].dropna().unique().tolist()]
    )
    selected_category = st.sidebar.selectbox("Category", categories)

    sentiments = ["All", "positive", "neutral", "negative"]
    selected_sentiment = st.sidebar.selectbox("Sentiment", sentiments)

    filtered = df.copy()
    if selected_source != "All":
        filtered = filtered[filtered["source"] == selected_source]
    if selected_category != "All":
        filtered = filtered[filtered["category"] == selected_category]
    if selected_sentiment != "All":
        filtered = filtered[filtered["sentiment_label"] == selected_sentiment]

    st.subheader("Summary")
    st.write(f"Total articles: {len(df)}")
    st.write(f"Filtered articles: {len(filtered)}")

    if not filtered.empty:
        avg_pol = filtered["sentiment_polarity"].mean()
        avg_subj = filtered["sentiment_subjectivity"].mean()
        st.write(f"Average polarity (filtered): {avg_pol:.3f}")
        st.write(f"Average subjectivity (filtered): {avg_subj:.3f}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Sentiment counts")
        if not filtered.empty:
            counts = (
                filtered["sentiment_label"]
                .value_counts()
                .reindex(["positive", "neutral", "negative"])
                .fillna(0)
            )

            counts_df = counts.reset_index()
            counts_df.columns = ["sentiment", "count"]

            color_scale = alt.Scale(
                domain=["positive", "neutral", "negative"],
                range=["#1976d2", "#000000", "#c62828"],  # blue, black, red
            )

            chart = (
                alt.Chart(counts_df)
                .mark_bar()
                .encode(
                    x=alt.X("sentiment:N", title="Sentiment"),
                    y=alt.Y("count:Q", title="Number of articles"),
                    color=alt.Color("sentiment:N", scale=color_scale, legend=None),
                )
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No articles for current filters.")

    with col2:
        st.subheader("Avg polarity by category")
        if not filtered.empty and "category" in filtered.columns:
            avg_pol_by_cat = filtered.groupby("category")[
                "sentiment_polarity"
            ].mean()
            st.bar_chart(avg_pol_by_cat)
        else:
            st.write("No category data.")

    with col3:
        st.subheader("Avg subjectivity by category")
        if not filtered.empty and "sentiment_subjectivity" in filtered.columns:
            avg_subj_by_cat = filtered.groupby("category")[
                "sentiment_subjectivity"
            ].mean()
            st.bar_chart(avg_subj_by_cat)
        else:
            st.write("No subjectivity data.")

        st.subheader("Articles")
    if filtered.empty:
        st.write("No articles match your filters.")
    else:
        for _, row in filtered.iterrows():
            st.markdown(f"### {row['title']}")

            sentiment_label = row["sentiment_label"]
            if sentiment_label == "positive":
                sentiment_class = "sentiment-positive"
            elif sentiment_label == "negative":
                sentiment_class = "sentiment-negative"
            else:
                sentiment_class = "sentiment-neutral"

            meta = (
                f"Source: {row['source']} | "
                f"Category: {row['category']} | "
                f"Sentiment: "
                f"<span class='{sentiment_class}'>{row['sentiment_label']}</span> "
                f"(polarity={row['sentiment_polarity']:.2f}, "
                f"subjectivity={row['sentiment_subjectivity']:.2f})"
            )
            st.markdown(meta, unsafe_allow_html=True)

            st.write(row["text"])
            st.markdown(f"[Open article]({row['url']})")
            st.markdown("---")

    # Footer
    st.markdown(
        "<hr><p style='text-align:center; color:#777;'>© George Sichinga</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
