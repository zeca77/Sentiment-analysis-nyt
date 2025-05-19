import pandas as pd
import sqlite3

from helper_functions import fetch_articles

def get_db_connection(db='nyt_articles.db'):
    return sqlite3.connect(db, timeout=10)

def create_table():
    print('Creating table articles_titles...')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS article_titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER,
                month INTEGER
            )
        ''')
        conn.commit()

def insert_articles_for_year_in_db(year, api_key):
    print(f'Inserting articles for year {year}...')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for month in range(1, 13):
            articles = fetch_articles(year, month, api_key=api_key)
            for title in articles:
                cursor.execute(
                    "INSERT INTO article_titles (title, year, month) VALUES (?, ?, ?)",
                    (title, year, month)
                )
            print(f'Month {month} done.')
            conn.commit()
    print('Done.')

def load_articles_from_db(db_path='nyt_articles.db'):
    with get_db_connection(db_path) as conn:
        df = pd.read_sql_query("SELECT * FROM article_titles", conn)
    return df
