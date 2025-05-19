import json
import os
from sentence_transformers import SentenceTransformer, util

# Load SentenceTransformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load rule-based aspect keywords
with open("rules/aspect_keywords.json", "r") as f:
    ASPECT_KEYWORDS = json.load(f)

# Get full aspect list
ASPECTS = list(ASPECT_KEYWORDS.keys())

# Precompute aspect embeddings
ASPECT_EMBEDDINGS = model.encode(ASPECTS, convert_to_tensor=True)

def identify_aspect(clause: str, threshold: float = 0.5) -> dict:
    """
    Identifies discussed aspect using rule-based keywords first,
    falls back to cosine similarity if no match is found.
    Returns best matching aspect and score.
    """
    clause_lower = clause.lower()

    # 1️⃣ Rule-based check
    for aspect, keywords in ASPECT_KEYWORDS.items():
        for kw in keywords:
            if kw in clause_lower:
                return {"aspect": aspect, "method": "rule", "score": 1.0}

    # 2️⃣ Embedding similarity fallback
    clause_embedding = model.encode(clause, convert_to_tensor=True)
    cosine_scores = util.cos_sim(clause_embedding, ASPECT_EMBEDDINGS)[0]
    top_score = float(cosine_scores.max())
    top_index = int(cosine_scores.argmax())

    if top_score >= threshold:
        return {
            "aspect": ASPECTS[top_index],
            "method": "embedding",
            "score": round(top_score, 3)
        }
    else:
        return {
            "aspect": None,
            "method": "none",
            "score": round(top_score, 3)
        }

if __name__ == "__main__":
    clauses = [
        "The battery drains too fast.",
        "App login fails frequently.",
        "The app is slow and keeps freezing.",
        "Can you add multi-language support?",
        "Layout feels cramped on small screens.",
        "Great app, but I wish notifications were customizable.",
    ]

    for clause in clauses:
        result = identify_aspect(clause)
        print(f"Clause: {clause}")
        print(f"→ Aspect: {result['aspect']} (method: {result['method']}, score: {result['score']})\n")
