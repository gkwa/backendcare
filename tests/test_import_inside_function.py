import libcst as cst

from backendcare import ImportTransformer


def test_import_inside_function():
    source = """
def load_config():
    from os.path import join
    return join('/etc', 'config')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import os" in result
    assert "os.path.join('/etc', 'config')" in result


def test_multiple_functions_with_imports():
    source = """
def load_config():
    from os.path import join
    return join('/etc', 'config')

def load_path():
    from pathlib import Path
    return Path('/tmp')
"""
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified = module.visit(transformer)
    result = modified.code

    assert "import os" in result
    assert "import pathlib" in result
    assert "os.path.join('/etc', 'config')" in result
    assert "pathlib.Path('/tmp')" in result
