from pathlib import Path

from fitparse_csv.converter import Converter


class FitparseCsv:
    def __init__(self, input_dir: Path, converter: Converter):
        self.input_dir = input_dir.resolve(strict=True)
        self.converter = converter

    def __call__(self):
        for fit in self.find_fits(self.input_dir):
            self.converter.convert(fit)

    def find_fits(self, path: Path):
        if path.is_dir():
            for file in path.iterdir():
                yield from self.find_fits(file)
        elif path.is_file() and path.suffix.lower() == ".fit":
            yield path
