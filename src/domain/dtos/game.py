from dataclasses import dataclass
from datetime import datetime


@dataclass
class LastScrapedDateRequestDto:
    game_id: int

    def to_dict(self) -> dict[str, int]:
        return {"game_id": self.game_id}


@dataclass
class LastScrapedDateResponseDto:
    steam_game_id: int
    last_scraped_date: datetime | None
