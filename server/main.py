import time

from src.application import Container
from src.application.common import Request
from src.application.features.query.get_recommendations import GetRecommendationsQueryHandler, GetRecommendationsQuery


from fastapi import FastAPI


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


def main() -> None:
    # Choose Steam game review page
    # steam_game_id = 730       # CS
    # steam_game_id = 413150    # Stardew Valley
    # steam_game_id = 2007520     # Rainbow High Runway Rush
    # steam_game_id = 2669320   # EA FC
    # steam_game_id = 599140  # Graveyard keeper

    # try:
    #     request: Request[GetRecommendationsQuery] = Request(
    #         GetRecommendationsQuery(steam_game_id=steam_game_id))
    #     response = get_recommendations_query_handler.handle(request)
    # except Exception as e:
    #     print("Stopping the program...")
    #     raise e
    # finally:
    #     scraper_service.quit_driver()
    #     print("Program terminated.")
    pass


if __name__ == "__main__":
    # main()
    pass

app = FastAPI()


@app.get("/recommendations")
def get_recommendations(steam_game_id: int):
    response = get_recommendations_query_handler.handle(
        Request(GetRecommendationsQuery(steam_game_id=steam_game_id))
    )
    return response.to_dict()
