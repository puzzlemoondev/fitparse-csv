# /// script
# dependencies = [
#     "packaging",
# ]
# ///
import shutil
from pathlib import Path

from packaging.version import Version


def find_fitparse_package(path: Path):
    if path.is_dir():
        if path.name == "fitparse":
            return path
        for child in path.iterdir():
            found = find_fitparse_package(child)
            if found:
                return found


venv_path = Path(".venv").resolve(strict=True)
package_path = find_fitparse_package(venv_path)
if package_path is None:
    print("fitparse package not found")
    raise FileNotFoundError
print(f"Found fitparse package at {package_path}")

print("Updating fitparse package...")

versioned_profile_path = sorted(
    Path("./profile").iterdir(), key=lambda p: Version(p.name)
)[-1]
if not versioned_profile_path.is_dir():
    print("Profile not found")
    raise FileNotFoundError
print(f"Latest profile: {versioned_profile_path.name}")

latest_profile_path = versioned_profile_path.joinpath("profile.py").resolve(strict=True)
package_profile_path = package_path.joinpath("profile.py")
print(f"Copying {latest_profile_path} to {package_profile_path}")
shutil.copy(latest_profile_path, package_profile_path)
print("Done!")
