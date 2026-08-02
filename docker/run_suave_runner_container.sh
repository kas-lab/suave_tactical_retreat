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

set -euo pipefail

IMAGE="${1:-suave-rebetmc:dev}"
SUAVE_REBETMC_WS="${2:-$HOME/ros_workspaces/suave_rebetmc_ws}"
SUAVE_REBETMC_WS_RESULTS="$SUAVE_REBETMC_WS/suave_results"
SUAVE_RESULTS_CONTAINER="/home/ubuntu-user/suave/results"

mkdir -p "$SUAVE_REBETMC_WS_RESULTS"

docker run -it --rm --name suave_rebetmc \
  -v "$SUAVE_REBETMC_WS_RESULTS":"$SUAVE_RESULTS_CONTAINER" \
  "$IMAGE" \
  ./run_suave_runner.sh "${@:3}"
