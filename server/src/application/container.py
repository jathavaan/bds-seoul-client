from dependency_injector import containers, providers
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from src import Config
from src.application.common import Logger
from src.application.kafka.consumers import LastScrapedDateConsumer, FinalResultConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer
from src.application.services.scraper_service import ScraperService


def driver_setup() -> webdriver.Remote:
    options = Options()
    options.binary_location = Config.BROWSER_PATH.value
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Remote(
        command_executor=Config.GECKODRIVER_HOST.value,
        options=options
    )

    return driver


class Container(containers.DeclarativeContainer):
    logger = providers.Singleton(Logger.get_logger, name="API", level=Config.LOGGING_LEVEL.value)
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
