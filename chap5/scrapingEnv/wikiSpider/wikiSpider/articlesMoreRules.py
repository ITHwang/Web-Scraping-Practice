from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 파서 함수 하나와 Rule, LinkExtractor 클래스를 사용하여 위키백과를 크롤링한 후,
# 문서 페이지를 모두 출력하고 나머지 페이지에는 표식만 남기는 스파이더


class ArticleSpider(CrawlSpider):
    name = "articles"

    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    rules = [
        Rule(
            LinkExtractor(allow="^(/wiki/)((?!:).)*$"),
            callback="parse_itmes",
            follow=True,
            cb_kwargs={"is_article": True},
        ),
        Rule(LinkExtractor(allow=".*"), callback="parse_items", cb_kwargs={"is_article": False}),
    ]

    def parse_items(self, response, is_article):
        print(response.url)
        title = response.css("h1::text").extract_first()

        if is_article:
            url = response.url
            text = response.xpath('//div[@id="mw-content-text"]//text()'.extract())
            lastUpdated = response.css("li#footer-info-lasted::text").extract_first()
            lastUpdated = lastUpdated.replace("This page was last edited on ", "")

            print("Title is: {}".format(title))
            print("Last updated: {}".format(lastUpdated))
            print("Text is: {}".format(text))
        else:
            print("This is not an article: {}".format(title))
