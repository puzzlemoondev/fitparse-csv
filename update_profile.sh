#!/usr/bin/env bash

set -euo pipefail

package_path=$(find .venv -type d -name fitparse | tail -n 1)
if [ -z "$package_path" ]; then
  echo "fitparse package not found"
  exit 1
fi
echo "Found fitparse package at $package_path"

echo "Updating fitparse package..."

profile_path="./profile"
if [ ! -d "$profile_path" ]; then
  echo "Profile directory not found"
  exit 1
fi

latest_profile=$(find "$profile_path" -depth 1 -type d -exec basename {} \; | sort -V | tail -n 1)
echo "Latest profile: $latest_profile"

cp "$profile_path/$latest_profile/profile.py" "$package_path/profile.py"
echo "Done!"
