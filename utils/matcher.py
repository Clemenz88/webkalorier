from utils.synonyms import SYNONYMS
from rapidfuzz import process

def oversæt_fuzzy(navn, kandidater):
    navn = SYNONYMS.get(navn.lower(), navn.lower())
    result = process.extractOne(navn, kandidater, score_cutoff=70)

    if result is None:
        return None
    else:
        match, score = result[0], result[1]
        return match
