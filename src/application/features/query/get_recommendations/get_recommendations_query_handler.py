import logging
import random
import time
from abc import ABC
from datetime import datetime

from src.application.base import RequestHandlerBase
from src.application.common import Request, Response
from src.application.kafka.consumers import LastScrapedDateConsumer, FinalResultConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer
from src.application.view_models import RecommendationVm
from src.domain.dtos import LastScrapedDateRequestDto, LastScrapedDateResponseDto, ReviewDto, FinalResultDto
from .get_recommendations_query import GetRecommendationsQuery


class GetRecommendationsQueryHandler(RequestHandlerBase[GetRecommendationsQuery, list[RecommendationVm]], ABC):
    __logger: logging.Logger
    __last_scraped_date_consumer: LastScrapedDateConsumer
    __last_scraped_date_producer: LastScrapedDateProducer
    __review_producer: ReviewProducer
    __final_result_consumer: FinalResultConsumer

    def __init__(
            self,
            logger: logging.Logger,
            last_scraped_date_consumer: LastScrapedDateConsumer,
            last_scraped_date_producer: LastScrapedDateProducer,
            review_producer: ReviewProducer,
            final_result_consumer: FinalResultConsumer
    ):
        self.__logger = logger
        self.__last_scraped_date_consumer = last_scraped_date_consumer
        self.__last_scraped_date_producer = last_scraped_date_producer
        self.__review_producer = review_producer
        self.__final_result_consumer = final_result_consumer

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

        last_scraped_date = response.last_scraped_date

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

        final_result: FinalResultDto | None = None
        while True:
            final_result = self.__final_result_consumer.consume()
            if final_result is not None and final_result.correlation_id == request.correlation_id:
                self.__logger.info(
                    f"Received response for Steam game ID {final_result.game_id} for correlation ID {final_result.correlation_id}"
                )
                break

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.__logger.info(f"Request {request.correlation_id} responded in {round(elapsed_time, 2)} second(s)")

        return Response([
            RecommendationVm(**recommendation.to_dict()) for recommendation in final_result.recommendations
        ])
