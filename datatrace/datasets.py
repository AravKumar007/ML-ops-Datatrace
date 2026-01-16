import hashlib
import sqlite3
import uuid
from pathlib import Path

from datatrace.utils import ensure_storage, now


def hash_file(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def log_dataset(path: str, rows: int, columns: int):
    """
    Register a dataset and return dataset_id
    """
    path = Path(path)
    file_hash = hash_file(path)

    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # check if dataset already exists
    cursor.execute(
        "SELECT id FROM datasets WHERE hash = ?",
        (file_hash,)
    )
    row = cursor.fetchone()

    if row:
        conn.close()
        return row[0]

    dataset_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO datasets (id, path, hash, rows, columns, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            dataset_id,
            str(path),
            file_hash,
            rows,
            columns,
            now(),
        )
    )

    conn.commit()
    conn.close()

    return dataset_id


# ────────────────────────────────────────────────────────────────
# NEW: List all versioned datasets
# ────────────────────────────────────────────────────────────────
def list_datasets():
    """
    Returns a list of all versioned datasets from the database.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, path, hash, rows, columns, timestamp
            FROM datasets
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()
        
        datasets = []
        for row in rows:
            datasets.append({
                "id": row[0],
                "path": row[1],
                "hash": row[2],
                "rows": row[3],
                "columns": row[4],
                "timestamp": row[5]
            })
        return datasets
    except Exception as e:
        print(f"Error listing datasets: {e}")
        return []
    finally:
        conn.close()
