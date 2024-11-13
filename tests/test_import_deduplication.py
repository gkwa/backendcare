import libcst as cst

from backendcare import ImportTransformer


def test_mixed_import_styles():
    source = """
import os
from os import path
from os.path import join
os.getcwd()
path.join('/tmp')
join('/tmp', 'file')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert result.count("import os") == 1  # Should deduplicate imports
    assert "os.getcwd()" in result
    assert "os.path.join" in result
