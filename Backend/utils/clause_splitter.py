import re
from nltk.tokenize import sent_tokenize

# Expanded conjunctions and discourse markers
CONJUNCTIONS = [
    "but", "and", "or", "so", "yet", "although", "though", "because", "however", "while", "whereas", "unless",
    "since", "if", "when", "after", "before", "except", "even though", "as", "besides", "despite", "in case", "still"
]

# Enumeration markers
ENUM_MARKERS = [
    r"\b\d+\.", r"\bfirst\b", r"\bsecond\b", r"\bthird\b", r"\bfourth\b", r"\bfifth\b"
]

def split_into_clauses(text: str) -> list:
    """
    Advanced clause splitter: handles conjunctions, punctuation, enumerations, and informal feedback.
    Cleans up enumeration markers and standalone conjunctions for production use.
    """
    import re
    from nltk.tokenize import sent_tokenize

    # First, split into sentences
    sentences = sent_tokenize(text)
    clauses = []

    # Build regex for conjunctions/discourse markers (with optional punctuation/space)
    conj_pattern = r"(\s*[,;:.!?]*\s*\b(?:{})\b\s*)".format("|".join(CONJUNCTIONS))
    # Build regex for enumerations (e.g., "1.", "first", etc.)
    enum_pattern = r"({})".format("|".join(ENUM_MARKERS))

    for sent in sentences:
        # First, split on enumerations
        enum_parts = re.split(enum_pattern, sent, flags=re.IGNORECASE)
        for enum_part in enum_parts:
            if not enum_part or not enum_part.strip():
                continue
            # Now split on conjunctions/discourse markers
            parts = re.split(conj_pattern, enum_part, flags=re.IGNORECASE)
            clause = ""
            for part in parts:
                if re.fullmatch(conj_pattern, part, flags=re.IGNORECASE):
                    if clause.strip():
                        clauses.append(clause.strip(" ,;:.!?"))
                    clause = part.lstrip()
                else:
                    clause += part
            if clause.strip():
                clauses.append(clause.strip(" ,;:.!?"))

    # --- Post-processing: remove enumeration markers and standalone conjunctions ---
    def is_enumeration_marker(clause):
        return re.fullmatch(r"(\d+\.|first|second|third|fourth|fifth)", clause.strip(), re.IGNORECASE)

    def is_short_conjunction(clause):
        return clause.strip().lower() in set(CONJUNCTIONS + ["also", "though", "so", "and", "but", "or", "yet"])

    cleaned = []
    buffer = ""
    for clause in clauses:
        if is_enumeration_marker(clause) or is_short_conjunction(clause):
            if cleaned:
                cleaned[-1] += " " + clause.strip()
            else:
                buffer += clause.strip() + " "
        elif len(clause.strip()) < 4:
            continue
        else:
            cleaned.append((buffer + clause).strip())
            buffer = ""
    return [c for c in cleaned if c]

if __name__ == "__main__":
    text = (
        "It's a great game but sometimes it lags. 1. The camera gets stuck. 2. The controls freeze. "
        "Also, even though my wifi is strong, it keeps disconnecting... and sometimes crashes! "
        "First, the UI is nice; second, the updates are too frequent."
        "very nice its very good to play i love this app so much! but the thing is that it keeps disconnecting even though my wifi is strong but i hope you can fix it! and.. im on a chromebook others says it crashes when you play on chromebook but mine is just fine no lagging accept disconnecting you will find it on 1 stars they said its crashes even mine is just very great! thats also weird though but thats for all"
    )
    result = split_into_clauses(text)
    for i, clause in enumerate(result):
        print(f"Clause {i+1}: {clause}")