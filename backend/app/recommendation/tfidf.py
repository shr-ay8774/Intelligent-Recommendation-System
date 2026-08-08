from sklearn.feature_extraction.text import TfidfVectorizer


def create_tfidf_matrix(courses_df):

    courses_df = courses_df.copy()

    courses_df["text"] = (
        courses_df["title"].fillna("")
        + " "
        + courses_df["description"].fillna("")
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        courses_df["text"]
    )

    return vectorizer, tfidf_matrix