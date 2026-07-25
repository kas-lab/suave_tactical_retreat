# suave_rebetmc

## Run SUAVE + rebetmc

```Bash
sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --console
```

```bash
ros2 launch suave simulation.launch.py x:=-17.0 y:=2.0
```

```bash
ros2 launch suave_rebetmc suave_rebetmc_bringup.launch.py
```

## Docker

### Build

To build the img you need to create a github personal access token to read access to private repos, then log in to gh with gh cli

```Bash
gh auth login
```

```Bash
docker build --secret id=gh_token,src=<(gh auth token) -t suave-rebetmc:dev .
```

### Run

```Bash
xhost +
```

The commands below assume you are running them from the workspace root, so `"$PWD/src/..."` points to the local packages:

```Bash
cd <workspace_root>
```

Choose the smallest command that matches your use case:
<!-- - plain container if you only need `typedb_tactics` -->
<!-- - NVIDIA variant if you need GPU support -->
<!-- - extra mounts if you are editing `ros_monitors` or `ros_typedb` together with this package -->

Start container in the background with typedb server running:

From <workspace_root>:

```Bash
docker run -d --rm --name suave_rebetmc --runtime=nvidia --gpus all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /etc/localtime:/etc/localtime:ro -v "$PWD/src/suave_rebetmc:/home/ubuntu-user/suave_ws/src/suave_rebetmc" suave-rebetmc:dev typedb server
```

Mounting ros_typedb

```Bash
docker run -d --rm --name suave_rebetmc --runtime=nvidia --gpus all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /etc/localtime:/etc/localtime:ro -v "$PWD/src/suave_rebetmc:/home/ubuntu-user/suave_ws/src/suave_rebetmc" -v "$PWD/src/ros_typedb:/home/ubuntu-user/suave_ws/src/ros_typedb" -v "$PWD/src/typedb_tactics:/home/ubuntu-user/suave_ws/src/typedb_tactics" suave-rebetmc:dev typedb server
```

Mounting adapt_x

```Bash
docker run -d --rm --name suave_rebetmc --runtime=nvidia --gpus all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /etc/localtime:/etc/localtime:ro -v "$PWD/src/suave_rebetmc:/home/ubuntu-user/suave_ws/src/suave_rebetmc" -v "$PWD/src/adapt_x:/home/ubuntu-user/suave_ws/src/adapt_x" -v "$PWD/src/typedb_tactics:/home/ubuntu-user/suave_ws/src/typedb_tactics" suave-rebetmc:dev typedb server
```

From pkg root:

```Bash
docker run -d --rm --name suave_rebetmc --runtime=nvidia --gpus all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /etc/localtime:/etc/localtime:ro -v "$PWD:/home/ubuntu-user/suave_ws/src/suave_rebetmc" suave-rebetmc:dev typedb server
```

Mounting suave_rebetm + typedb_tactics + adapt_x + rebet_monitors

```Bash
docker run -d --rm --name suave_rebetmc --runtime=nvidia --gpus all -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /etc/localtime:/etc/localtime:ro -v "$PWD/src/suave_rebetmc:/home/ubuntu-user/suave_ws/src/suave_rebetmc" -v "$PWD/src/adapt_x:/home/ubuntu-user/suave_ws/src/adapt_x" -v "$PWD/src/typedb_tactics:/home/ubuntu-user/suave_ws/src/typedb_tactics" -v "$PWD/src/rebet_monitors:/home/ubuntu-user/suave_ws/src/rebet_monitors" -v "$PWD/src/aal:/home/ubuntu-user/suave_ws/src/aal" suave-rebetmc:dev typedb server
```

## Tests

```Bash
docker exec suave_rebetmc bash -lc '
  cd /home/ubuntu-user/suave_ws &&
  source /opt/ros/humble/setup.bash &&
  source install/setup.bash &&
  colcon test --event-handlers console_direct+ --packages-select suave_rebetmc --pytest-args -k test_suave_tactics_kb
'
```

## Runner

```Bash
ros2 run suave_runner suave_runner \
  --ros-args \
  -p gui:=False \
  -p experiment_logging:=True \
  -p experiments:='[
    "{\"experiment_launch\": \"ros2 launch suave_rebetmc suave_rebetmc_bringup.launch.py\", \
      \"num_runs\": 2, \
      \"adaptation_manager\": \"rebetmc\", \
      \"mission_name\": \"suave\"}"
  ]'
```
