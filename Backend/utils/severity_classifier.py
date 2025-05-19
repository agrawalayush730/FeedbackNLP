import json

# Load severity keywords from JSON file
with open("C:/Projects/FeedbackNLP/Backend/rules/severity_keywords.json", "r") as f:
    SEVERITY_KEYWORDS = json.load(f)


def classify_severity(clause: str) -> str:
    """
    Classifies the severity of a clause with negative sentiment.
    Returns 'high', 'medium', 'low', or None if no match is found.
    """
    text = clause.lower()

    for severity, keywords in SEVERITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return severity

    return None  # fallback if nothing matched


if __name__ == "__main__":
    negative_clauses = [
        "The app crashes every time I open the camera.",
        "It’s a bit slow while switching between tabs.",
        "The layout feels inconsistent and confusing.",
        "Completely unusable after last update!",
        "It lags a little on startup.",
        "The login screen looks cluttered."
    ]

    for clause in negative_clauses:
        severity = classify_severity(clause)
        print(f"Clause: {clause}")
        print(f"→ Severity: {severity}\n")
