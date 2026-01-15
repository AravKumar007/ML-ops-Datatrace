import shutil
import pandas as pd
from pathlib import Path
from datatrace.core import file_hash, dataset_hash, version_id
from datatrace.datasets import log_dataset
from datatrace.utils import BASE_DIR, ensure_storage

def add_dataset(path: str) -> str:
    ensure_storage()
    path = Path(path)
    
    if path.is_file():
        # Single file (assume CSV for stats)
        hash_val = file_hash(path)
        version = version_id(hash_val)
        stored_path = BASE_DIR / "datasets" / f"{version}_{path.name}"
        stored_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, stored_path)
        
        # Auto-compute rows/columns if CSV
        if path.suffix == '.csv':
            df = pd.read_csv(path)
            rows, columns = df.shape
        else:
            rows, columns = 0, 0  # Or handle other formats
        
        log_dataset(str(stored_path), rows, columns)
    else:
        # Directory
        hash_val = dataset_hash(path)
        version = version_id(hash_val)
        stored_path = BASE_DIR / "datasets" / version
        shutil.copytree(path, stored_path, dirs_exist_ok=True)
        rows, columns = 0, 0  # Dir stats TBD
    
    return version

def load_metadata() -> dict:
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, path, hash, rows, columns, timestamp FROM datasets")
    rows = cursor.fetchall()
    
    metadata = {}
    for row in rows:
        version = version_id(row[2])  # Use short version from hash
        metadata[version] = {
            "id": row[0],
            "file": row[1],
            "stored_as": str(BASE_DIR / "datasets" / f"{version}_{Path(row[1]).name}"),
            "rows": row[3],
            "columns": row[4],
            "timestamp": row[5]
        }
    
    conn.close()
    return metadata

