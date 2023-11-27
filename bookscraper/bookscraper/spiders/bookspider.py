import scrapy
from bookscraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.jjwxc.net"]
    start_urls = [
        "https://www.jjwxc.net/bookbase.php?yc=1&xx=3&lx=1&isfinish=0&collectiontypes=&searchkeywords=&page=1&sortType=2"
    ]

    def parse(self, response):
        # fetch('https://www.jjwxc.net/bookbase.php?yc=1&xx=3&lx=1&isfinish=0&collectiontypes=&searchkeywords=&page=1&sortType=2')
        books = response.css("table.cytable tbody tr")

        for book in books:
            if book.css("td a") != []:
                relative_url = book.css("td a")[1].attrib["href"]
                url = "https://www.jjwxc.net/" + relative_url
                yield response.follow(url, callback=self.parse_book_page)

        page_field = "page="
        current_page_index = int(
            response.url[response.url.find(page_field) + len(page_field)]
        )
        next_page_index = current_page_index + 1
        next_page_url = (
            "https://www.jjwxc.net/bookbase.php?fw0=0&fbsj0=0&novelbefavoritedcount0=0&yc1=1&xx3=3&mainview0=0&sd0=0&lx1=1&bq=&removebq=&isfinish=0&collectiontypes=ors&searchkeywords=&sortType=1&page="
            + next_page_index
        )

        if next_page_index <= 10:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()
        book_item["url"] = response.url
        book_item["title"] = response.css("span.bigtext h1 span::text").get()
        book_item["description"] = response.xpath(
            "//div[@id='novelintro']/text()"
        ).getall()
        yield book_item
