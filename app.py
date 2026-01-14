# app.py
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Clean imports from the package root (after fixing __init__.py)
from datatrace import (
    add_dataset,
    list_datasets,
    log_experiment,
    get_experiments,
    track_usage,
    visualize_metric
)

def add_dataset_fn(file, metadata: str = ""):
    if file is None:
        return "Please upload a file first!"
    try:
        meta_dict = {"note": metadata.strip()} if metadata.strip() else {}
        dataset_hash = add_dataset(file.name, metadata=meta_dict)
        return f"**Dataset versioned successfully!**\nHash: `{dataset_hash}`"
    except Exception as e:
        return f"Error: {str(e)}"

def list_datasets_fn():
    datasets = list_datasets()
    if not datasets:
        return pd.DataFrame([{"message": "No datasets versioned yet"}])
    return pd.DataFrame(datasets)

def log_experiment_fn(name: str, dataset_hash: str, params: str, metrics: str):
    if not name or not dataset_hash:
        return "Name and Dataset Hash are required!"
    try:
        params_dict = dict(item.split(":", 1) for item in params.split(",") if ":" in item.strip())
        metrics_dict = dict(item.split(":", 1) for item in metrics.split(",") if ":" in item.strip())
        log_experiment(name, dataset_hash, params_dict, metrics_dict)
        return "Experiment logged successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def show_experiments_fn():
    exps = get_experiments()
    if not exps:
        return pd.DataFrame([{"message": "No experiments logged yet"}])
    return pd.DataFrame(exps)

def track_usage_fn(dataset_hash: str, action: str):
    if not dataset_hash or not action:
        return "Hash and action description required!"
    try:
        track_usage(dataset_hash, action)
        return "Usage tracked successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

def visualize_metric_fn(metric_name: str):
    try:
        fig = visualize_metric(metric_name)
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception as e:
        return f"Could not generate plot: {str(e)}"

# ────────────────────────────────────────────────────────────────
# Gradio UI
# ────────────────────────────────────────────────────────────────

with gr.Blocks(title="Datatrace - MLOps Tracker") as demo:
    gr.Markdown("# Datatrace\nLightweight Dataset Versioning & Experiment Tracking")

    with gr.Tabs():
        with gr.Tab("Datasets"):
            file_upload = gr.File(label="Upload file (csv, etc.)")
            metadata = gr.Textbox(label="Optional note/metadata")
            btn_add = gr.Button("Add & Version Dataset")
            result_add = gr.Markdown()
            btn_add.click(add_dataset_fn, [file_upload, metadata], result_add)

            gr.Markdown("---")
            btn_list = gr.Button("Show All Datasets")
            table_datasets = gr.Dataframe()
            btn_list.click(list_datasets_fn, None, table_datasets)

        with gr.Tab("Experiments"):
            exp_name = gr.Textbox(label="Experiment Name")
            ds_hash = gr.Textbox(label="Dataset Hash")
            params = gr.Textbox(label="Parameters", placeholder="lr:0.01,epochs:10")
            metrics = gr.Textbox(label="Metrics", placeholder="accuracy:0.95,loss:0.23")
            btn_log = gr.Button("Log Experiment")
            result_log = gr.Markdown()
            btn_log.click(log_experiment_fn, [exp_name, ds_hash, params, metrics], result_log)

            gr.Markdown("---")
            btn_show = gr.Button("Show All Experiments")
            table_exps = gr.Dataframe()
            btn_show.click(show_experiments_fn, None, table_exps)

        with gr.Tab("Tracking & Plots"):
            track_hash = gr.Textbox(label="Dataset Hash")
            action_desc = gr.Textbox(label="Action / Usage Description")
            btn_track = gr.Button("Track Usage")
            result_track = gr.Markdown()
            btn_track.click(track_usage_fn, [track_hash, action_desc], result_track)

            gr.Markdown("---")
            metric_input = gr.Textbox(label="Metric name to plot", value="accuracy")
            btn_plot = gr.Button("Show Plot")
            plot_output = gr.Image()
            btn_plot.click(visualize_metric_fn, metric_input, plot_output)

if __name__ == "__main__":
    demo.launch()
