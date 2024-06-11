import csv
import sys
import warnings
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from pathlib import Path

from fitparse import FitFile, FitParseError


class Converter(metaclass=ABCMeta):
    def __init__(self, remove_unknown: bool, overwrite: bool):
        self.remove_unknown = remove_unknown
        self.overwrite = overwrite

    @abstractmethod
    def convert(self, file: Path):
        pass

    def _parse(self, file: Path):
        try:
            fit_file = FitFile(str(file))
            fit_file.parse()
        except FitParseError as e:
            warnings.warn(f"skipping file containing invalid data: {file}. error: {e}")
            return

        def is_unknown(x: str):
            return x.lower().startswith("unknown")

        groups = OrderedDict()
        for message in fit_file.get_messages():
            name = message.name
            values = message.get_values()

            if self.remove_unknown:
                if is_unknown(name):
                    continue
                for k in [*values.keys()]:
                    if is_unknown(k):
                        del values[k]

            if name not in groups:
                groups[name] = [values]
            else:
                groups[name].append(values)

        for key, group in groups.items():
            columns = []
            for values in group:
                for k in values.keys():
                    if k not in columns:
                        columns.append(k)
            if not len(columns):
                continue

            rows = []
            for values in group:
                row = OrderedDict.fromkeys(columns)
                for k, v in values.items():
                    if v is not None:
                        row[k] = v if isinstance(v, (int, float, str)) else str(v)
                rows.append(row)

            yield key, columns, rows


class CsvConverter(Converter):
    def convert(self, file):
        for key, columns, rows in self._parse(file):
            output_file = file.with_name("_".join([file.stem, key]) + ".csv")
            if output_file.exists() and not self.overwrite:
                warnings.warn(
                    f"file {output_file} exists. skipped. use -f to overwrite."
                )
                continue

            with output_file.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)


class XlsxConverter(Converter):
    def convert(self, file):
        output_file = file.with_suffix(".xlsx")
        if output_file.exists() and not self.overwrite:
            warnings.warn(f"file {output_file} exists. skipped. use -f to overwrite.")
            return

        try:
            from openpyxl.workbook import Workbook
        except ImportError:
            warnings.warn("xlsx conversion requires openpyxl to work", ImportWarning)
            sys.exit(1)

        workbook = Workbook()
        workbook.remove(workbook.active)
        for key, columns, rows in self._parse(file):
            worksheet = workbook.create_sheet(key)
            worksheet.append(columns)
            for row in rows:
                worksheet.append([*row.values()])

        workbook.save(output_file)


class ConverterFactory:
    @staticmethod
    def create(converter_kind: str, **kwargs) -> Converter:
        if converter_kind == "csv":
            converter = CsvConverter(**kwargs)
        elif converter_kind == "xlsx":
            converter = XlsxConverter(**kwargs)
        else:
            raise ValueError(f"unsupported converter {converter_kind}")

        return converter
