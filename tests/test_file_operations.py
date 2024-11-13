import pathlib

import libcst as cst
import pytest

from backendcare import ImportTransformer, convert_file


def test_same_output_as_input(temp_python_file):
    original_code = """
from pathlib import Path
path = Path('/tmp')
"""
    temp_python_file.write_text(original_code)

    # Test explicit output=input_path
    convert_file(temp_python_file, temp_python_file)

    result = temp_python_file.read_text()
    assert "import pathlib" in result
    assert "pathlib.Path" in result
    assert not temp_python_file.with_suffix(temp_python_file.suffix + ".bak").exists()


def test_file_conversion_with_output(temp_python_file):
    original_code = """
from urllib.parse import urlparse
from os.path import join
url = urlparse('https://example.com')
path = join('/tmp', 'file')
"""
    temp_python_file.write_text(original_code)

    output_file = temp_python_file.parent / "output.py"
    convert_file(temp_python_file, output_file)

    result = output_file.read_text()
    assert "import urllib" in result
    assert "import os" in result
    assert "urllib.parse.urlparse" in result
    assert "os.path.join" in result

    # Original file should be unchanged
    assert temp_python_file.read_text() == original_code


def test_inplace_modification(temp_python_file):
    original_code = """
from pathlib import Path
path = Path('/tmp')
"""
    temp_python_file.write_text(original_code)

    # Test default behavior (in-place modification)
    convert_file(temp_python_file)

    result = temp_python_file.read_text()
    assert "import pathlib" in result
    assert "pathlib.Path" in result
    assert not temp_python_file.with_suffix(temp_python_file.suffix + ".bak").exists()


def test_backup_cleanup_on_success(temp_python_file):
    original_code = """
from pathlib import Path
path = Path('/tmp')
"""
    temp_python_file.write_text(original_code)

    # Modify in place
    convert_file(temp_python_file)

    # Backup should be cleaned up
    backup_path = temp_python_file.with_suffix(temp_python_file.suffix + ".bak")
    assert not backup_path.exists()


def test_maintains_existing_imports():
    source = """
import urllib.parse
from os.path import join
urllib.parse.urlparse('https://example.com')
join('/tmp', 'file')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import urllib.parse" in result  # Keep existing import style
    assert "import os" in result  # New import uses base module
    assert "urllib.parse.urlparse" in result
    assert "os.path.join" in result


def test_nonexistent_input_file():
    with pytest.raises(FileNotFoundError):
        convert_file(pathlib.Path("nonexistent.py"))


def test_input_not_a_file(tmp_path):
    with pytest.raises(ValueError):
        convert_file(tmp_path)
