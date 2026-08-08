from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)