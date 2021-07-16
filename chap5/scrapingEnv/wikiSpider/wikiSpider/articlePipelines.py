# 파이프라인: 비동기적으로 처리하기(웹 서버에게 과도한 부하를 줄 수 있음)
# settings.py에서 ITEM_PIPELINES 주석 해제하기

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article


class ArticleSpider(CrawlSpider):
    name = "articlePipelines"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    rules = [
        Rule(LinkExtractor(allow="(/wiki/)((?!:).)*$"), callback="parse_items", follow=True),
    ]

    def parse_items(self, response):
        article = Article()
        article["url"] = response.url
        article["title"] = response.css("h1::text").extract_first()
        article["text"] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        article["lastUpdated"] = response.css("li#footer-info-lastmod::text").extract_first()
        return article
