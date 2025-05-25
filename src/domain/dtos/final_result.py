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


@dataclass
class FinalResultDto:
    game_id: int
    correlation_id: str
    recommendations: list[RecommendationDto]
