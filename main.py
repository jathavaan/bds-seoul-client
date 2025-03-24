from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.persistence import create_db_session, close_db_session
from src.scraper.spiders import QuoteSpider


def main() -> None:
    session = create_db_session()

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(QuoteSpider)
    process.start()

    close_db_session(session)


if __name__ == "__main__":
    main()
