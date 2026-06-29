from bs4 import BeautifulSoup
import requests
from string import Template
from practice.m6_web_scraping.model import BookRaw
import time


class InvlaidURLScrapingException(Exception):
    pass


class FetchingError(Exception):
    pass


class BookScraper:
    def __init__(self, rate_limiting_delay=1):
        self.catalog_page_url_templeate = Template(
            "https://books.toscrape.com/catalogue/page-${page_nr}.html"
        )
        self.delay = rate_limiting_delay

    def scrap_catalog_page(self, page_nr):
        url = self.catalog_page_url_templeate.substitute(page_nr=page_nr)
        page = requests.get(url)

        if page.status_code == 404:
            raise InvlaidURLScrapingException
        elif page.status_code != 200:
            raise FetchingError

        soup = BeautifulSoup(page.content, "html.parser")

        books_containers = soup.find_all(class_="product_pod")

        books = []

        for i in range(20):
            rating_tag = books_containers[i].find("p")
            rating_str = rating_tag.get("class")[1]

            title_tag = books_containers[i].find("h3").find("a")
            title_str = title_tag.get("title")

            price_tag = books_containers[i].find(class_="price_color")
            price_str = price_tag.text
            books.append(
                BookRaw(title=title_str, price_raw=price_str, rating_raw=rating_str)
            )
        return books

    def scrap_multiple_catalog_pages(self, page_from, page_to):
        books_raw = []
        for page_nr in range(page_from, page_to + 1):
            batch = self.scrap_catalog_page(page_nr)
            books_raw.extend(batch)
            time.sleep(self.delay)
        return books_raw
