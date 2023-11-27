import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.jjwxc.net"]
    start_urls = [
        "https://www.jjwxc.net/bookbase.php?fw0=0&fbsj0=0&novelbefavoritedcount0=0&yc1=1&xx3=3&mainview0=0&sd0=0&lx1=1&bq=&removebq=&isfinish=0&collectiontypes=ors&searchkeywords=&sortType=1&page=1"
    ]

    def parse(self, response):
        # fetch('https://www.jjwxc.net/bookbase.php?yc=1&xx=3&lx=1&sortType=1&page=1')
        books = response.css("table.cytable tbody tr")

        for book in books:
            if book.css("td a") is not []:
                yield {
                    "name": book.css("td a::text")[1].get(),
                    "url": book.css("td a")[1].attrib["href"],
                }

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
