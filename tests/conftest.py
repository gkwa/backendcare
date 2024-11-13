import pytest


@pytest.fixture
def temp_python_file(tmp_path):
    test_file = tmp_path / "test.py"
    return test_file
