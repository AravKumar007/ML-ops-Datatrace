# datatrace/__init__.py
"""
Package initializer - exposes main functions at the top level
"""

# Core utilities
from .core import file_hash, dataset_hash, version_id

# Dataset related - pick correct location for each function
from .versioning import add_dataset                  # assuming this is where add_dataset lives

# Experiments
from .experiments import init_experiments_table, log_experiment, get_experiments

# Tracking
from .tracking import track_usage

# Visualization
from .visualize import visualize_metric, plot_experiments

# Utils
from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB


__all__ = [
    'add_dataset',
    'list_datasets',          
    'log_experiment',
    'get_experiments',
    'track_usage',
    'visualize_metric',
    'plot_experiments',
    'file_hash',
    'dataset_hash',
    'version_id',
]

