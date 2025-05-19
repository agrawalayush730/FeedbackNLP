from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime
import certifi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Connection
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client["feedback_analyzer"]
    feedback_collection = db["analyzed_feedback"]
except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    raise RuntimeError("Failed to connect to MongoDB")

def get_dashboard_data():
    category_counts = defaultdict(int)
    sentiment_counts = defaultdict(int)
    severity_counts = defaultdict(int)
    aspect_counts = defaultdict(int)
    feedback_over_time = defaultdict(int)
    positive_aspect_counts = defaultdict(int)
    category_sentiment_counts = defaultdict(lambda: {"positive": 0, "negative": 0})

    try:
        all_docs = list(feedback_collection.find({}))
    except Exception as e:
        print("❌ Error fetching data from MongoDB:", e)
        return {
            "category_counts": {},
            "sentiment_distribution": {},
            "severity_levels": {},
            "top_aspects": {},
            "feedback_over_time": {},
            "category_sentiment_counts": {}
        }

    if not all_docs:
        return {
            "category_counts": {},
            "sentiment_distribution": {},
            "severity_levels": {},
            "top_aspects": {},
            "feedback_over_time": {},
            "category_sentiment_counts": {}
        }

    for doc in all_docs:
        # ✅ Categories (and sentiment per category)
        categories = doc.get("category", [])
        for cat in categories:
            if isinstance(cat, str):
                cat_clean = cat.strip()
                category_counts[cat_clean] += 1

        # ✅ Improvement areas
        for imp in doc.get("improvement_areas", []):
            if isinstance(imp, dict):
                sentiment = (imp.get("sentiment") or "unknown").lower()
                severity = (imp.get("severity") or "unknown").lower()
                aspect = (imp.get("aspect") or "").strip().lower()

                sentiment_counts[sentiment] += 1
                severity_counts[severity] += 1
                if aspect:
                    aspect_counts[aspect] += 1

                # Add to category_sentiment_counts
                for cat in categories:
                    if isinstance(cat, str):
                        category_sentiment_counts[cat.strip()][sentiment] += 1

        # ✅ Positive aspects
        for pos in doc.get("positive_aspects", []):
            if isinstance(pos, dict):
                sentiment = (pos.get("sentiment") or "positive").lower()
                aspect = (pos.get("aspect") or "").strip().lower()
                sentiment_counts[sentiment] += 1
                if aspect:
                    aspect_counts[aspect] += 1
                    if sentiment == "positive":
                        positive_aspect_counts[aspect] += 1
                for cat in categories:
                    if isinstance(cat, str):
                        category_sentiment_counts[cat.strip()][sentiment] += 1
            elif isinstance(pos, str):
                aspect = pos.strip().lower()
                if aspect:
                    aspect_counts[aspect] += 1
                    positive_aspect_counts[aspect] += 1

        # ✅ Timestamp
        ts = doc.get("timestamp")
        if isinstance(ts, datetime):
            date_str = ts.strftime("%Y-%m-%d")
        else:
            date_str = "unknown"
        feedback_over_time[date_str] += 1

    return {
        "category_counts": dict(category_counts),
        "sentiment_distribution": dict(sentiment_counts),
        "severity_levels": dict(severity_counts),
        "top_aspects": dict(aspect_counts),
        "positive_aspects": dict(positive_aspect_counts),
        "feedback_over_time": dict(feedback_over_time),
        "category_sentiment_counts": dict(category_sentiment_counts)
    }
