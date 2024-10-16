import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

def sanitize(link):
    url = link.get('href')
    link['href'] = url.split('#')[0]
    text = link.text.strip()
    if (text == '' or text == 'From The Newsroom'):
        return []
    parts = PurePosixPath(unquote(urlparse(url).path)).parts
    if len(parts) < 3:
        return []
    if not (parts[1] == 'india-news'):
        return []
    return link

def test():
    with open('downloads/ndtv.html') as f:
        soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a', href=lambda href: href and href.startswith('https://www.ndtv.com/'))
        for link in links:
            sanitized = sanitize(link)
            if (sanitized):
                print(link)

def update(): 
    url = 'https://www.ndtv.com/'

    init_db()
    response = requests.get(url)
    response.raise_for_status()  # This will raise an exception if there was an error fetching the page

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=lambda href: href and href.startswith('https://www.ndtv.com/india-news/'))

    total = 0
    inserted = 0
    for link in links:
        sanitized = sanitize(link)
        if (sanitized): 
            total += 1
            inserted += insert_data(link.get('href'), link.text.strip(), "India")

    print(f"Total: {total}, inserted: {inserted}, dup: {total - inserted} ")

def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS ndtv (
        date TEXT,
        link TEXT UNIQUE,
        title TEXT,
        category TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_data(url, title, category):
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = [(date, url, title, category),]
   
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    inserted = 1
    try: 
        c.executemany('INSERT INTO ndtv (date, link, title, category) VALUES (?, ?, ?, ?)', data)
    except sqlite3.IntegrityError as e:
        inserted = 0
        pass

    conn.commit()
    conn.close()
    return inserted

def main():
    import sys
    if (len(sys.argv) > 1 and sys.argv[1] == "test"):
        test()
    else:
        update()

main()