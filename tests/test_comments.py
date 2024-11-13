import libcst as cst

from backendcare import ImportTransformer


def test_import_with_comments():
    source = """
# Import path utilities
from os.path import join  # Used for joining paths
join('/tmp', 'file')  # Join example
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "# Import path utilities" in result
    assert "import os" in result
    assert "# Used for joining paths" in result
    assert "# Join example" in result
