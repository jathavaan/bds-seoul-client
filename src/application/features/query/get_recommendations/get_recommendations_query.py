from dataclasses import dataclass


@dataclass
class GetRecommendationsQuery:
    steam_game_id: int
