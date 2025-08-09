import requests
from bs4 import BeautifulSoup
import re
import csv

BASE_URL = "https://www.aozora.gr.jp/index_pages/person{}.html"

def extract_author_data(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Extract author name
    author_match = re.search(r"作家名[:：]?\s*(.+)", text)
    author = author_match.group(1).strip() if author_match else "N/A"

    # Extract birth year
    birth_match = re.search(r"生年[:：]?\s*([0-9]{4})", text)
    birth_year = birth_match.group(1).strip() if birth_match else "N/A"

    # Extract death year
    death_match = re.search(r"没年[:：]?\s*([0-9]{4})", text)
    death_year = death_match.group(1).strip() if death_match else "N/A"

    # Extract author name romaji
    romaji_match = re.search(r"ローマ字表記[:：]?\s*(.+)", text)
    romaji = romaji_match.group(1).strip() if romaji_match else "N/A"

    return author, birth_year, death_year, romaji

def fetch_and_save_authors(start=1, end=10, output_file="aozora_authors.csv"):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Author", "Birth Year", "Death Year"])

        for i in range(start, end + 1):
            url = BASE_URL.format(i)
            try:
                response = requests.get(url)
                response.encoding = response.apparent_encoding
                if response.status_code == 200:
                    author, birth, death, romaji = extract_author_data(response.text)
                    print(f"{i}: {author}, {birth}, {death}, {romaji}")
                    writer.writerow([i, author, birth, death,romaji])
                else:
                    print(f"{i}: Failed to fetch (status {response.status_code})")
            except Exception as e:
                print(f"{i}: Error: {e}")

# Example usage
fetch_and_save_authors(1,2000)
