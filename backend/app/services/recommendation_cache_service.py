import json

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.recommendation_cache import RecommendationCache


CACHE_DURATION_MINUTES = 30


def get_cached_recommendations(
    db: Session,
    user_id: int
):
    cache = (
        db.query(RecommendationCache)
        .filter(
            RecommendationCache.user_id == user_id
        )
        .first()
    )

    if cache is None:
        return None

    if (
        datetime.utcnow() - cache.created_at
        > timedelta(minutes=CACHE_DURATION_MINUTES)
    ):
        db.delete(cache)
        db.commit()

        return None

    return json.loads(cache.recommendations)


def save_recommendations_to_cache(
    db: Session,
    user_id: int,
    recommendations: list
):
    cache = (
        db.query(RecommendationCache)
        .filter(
            RecommendationCache.user_id == user_id
        )
        .first()
    )

    recommendations_json = json.dumps(
        recommendations
    )

    if cache:

        cache.recommendations = recommendations_json
        cache.created_at = datetime.utcnow()

    else:

        cache = RecommendationCache(
            user_id=user_id,
            recommendations=recommendations_json,
            created_at=datetime.utcnow()
        )

        db.add(cache)

    db.commit()

    return recommendations