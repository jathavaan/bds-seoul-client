from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScraperDto:
    game_id: int
    max_reviews_count: int
    last_scraped_date: datetime | None
    correlation_id: str
