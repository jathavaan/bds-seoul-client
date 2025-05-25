import json
import logging

from confluent_kafka.cimpl import Consumer

from src import Config
from src.application.base import ConsumerBase
from src.domain.dtos import FinalResultDto


class FinalResultConsumer(ConsumerBase[FinalResultDto | None]):
    __logger: logging.Logger
    __consumer: Consumer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

        topics = [Config.KAFKA_FINAL_RESULT_TOPIC.value]
        self.__consumer = Consumer({
            "bootstrap.servers": Config.KAFKA_BOOTSTRAP_SERVERS.value,
            "group.id": Config.KAFKA_GROUP_ID.value,
            "enable.auto.commit": True
        })

        self.__consumer.subscribe(topics)
        self.__logger.info(
            f"Kafka Consumer connected to bootstrap server [{Config.KAFKA_BOOTSTRAP_SERVERS.value}] "
            f"with group ID {Config.KAFKA_GROUP_ID.value}, subscribed to topic(s): {', '.join(topics)}"
        )

    def consume(self) -> tuple[bool, FinalResultDto | None]:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False, None

        if message.error():
            self.__logger.error(message.error())
            return False, None

        final_result = FinalResultDto(**json.loads(message.values().decode("utf-8")))
        return True, final_result

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shutting down final result consumer")
