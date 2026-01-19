# datatrace/tracking.py - Usage tracking module
# This file was missing the track_usage function - now added completely

import sqlite3
from datatrace.utils import ensure_storage, now  # your utils for DB path and timestamp


def init_usage_table():
    """
    Create the usage tracking table if it doesn't exist.
    """
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
    Track how a dataset is used (e.g., 'used in training', 'visualized').
    This is the missing function causing the ImportError.
    """
    if not dataset_hash or not action:
        raise ValueError("Dataset hash and action description are required!")

    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure table exists
    init_usage_table()

    cursor.execute("""
        INSERT INTO usage (dataset_hash, action, timestamp)
        VALUES (?, ?, ?)
    """, (dataset_hash, action, now()))

    conn.commit()
    conn.close()


# Optional helper (for future CLI/UI)
def get_usage_for_dataset(dataset_hash: str):
    """Get all usage records for a specific dataset."""
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT action, timestamp
            FROM usage
            WHERE dataset_hash = ?
            ORDER BY timestamp DESC
        """, (dataset_hash,))
        rows = cursor.fetchall()
        return [{"action": r[0], "timestamp": r[1]} for r in rows]
    except Exception as e:
        print(f"Error getting usage: {e}")
        return []
    finally:
        conn.close()
        
