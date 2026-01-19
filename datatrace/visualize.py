# datatrace/visualize.py
# Visualization module for metrics and experiments
# Missing functions 'visualize_metric' and 'plot_experiments' added here

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from datatrace.utils import ensure_storage


def visualize_metric(metric_name: str):
    """
    Generate a simple line plot for a given metric across experiments.
    Returns a matplotlib Figure object.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT name, metrics
            FROM experiments
            ORDER BY timestamp
        """)
        rows = cursor.fetchall()

        if not rows:
            raise ValueError(f"No experiments found for metric '{metric_name}'")

        x_labels = []
        y_values = []

        for row in rows:
            exp_name = row[0]
            metrics_json = row[1]
            metrics = pd.read_json(metrics_json) if metrics_json else {}
            if metric_name in metrics:
                x_labels.append(exp_name)
                y_values.append(metrics[metric_name])

        if not y_values:
            raise ValueError(f"Metric '{metric_name}' not found in any experiment")

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_labels, y_values, marker='o', linestyle='-', color='b')
        ax.set_xlabel('Experiment')
        ax.set_ylabel(metric_name.capitalize())
        ax.set_title(f'{metric_name.capitalize()} Across Experiments')
        ax.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return fig

    except Exception as e:
        print(f"Visualization error: {e}")
        # Return a dummy empty figure on error
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"Error: {e}", ha='center', va='center')
        return fig
    finally:
        conn.close()


def plot_experiments():
    """
    Generate an overview plot of all experiments (e.g., number of experiments over time).
    Returns a matplotlib Figure.
    """
    db_path = ensure_storage()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT timestamp FROM experiments ORDER BY timestamp", conn)
    conn.close()

    if df.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No experiments yet", ha='center', va='center')
        return fig

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    counts = df['date'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts.index, counts.values, color='skyblue')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Experiments')
    ax.set_title('Experiments Over Time')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig
