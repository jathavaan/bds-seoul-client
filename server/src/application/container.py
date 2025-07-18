﻿from dependency_injector import containers, providers
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from src import Config
from src.application.common import Logger
from src.application.kafka.consumers import LastScrapedDateConsumer, FinalResultConsumer, ProcessStatusConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer, ProcessStatusProducer
from src.application.services.scraper_service import ScraperService


def driver_setup() -> webdriver.Remote:
    options = Options()
    options.binary_location = Config.BROWSER_PATH.value
    options.add_argument("--headless")

    driver = webdriver.Remote(
        command_executor=Config.GECKODRIVER_HOST.value,
        options=options
    )

    return driver


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger.get_logger, name="API", level=Config.LOGGING_LEVEL.value)
    driver = providers.Singleton(driver_setup)

    process_status_consumer = providers.Singleton(ProcessStatusConsumer, logger=logger)
    process_status_producer = providers.Singleton(ProcessStatusProducer, logger=logger)

    last_scraped_date_producer = providers.Singleton(LastScrapedDateProducer, logger=logger)
    last_scraped_date_consumer = providers.Singleton(LastScrapedDateConsumer, logger=logger)

    review_producer = providers.Singleton(ReviewProducer, logger=logger)
    final_result_consumer = providers.Singleton(FinalResultConsumer, logger=logger)

    scraper_service = providers.Singleton(
        ScraperService,
        logger=logger,
        driver=driver,
        review_producer=review_producer,
        process_status_producer=process_status_producer
    )
