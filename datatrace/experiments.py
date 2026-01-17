# datatrace/experiments.py
# Full experiment tracking module using SQLite

import sqlite3
import json
from datatrace.utils import ensure_storage, now


def init_experiments_table():
    """
    Create the experiments table if it doesn't exist.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dataset_hash TEXT NOT NULL,
            params TEXT,               -- JSON string of parameters
            metrics TEXT,              -- JSON string of metrics
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def log_experiment(name: str, dataset_hash: str, params: dict, metrics: dict):
    """
    Log an experiment with parameters and metrics.
    Params and metrics are stored as JSON strings.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Initialize table if not exists
    init_experiments_table()

    params_json = json.dumps(params) if params else '{}'
    metrics_json = json.dumps(metrics) if metrics else '{}'

    cursor.execute("""
        INSERT INTO experiments (name, dataset_hash, params, metrics, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (name, dataset_hash, params_json, metrics_json, now()))

    conn.commit()
    conn.close()


def get_experiments():
    """
    Retrieve all logged experiments.
    Returns list of dicts with parsed JSON params/metrics.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, name, dataset_hash, params, metrics, timestamp
            FROM experiments
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()

        experiments = []
        for row in rows:
            experiments.append({
                "id": row[0],
                "name": row[1],
                "dataset_hash": row[2],
                "params": json.loads(row[3]) if row[3] else {},
                "metrics": json.loads(row[4]) if row[4] else {},
                "timestamp": row[5]
            })
        return experiments
    except sqlite3.Error as e:
        print(f"Database error in get_experiments: {e}")
        return []
    finally:
        conn.close()
