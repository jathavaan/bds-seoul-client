from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

from src.config import Config


class ScraperService:
    # Setup Edge
    __driver: webdriver.Edge
    __url: str | None = None
    __game_id: int

    def __init__(self, driver: webdriver.Edge):
        self.__driver = driver

    def set_game_id(self, game_id: int):
        self.__game_id = game_id
        self.__url = f'https://steamcommunity.com/app/{self.__game_id}/reviews/?p=1&browsefilter=mostrecent'

    def parse_posted_date(date: str) -> tuple[str, datetime]:
        date = date.replace("Posted: ", "").strip()
        if "," not in date:
            date = f"{date}, {datetime.now().year}"

        if date[0].isdigit():                   # Format: "31 October, 2024"
            date_obj = datetime.strptime(date, "%d %B, %Y")
        else:                                   # Format: "May 5, 2023"
            date_obj = datetime.strptime(date, "%B %d, %Y")
        date = date_obj.strftime("%Y.%m.%d")
        return date, date_obj

    def is_last_review_check(review_number: int, date_obj: datetime) -> bool:
        if date_obj < Config.CUTOFF_DATE.value:
            print(f'{Config.CUTOFF_DATE.value} reached. Ending scroll.')
            return True
        if review_number >= Config.TARGET_REVIEW_COUNT.value:
            print(
                f'{Config.TARGET_REVIEW_COUNT.value} reviews loaded. Ending scroll.')
            return True
        return False

    def parse_review(self, review_number: int, container: webdriver) -> dict | None:
        try:
            date = container.find_element(By.CLASS_NAME, "date_posted").text
            hours = container.find_element(By.CLASS_NAME, "hours").text.strip()
            is_recommended_string = container.find_element(
                By.CLASS_NAME,
                "title"
            ).text

        except Exception as e:
            print(
                f'❌ Skipped review from {review_number} due to missing info.')
            print(e)
            return None

        # Date handling
        date_string, date_obj = self.parse_posted_date(date)

        # Recommended handling
        is_recommended = is_recommended_string == "Recommended"

        # Hours
        hours = float(hours.split()[0].replace(
            ",", "")) if hours else 0.0  # Turn into a number

        # is last review check
        is_last_review = self.is_last_review_check(review_number, date_obj)

        return {
            "game_id": self.__game_id,
            "date_posted": date,
            "is_recommended": is_recommended,
            "hours_played": hours,
            # "helpful": helpful,
            # "content": content,
            "user_id": review_number,
            "is_last_review": is_last_review
        }

    def scroll_down(self, old_review_count: int) -> bool:
        try:
            self.__driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.__driver, 2).until(
                lambda d: len(d.find_elements(
                    By.CLASS_NAME, "apphub_CardContentMain")) > old_review_count
            )
            return True
        except:
            print("No new reviews loaded. Ending scroll.")
            return False

    def extract_and_send(self, old_review_count: int, current_review_count: int, reviews: list[WebElement]) -> bool:
        print(
            f'Sending reviews {old_review_count} to {current_review_count} to kafka')
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.parse_review, old_review_count + i, container)
                       for i, container in enumerate(reviews[old_review_count:current_review_count], start=1)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(result)  # Send to Kafka
                    if result["is_last_review"]:
                        return True
        return False

    def scrape(self, game_id: int):
        start_time = time.time()
        self.set_game_id(game_id)
        if self.__driver is None:
            raise ValueError("url is None")

        self.__driver.get(self.__url)
        old_review_count = 0
        while True:
            has_more_reviews = self.scroll_down(old_review_count)
            if not has_more_reviews:
                break

            try:
                reviews = self.__driver.find_elements(
                    By.CLASS_NAME, "apphub_CardContentMain")
            except Exception as e:
                print("❌ Failed to collect review containers.")
                print(e)

            current_review_count = len(reviews)

            is_done_extracting = self.extract_and_send(
                old_review_count, current_review_count, reviews)
            if is_done_extracting:
                break

            old_review_count = current_review_count

        end_time = time.time()
        print(f"⏱️ Script finished in {end_time - start_time:.2f} seconds")

    def quit_driver(self):
        self.__driver.quit()
