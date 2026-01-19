import sqlite3
from datatrace.utils import ensure_storage, now


def init_usage_table():
    """Create the usage table if it does not exist."""
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
    Track usage of a dataset.
    This function was missing, causing the ImportError.
    """
    if not dataset_hash or not action:
        raise ValueError("dataset_hash and action are required!")

    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    init_usage_table()  # ensure table exists

    cursor.execute("""
        INSERT INTO usage (dataset_hash, action, timestamp)
        VALUES (?, ?, ?)
    """, (dataset_hash, action, now()))

    conn.commit()
    conn.close()


def get_usage_records(dataset_hash: str = None):
    """Optional: Get usage records (for future use)."""
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if dataset_hash:
            cursor.execute("""
                SELECT action, timestamp
                FROM usage
                WHERE dataset_hash = ?
                ORDER BY timestamp DESC
            """, (dataset_hash,))
        else:
            cursor.execute("SELECT dataset_hash, action, timestamp FROM usage ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        return [{"hash": r[0], "action": r[1], "timestamp": r[2]} for r in rows] if not dataset_hash else [{"action": r[0], "timestamp": r[1]} for r in rows]
    except Exception as e:
        print(f"Error getting usage: {e}")
        return []
    finally:
        conn.close()
