import logging

from confluent_kafka import Consumer

from src import Config
from src.application.base import ConsumerBase
from src.domain.enums import ProcessType, ProcessStatus


class ProcessStatusConsumer(ConsumerBase[tuple[int, str, str] | None]):
    __logger: logging.Logger
    __consumer: Consumer

    def __init__(self, logger: logging.Logger):
        self.__logger = logger

        topics = [Config.KAFKA_PROCESS_STATUS_TOPIC.value]
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

    def consume(self) -> tuple[bool, tuple[int, ProcessType, ProcessStatus] | None]:
        message = self.__consumer.poll(Config.KAFKA_POLL_TIMEOUT.value)

        if not message:
            return False, None

        if message.error():
            self.__logger.error(message.error())
            return False, None

        value = message.value().decode("utf-8")
        parts = value.split(",", 2)

        if len(parts) != 3:
            self.__logger.error(f"Malformed message: {value}")
            return False, None

        try:
            result = (int(parts[0]), ProcessType.from_string(parts[1]), ProcessStatus.from_string(parts[2]))
            self.__logger.info(result)
        except ValueError as e:
            self.__logger.error(f"Error parsing message: {e}")
            return False, None

        return True, result

    def close(self) -> None:
        self.__consumer.close()
        self.__logger.info("Shutting down Final Result Producer")
