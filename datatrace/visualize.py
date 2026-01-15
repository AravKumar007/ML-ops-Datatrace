import sqlite3
import json
import matplotlib.pyplot as plt
from datatrace.utils import ensure_storage

def plot_experiments(metric_name: str = "accuracy"):
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, metrics FROM experiments")
    rows = cursor.fetchall()

    values = []
    for row in rows:
        metrics = json.loads(row[1])
        if metric_name in metrics:
            values.append((row[0], metrics[metric_name]))

    if not values:
        print("No data to plot")
        return

    ids, vals = zip(*values)
    plt.plot(ids, vals, marker='o')
    plt.xlabel("Experiment ID")
    plt.ylabel(metric_name.capitalize())
    plt.title(f"{metric_name} Over Experiments")
    plt.show()

    conn.close()
