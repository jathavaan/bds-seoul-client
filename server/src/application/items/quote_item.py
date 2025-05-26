from scrapy import Field, Item


class QuoteItem(Item):
    quote = Field()
    author = Field()
    about_author_url = Field()
    tags = Field()
    tag_urls = Field()
