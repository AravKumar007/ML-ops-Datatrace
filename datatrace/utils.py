import json
import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path("datastore")
META_DB = BASE_DIR / "meta.db"


def ensure_storage():
    """
    Ensure datastore folder and SQLite DB exist
    """
    BASE_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(META_DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        name TEXT,
        params TEXT,
        metrics TEXT,
        notes TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets (
        id TEXT PRIMARY KEY,
        path TEXT,
        hash TEXT,
        rows INTEGER,
        columns INTEGER,
        timestamp TEXT
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS experiment_datasets (
    experiment_id TEXT,
    dataset_id TEXT,
    PRIMARY KEY (experiment_id, dataset_id)
)
""")


    conn.commit()
    conn.close()

    return META_DB


def now():
    return datetime.utcnow().isoformat()


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

