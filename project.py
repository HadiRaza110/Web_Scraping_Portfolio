import csv
import requests
from bs4 import BeautifulSoup


def scrape_books():
  # Using a public sandbox testing site built specifically for web scraping practice
  url = "https://books.toscrape.com/"

  print(f"Fetching data from {url}...")
  response = requests.get(url, timeout=10)

  if response.status_code != 200:
    print(f"Failed to load page. Status code: {response.status_code}")
    return []

  # Parse the HTML content
  soup = BeautifulSoup(response.text, "html.parser")

  # Find all product containers on the page
  books = soup.find_all("article", class_="product_pod")

  scraped_data = []
  for book in books:
    # Extract title from the 'title' attribute of the <a> tag inside <h3>
    title = book.h3.a["title"]

    # Extract price text
    price = book.find("p", class_="price_color").text.strip()

    scraped_data.append({"Title": title, "Price": price})

  return scraped_data


def save_to_csv(data, filename="books_output.csv"):
  if not data:
    print("No data to save.")
    return

  # Write the collected dictionaries into a CSV file
  fieldnames = ["Title", "Price"]
  with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

  print(f"Success! Saved {len(data)} records to '{filename}'")


if __name__ == "__main__":
  books_data = scrape_books()
  save_to_csv(books_data)