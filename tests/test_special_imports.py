import libcst as cst
import pytest

from backendcare import ImportTransformer


def test_star_imports():
    source = """
from os.path import *
join('/tmp', 'file')
dirname('/tmp')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    with pytest.raises(TypeError):  # We expect TypeError for ImportStar
        module.visit(transformer)  # Removed unused variable assignment


def test_relative_imports():
    source = """
from ..utils import helper
from . import local_module
helper.do_something()
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    # Should preserve relative imports
    assert "from ..utils import helper" in result
    assert "from . import local_module" in result
