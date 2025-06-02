from dependency_injector import containers, providers
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from src import Config
from src.application.common import Logger
from src.application.kafka.consumers import LastScrapedDateConsumer, FinalResultConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer
from src.application.services.scraper_service import ScraperService


def driver_setup() -> webdriver.Firefox:
    options = Options()
    options.binary_location = Config.BROWSER_PATH.value
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(Config.DRIVER_PATH.value)

    driver = webdriver.Firefox(service=service, options=options)
    return driver


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.scraper.pipelines"])

    logger = providers.Singleton(
        Logger.get_logger, name="API", level=Config.LOGGING_LEVEL.value)

    driver = providers.Singleton(driver_setup)

    last_scraped_date_producer = providers.Singleton(
        LastScrapedDateProducer, logger=logger)
    last_scraped_date_consumer = providers.Singleton(
        LastScrapedDateConsumer, logger=logger)
    review_producer = providers.Singleton(ReviewProducer, logger=logger)
    final_result_consumer = providers.Singleton(
        FinalResultConsumer, logger=logger)
    scraper_service = providers.Singleton(
        ScraperService, logger=logger, driver=driver, review_producer=review_producer)
