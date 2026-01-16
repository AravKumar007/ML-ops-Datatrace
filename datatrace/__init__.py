# datatrace/__init__.py
from .core import file_hash, dataset_hash, version_id

# Dataset functions (now correct locations)
from .versioning import add_dataset
from .datasets import list_datasets, log_dataset, hash_file

# Experiments
from .experiments import init_experiments_table, log_experiment, get_experiments

# Tracking
from .tracking import track_usage

# Visualization
from .visualize import visualize_metric, plot_experiments

# Utils
from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB

# What you can import with from datatrace import *
__all__ = [
    'add_dataset', 'list_datasets', 'log_dataset', 'hash_file',
    'log_experiment', 'get_experiments',
    'track_usage', 'visualize_metric', 'plot_experiments',
    'file_hash', 'dataset_hash', 'version_id',
    'ensure_storage', 'now', 'save_json',
]
