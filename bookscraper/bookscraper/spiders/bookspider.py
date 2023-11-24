import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["www.jjwxc.net"]
    start_urls = ["https://www.jjwxc.net/bookbase.php?yc=1&xx=3&lx=1&sortType=1&page=1"]

    def parse(self, response):
        books = response.css("tr")

        for book in books:
            yield {
                "name": book.css("td a::text").get(),
                "url": book.css("td a").attrib["href"],
            }
