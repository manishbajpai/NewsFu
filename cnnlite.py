import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from pathlib import Path


def main(): 
    url = 'https://lite.cnn.com/'

    init_db()
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception if there was an error fetching the page

    # Use BeautifulSoup to parse the downloaded webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with href attributes that are relative URLs
    relative_links = soup.find_all('a', href=lambda href: href and href.startswith('/'))

    # Loop through each relative link, extract the URL and the text
    total = 0
    inserted = 0
    for link in relative_links:
        url = link.get('href')  # Extract the href attribute
        text = link.text.strip()  # Get the text content of the link, stripping any extra whitespace
        #print(f"URL: {url}, Text: {text}")
        total +=1
        inserted += insert_data(url, text)
    print(f"Total: {total}, inserted: {inserted}, dup: {total - inserted} ")

def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        date TEXT,
        link TEXT UNIQUE,
        title TEXT,
        category TEXT
    )
    ''')
    conn.commit()

    conn.close()
import re

def is_unix_path(path):
    # Pattern to match a valid Unix path
    pattern = r'^(/[^/\0]*)+/?$'
    
    # Validate against the pattern
    if re.match(pattern, path):
        return True
    else:
        return False

def insert_data(url, title):
    #make sure we understand the relative URL.
    if not is_unix_path(url):
        #todo: log the url for future analysis
        return 0
    # Split the path into parts
    path = Path(url)
    parts = path.parts
    if (len(parts) < 6):
        return 0
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    category = parts[4]
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # Data to be inserted
    data = [(date, url, title, category),]

    inserted = 1
    try: 
        c.executemany('INSERT INTO articles (date, link, title, category) VALUES (?, ?, ?, ?)', data)
    except sqlite3.IntegrityError as e:
        inserted = 0
        pass

    conn.commit()
    conn.close()
    return inserted

main()
