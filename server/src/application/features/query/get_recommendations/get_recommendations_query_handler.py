import logging
import time
from abc import ABC

from src.application.base import RequestHandlerBase
from src.application.common import Request, Response
from src.application.kafka.consumers import LastScrapedDateConsumer, FinalResultConsumer
from src.application.kafka.producers import LastScrapedDateProducer
from src.application.services.scraper_service.scraper_service import ScraperService
from src.application.view_models import RecommendationVm
from src.domain.dtos import LastScrapedDateRequestDto, LastScrapedDateResponseDto, FinalResultDto
from .get_recommendations_query import GetRecommendationsQuery


class GetRecommendationsQueryHandler(RequestHandlerBase[GetRecommendationsQuery, list[RecommendationVm]], ABC):
    __logger: logging.Logger
    __last_scraped_date_consumer: LastScrapedDateConsumer
    __last_scraped_date_producer: LastScrapedDateProducer
    __final_result_consumer: FinalResultConsumer
    __scraper_service: ScraperService

    def __init__(
            self,
            logger: logging.Logger,
            last_scraped_date_consumer: LastScrapedDateConsumer,
            last_scraped_date_producer: LastScrapedDateProducer,
            final_result_consumer: FinalResultConsumer,
            scraper_service: ScraperService
    ):
        self.__logger = logger
        self.__last_scraped_date_consumer = last_scraped_date_consumer
        self.__last_scraped_date_producer = last_scraped_date_producer
        self.__final_result_consumer = final_result_consumer
        self.__scraper_service = scraper_service

    def handle(self, request: Request[GetRecommendationsQuery]) -> Response[list[RecommendationVm]]:
        start_time = time.time()

        self.__last_scraped_date_producer.produce(LastScrapedDateRequestDto(
            game_id=request.payload.steam_game_id,
            correlation_id=request.correlation_id
        ))

        response: LastScrapedDateResponseDto | None
        while True:
            has_responded, response = self.__last_scraped_date_consumer.consume()
            if has_responded and response.correlation_id == request.correlation_id:
                break

        if response.result and request.correlation_id == response.correlation_id:
            self.__logger.info(f"Result for {request.payload.steam_game_id} was cached.")

            end_time = time.time()
            elapsed_time = end_time - start_time
            self.__logger.info(
                f"Request {request.correlation_id} responded in {round(elapsed_time, 2)} second(s)"
            )

            return Response([
                RecommendationVm(**recommendation.to_dict()) for recommendation in response.result.recommendations
            ])

        last_scraped_date = response.last_scraped_date
        self.__scraper_service.scrape(
            request.payload.steam_game_id, request.correlation_id
        )

        while True:
            final_result = self.__final_result_consumer.consume()
            if final_result is not None and final_result.correlation_id == request.correlation_id:
                self.__logger.info(
                    f"Received response for Steam game ID {final_result.game_id} for correlation ID {final_result.correlation_id}"
                )
                break

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.__logger.info(
            f"Request {request.correlation_id} responded in {round(elapsed_time, 2)} second(s)")

        return Response([
            RecommendationVm(**recommendation.to_dict()) for recommendation in final_result.recommendations
        ])
