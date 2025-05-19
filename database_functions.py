from datetime import date
import pandas as pd
import sqlite3

from helper_functions import fetch_articles_by_week

def get_db_connection(db='nyt_articles.db'):
    return sqlite3.connect(db, timeout=10)


def create_table():
    print('Creating table article_titles...')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS article_titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                year INTEGER,
                month INTEGER,
                week INTEGER
            )
        ''')
        conn.commit()



def insert_articles_for_week_range(year, start_week, end_week, api_key):
    print(f'Inserting articles for year {year}, weeks {start_week} to {end_week}...')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for week in range(start_week, end_week + 1):
            articles = fetch_articles_by_week(year, week, api_key=api_key)
            try:
                start_of_week = date.fromisocalendar(year, week, 1)  # Monday
                month = start_of_week.month
            except ValueError:
                print(f"Skipping invalid week {week} for year {year}")
                continue

            for title in articles:
                cursor.execute(
                    "INSERT INTO article_titles (title, year, month, week) VALUES (?, ?, ?, ?)",
                    (title, year, month, week)
                )
            print(f'Week {week} done.')
            conn.commit()
    print('Done.')


def insert_articles_for_year_in_db(year, api_key):
    # Get the last ISO week number of the year
    last_week = date(year, 12, 28).isocalendar()[1]
    insert_articles_for_week_range(year, start_week=1, end_week=last_week, api_key=api_key)



def load_articles_from_db(db_path='nyt_articles.db'):
    with get_db_connection(db_path) as conn:
        df = pd.read_sql_query("SELECT * FROM article_titles", conn)
    return df
