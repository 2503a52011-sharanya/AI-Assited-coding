import pytest
from services.recommendation_service import RecommendationService
from config.database import init_db


def test_recommendation_scoring():
    init_db()
    recs = RecommendationService.get_personalized_recommendations(
        origin="Hyderabad",
        target_budget=20000.0,
        days=3,
        traveler_type="Couple",
        interests=["Nature", "Photography"],
        limit=5
    )

    assert len(recs) > 0
    # Destination names should be valid strings
    assert all(r.destination_name for r in recs)
    # Scores should be in valid range [0, 100]
    assert all(0 <= r.total_score <= 100 for r in recs)
    # Sorted descending
    scores = [r.total_score for r in recs]
    assert scores == sorted(scores, reverse=True)
