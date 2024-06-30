from flask import Flask, render_template, request, make_response
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def set_visit_cookie(response):
    expiry_date = datetime.now() + timedelta(days=30)  # Adjust expiry as needed
    response.set_cookie('last_visit', datetime.now().isoformat(), expires=expiry_date)
    return response

def freshness(article_t, visit_t):
     
    if (len(article_t) <=10):
        time_object = datetime.strptime(article_t, '%Y-%m-%d')
    else:
        time_object = datetime.strptime(article_t, '%Y-%m-%d %H:%M:%S')

    
    if (time_object > visit_t):
        return "new"
    else:
        return "old"
     
def get_cnn_by_category(query_date, categories, last_visited):
    base_url = "https://lite.cnn.com/"  # Set the base URL
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    # Query to fetch all articles grouped by category
    c.execute("SELECT date, link, title, category FROM articles WHERE date(date) LIKE ? ORDER BY category", (f"{query_date}%",))
    articles = c.fetchall()
    
    # Organize articles by category
    for article in articles:
        cat = article[3].capitalize()
        if cat == "Us":
            cat = "US"
        elif cat == "Middleeast":
            cat = "Middle East"

        if cat not in categories:
            categories[cat] = []

        link = article[1]

        if link.startswith('/'):
            link = base_url + link
        
        updated = (article[0], link, article[2], cat, freshness(article[0], last_visited))

        categories[cat].append(updated)
    
    conn.close()
    return categories

def get_kron4_by_category(query_date, categories, last_visited):
    base_url = "https://www.kron4.com/"
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
    c.execute("SELECT date, link, title, category FROM kron4 WHERE date(date) LIKE ? ORDER BY category", (f"{query_date}%",))
    articles = c.fetchall()
    
    # Organize articles by category
    for article in articles:
        cat = article[3].capitalize()
        if (cat == "National"):
            cat = "US"
        if cat not in categories:
            categories[cat] = []

        link = article[1]

        updated = (article[0], article[1], article[2], cat, freshness(article[0], last_visited))

        categories[cat].append(updated)
    
    conn.close()
    return categories

@app.route('/', methods=['GET'])
def home():
    # Get the last visit timestamp from the cookie
    last_visit_cookie = request.cookies.get('last_visit')
    if last_visit_cookie:
        last_visit = datetime.fromisoformat(last_visit_cookie)
        #print(f"last visit: {last_visit}")
    else:
        last_visit = datetime.min  # Default to very old date if no cookie is set

    date_query = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))
    categories = {}

    get_cnn_by_category(date_query, categories, last_visit)
    get_kron4_by_category(date_query, categories, last_visit)
    
    response = make_response(render_template('index.html', date=date_query, categories=categories))

    return set_visit_cookie(response)

@app.route('/settings')
def settings():
    # Logic to render settings page
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
