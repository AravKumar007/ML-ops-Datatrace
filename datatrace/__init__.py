# datatrace/__init__.py
from .core import file_hash, dataset_hash, version_id

# Dataset operations (correct locations)
from .versioning import add_dataset
from .datasets import list_datasets

from .experiments import init_experiments_table, log_experiment, get_experiments
from .tracking import track_usage
from .visualize import visualize_metric, plot_experiments

from .utils import ensure_storage, now, save_json, BASE_DIR, META_DB

__all__ = [
    'add_dataset', 'list_datasets',
    'log_experiment', 'get_experiments',
    'track_usage', 'visualize_metric',
    'plot_experiments',
    'file_hash', 'dataset_hash', 'version_id',
]

