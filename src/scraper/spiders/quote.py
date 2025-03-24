import scrapy
from ...application.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = "Quote Spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")

        for quote in quotes:
            quote_item = QuoteItem()

            quote_item["quote"] = quote.xpath("span[@class='text']/text()").get()
            quote_item["author"] = quote.xpath("span/small[@class='author']/text()").get()
            quote_item["about_author_url"] = self.start_urls[0] + quote.xpath("span/a/@href").get()
            quote_item["tags"] = quote.xpath("div[@class='tags']/a/text()").getall()
            quote_item["tag_urls"] = [
                self.start_urls[0] + endpoint
                for endpoint in quote.xpath("div[@class='tags']/a/@href").getall()
            ]

            yield quote_item

        next_page_button = response.xpath("//li[@class='next']/a/@href").get()
        if next_page_button:
            next_page_url = self.start_urls[0] + next_page_button
            yield scrapy.Request(url=next_page_url, callback=self.parse)
