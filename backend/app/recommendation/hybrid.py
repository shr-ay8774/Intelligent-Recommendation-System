import pandas as pd


def calculate_hybrid_scores(
    courses_df: pd.DataFrame,
    content_scores,
    ratings,
    enrollments,
    learning_history
):
    courses_df = courses_df.copy()

    # Start with content-based score
    courses_df["content_score"] = content_scores

    # Create lookup dictionary for ratings
    rating_map = {
        rating.course_id: rating.rating
        for rating in ratings
    }

    # Courses already enrolled by the user
    enrolled_courses = {
        enrollment.course_id
        for enrollment in enrollments
    }

    # Create lookup dictionary for learning progress
    progress_map = {
        history.course_id: history.progress
        for history in learning_history
    }

    # Calculate rating score
    courses_df["rating_score"] = courses_df["id"].apply(
        lambda course_id:
            rating_map.get(course_id, 0) / 5
    )

    # Calculate enrollment score
    courses_df["enrollment_score"] = courses_df["id"].apply(
        lambda course_id:
            1.0 if course_id in enrolled_courses else 0.0
    )

    # Calculate learning progress score
    courses_df["progress_score"] = courses_df["id"].apply(
        lambda course_id:
            progress_map.get(course_id, 0) / 100
    )

    # Calculate hybrid score
    courses_df["hybrid_score"] = (
        courses_df["content_score"] * 0.50
        + courses_df["rating_score"] * 0.20
        + courses_df["enrollment_score"] * 0.10
        + courses_df["progress_score"] * 0.20
    )

    # Exclude courses already enrolled by the user
    courses_df = courses_df[
        courses_df["enrollment_score"] == 0
    ]

    # Sort by highest recommendation score
    return courses_df.sort_values(
        by="hybrid_score",
        ascending=False
    )