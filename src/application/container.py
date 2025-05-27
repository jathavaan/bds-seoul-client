from dependency_injector import containers, providers
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service

from src import Config
from src.application.common import Logger
from src.application.kafka.consumers import LastScrapedDateConsumer
from src.application.kafka.producers import LastScrapedDateProducer, ReviewProducer
from src.application.services.scraper_service import ScraperService


def driver_setup():
    options = EdgeOptions()
    options.binary_location = Config.EDGE_PATH.value
    # If you want to see whats happening
    # options.add_argument("start-maximized")
    options.add_argument("--headless")  # It just happends in the background
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Edge(service=Service(
        EdgeChromiumDriverManager().install()), options=options)
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
    scraper_service = providers.Singleton(ScraperService, driver=driver)
