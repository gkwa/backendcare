import argparse
import pathlib
import sys

from .converter import convert_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Python import statements to use fully qualified names"
    )
    parser.add_argument(
        "input_file",
        type=pathlib.Path,
        help="Input Python file to convert (will be modified in place unless -o/--output is specified)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        help="Optional output file path (if not specified, input file will be modified in place)",
        default=None,
    )

    try:
        args = parser.parse_args()
        convert_file(args.input_file, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
