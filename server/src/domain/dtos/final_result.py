from dataclasses import dataclass

from src.domain.enums import TimeInterval


@dataclass
class RecommendationDto:
    time_interval: TimeInterval
    sum_recommended: int
    sum_not_recommended: int

    def __post_init__(self):
        if isinstance(self.time_interval, int):
            self.time_interval = TimeInterval(self.time_interval)

        if isinstance(self.sum_recommended, float):
            self.sum_recommended = int(self.sum_recommended)

        if isinstance(self.sum_not_recommended, float):
            self.sum_not_recommended = int(self.sum_not_recommended)

    def to_dict(self) -> dict[str, str | int]:
        return {
            "time_interval": TimeInterval.humanize(self.time_interval),
            "sum_recommended": self.sum_recommended,
            "sum_not_recommended": self.sum_not_recommended
        }


@dataclass
class FinalResultDto:
    game_id: int
    correlation_id: str
    recommendations: list[RecommendationDto]

    def __init__(
            self,
            game_id: int,
            correlation_id: str,
            recommendations: list[RecommendationDto] | list[dict[str, int]]
    ):
        self.game_id = game_id
        self.correlation_id = correlation_id

        if isinstance(recommendations, list) and all(isinstance(x, dict) for x in recommendations):
            self.recommendations = [RecommendationDto(**recommendation) for recommendation in recommendations]
        else:
            self.recommendations = recommendations
