import hashlib
from pathlib import Path

CHUNK_SIZE = 8192


def file_hash(path: Path) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha.update(chunk)
    return sha.hexdigest()


def dataset_hash(dataset_dir: Path) -> str:
    sha = hashlib.sha256()

    for file in sorted(dataset_dir.rglob("*")):
        if file.is_file():
            sha.update(str(file.relative_to(dataset_dir)).encode())
            sha.update(file_hash(file).encode())

    return sha.hexdigest()


def version_id(hash_value: str) -> str:
    return hash_value[:8]
