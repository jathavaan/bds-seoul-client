from fastapi import APIRouter

from src.application import Container
from src.application.common import Request
from src.application.features.query.get_recommendations import GetRecommendationsQueryHandler, GetRecommendationsQuery

container = Container()

logger = container.logger()
last_scraped_date_producer = container.last_scraped_date_producer()
last_scraped_date_consumer = container.last_scraped_date_consumer()
review_producer = container.review_producer()
final_result_consumer = container.final_result_consumer()
scraper_service = container.scraper_service()

get_recommendations_query_handler = GetRecommendationsQueryHandler(
    logger=logger,
    last_scraped_date_consumer=last_scraped_date_consumer,
    last_scraped_date_producer=last_scraped_date_producer,
    final_result_consumer=final_result_consumer,
    scraper_service=scraper_service
)

recommendations_router = APIRouter()


@recommendations_router.get("/recommendations")
def get_recommendations(steam_game_id: int):
    response = get_recommendations_query_handler.handle(
        Request(GetRecommendationsQuery(steam_game_id=steam_game_id))
    )

    return response.to_dict()
