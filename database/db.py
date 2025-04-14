# database/db.py
import sqlite3
from datetime import datetime

DB_NAME = "candidates.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        candidate_id TEXT,
        job_id TEXT,
        score REAL,
        match_date TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_match(candidate_id, job_id, score):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO matches VALUES (?, ?, ?, ?)", (
        candidate_id,
        job_id,
        score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def fetch_all_matches():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM matches")
    rows = cur.fetchall()
    conn.close()
    return rows
