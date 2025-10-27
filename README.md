# fitparse-csv

Simple `.FIT` to csv/xlsx converter using [python-fitparse](https://github.com/dtcooper/python-fitparse).

## Usage

```shell
usage: fitparse-csv [-h] [-t {csv,xlsx}] [-r] [-f] dir

fitparse csv converter

positional arguments:
  dir                   directory where the fit files are stored

optional arguments:
  -h, --help            show this help message and exit
  -t {csv,xlsx}, --type {csv,xlsx}
                        file type to output (default: xlsx)
  -r, --remove-unknown  remove unknown fields
  -f, --force           force mode. overwrites existing files
```

## Installation

```bash
uv run fitparse_csv --help
```

### Update fitparse profile

You can run `./update_profile.sh` to update sdk profile if needed.
