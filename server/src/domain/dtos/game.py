from dataclasses import dataclass
from datetime import datetime

from src.domain.dtos import FinalResultDto


@dataclass
class LastScrapedDateRequestDto:
    game_id: int
    correlation_id: str

    def to_dict(self) -> dict[str, int]:
        return {"game_id": self.game_id, "correlation_id": self.correlation_id}


@dataclass
class LastScrapedDateResponseDto:
    steam_game_id: int
    last_scraped_date: datetime | None
    result: FinalResultDto | None
    correlation_id: str

    def __post_init__(self):
        if isinstance(self.result, dict):
            self.result = FinalResultDto(**self.result)
