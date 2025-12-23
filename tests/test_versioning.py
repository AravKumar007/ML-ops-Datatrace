import pytest
from datatrace.versioning import add_dataset

def test_add_dataset(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a,b\n1,2")
    version = add_dataset(str(p))
    assert len(version) == 8
    