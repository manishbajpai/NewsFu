from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_articles_by_date(query_date):
    base_url = "https://lite.cnn.com/"  # Set the base URL

    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Query for articles by date
    c.execute("SELECT date, link, title FROM articles WHERE date LIKE ?", (f"{query_date}%",))
    articles = []
    for article in c.fetchall():
        # Append the base URL to the link if it's a relative URL
        link = article[1]
        if link.startswith('/'):
            link = base_url + link
        articles.append((article[0], link, article[2]))
    
    # Close the database connection
    conn.close()
    return articles

@app.route('/', methods=['GET'])
def home():
    date_query = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))
    articles = get_articles_by_date(date_query)
    return render_template('index.html', date=date_query, articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
