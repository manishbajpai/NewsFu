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
    for link in relative_links:
        url = link.get('href')  # Extract the href attribute
        text = link.text.strip()  # Get the text content of the link, stripping any extra whitespace
        #print(f"URL: {url}, Text: {text}")
        insert_data(url, text)

def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        date TEXT,
        link TEXT UNIQUE,
        title TEXT
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
        return
# Split the path into parts
    parts = url.parts
    date = parts[1]+'-'+parts[2]+'-'+parts[3]
    category = parts[4]
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # Data to be inserted
    data = [
        (date, url, title, category),
        #(datetime.now().strftime('%Y-%m-%d'), url, title),

    ]

    # Insert data into the table
    try: 
        c.executemany('INSERT INTO articles (date, link, title) VALUES (?, ?, ?)', data)
    except sqlite3.IntegrityError as e:
        #do nothing
        print("dup")

    # Commit the insertions
    conn.commit()
    # Close the connection to free the resources
    conn.close()

main()
