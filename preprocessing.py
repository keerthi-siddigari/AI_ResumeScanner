import spacy
import pdfplumber

nlp = spacy.load("en_core_web_sm")

def read_pdf(path):
    with pdfplumber.open(path) as pdf:
        return " ".join(page.extract_text() or "" for page in pdf.pages)

def preprocess(text):
    doc = nlp(text.lower())
    tokens = []

    for token in doc:
        # DO NOT remove stopwords
        if token.text in {".", "+", "#"}:
            continue
        tokens.append(token.text)

    return " ".join(tokens)

