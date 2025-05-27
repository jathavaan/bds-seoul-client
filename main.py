import time

from src.application import Container
from src.application.common import Request
from src.application.features.query.get_recommendations import GetRecommendationsQueryHandler, GetRecommendationsQuery

container = Container()

logger = container.logger()
last_scraped_date_producer = container.last_scraped_date_producer()
last_scraped_date_consumer = container.last_scraped_date_consumer()
review_producer = container.review_producer()
final_result_consumer = container.final_result_consumer()

get_recommendations_query_handler = GetRecommendationsQueryHandler(
    logger=logger,
    last_scraped_date_consumer=last_scraped_date_consumer,
    last_scraped_date_producer=last_scraped_date_producer,
    review_producer=review_producer,
    final_result_consumer=final_result_consumer
)
scraper_service = container.scraper_service()


def main() -> None:
    # Choose Steam game review page
    # game_id = 730      #CS
    # game_id = 413150   #Stardew Valley
    # game_id = 2007520  #Rainbow High Runway Rush

    scraper_service.scrape(730)
    scraper_service.scrape(413150)
    scraper_service.quit_driver()
    return
    try:
        steam_game_id = 100_000
        while True:
            request: Request[GetRecommendationsQuery] = Request(
                GetRecommendationsQuery(steam_game_id=steam_game_id))
            response = get_recommendations_query_handler.handle(request)

            steam_game_id += 1
            time.sleep(80)
    except Exception as e:
        print("Stopping the program...")
        raise e
    finally:
        print("Program terminated.")


if __name__ == "__main__":
    main()
