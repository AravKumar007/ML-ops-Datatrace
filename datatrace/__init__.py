# datatrace/__init__.py - Package entry point

from .core import file_hash, dataset_hash, version_id

# Dataset functions
from .datasets import hash_file, log_dataset, list_datasets

# Dataset addition/versioning
from .versioning import add_dataset

# Experiments
from .experiments import init_experiments_table, log_experiment, get_experiments

# Usage tracking
from .tracking import track_usage

# Visualization
from .visualize import visualize_metric, plot_experiments

# Utilities
from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB

__all__ = [
    'add_dataset',
    'list_datasets',
    'log_dataset',
    'hash_file',
    'log_experiment',
    'get_experiments',
    'track_usage',
    'visualize_metric',
    'plot_experiments',
    'file_hash',
    'dataset_hash',
    'version_id',
    'ensure_storage',
    'now',
    'save_json',
]
