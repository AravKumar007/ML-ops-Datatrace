import hashlib
import shutil
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

from datatrace.utils import (
    DATASETS_DIR,
    METADATA_FILE,
    DB_FILE,
    ensure_storage
)
import sqlite3


def add_dataset(file_path: str) -> str:
    ensure_storage()

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError("Dataset not found")

    file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()[:8]
    stored_name = f"{file_path.stem}_{file_hash}{file_path.suffix}"
    destination = DATASETS_DIR / stored_name

    shutil.copy(file_path, destination)

    df = pd.read_csv(file_path)

    metadata = json.loads(METADATA_FILE.read_text())
    metadata[file_hash] = {
        "file": file_path.name,
        "stored_as": stored_name,
        "rows": len(df),
        "columns": len(df.columns),
        "timestamp": datetime.utcnow().isoformat()
    }

    METADATA_FILE.write_text(json.dumps(metadata, indent=4))

    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR REPLACE INTO datasets VALUES (?, ?, ?, ?, ?, ?)",
        (
            file_hash,
            file_path.name,
            stored_name,
            len(df),
            len(df.columns),
            metadata[file_hash]["timestamp"]
        )
    )
    conn.commit()
    conn.close()

    return file_hash


def list_datasets():
    ensure_storage()
    return json.loads(METADATA_FILE.read_text())
