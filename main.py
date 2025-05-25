import time

from src.application import Container
from src.application.common import Request
from src.application.features.query.get_recommendations import GetRecommendationsQueryHandler, GetRecommendationsQuery

container = Container()

logger = container.logger()
last_scraped_date_producer = container.last_scraped_date_producer()
last_scraped_date_consumer = container.last_scraped_date_consumer()
review_producer = container.review_producer()
get_recommendations_query_handler = GetRecommendationsQueryHandler(
    logger=logger,
    last_scraped_date_consumer=last_scraped_date_consumer,
    last_scraped_date_producer=last_scraped_date_producer,
    review_producer=review_producer
)


def main() -> None:
    try:
        steam_game_id = 100_000
        while True:
            request: Request[GetRecommendationsQuery] = Request(GetRecommendationsQuery(steam_game_id=steam_game_id))
            get_recommendations_query_handler.handle(request)
            steam_game_id += 1
            time.sleep(40)
    except Exception as e:
        print("Stopping the program...")
        raise e
    finally:
        print("Program terminated.")


if __name__ == "__main__":
    main()
