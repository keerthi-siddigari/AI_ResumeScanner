from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0

    tfidf = TfidfVectorizer(ngram_range=(1, 2))
    matrix = tfidf.fit_transform([text1, text2])

    return cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
