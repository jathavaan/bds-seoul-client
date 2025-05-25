import logging
import random
from abc import ABC
from datetime import datetime
from statistics import correlation

from src.application.base import RequestHandlerBase
from src.application.common import Request, Response
from src.application.kafka.consumers import LastScrapedDateConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer
from src.application.view_models import RecommendationVm
from src.domain.dtos import LastScrapedDateRequestDto, LastScrapedDateResponseDto, ReviewDto
from .get_recommendations_query import GetRecommendationsQuery


class GetRecommendationsQueryHandler(RequestHandlerBase[GetRecommendationsQuery, list[RecommendationVm]], ABC):
    __logger: logging.Logger
    __last_scraped_date_consumer: LastScrapedDateConsumer
    __last_scraped_date_producer: LastScrapedDateProducer
    __review_producer: ReviewProducer

    def __init__(
            self,
            logger: logging.Logger,
            last_scraped_date_consumer: LastScrapedDateConsumer,
            last_scraped_date_producer: LastScrapedDateProducer,
            review_producer: ReviewProducer
    ):
        self.__logger = logger
        self.__last_scraped_date_consumer = last_scraped_date_consumer
        self.__last_scraped_date_producer = last_scraped_date_producer
        self.__review_producer = review_producer

    def handle(self, request: Request[GetRecommendationsQuery]) -> Response[list[RecommendationVm]]:
        self.__last_scraped_date_producer.produce(LastScrapedDateRequestDto(
            game_id=request.payload.steam_game_id,
            correlation_id=request.correlation_id
        ))

        response: LastScrapedDateResponseDto | None
        while True:
            has_responded, response = self.__last_scraped_date_consumer.consume()
            if has_responded and response.correlation_id == request.correlation_id:
                break

        last_scraped_date = response.last_scraped_date
        self.__logger.debug("Sending messages from Review producer")

        NUMBER_OF_DUMMY_MESSAGES = 45

        for i in range(1, NUMBER_OF_DUMMY_MESSAGES + 1):
            is_last_review = i == NUMBER_OF_DUMMY_MESSAGES
            review = ReviewDto(
                game_id=request.payload.steam_game_id,
                date_posted=datetime.now().strftime("%Y-%m-%d"),
                is_recommended=random.choice((True, False)),
                hours_played=round(random.uniform(0, 700), 2),
                user_id=random.randint(1, 10_000),
                is_last_review=is_last_review,
                correlation_id=request.correlation_id
            )

            self.__review_producer.produce(review)

        self.__logger.debug("Messages sent from Review producer")
        return Response([])
