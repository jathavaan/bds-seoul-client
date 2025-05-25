from dataclasses import dataclass


@dataclass
class RecommendationVm:
    time_interval: str
    sum_recommended: int
    sum_not_recommended: int

    def to_dict(self) -> dict[str, str | int]:
        return {
            "time_interval": self.time_interval,
            "sum_recommended": self.sum_recommended,
            "sum_not_recommended": self.sum_not_recommended
        }
