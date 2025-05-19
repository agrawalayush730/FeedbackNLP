from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import json
# ----------------------------
# Category Labels + Descriptions
# ----------------------------
with open("C:/Projects/FeedbackNLP/Backend/rules/category_label_map.json", "r") as f:
    CATEGORY_LABEL_MAP = json.load(f)


CATEGORY_LABELS = list(CATEGORY_LABEL_MAP.keys())             # for zero-shot
CATEGORY_DESCRIPTIONS = list(CATEGORY_LABEL_MAP.values())     # for cosine fallback

ZERO_SHOT_THRESHOLD = 0.3
COSINE_THRESHOLD = 0.3

# ----------------------------
# Load Models Once
# ----------------------------

zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
embedder = SentenceTransformer("all-MiniLM-L6-v2")
CATEGORY_EMBEDDINGS = embedder.encode(CATEGORY_DESCRIPTIONS, convert_to_tensor=True)

# ----------------------------
# Main Function
# ----------------------------

def classify_category(text: str) -> dict:
    """
    Uses zero-shot classification to assign a feedback category.
    Falls back to cosine similarity with sentence embeddings if no confident match.
    """
    try:
        # --- Zero-Shot ---
        result = zero_shot_classifier(text, CATEGORY_LABELS)
        top_label = result["labels"][0]
        top_score = result["scores"][0]

        if top_score >= ZERO_SHOT_THRESHOLD:
            return {
                "label": top_label,
                "score": round(top_score, 3),
                "method": "zero-shot"
            }

        # --- Cosine Fallback ---
        text_embedding = embedder.encode(text, convert_to_tensor=True)
        cosine_scores = util.cos_sim(text_embedding, CATEGORY_EMBEDDINGS)[0]
        best_score = float(cosine_scores.max())
        best_index = int(cosine_scores.argmax())

        if best_score >= COSINE_THRESHOLD:
            return {
                "label": CATEGORY_LABELS[best_index],
                "score": round(best_score, 3),
                "method": "cosine"
            }

        # No match
        return {
            "label": None,
            "score": round(best_score, 3),
            "method": "none"
        }

    except Exception as e:
        print(f"[ERROR] classify_category failed: {e}")
        return {
            "label": None,
            "score": 0.0,
            "method": "error"
        }

# ----------------------------
# Test Block
# ----------------------------

if __name__ == "__main__":
    test_clauses = [
        "The app crashes when I open the settings.",
        "It takes forever to load the dashboard.",
        "Can you add support for fingerprint login?",
        "The buttons are too close together on mobile.",
        "I love the smooth animations and design!",
        "I wish the app had face ID unlock.",
        "The battery drains quickly."
    ]

    for clause in test_clauses:
        result = classify_category(clause)
        print(f"Clause: {clause}")
        print(f"→ Category: {result['label']} (method: {result['method']}, score: {result['score']})\n")
