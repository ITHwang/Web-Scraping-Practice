import scrapy

# 5.2 간단한 스크레이퍼 작성하기
# url과 title 크롤링

# 문서 페이지 크롤링 담당
class ArticleSpider(scrapy.Spider):
    name = "article"

    def start_requests(self):
        urls = [
            "http://en.wikipedia.org/wiki/Python_%28programming_language%29",
            "https://en.wikipedia.org/wiki/Functional_programming",
            "https://en.wikipedia.org/wiki/Monty_Python",
        ]

        return [scrapy.Request(url=url, callback=self.parse) for url in urls]

    # 사용자가 정의한 콜백 함수
    def parse(self, response):
        url = response.url
        title = response.css("h1::text").extract_first()
        print("URL is : {}".format(url))
        print("Title is : {}".format(title))
