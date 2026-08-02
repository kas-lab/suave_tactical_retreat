#!/usr/bin/env bash
# Copyright 2026 KAS-lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${script_dir}/install/setup.bash" ]]; then
  workspace_dir="${script_dir}"
else
  workspace_dir="$(cd -- "${script_dir}/../../.." && pwd)"
fi
ros_setup="/opt/ros/humble/setup.bash"
workspace_setup="${workspace_dir}/install/setup.bash"

if [[ ! -f "${ros_setup}" ]]; then
  echo "ROS 2 Humble setup not found: ${ros_setup}" >&2
  exit 1
fi

if [[ ! -f "${workspace_setup}" ]]; then
  echo "Workspace setup not found: ${workspace_setup}" >&2
  echo "Build the workspace before running this script." >&2
  exit 1
fi

source "${ros_setup}"
source "${workspace_setup}"

exec ros2 launch suave_rebetmc suave_runner.launch.py "$@"
