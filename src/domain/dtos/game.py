from dataclasses import dataclass
from datetime import datetime


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
