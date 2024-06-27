from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_articles_by_category(query_date):
    base_url = "https://lite.cnn.com/"  # Set the base URL
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Query to fetch all articles grouped by category
    c.execute("SELECT date, link, title, category FROM articles WHERE date LIKE ? ORDER BY category", (f"{query_date}%",))
    articles = c.fetchall()
    
    # Organize articles by category
    categories = {}
    for article in articles:
        if article[3] not in categories:
            categories[article[3]] = []
        categories[article[3]].append(article)
    
    # Close the database connection
    conn.close()
    return categories

@app.route('/', methods=['GET'])
def home():
    date_query = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))
    categories = get_articles_by_category(date_query)
    return render_template('index.html', date=date_query, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
