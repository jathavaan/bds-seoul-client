from dataclasses import dataclass


@dataclass
class RecommendationVm:
    group: str
    sum_recommended: int
    sum_not_recommended: int


