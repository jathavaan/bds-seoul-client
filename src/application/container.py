from dependency_injector import containers, providers

from src import Config
from src.application.common import Logger
from src.application.kafka.producers import LastScrapedDateProducer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.scraper.pipelines"])

    logger = providers.Singleton(Logger.get_logger, name="API", level=Config.LOGGING_LEVEL.value)
    last_scraped_date_producer = providers.Singleton(LastScrapedDateProducer, logger=logger)
