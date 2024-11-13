import pathlib

import libcst as cst

from .transformer import ImportTransformer


def convert_file(
    input_path: pathlib.Path, output_path: pathlib.Path | None = None
) -> None:
    """Convert import statements in a Python file to the preferred style.

    Args:
        input_path: Path to the Python file to convert
        output_path: Optional path for output. If None, modifies input file in place.
                    If provided, writes to a new file at that path.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    # Read the input file
    source = input_path.read_text()

    # Process the content
    module = cst.parse_module(source)
    transformer = ImportTransformer()
    modified_module = module.visit(transformer)
    output_source = modified_module.code

    if output_path is None:
        # Modifying in place (default behavior)
        # Create a backup
        backup_path = input_path.with_suffix(input_path.suffix + ".bak")
        input_path.rename(backup_path)
        try:
            input_path.write_text(output_source)
        except Exception as e:
            # Restore from backup if something goes wrong
            backup_path.rename(input_path)
            raise RuntimeError(f"Failed to update file {input_path}: {e}")
        else:
            # Success - remove backup
            backup_path.unlink()
    else:
        # Writing to a different file
        if output_path == input_path:
            # If output_path is explicitly set to input_path, treat as in-place modification
            return convert_file(input_path, None)
        output_path.write_text(output_source)
