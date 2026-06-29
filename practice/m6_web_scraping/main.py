from practice.m6_web_scraping.book_scraper import BookScraper
from practice.m6_web_scraping.model import BookRaw, Book
from practice.m6_web_scraping.pipeline import (
    standarize_books,
    filter_by_rating,
    sort_by_price_acs,
    calculate_agg_statistics,
    BookStats,
    write_stats_formatted,
    write_budget_books_formatted,
    write_books_to_file,
)
from pathlib import Path

CURR_DIR = Path(__file__).parent
OUTPUT_DIR = CURR_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "books_dataset.json"


def main():
    scraper = BookScraper()
    # Every iteration is reference to previous one so its SharedState
    books_raw = scraper.scrap_multiple_catalog_pages(1, 5)
    books_standarized = standarize_books(books_raw)
    ranked_5_books = filter_by_rating(books_standarized, 5)
    asc_price_ranked_5_books = sort_by_price_acs(ranked_5_books)
    top_5_cheap_books = asc_price_ranked_5_books[:5]
    books_stats = calculate_agg_statistics(books_standarized)

    # Report 1
    write_budget_books_formatted(top_5_cheap_books)

    # Report 2
    write_stats_formatted(books_stats)

    # write to file
    write_books_to_file(books_standarized, OUTPUT_DIR, OUTPUT_FILE)


if __name__ == "__main__":
    main()
