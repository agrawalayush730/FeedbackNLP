import uuid
from datetime import datetime

from utils.clause_splitter import split_into_clauses
from utils.sentiment_analyzer import analyze_sentiment
from utils.category_classifier import classify_category
from utils.aspect_identifier import identify_aspect
from utils.severity_classifier import classify_severity

def format_feedback_json(feedback_text: str, user_id: str = None) -> dict:
    """
    Process raw feedback into structured JSON output.
    """
    clauses = split_into_clauses(feedback_text)
    
    categories = set()
    positive_aspects = []
    improvement_areas = []

    for clause in clauses:
        sentiment_result = analyze_sentiment(clause)
        sentiment = sentiment_result["label"]
        sentiment_score = sentiment_result["score"]

        category_result = classify_category(clause)
        category = category_result["label"]

        aspect_result = identify_aspect(clause)
        aspect = aspect_result["aspect"]

        # Add category if valid
        if category:
            categories.add(category)

        # Handle clause based on sentiment
        if sentiment == "positive" and aspect:
            positive_aspects.append(aspect)

        elif sentiment == "negative" and aspect:
            severity = classify_severity(clause)
            improvement_areas.append({
                "aspect": aspect,
                "sentiment": sentiment,
                "severity": severity
            })

    return {
        "feedback_id": str(uuid.uuid4()),
        "feedback_text": feedback_text,
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id if user_id else "anonymous",
        "category": list(set(categories)),              
        "positive_aspects": list(set(positive_aspects)),
        "improvement_areas": improvement_areas          
    }

if __name__ == "__main__":
    feedback = "the ui is good but loging page crashes sometimes."
    result = format_feedback_json(feedback, user_id="user_001")

    import json
    print(json.dumps(result, indent=2))