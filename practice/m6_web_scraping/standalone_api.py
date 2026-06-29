import requests


def mainAPI():
    url = "https://openlibrary.org/search.json?q=data+engineering"

    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        books = data["docs"]

        for book in books[:3]:
            author_name_list = book["author_name"]
            first_publish_year = book["first_publish_year"]
            title = book["title"]

            print("Book From API:")
            print(f"title: {title}")
            print(f"Auhtor(s): {", ".join(author_name_list)[:-1]}")
            print(f"First publish year: {first_publish_year}")
            print()

    except requests.exceptions.HTTPError as err:
        print(f"Requests Error: {err}")


if __name__ == "__main__":
    mainAPI()
