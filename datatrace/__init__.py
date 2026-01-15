# datatrace/__init__.py
"""
Make the most important functions available directly:
from datatrace import add_dataset, list_datasets, log_experiment, ...
"""

# Hashing & versioning
from .core import file_hash, dataset_hash, version_id

# Dataset operations (most important ones are actually here)
from .versioning import add_dataset, list_datasets

# Experiments
from .experiments import init_experiments_table, log_experiment, get_experiments

# Usage tracking / auditing
from .tracking import track_usage

# Visualization
from .visualize import visualize_metric, plot_experiments

# Optional useful utils
from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB



from .versioning import add_dataset, list_datasets  # or whatever functions you have there
from .visualize import visualize_metric, plot_experiments  

# Controls what you get with "from datatrace import *"
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
    'ensure_storage',
    'now',
    'save_json',
]


