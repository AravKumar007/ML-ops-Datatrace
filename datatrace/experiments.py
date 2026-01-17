import sqlite3
from datatrace.utils import ensure_storage, now  
def get_experiments():
    """
    Retrieve all logged experiments from the database.
    Returns a list of dictionaries with experiment details.
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
                "params": row[3],
                "metrics": row[4],
                "timestamp": row[5]
            })
        return experiments
    except sqlite3.Error as e:
        print(f"Database error in get_experiments: {e}")
        return []
    finally:
        conn.close()
        
