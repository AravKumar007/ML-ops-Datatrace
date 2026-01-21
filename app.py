import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


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
        return "Hash and action description required!"
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

with gr.Blocks(title="Datatrace • MLOps Tracker") as demo:
    gr.Markdown("# Datatrace\nLightweight Dataset Versioning & Experiment Tracking")

    with gr.Tabs():
        with gr.Tab("Datasets"):
            file_upload = gr.File(label="Upload dataset (CSV, etc.)")
            metadata = gr.Textbox(label="Optional note/metadata")
            add_btn = gr.Button("Version Dataset")
            add_result = gr.Markdown()
            add_btn.click(add_dataset_fn, [file_upload, metadata], add_result)

            gr.Markdown("---")
            list_btn = gr.Button("Show All Datasets")
            datasets_table = gr.Dataframe()
            list_btn.click(list_datasets_fn, None, datasets_table)

        with gr.Tab("Experiments"):
            exp_name = gr.Textbox(label="Experiment Name")
            ds_hash = gr.Textbox(label="Dataset Hash")
            params = gr.Textbox(label="Parameters", placeholder="optimizer:adam,epochs:5")
            metrics = gr.Textbox(label="Metrics", placeholder="accuracy:0.95")
            log_btn = gr.Button("Log Experiment")
            log_result = gr.Markdown()
            log_btn.click(log_experiment_fn, [exp_name, ds_hash, params, metrics], log_result)

            gr.Markdown("---")
            show_exp_btn = gr.Button("Show All Experiments")
            exp_table = gr.Dataframe()
            show_exp_btn.click(show_experiments_fn, None, exp_table)

        with gr.Tab("Tracking & Visualization"):
            track_hash = gr.Textbox(label="Dataset Hash")
            action = gr.Textbox(label="Action Description")
            track_btn = gr.Button("Track Usage")
            track_result = gr.Markdown()
            track_btn.click(track_usage_fn, [track_hash, action], track_result)

            gr.Markdown("---")
            metric = gr.Textbox(label="Metric to plot", value="accuracy")
            plot_btn = gr.Button("Generate Plot")
            plot_img = gr.Image()
            plot_btn.click(visualize_metric_fn, metric, plot_img)
if __name__ == "__main__":
    demo.launch(
        share=False,                    
        server_name="127.0.0.1",        
        server_port=7860,               
        debug=True,                     
        inbrowser=True                  
    )
    
