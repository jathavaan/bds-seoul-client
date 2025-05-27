import json
import logging

from confluent_kafka import Producer

from src import Config
from src.application.base import ProducerBase
from src.domain.dtos import LastScrapedDateRequestDto


class LastScrapedDateProducer(ProducerBase[LastScrapedDateRequestDto]):
    __logger: logging.Logger
    __producer: Producer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__producer = Producer({"bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value})

    def produce(self, producer_content: LastScrapedDateRequestDto) -> None:
        self.__logger.info(f"Requested last scraped date for Steam game ID {producer_content.game_id}")
        self.__producer.produce(
            topic=Config.KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC.value,
            value=json.dumps(producer_content.to_dict())
        )

    def close(self) -> None:
        self.__producer.flush()
        self.__logger.info("Shutting down last scraped date producer")
