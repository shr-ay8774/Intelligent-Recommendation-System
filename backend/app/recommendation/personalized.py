from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_personalized_recommendations(
    user,
    courses_df,
    top_n=5
):
    courses_df = courses_df.copy()

    # Create text for every course
    courses_df["text"] = (
        courses_df["title"].fillna("")
        + " "
        + courses_df["description"].fillna("")
    )

    # Create a profile from the user's interests
    user_profile = (
        f"{user.skill_level or ''} "
        f"{user.interests or ''}"
    )

    # Convert course text + user profile into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    course_vectors = vectorizer.fit_transform(
        courses_df["text"]
    )

    user_vector = vectorizer.transform(
        [user_profile]
    )

    # Calculate similarity between user and every course
    scores = cosine_similarity(
        user_vector,
        course_vectors
    ).flatten()

    courses_df["score"] = scores

    # Highest score first
    recommendations = courses_df.sort_values(
        by="score",
        ascending=False
    )

    return recommendations.head(top_n)