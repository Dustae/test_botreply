from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape")
def scrape_books():
    all_data = {}

    for i in range(1, 11):  # Loop through 10 pages
        page = i
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            data = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

            hrefs = [li.find("a")["href"] for li in data if li.find("a")]

            for link in hrefs:
                book_link = "https://books.toscrape.com/catalogue/" + link
                book_response = requests.get(book_link)

                if book_response.status_code == 200:
                    book_data = BeautifulSoup(book_response.text, "html.parser")

                    book_name = book_data.find("h1").text
                    product_description_section = book_data.find("div", id="product_description")

                    book_description = (
                        product_description_section.find_next("p").text.strip()
                        if product_description_section
                        else "No description available"
                    )

                    all_data[book_name] = {"description": book_description}

    return all_data  # Return JSON response
