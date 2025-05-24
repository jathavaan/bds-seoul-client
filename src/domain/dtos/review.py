from dataclasses import dataclass, field


@dataclass
class ReviewDto:
    game_id: int = field(metadata={"description": "Steam game ID"})
    date_posted: str
    is_recommended: bool
    hours_played: float
    user_id: int
    is_last_review: bool
    correlation_id: str

    def to_dict(self) -> dict[str, str | int | bool]:
        return {
            "game_id": self.game_id,
            "date_posted": self.date_posted,
            "is_recommended": self.is_recommended,
            "hours_played": self.hours_played,
            "user_id": self.user_id,
            "is_last_review": self.is_last_review,
            "correlation_id": self.correlation_id
        }
