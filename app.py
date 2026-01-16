# app.py - Clean Gradio dashboard for Datatrace
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ==========================================
# Choose ONE import style below - pick what matches your __init__.py
# ==========================================

# Style A: Use package-level imports (recommended if __init__.py is correct)
# from datatrace import add_dataset, list_datasets, log_experiment, get_experiments, track_usage, visualize_metric

# Style B: Direct module imports (safer while debugging, use this for now)
from datatrace.versioning import add_dataset
from datatrace.datasets import list_datasets          # change to .versioning if function is there
from datatrace.experiments import log_experiment, get_experiments
from datatrace.tracking import track_usage
from datatrace.visualize import visualize_metric

# ==========================================
# Functions for Gradio buttons
# ==========================================

def add_dataset_fn(file, metadata: str = ""):
    if file is None:
        return "Please upload a file first!"
    try:
        meta_dict = {"note": metadata.strip()} if metadata.strip() else {}
        dataset_hash = add_dataset(file.name, metadata=meta_dict)
        return f"**Success!** Dataset versioned.\nHash: `{dataset_hash}`"
    except Exception as e:
        return f"Error: {str(e)}"


def list_datasets_fn():
    try:
        datasets = list_datasets()
        if not datasets:
            return pd.DataFrame([{"Status": "No datasets versioned yet"}])
        return pd.DataFrame(datasets)
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])


def log_experiment_fn(name: str, dataset_hash: str, params: str, metrics: str):
    if not name or not dataset_hash:
        return "Name and Dataset Hash are required!"
    try:
        params_dict = dict(item.split(":", 1) for item in params.split(",") if ":" in item.strip())
        metrics_dict = dict(item.split(":", 1) for item in metrics.split(",") if ":" in item.strip())
        log_experiment(name, dataset_hash, params_dict, metrics_dict)
        return "**Experiment logged successfully!**"
    except Exception as e:
        return f"Error: {str(e)}"


def show_experiments_fn():
    try:
        exps = get_experiments()
        if not exps:
            return pd.DataFrame([{"Status": "No experiments logged yet"}])
        return pd.DataFrame(exps)
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])


def track_usage_fn(dataset_hash: str, action: str):
    if not dataset_hash or not action:
        return "Both hash and action description are required!"
    try:
        track_usage(dataset_hash, action)
        return "**Usage tracked successfully!**"
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


# ==========================================
# Gradio Interface
# ==========================================

with gr.Blocks(title="Datatrace • MLOps Tracker") as demo:
    gr.Markdown("# Datatrace\nLightweight Dataset Versioning & Experiment Tracking")

    with gr.Tabs():
        with gr.Tab("Datasets"):
            file_upload = gr.File(label="Upload dataset (CSV, etc.)")
            metadata_input = gr.Textbox(label="Optional metadata/note")
            add_button = gr.Button("Version Dataset")
            add_output = gr.Markdown()
            add_button.click(add_dataset_fn, [file_upload, metadata_input], add_output)

            gr.Markdown("---")
            list_button = gr.Button("List All Datasets")
            datasets_table = gr.Dataframe()
            list_button.click(list_datasets_fn, None, datasets_table)

        with gr.Tab("Experiments"):
            exp_name = gr.Textbox(label="Experiment Name")
            ds_hash = gr.Textbox(label="Dataset Hash")
            params_input = gr.Textbox(label="Parameters", placeholder="lr:0.01,epochs:10")
            metrics_input = gr.Textbox(label="Metrics", placeholder="accuracy:0.95,loss:0.12")
            log_button = gr.Button("Log Experiment")
            log_output = gr.Markdown()
            log_button.click(log_experiment_fn, [exp_name, ds_hash, params_input, metrics_input], log_output)

            gr.Markdown("---")
            show_exp_button = gr.Button("Show All Experiments")
            experiments_table = gr.Dataframe()
            show_exp_button.click(show_experiments_fn, None, experiments_table)

        with gr.Tab("Tracking & Visualization"):
            track_hash = gr.Textbox(label="Dataset Hash")
            action_input = gr.Textbox(label="Action/Usage Description")
            track_button = gr.Button("Track Usage")
            track_output = gr.Markdown()
            track_button.click(track_usage_fn, [track_hash, action_input], track_output)

            gr.Markdown("---")
            metric_name = gr.Textbox(label="Metric to Visualize", value="accuracy")
            plot_button = gr.Button("Generate Plot")
            plot_image = gr.Image()
            plot_button.click(visualize_metric_fn, metric_name, plot_image)

if __name__ == "__main__":
    demo.launch()
