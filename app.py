import gradio as gr
from datatrace.datasets import add_dataset, list_datasets
from datatrace.experiments import log_experiment, get_experiments
from datatrace.tracking import track_usage
from datatrace.visualize import visualize_metric  # Assuming this returns a matplotlib fig
import matplotlib.pyplot as plt
import io
import pandas as pd

def add_dataset_ui(file, metadata=""):
    if file is None:
        return "Upload a file first!"
    path = file.name  # Gradio saves temp file
    dataset_hash = add_dataset(path, metadata={"user_note": metadata})
    return f"Dataset added! Hash: {dataset_hash}"

def list_datasets_ui():
    datasets = list_datasets()
    if not datasets:
        return "No datasets yet."
    df = pd.DataFrame(datasets)  # Convert to DF for table
    return df

def log_experiment_ui(name, dataset_hash, params, metrics):
    params_dict = dict(p.split(":") for p in params.split(",") if p)  # e.g., "lr:0.01,epochs:5"
    metrics_dict = dict(m.split(":") for m in metrics.split(",") if m)
    log_experiment(name, dataset_hash, params_dict, metrics_dict)
    return "Experiment logged!"

def get_experiments_ui():
    experiments = get_experiments()
    if not experiments:
        return "No experiments yet."
    df = pd.DataFrame(experiments)
    return df

def track_usage_ui(dataset_hash, action):
    track_usage(dataset_hash, action)
    return "Usage tracked!"

def visualize_ui(metric):
    fig = visualize_metric(metric)  # Assume your func returns fig
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

with gr.Blocks(title="Datatrace Dashboard") as demo:
    gr.Markdown("# Datatrace: MLOps Tracker")
    
    with gr.Tab("Datasets"):
        file_input = gr.File(label="Upload Dataset")
        metadata_input = gr.Textbox(label="Metadata (optional)")
        add_btn = gr.Button("Add Dataset")
        output = gr.Textbox(label="Result")
        add_btn.click(add_dataset_ui, [file_input, metadata_input], output)
        
        list_btn = gr.Button("List Datasets")
        datasets_table = gr.Dataframe()
        list_btn.click(list_datasets_ui, None, datasets_table)
    
    with gr.Tab("Experiments"):
        name_input = gr.Textbox(label="Experiment Name")
        hash_input = gr.Textbox(label="Dataset Hash")
        params_input = gr.Textbox(label="Params (comma-separated, e.g., lr:0.01,epochs:5)")
        metrics_input = gr.Textbox(label="Metrics (comma-separated, e.g., accuracy:0.95)")
        log_btn = gr.Button("Log Experiment")
        log_output = gr.Textbox(label="Result")
        log_btn.click(log_experiment_ui, [name_input, hash_input, params_input, metrics_input], log_output)
        
        exp_btn = gr.Button("View Experiments")
        exp_table = gr.Dataframe()
        exp_btn.click(get_experiments_ui, None, exp_table)
    
    with gr.Tab("Tracking & Viz"):
        track_hash = gr.Textbox(label="Dataset Hash")
        action_input = gr.Textbox(label="Action Description")
        track_btn = gr.Button("Track Usage")
        track_output = gr.Textbox(label="Result")
        track_btn.click(track_usage_ui, [track_hash, action_input], track_output)
        
        metric_input = gr.Textbox(label="Metric to Visualize (e.g., accuracy)")
        viz_btn = gr.Button("Visualize")
        plot_output = gr.Image(label="Plot")
        viz_btn.click(visualize_ui, metric_input, plot_output)

if __name__ == "__main__":
    demo.launch()
