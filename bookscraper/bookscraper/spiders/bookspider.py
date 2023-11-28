import scrapy
from bookscraper.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.jjwxc.net"]

	url_no_index = "https://www.jjwxc.net/bookbase.php?yc=1&xx=3&lx=1&isfinish=0&collectiontypes=&searchkeywords=&sortType=2&page="
    start_urls = [
        url + "1"
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
            url_no_index
            + str(next_page_index)
        )

        if next_page_index <= 10:
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()
        book_item["url"] = response.url
        book_item["title"] = response.css("span.bigtext h1 span::text").get()
		description = response.xpath(
            "//div[@id='novelintro']/text()"
        ).getall() or response.xpath("//div[@id='novelintro']/font/text()").getall()
        book_item["description"] = 
        yield book_item
