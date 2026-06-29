import pytest
import requests
from practice.m6_web_scraping.book_scraper import (
    BookScraper,
    InvlaidURLScrapingException,
    FetchingError,
)
from practice.m6_web_scraping.model import BookRaw, Book
from practice.m6_web_scraping.pipeline import standarize_books
from unittest.mock import patch


def test_scrap_invalid_catalog_page():
    scraper = BookScraper()
    with pytest.raises(InvlaidURLScrapingException):
        books_raw = scraper.scrap_multiple_catalog_pages(999, 1000)


def test_standarize_books():
    books_raw = [BookRaw("Mock Book", "£13.99", "Two")]
    books_standarized = standarize_books(books_raw)
    assert isinstance(books_standarized[0], Book)
    assert books_standarized[0].title == "Mock Book"
    assert books_standarized[0].price == 13.99
    assert isinstance(books_standarized[0].price, float)
    assert books_standarized[0].rating == 2
    assert isinstance(books_standarized[0].rating, int)
