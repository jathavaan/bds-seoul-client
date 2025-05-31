import json
import logging

from confluent_kafka.cimpl import Consumer

from src import Config
from src.application.base import ConsumerBase
from src.domain.dtos import LastScrapedDateResponseDto


class LastScrapedDateConsumer(ConsumerBase[LastScrapedDateResponseDto | None]):
    __logger: logging.Logger
    __consumer: Consumer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

        topics = [Config.KAFKA_LAST_SCRAPED_DATE_RES_TOPIC.value]
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
            "session.timeout.ms": Config.KAFKA_SESSION_TIMEOUT.value,
            "max.poll.interval.ms": Config.KAFKA_MAX_POLL_TIMEOUT.value,
            "heartbeat.interval.ms": Config.KAFKA_HEARTBEAT_INTERVAL.value
        })

        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> tuple[bool, LastScrapedDateResponseDto | None]:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False, None

        if message.error():
            self.__logger.error(message.error())
            return False, None

        self.__logger.info("Response received from last scraped date topic")
        response = LastScrapedDateResponseDto(**json.loads(message.value().decode("utf-8")))
        return True, response

    def close(self) -> None:
        self.__logger.info("Closing last scraped date response consumer")
        self.__consumer.close()
