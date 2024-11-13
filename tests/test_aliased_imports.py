import libcst as cst

from backendcare import ImportTransformer


def test_aliased_imports():
    source = """
from os.path import join as pjoin
pjoin('/tmp', 'file')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import os" in result
    assert "os.path.join('/tmp', 'file')" in result
