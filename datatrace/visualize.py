import matplotlib.pyplot as plt
import json
import sqlite3
import pandas as pd
from datatrace.utils import ensure_storage


def visualize_metric(metric_name: str = "accuracy"):
    """
    Create a line plot of a metric across all experiments.
    Returns a matplotlib Figure object (for Gradio or saving).
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, metrics FROM experiments ORDER BY timestamp")
        rows = cursor.fetchall()

        if not rows:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No experiments logged yet", ha='center', va='center')
            return fig

        x = []
        y = []
        for row in rows:
            name = row[0]
            metrics = json.loads(row[1]) if row[1] else {}
            if metric_name in metrics:
                x.append(name)
                y.append(metrics[metric_name])

        if not y:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, f"No data for metric '{metric_name}'", ha='center', va='center')
            return fig

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, marker='o', linestyle='-', color='teal')
        ax.set_xlabel('Experiment Name')
        ax.set_ylabel(metric_name.capitalize())
        ax.set_title(f'{metric_name.capitalize()} Over Experiments')
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return fig

    except Exception as e:
        print(f"Visualization error: {e}")
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center')
        return fig
    finally:
        conn.close()


def plot_experiments():
    """
    Plot number of experiments over time (bar chart).
    Returns a matplotlib Figure.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT timestamp FROM experiments", conn)
    conn.close()

    if df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No experiments yet", ha='center', va='center')
        return fig

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    counts = df['date'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts.index, counts.values, color='coral')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Experiments')
    ax.set_title('Experiments Created Over Time')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig

