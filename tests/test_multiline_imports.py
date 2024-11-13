import libcst as cst

from backendcare import ImportTransformer


def test_multiline_imports():
    source = """
from os.path import (
    join,
    dirname,
    basename,
)
join('/tmp', 'file')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import os" in result
    assert "os.path.join" in result
