from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_cnn_by_category(query_date, categories):
    base_url = "https://lite.cnn.com/"  # Set the base URL
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Query to fetch all articles grouped by category
    c.execute("SELECT date, link, title, category FROM articles WHERE date LIKE ? ORDER BY category", (f"{query_date}%",))
    articles = c.fetchall()
    
    # Organize articles by category
    for article in articles:
        cat = article[3].capitalize()
        if cat not in categories:
            categories[cat] = []

        link = article[1]

        if link.startswith('/'):
            link = base_url + link

        updated = (article[0], link, article[2], cat)
        categories[cat].append(updated)
    
    # Close the database connection
    conn.close()
    return categories

def get_kron4_by_category(query_date, categories):
    base_url = "https://www.kron4.com/"  # Set the base URL
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Query to fetch all articles grouped by category
    c.execute("SELECT date, link, title, category FROM kron4 WHERE date LIKE ? ORDER BY category", (f"{query_date}%",))
    articles = c.fetchall()
    
    # Organize articles by category
    for article in articles:
        cat = article[3].capitalize()
        if cat not in categories:
            categories[cat] = []

        link = article[1]

        updated = (article[0], article[1], article[2], cat)
        categories[cat].append(updated)
    
    # Close the database connection
    conn.close()
    return categories

@app.route('/', methods=['GET'])
def home():
    date_query = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))
    categories = {}

    get_cnn_by_category(date_query, categories)
    get_kron4_by_category(date_query, categories)

    return render_template('index.html', date=date_query, categories=categories)

@app.route('/settings')
def settings():
    # Logic to render settings page
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
