import json
import logging

from confluent_kafka.cimpl import Producer

from src import Config
from src.application.base import ProducerBase
from src.application.base.kafka_base import T
from src.domain.dtos import ReviewDto


class ReviewProducer(ProducerBase[ReviewDto]):
    __logger: logging.Logger
    __producer: Producer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__producer = Producer(
            {"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, producer_content: ReviewDto) -> None:
        payload = json.dumps(producer_content.to_dict()).encode("utf-8")
        self.__producer.produce(
            topic=Config.KAFKA_REVIEW_TOPIC.value, value=payload)

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info(f"Shut down Review producer")
