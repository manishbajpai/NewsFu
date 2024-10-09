#import requests
from curl_cffi import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
#from hyper.contrib import HTTP20Adapter

def test():
    with open('downloads/kron4.index.html') as f:
        soup = BeautifulSoup(f, 'html.parser')
        links = soup.find_all('a', href=lambda href: href and href.startswith('https://www.kron4.com/news/'))
        for link in links:
            url = link.get('href')
            text = link.text.strip()
            if text == '':
                continue
            parts = PurePosixPath(unquote(urlparse(url).path)).parts
            if len(parts) < 4:
                continue
            if not (parts[2] == 'bay-area' or parts[2] == 'california' or parts[2] == 'national'):
                continue
            if parts[3] == 'watch-news-live':
                continue
            print(f"{parts[2]}, {parts[3]}, {text}")


def main(): 

    url = 'https://www.kron4.com/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0', 'Accept': '*/*', 'referer':'https://www.google.com/'}

    #, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
# 'Accept-Language': 'en-US,en;q=0.5',
# 'Accept-Encoding': 'gzip, deflate, br, zstd',
# 'DNT': '1',
# 'Sec-GPC': '1',
# 'Connection': 'keep-alive',
# 'Upgrade-Insecure-Requests': '1',
# 'Sec-Fetch-Dest': 'document',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-Site': 'none',
# 'Sec-Fetch-User': '?1',
# 'Priority': 'u=1'}
    init_db()
    #response = requests.get(url, headers=headers)
    response = requests.get(url, impersonate="chrome110")

    # session = requests.Session()
    # session.mount("https://", HTTP20Adapter())
    # response = session.get(url, headers=headers)

    #print(response.request.headers)

    response.raise_for_status()  # This will raise an exception if there was an error fetching the page

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=lambda href: href and href.startswith('https://www.kron4.com/news/'))

    total = 0
    inserted = 0
    for link in links:
        url = link.get('href')
        text = link.text.strip()
        if text == '' or text == "Top Story":
            continue
        parts = PurePosixPath(unquote(urlparse(url).path)).parts
        if len(parts) < 4:
            continue
        if not (parts[2] == 'bay-area' or parts[2] == 'california' or parts[2] == 'national'):
            continue
        if parts[3] == 'watch-news-live':
            continue
        total += 1
        inserted += insert_data(url, text, parts[2])

    print(f"Total: {total}, inserted: {inserted}, dup: {total - inserted} ")

def init_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create a table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS kron4 (
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
        c.executemany('INSERT INTO kron4 (date, link, title, category) VALUES (?, ?, ?, ?)', data)
    except sqlite3.IntegrityError as e:
        inserted = 0
        pass

    conn.commit()
    conn.close()
    return inserted

main()
