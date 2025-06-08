from utils.synonyms import SYNONYMS
from rapidfuzz import process

def oversæt_fuzzy(navn, kandidater):
    navn = SYNONYMS.get(navn.lower(), navn.lower())
    match, score, _ = process.extractOne(navn, kandidater, score_cutoff=70)
    return match if match else None
