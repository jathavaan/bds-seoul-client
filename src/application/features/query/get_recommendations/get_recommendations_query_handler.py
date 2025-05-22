import logging
from abc import ABC

from src.application.base import RequestHandlerBase
from src.application.common import Request, Response
from src.application.kafka.consumers import LastScrapedDateConsumer
from src.application.kafka.producers import LastScrapedDateProducer
from src.application.view_models import RecommendationVm
from src.domain.dtos import LastScrapedDateRequestDto, LastScrapedDateResponseDto
from .get_recommendations_query import GetRecommendationsQuery


class GetRecommendationsQueryHandler(RequestHandlerBase[GetRecommendationsQuery, list[RecommendationVm]], ABC):
    __logger: logging.Logger
    __last_scraped_date_consumer: LastScrapedDateConsumer
    __last_scraped_date_producer: LastScrapedDateProducer

    def __init__(
            self,
            logger: logging.Logger,
            last_scraped_date_consumer: LastScrapedDateConsumer,
            last_scraped_date_producer: LastScrapedDateProducer
    ):
        self.__logger = logger
        self.__last_scraped_date_consumer = last_scraped_date_consumer
        self.__last_scraped_date_producer = last_scraped_date_producer

    def handle(self, request: Request[GetRecommendationsQuery]) -> Response[list[RecommendationVm]]:
        self.__last_scraped_date_producer.produce(LastScrapedDateRequestDto(game_id=request.payload.steam_game_id))
        response: LastScrapedDateResponseDto | None

        while True:
            has_responded, response = self.__last_scraped_date_consumer.consume()
            if has_responded:
                break

        last_scraped_date = response.last_scraped_date
        for i in range(0, 201):
            pass

        return Response([])
