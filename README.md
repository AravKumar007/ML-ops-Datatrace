# Datatrace: Lightweight MLOps Dataset & Experiment Tracker

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AravKumar007/ML-ops-Datatrace/actions/badge.svg)](https://github.com/AravKumar007/ML-ops-Datatrace/actions)
Datatrace is a custom CLI tool for MLOps, focusing on dataset versioning, experiment tracking, and reproducibility. Built from scratch with Python and SQLite—no heavy dependencies like MLflow or DVC.

Ideal for personal ML projects or learning MLOps fundamentals.

## Why Datatrace?
- **Lightweight**: Pure Python + SQLite for fast setup.
- **Proper execution**: Demonstrates core MLOps concepts (hashing, tracking, linking).
- **Tech stacks**: Includes CI/CD, tests, Docker, and ML demo—showcases Python packaging, DB management, DevOps.

## Key Features
- Dataset versioning with SHA-256 hashing and auto-metadata (e.g., rows/cols for CSVs).
- Experiment logging with params/metrics linked to datasets.
- Usage auditing for datasets.
- Metric visualization (e.g., accuracy plots).
- End-to-end ML demo with scikit-learn.

## Screenshots

### Dataset List Command (Rich Table Output)
Your `datatrace list` command renders beautiful tables like this:

![Rich Table Example](https://raw.githubusercontent.com/Textualize/rich-cli/main/imgs/padding1.png)

### Experiment Visualization
The `datatrace visualize` command plots metrics across runs:

![Accuracy Plot](https://machinelearningmastery.com/wp-content/uploads/2020/09/Line-Plot-of-Decision-Tree-Accuracy-on-Train-and-Test-Datasets-for-Different-Tree-Depths.png)

![Learning Curve](https://machinelearningmastery.com/wp-content/uploads/2018/12/Example-of-Train-and-Validation-Learning-Curves-Showing-a-Training-Dataset-the-May-be-too-Small-Relative-to-the-Validation-Dataset.png)

### CLI in Action
Rich-powered colorful output:

![Rich CLI Demo](https://files.realpython.com/media/python-rich-example.a5212b91d9b6.png)

## Project Structure
ML-ops-Datatrace/
├── datatrace/              # Core package
│   ├── init.py
│   ├── cli.py             # Typer CLI
│   ├── core.py            # Hashing
│   ├── datasets.py        # Logging
│   ├── versioning.py      # Add/load
│   ├── tracking.py        # Usage audit
│   ├── experiments.py     # Logging/linking
│   ├── visualize.py       # Plots
│   └── utils.py           # DB helpers
├── examples/               # ML demo
├── tests/                  # Unit tests
├── .github/workflows/      # CI
├── Dockerfile
├── requirements.txt
└── README.md
text## Installation
```bash
git clone https://github.com/AravKumar007/ML-ops-Datatrace.git
cd ML-ops-Datatrace
pip install -r requirements.txt
Usage
Run commands via python -m datatrace.cli <command>.

Add dataset: add path/to/data.csv
List datasets: list
Track usage: track path/to/data.csv
Log experiment: experiment my_run abc123d4 --lr 0.01 --accuracy 0.95
Visualize: visualize --metric accuracy

Full Demo
Bashpython examples/demo_train.py run-demo
Generates Iris data, versions it, trains a model, logs experiment, and tracks usage.
Development & Testing

Tests: pytest
CI: GitHub Actions (auto-runs tests on push)
Docker: docker build -t datatrace . → docker run -it -v $(pwd)/datastore:/app/datastore datatrace

Tech Stack

CLI: Typer + Rich
Data: pandas, scikit-learn (demo)
Viz: matplotlib
Testing/CI: pytest, GitHub Actions
Container: Docker

Future Enhancements

Web dashboard (Streamlit)
Model artifact storage
Cloud integration (S3)
Contributions welcome!
