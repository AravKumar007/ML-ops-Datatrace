import json
import sqlite3
from datetime import datetime
from datatrace.utils import ensure_storage

def init_experiments_table():
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        params TEXT,
        metrics TEXT,
        timestamp TEXT
    )
    """)  # Removed dataset_version; use junction

    conn.commit()
    conn.close()

def log_experiment(experiment_name: str, dataset_version: str, params: dict, metrics: dict):
    db_path = ensure_storage()
    init_experiments_table()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert experiment
    cursor.execute("""
    INSERT INTO experiments (name, params, metrics, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        experiment_name,
        json.dumps(params),
        json.dumps(metrics),
        datetime.now().isoformat()
    ))
    exp_id = cursor.lastrowid

    # Find dataset_id from version (assuming version is short hash)
    cursor.execute("SELECT id FROM datasets WHERE hash LIKE ?", (dataset_version + '%',))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Dataset version not found")
    dataset_id = row[0]

    # Link in junction
    cursor.execute("""
    INSERT OR IGNORE INTO experiment_datasets (experiment_id, dataset_id)
    VALUES (?, ?)
    """, (exp_id, dataset_id))

    conn.commit()
    conn.close()
    