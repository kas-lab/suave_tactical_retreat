#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-suave-rebetmc:dev}"
SUAVE_REBETMC_WS="${2:-$HOME/ros_workspaces/suave_rebetmc_ws}"
SUAVE_REBETMC_WS_SRC="$SUAVE_REBETMC_WS/src"
SUAVE_REBETMC_WS_RESULTS="$SUAVE_REBETMC_WS/suave_results"

SUAVE_WS_CONTAINER="/home/ubuntu-user/suave_ws/"
SUAVE_WS_SRC_CONTAINER="/home/ubuntu-user/suave_ws/src"
SUAVE_RESULTS_CONTAINER="/home/ubuntu-user/suave/results"

# Packages to mount
AAL="$SUAVE_REBETMC_WS_SRC/aal"
ADAPT_X="$SUAVE_REBETMC_WS_SRC/adapt_x"
REBET_MONITORS="$SUAVE_REBETMC_WS_SRC/rebet_monitors"
ROS_MONITORS="$SUAVE_REBETMC_WS_SRC/ros_monitors"
ROS_TYPEDB="$SUAVE_REBETMC_WS_SRC/ros_typedb"
SUAVE="$SUAVE_REBETMC_WS_SRC/suave"
SUAVE_REBETMC="$SUAVE_REBETMC_WS_SRC/suave_rebetmc"
TYPEDB_TACTICS="$SUAVE_REBETMC_WS_SRC/typedb_tactics"

XAUTH=/tmp/.docker.xauth.$USER
touch "$XAUTH"
chmod 600 "$XAUTH"

xauth nlist "$DISPLAY" | sed -e 's/^..../ffff/' | xauth -f "$XAUTH" nmerge -

docker run -it --rm --name suave_rebetmc \
    --runtime=nvidia --gpus all \
    -e DISPLAY=$DISPLAY \
    -e XAUTHORITY=/tmp/.docker.xauth \
    -e QT_X11_NO_MITSHM=1 \
    -v "$XAUTH":/tmp/.docker.xauth:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v "$AAL":"$SUAVE_WS_SRC_CONTAINER/aal" \
    -v "$ADAPT_X":"$SUAVE_WS_SRC_CONTAINER/adapt_x" \
    -v "$REBET_MONITORS":"$SUAVE_WS_SRC_CONTAINER/rebet_monitors" \
    -v "$ROS_MONITORS":"$SUAVE_WS_SRC_CONTAINER/ros_monitors" \
    -v "$ROS_TYPEDB":"$SUAVE_WS_SRC_CONTAINER/ros_typedb" \
    -v "$SUAVE":"$SUAVE_WS_SRC_CONTAINER/suave" \
    -v "$SUAVE_REBETMC":"$SUAVE_WS_SRC_CONTAINER/suave_rebetmc" \
    -v "$TYPEDB_TACTICS":"$SUAVE_WS_SRC_CONTAINER/typedb_tactics" \
    -v "$SUAVE_REBETMC_WS_RESULTS":"$SUAVE_RESULTS_CONTAINER" \
    "$IMAGE" \
    bash
