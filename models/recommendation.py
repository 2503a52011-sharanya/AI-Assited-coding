from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class RecommendationScore:
    destination_id: int
    destination_name: str
    state: str
    total_score: float
    interest_match_score: float
    budget_fit_score: float
    traveler_fit_score: float
    reasons: List[str] = field(default_factory=list)
    image_url: str = ""
    tags: str = ""
    avg_daily_budget: float = 3500.0
    ideal_duration_days: int = 3
