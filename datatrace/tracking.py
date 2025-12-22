import sqlite3
from datatrace.utils import ensure_storage, now

def init_tracking_table():
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id TEXT,
        usage_note TEXT,
        timestamp TEXT
    )
    """)
    
    conn.commit()
    conn.close()

def track_dataset(path: str, note: str = "Tracked usage"):
    init_tracking_table()
    # Find dataset_id from path (simplified: hash to match)
    file_hash = hash_file(Path(path))  # From datasets
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM datasets WHERE hash = ?", (file_hash,))
    row = cursor.fetchone()
    if not row:
        raise ValueError("Dataset not found")
    
    dataset_id = row[0]
    cursor.execute(
        "INSERT INTO dataset_usage (dataset_id, usage_note, timestamp) VALUES (?, ?, ?)",
        (dataset_id, note, now())
    )
    
    conn.commit()
    conn.close()
    