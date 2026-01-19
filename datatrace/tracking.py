# datatrace/tracking.py
# Complete usage tracking module - this file was missing track_usage

import sqlite3
from datatrace.utils import ensure_storage, now


def init_usage_table():
    """Create the usage table if it doesn't exist."""
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_hash TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def track_usage(dataset_hash: str, action: str):
    """
    Track usage of a dataset (the missing function that caused the error).
    Logs what was done with the dataset (e.g., 'used in training', 'visualized').
    """
    if not dataset_hash or not action:
        raise ValueError("Both dataset_hash and action are required!")

    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    init_usage_table()  # make sure table exists

    cursor.execute("""
        INSERT INTO usage (dataset_hash, action, timestamp)
        VALUES (?, ?, ?)
    """, (dataset_hash, action, now()))

    conn.commit()
    conn.close()


def get_usage_records():
    """Optional: Get all usage records (for future use)."""
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT dataset_hash, action, timestamp FROM usage ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        return [{"hash": r[0], "action": r[1], "timestamp": r[2]} for r in rows]
    except Exception as e:
        print(f"Error getting usage: {e}")
        return []
    finally:
        conn.close()
