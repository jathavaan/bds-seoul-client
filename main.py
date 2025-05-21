import json
import random
import time
from datetime import datetime

from confluent_kafka import Producer
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.scraper.spiders import QuoteSpider


def generate_random_review(producer: Producer) -> None:
    review = {
        "game_id": 308,
        "date_posted": datetime.now().strftime("%Y-%m-%d"),
        "is_recommended": random.choice((True, False)),
        "hours_played": round(random.uniform(0, 700), 2),
        "user_id": random.randint(1, 10_000)
    }

    payload = json.dumps(review).encode("utf-8")
    print(payload.decode("utf-8"))

    producer.produce("reviews", value=payload)
    producer.flush()


def main() -> None:
    producer = Producer({
        "bootstrap.servers": "host.docker.internal:9092",
    })

    try:
        while True:
            time.sleep(0.5)
            generate_random_review(producer=producer)
    except Exception as e:
        print("Stopping the program...")
        raise e
    finally:
        print("Program terminated.")

    # session = create_db_session()
    #
    # settings = get_project_settings()
    # process = CrawlerProcess(settings)
    # process.crawl(QuoteSpider)
    # process.start()
    #
    # close_db_session(session)


if __name__ == "__main__":
    main()
