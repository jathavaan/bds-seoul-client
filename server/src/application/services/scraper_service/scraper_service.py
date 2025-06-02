import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.application.kafka.producers.review_producer import ReviewProducer
from src.application.services.scraper_service import ScraperDto
from src.domain.dtos.review import ReviewDto


class ScraperService:
    __driver: webdriver.Edge
    __url: str | None = None
    __game_id: int
    __logger: logging.Logger
    __review_producer: ReviewProducer

    def __init__(self, logger: logging.Logger, driver: webdriver.Edge, review_producer: ReviewProducer):
        self.__driver = driver
        self.__logger = logger
        self.__review_producer = review_producer

    def scrape(self, dto: ScraperDto):
        self.__logger.info(f"Scraping Steam game ID {dto.game_id}")
        start_time = time.time()
        self.__set_game_id(dto.game_id)
        if self.__driver is None:
            raise ValueError("URL is None")

        self.__driver.get(self.__url)
        previous_review_count = 0

        while True:
            has_more_reviews = self.__scroll_down(previous_review_count)
            if not has_more_reviews:
                break

            reviews: list[WebElement] = []
            try:
                reviews = self.__driver.find_elements(
                    By.CLASS_NAME, "apphub_CardContentMain")
            except Exception:
                self.__logger.error("Failed to collect review containers.")

            current_review_count = len(reviews)
            is_done_extracting = self.extract_and_send(
                previous_review_count=previous_review_count,
                current_review_count=current_review_count,
                reviews=reviews,
                max_review_count=dto.max_reviews_count,
                last_scraped_date=dto.last_scraped_date,
                correlation_id=dto.correlation_id
            )

            if is_done_extracting:
                break

            previous_review_count = current_review_count

        end_time = time.time()
        self.__logger.info(
            f"Scraping finished for {dto.game_id} in {end_time - start_time:.2f} seconds."
        )

    def quit_driver(self):
        self.__logger.info("Shut down Selenium driver")
        self.__driver.quit()

    def __set_game_id(self, game_id: int):
        self.__game_id = game_id
        self.__url = f"https://steamcommunity.com/app/{self.__game_id}/reviews/?browsefilter=mostrecent&snr=1_5_100010_&p=1&filterLanguage=all"
        self.__logger.info(f"Scraping {self.__url}")

    @staticmethod
    def __parse_posted_date(date: str) -> tuple[str, datetime]:
        date = date.replace("Posted: ", "").strip()
        if "," not in date:
            date = f"{date}, {datetime.now().year}"

        if date[0].isdigit():
            date_obj = datetime.strptime(date, "%d %B, %Y")
        else:
            date_obj = datetime.strptime(date, "%B %d, %Y")
        date = date_obj.strftime("%Y-%m-%d")
        return date, date_obj

    def __is_last_review_check(
            self,
            review_count: int,
            max_reviews_count: int,
            review_date: datetime,
            last_scraped_date: datetime | None
    ) -> bool:
        if last_scraped_date and review_date < last_scraped_date:
            self.__logger.info(
                f'Ending scrolling after scraping {review_count} reviews. Reached last scraped date ({last_scraped_date})'
            )
            return True

        if review_count >= max_reviews_count:
            self.__logger.info(
                f'Ending scrolling after scraping {review_count} reviews. Reached max number of reviews to scrape'
            )
            return True

        return False

    def __parse_review(
            self,
            container: webdriver,
            review_count: int,
            max_review_count: int,
            last_scraped_date: datetime | None,
            correlation_id: str
    ) -> ReviewDto | None:
        try:
            date = container.find_element(By.CLASS_NAME, "date_posted").text
            hours = container.find_element(By.CLASS_NAME, "hours").text.strip()
            is_recommended_string = container.find_element(
                By.CLASS_NAME, "title"
            ).text

        except Exception:
            self.__logger.exception(
                f'Skipped review from {review_count} due to missing info.'
            )
            return None

        review_date_string, review_date = ScraperService.__parse_posted_date(date)
        is_recommended = is_recommended_string == "Recommended"
        hours = float(hours.split()[0].replace(
            ",", "")
        ) if hours else 0.0

        is_last_review = self.__is_last_review_check(
            review_count=review_count,
            max_reviews_count=max_review_count,
            review_date=review_date,
            last_scraped_date=last_scraped_date
        )

        return ReviewDto(
            game_id=self.__game_id,
            date_posted=review_date_string,
            is_recommended=is_recommended,
            hours_played=hours,
            user_id=review_count,
            is_last_review=is_last_review,
            correlation_id=correlation_id
        )

    def __scroll_down(self, old_review_count: int) -> bool:
        try:
            self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.__driver, 2).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "apphub_CardContentMain")) > old_review_count
            )
            return True
        except TimeoutException:
            self.__logger.info(f"No new reviews loaded. Stopped scrolling.")
            return False

    def extract_and_send(
            self,
            previous_review_count: int,
            current_review_count: int,
            reviews: list[WebElement],
            max_review_count: int,
            last_scraped_date: datetime | None,
            correlation_id: str
    ) -> bool:
        self.__logger.debug(
            f'Sending reviews {previous_review_count} to {current_review_count} to Kafka'
        )

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.__parse_review,
                    container,
                    previous_review_count + i,
                    max_review_count,
                    last_scraped_date,
                    correlation_id
                ) for i, container in enumerate(reviews[previous_review_count:current_review_count], start=1)
            ]

            for future in as_completed(futures):
                result: ReviewDto | None = future.result()

                if result:
                    self.__review_producer.produce(result)
                    if result.is_last_review:
                        return True

        return False
