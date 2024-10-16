# News Now
News reporting: The way it should be

## What is it about?
Many news websites today are cluttered with distracting designs, filled with clickbait and ragebait content. While some articles cover actual news, many others are irrelevant and linger on the front page to drive user engagement. This project envisions a clean and simplified user interface that prioritizes showing the latest headlines from multiple trusted sources, tailored to your preferences. We understand that people have different ways they like to consume news, so we offer customization options for the look and feel to suit your style.

## Run
```bash
Python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```
Now point your browser to [http://localhost:5001/](http://localhost:5001/) or whatever url is printed by app.py

## Development
The development of this project consists of two main components: updating the database and presenting the news. These components are connected through a standardized database schema that is shared across all news sources.

### Update the database
To add a new news source, you'll need to create a script that fetches data from the source and stores it in the database. This script can be written in any programming language, though we are currently using Python for this task.

### Present the news
This involves retrieving the relevant links from the database and displaying them to the user based on their preferences. This part of the project is also built using Python.

If you have any questions, feel free to reach out by posting on the project page on GitHub: https://github.com/manishbajpai/NewsFu.
