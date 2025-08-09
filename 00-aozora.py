import requests
from bs4 import BeautifulSoup
import re

def analyze_page(url, word):
    # Get the page content
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed

    # Let requests try to guess the correct encoding from headers or content
    response.encoding = response.apparent_encoding
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the page title
    title = soup.title.string if soup.title else "No title found"

    # Get all the visible text from the page
    text = soup.get_text(separator=' ', strip=True)

    # Count word occurrences (case-insensitive)
    word_count = text.lower().count(word.lower())

    # Output results
    print(f"Title: {title}")
    print(f"Occurrences of '{word}': {word_count}")

BASE_URL = "https://www.aozora.gr.jp/index_pages/person{}.html"

def extract_author_and_birth(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    
    # Look for "作家名" followed by a name (possibly on the same or next line)
    author_match = re.search(r"作家名[:：]?\s*(.+)", text)
    author = author_match.group(1).strip() if author_match else "N/A"

    # Look for "生年：" or "生年" followed by digits (maybe with Japanese era or kanji)
    birth_match = re.search(r"生年[:：]?\s*([0-9]{4})", text)
    birth_year = birth_match.group(1).strip() if birth_match else "N/A"
    # Look for "生年：" or "生年" followed by digits (maybe with Japanese era or kanji)
    death_match = re.search(r"没年[:：]?\s*([0-9]{4})", text)
    death_year = death_match.group(1).strip() if death_match else "N/A"

    return author, birth_year, death_year

fo= open("aozora_list.txt",'w')

def fetch_authors(start=1, end=5):
    for i in range(start, end + 1):
        url = BASE_URL.format(i)
        print(url)
        try:
            response = requests.get(url)
            # response.encoding = 'shift_jis'  # Aozora uses Shift_JIS encoding
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                author, birth_year, death_year = extract_author_and_birth(response.text)
                print(f"{i}: Author: {author}, Birth Year: {birth_year}")
                fo.write("B="+birth_year+" D="+death_year+" A="+author)
            else:
                print(f"{i}: Failed to fetch (status {response.status_code})")
        except Exception as e:
            print(f"{i}: Error fetching or parsing: {e}")

# Example usage
fetch_authors(1, 200)
