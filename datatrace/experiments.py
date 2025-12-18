import json
import sqlite3
from datetime import datetime
from datatrace.utils import ensure_storage


def init_experiments_table():
    _, db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dataset_version TEXT,
        params TEXT,
        metrics TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_experiment(name: str, dataset_version: str, params: dict, metrics: dict):
    _, db_path = ensure_storage()
    init_experiments_table()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO experiments (name, dataset_version, params, metrics, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        dataset_version,
        json.dumps(params),
        json.dumps(metrics),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

