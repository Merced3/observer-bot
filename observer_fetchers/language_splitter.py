# observer_fetchers/language_splitter.py

import spacy

nlp = spacy.load("en_core_web_sm")

def split_text(text):
    text = text.lower() 
    doc = nlp(text)

    nouns = []
    proper_nouns = []

    for token in doc:
        if token.pos_ == "NOUN":
            nouns.append(token.text)
        elif token.pos_ == "PROPN":
            proper_nouns.append(token.text)

    return {
        "nouns": nouns,
        "proper_nouns": proper_nouns
    }
