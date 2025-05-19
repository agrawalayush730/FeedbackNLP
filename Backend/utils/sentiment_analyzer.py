from transformers import pipeline

# Load pipeline once
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

# Manual mapping of model labels
LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment prediction as a dictionary with readable label and confidence score.
    """
    result = sentiment_pipeline(text)[0]
    readable_label = LABEL_MAP.get(result["label"], result["label"])
    return {
        "label": readable_label,
        "score": round(result["score"], 3)
    }



if __name__ == "__main__":
    clauses = [
        "The app crashes frequently.",
        "I love the design and layout!",
        "Notifications are okay, nothing special."
    ]

    for clause in clauses:
        result = analyze_sentiment(clause)
        print(f"Clause: {clause}")
        print(f"→ Sentiment: {result['label']} (score: {result['score']})")
        print()