# app.py
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Import your own modules - adjust paths if needed
from datatrace.datasets import add_dataset, list_datasets
from datatrace.experiments import log_experiment, get_experiments
from datatrace.tracking import track_usage
from datatrace.visualize import visualize_metric

def add_dataset_fn(file, metadata: str):
    if file is None:
        return "Please upload a file first!"
    
    # Gradio temp file path
    file_path = file.name
    
    try:
        meta_dict = {"note": metadata} if metadata.strip() else {}
        dataset_hash = add_dataset(file_path, metadata=meta_dict)
        return f"Dataset successfully versioned!\nHash: **{dataset_hash}**"
    except Exception as e:
        return f"Error: {str(e)}"

def list_datasets_fn():
    datasets = list_datasets()
    if not datasets:
        return "No datasets found yet."
    return pd.DataFrame(datasets)

def log_experiment_fn(name: str, dataset_hash: str, params: str, metrics: str):
    if not name or not dataset_hash:
        return "Name and Dataset Hash are required!"
    
    try:
        # Simple parsing - in real use you might want better input format
        params_dict = dict(item.split(":", 1) for item in params.split(",") if ":" in item)
        metrics_dict = dict(item.split(":", 1) for item in metrics.split(",") if ":" in item)
        
        log_experiment(name, dataset_hash, params_dict, metrics_dict)
        return "Experiment logged successfully!"
    except Exception as e:
        return f"Error logging experiment: {str(e)}"

def show_experiments_fn():
    exps = get_experiments()
    if not exps:
        return "No experiments logged yet."
    return pd.DataFrame(exps)

def track_usage_fn(dataset_hash: str, action_desc: str):
    if not dataset_hash or not action_desc:
        return "Both hash and action description required!"
    try:
        track_usage(dataset_hash, action_desc)
        return "Usage tracked!"
    except Exception as e:
        return f"Error: {str(e)}"

def visualize_metric_fn(metric_name: str):
    try:
        fig = visualize_metric(metric_name)  # Your function should return matplotlib Figure
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)  # Important - prevent memory leak
        return buf
    except Exception as e:
        return f"Error generating plot: {str(e)}"

# ────────────────────────────────────────────────────────────────
#               Gradio Interface
# ────────────────────────────────────────────────────────────────

with gr.Blocks(title="Datatrace • Lightweight MLOps Tracker") as demo:
    gr.Markdown(
        """
        # Datatrace
        **Lightweight Dataset Versioning • Experiment Tracking • Usage Auditing**
        
        Built from scratch with Python + SQLite • No heavy frameworks
        """
    )
    
    with gr.Tabs():
        with gr.Tab("Datasets"):
            with gr.Row():
                file_upload = gr.File(label="Upload dataset (CSV, etc.)")
                metadata = gr.Textbox(label="Optional metadata / note", placeholder="e.g. initial version v1")
            add_btn = gr.Button("Version Dataset")
            dataset_result = gr.Markdown()
            add_btn.click(add_dataset_fn, [file_upload, metadata], dataset_result)
            
            gr.Markdown("---")
            list_btn = gr.Button("Show All Versioned Datasets")
            datasets_table = gr.Dataframe()
            list_btn.click(list_datasets_fn, None, datasets_table)
        
        with gr.Tab("Experiments"):
            exp_name = gr.Textbox(label="Experiment Name", placeholder="mnist_cnn_v2")
            ds_hash = gr.Textbox(label="Dataset Hash")
            params_input = gr.Textbox(
                label="Parameters", 
                placeholder="optimizer:adam,lr:0.001,epochs:10",
                info="comma separated key:value pairs"
            )
            metrics_input = gr.Textbox(
                label="Metrics", 
                placeholder="accuracy:0.96,val_loss:0.12",
                info="comma separated key:value pairs"
            )
            log_btn = gr.Button("Log Experiment")
            log_result = gr.Markdown()
            log_btn.click(
                log_experiment_fn,
                [exp_name, ds_hash, params_input, metrics_input],
                log_result
            )
            
            gr.Markdown("---")
            show_exp_btn = gr.Button("Show All Experiments")
            experiments_table = gr.Dataframe()
            show_exp_btn.click(show_experiments_fn, None, experiments_table)
        
        with gr.Tab("Tracking & Visualization"):
            track_hash = gr.Textbox(label="Dataset Hash")
            action = gr.Textbox(label="What did you do?", placeholder="Used in random forest training")
            track_btn = gr.Button("Track Usage")
            track_result = gr.Markdown()
            track_btn.click(track_usage_fn, [track_hash, action], track_result)
            
            gr.Markdown("---")
            metric_select = gr.Textbox(label="Metric to plot", value="accuracy", placeholder="accuracy / loss / f1")
            plot_btn = gr.Button("Generate Plot")
            plot_output = gr.Image(label="Metric Evolution")
            plot_btn.click(visualize_metric_fn, metric_select, plot_output)

demo.launch()

