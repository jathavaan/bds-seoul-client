from dataclasses import dataclass, field


@dataclass
class ReviewDto:
    game_id: int = field(metadata={"description": "Steam game ID"})
    date_posted: str
    is_recommended: bool
    hours_played: float
    user_id: int
    is_last_review_in_batch: bool
