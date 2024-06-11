import argparse
from pathlib import Path

from fitparse_csv.converter import ConverterFactory
from fitparse_csv.fitparse_csv import FitparseCsv


def main():
    parser = argparse.ArgumentParser(description="fitparse csv converter")
    parser.add_argument(
        "dir",
        type=Path,
        help="directory where the fit files are stored",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=("csv", "xlsx"),
        default="xlsx",
        help="file type to output (default: %(default)s)",
    )
    parser.add_argument(
        "-r", "--remove-unknown", action="store_true", help="remove unknown fields"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force mode. overwrites existing files",
    )
    args = parser.parse_args()

    converter = ConverterFactory.create(
        args.type, remove_unknown=args.remove_unknown, overwrite=args.force
    )
    run = FitparseCsv(args.dir, converter)
    run()


if __name__ == "__main__":
    main()
