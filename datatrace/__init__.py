# datatrace/__init__.py
# Expose key functions at package level for easy import: from datatrace import add_dataset, etc.

# Hashing & core utilities
from .core import file_hash, dataset_hash, version_id

# Dataset management
from .versioning import add_dataset, list_datasets   # ← Correct location!

# Experiments
from .experiments import init_experiments_table, log_experiment, get_experiments

# Tracking / auditing
from .tracking import track_usage

# Visualization
from .visualize import visualize_metric, plot_experiments

# Utils (optional exposure)
from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB

# What gets imported with "from datatrace import *"
__all__ = [
    'add_dataset', 'list_datasets',
    'log_experiment', 'get_experiments',
    'track_usage', 'visualize_metric',
    'plot_experiments', 'file_hash', 'dataset_hash', 'version_id',
    # Add more if you use them often
]
