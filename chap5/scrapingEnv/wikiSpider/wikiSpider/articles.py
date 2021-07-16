from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# 5.3 규칙에 의한 스파이더링
# wikipedia.org 도메인의 모든 링크를 따라 페이지 제목을 인쇄하고 외부 링크는 모두 무시하며 wikipedia.org를 탐색합니다.

# Rule에는 6개의 매개변수를 넘길 수 있음
# link_extractor: 필수 매개변수
# callback: 페이지 내용을 구문 분석하는 함수
# cb_kwargs: 콜백 함수에 전달할 매개변수 딕셔너리
# follow: 현재 페이지의 링크를 크롤링에 포함할지 여부
# 		  콜백 함수가 제공되지 않으면 기본값 True
# 		  콜백 함수가 제공되면 기본값 False

# LinkExtractor에는 일반적으로 allow, deny 매개변수를 사용함


class ArticleSpider(CrawlSpider):
    name = "articles"

    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"]
    # 규칙 리스트 제공: 모든 url 허용
    rules = [Rule(LinkExtractor(allow=r".*"), callback="parse_items", follow=True)]

    def parse_items(self, response):
        url = response.url
        title = response.css("h1::text").extract_first()
        # xpath: 텍스트 콘텐츠를 검색할 때 자주 사용
        text = response.xpath('//div[@id="mw-content-text"]//text()').extract()

        lastUpdated = response.css("li#footer-info-lastmod::text").extract_first()
        lastUpdated = lastUpdated.replace("This page was last edited on ", "")

        print("URL is : {}".format(url))
        print("Title is : {}".format(title))
        print("Text is : {}".format(text))
        print("Last updated is : {}".format(lastUpdated))
