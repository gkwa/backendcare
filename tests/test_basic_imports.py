import libcst as cst

from backendcare import ImportTransformer


def test_basic_import_conversion():
    source = """
from urllib.parse import urlparse
urlparse('https://example.com')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import urllib.parse" not in result  # Should just be 'import urllib'
    assert "import urllib" in result
    assert "urllib.parse.urlparse" in result
    assert "from urllib.parse import" not in result


def test_typing_import():
    source = """
from typing import Union
x: Union[int, str] = 5
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import typing" in result
    assert "typing.Union" in result
    assert "from typing import" not in result


def test_pathlib_import():
    source = """
from pathlib import Path
my_path = Path('/tmp')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import pathlib\n" in result
    assert "pathlib.Path('/tmp')" in result
    assert "from pathlib import" not in result
    assert "import pathlib.Path" not in result


def test_multiple_imports_same_module():
    source = """
from os.path import join, dirname
join('/tmp', 'file')
dirname('/tmp/file')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import os.path" not in result  # Should just be 'import os'
    assert "import os" in result
    assert "os.path.join" in result
    assert "os.path.dirname" in result
