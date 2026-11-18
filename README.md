# Tactical Retreat on SUAVE

[![DOI](https://zenodo.org/badge/1233180965.svg)](https://doii.org/10.5281/zenodo.24326117)
[![Docker Images](https://github.com/kas-lab/suave_tactical_retreat/actions/workflows/container.yml/badge.svg?branch=main)](https://github.com/kas-lab/suave_tactical_retreat/actions/workflows/container.yml)

This repository applies **Tactical Retreat** to [SUAVE](https://github.com/kas-lab/suave), an exemplar of an autonomous underwater vehicle (AUV) that inspects pipelines. It contains the models, configuration, launch files and experiment setup used to evaluate the paper *Tactical Retreat: Leveraging Runtime Models for Robotics
Self-Adaptation*.

## Contents

- [How it works](#how-it-works)
- [Models](#models)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [Run one mission](#run-one-mission)
- [Run the paper experiments](#run-the-paper-experiments)
- [SUAVE runner](#suave-runner)
- [Development](#development)
- [Citation](#citation)
- [License](#license)

## How it works

SUAVE has to find a pipeline on the seabed (`spiral_search`) and then follow it
(`follow_pipeline`), while the water visibility changes and thrusters fail.
Tactical Retreat adapts the vehicle at runtime:

| Component | Package | Role |
|---|---|---|
| Runtime-model node (`tactical_retreat_kb`) | `tactical_retreat_kb` | Loads the models in [`models/tactical_retreat/`](models/tactical_retreat/), tracks the context from ROS topics, evaluates requirements and tactic guards, and computes reconfiguration plans |
| Adaptation proxies | `adapt_x` | Stand between the mission and SUAVE's `spiral_search` and `follow_pipeline` actions. While a task runs, they apply the tactics whose guards hold |
| Adaptation layer | `aal` | Carries out the reconfiguration plans on the ROS system |
| Mission | `suave_tactical_retreat` | Behavior tree (`suave_tactical_retreat_bt`) that sends the mission tasks to the proxies |

For example, the tactic below starts motion recovery during `follow_pipeline`
when the `ThrustersOperational` requirement is violated:

```text
ThrustersOperational FollowPipeline {
rule start_recover_motion_2 {
    guard {
        context(operational_thrusters_delta > 0.0)
        features(!selected(suave_resolution.RECOVER_MOTION))
    }
    action {
        select_variant(suave_resolution.RECOVER_MOTION)
    }
};
}
```

## Models

The runtime models are xtext files, written in Xtext DSLs. The node reads them
when it starts:

| File | Contents |
|---|---|
| [`suave.context`](models/tactical_retreat/suave.context) | Context variables, such as water visibility, battery level and failed thrusters, and the ROS topics they come from |
| [`suave.var`](models/tactical_retreat/suave.var) | Feature model of the vehicle's variability |
| [`suave.resolution`](models/tactical_retreat/suave.resolution) | How each feature maps onto the ROS system (nodes, modes, parameters) |
| [`suave.reqs`](models/tactical_retreat/suave.reqs) | Requirements with relaxed fulfillment functions |
| [`suave.tactics`](models/tactical_retreat/suave.tactics) | Tactics: guarded rules, per task, that select or unselect features |
| [`models/interfaces/`](models/interfaces/), [`models/ros/`](models/ros/), [`models/system/`](models/system/) | ROS interfaces, nodes and the system model |

The node's configuration, [`config/xtext_kb_config.yaml`](config/xtext_kb_config.yaml) lists which model files it loads.

## Requirements

- Docker. If you want to run with graphical display enable by a NVIDIA GPU,
also install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/)
- The [SUAVE CLI](https://github.com/kas-lab/suave/tree/main/suave_cli). It is plain Python 3.10+ and needs no ROS on the host.

## Quick start

1. Get the SUAVE CLI and put it on `PATH`:

   ```bash
   git clone --branch v1.6.0 https://github.com/kas-lab/suave.git
   source suave/env.sh        # add this to ~/.bashrc to make it permanent
   ```

2. Start the container in the background:

   ```bash
   suave docker run --image ghcr.io/kas-lab/suave-tactical-retreat:main --no-mount-src --yes
   ```

   Without an NVIDIA GPU, add `--gpu none`. The CLI forwards your display to the
   container, so you do not need `xhost +`. On the host, results appear in
   `~/suave/results`.

3. Open a shell in the container. ROS and the workspace are already sourced:

   ```bash
   suave docker shell
   ```

When you are done, run `suave docker stop`.

The container is named `suave`. To use another name, pass `--container NAME`
to every `suave` command. See the
[SUAVE CLI guide](https://github.com/kas-lab/suave/blob/main/suave_cli/README.md)
for all options.

## Run one mission

Run each of these commands in its own terminal, each opened with
`suave docker shell`:

1. Start ArduSub SITL:

   ```bash
   sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --console
   ```

2. Start the Gazebo simulation:

   ```bash
   ros2 launch suave simulation.launch.py x:=-17.0 y:=2.0
   ```

3. Wait until SITL and the simulation are ready, then start SUAVE with
   Tactical Retreat:

   ```bash
   ros2 launch suave_tactical_retreat xtext_suave_tactical_retreat_bringup.launch.py
   ```

## Run the paper experiments

The SUAVE runner starts and stops SITL, the simulation and the managing system
for every run. It also injects perturbations and writes one result folder per
campaign. It runs Tactical Retreat and the baselines (ROSA, BT,
Metacontrol, random and no adaptation) 30 times each. Run it the batch with:

Get and source the suave CLI:

```bash
git clone --branch v1.6.0 https://github.com/kas-lab/suave.git
source suave/env.sh        # add this to ~/.bashrc to make it permanent
```

Start the `suave` container:

```bash
suave docker run --image ghcr.io/kas-lab/suave-tactical-retreat:main --no-mount-src --yes
```

This command starts a container in the background without mounting the suave repo
you just cloned. If you omit `--no-mount-src` the suave repo will be mounted in the container.


Then run the experiments:

```bash
suave batch start --config src/suave_tactical_retreat/config/runner/batch_campaigns.yml
```

[!> [!NOTE]
> The experiments take around 14 hours to run. We suggest running it in a detachable terminal session like tmux or screen to run the experiments in the background: `screen -dmS suave suave batch start --config src/suave_tactical_retreat/config/runner/batch_campaigns.yml`. Then to resume the session `screen -r suave` ]

Configuration paths are resolved inside the container, from the workspace root
`/home/ubuntu-user/suave_ws`. Add `--gui` to see Gazebo during a campaign.

You can inspect the batches performed with:

```bash
suave batch list
```

In case you have to stop the execution an experiment batch or if the computer 
crashes you can safely resume a batch with:

```bash
suave batch resume --latest
```

To analyze the results, use `suave analyze` (for example
`suave analyze summarize -- --help`). See
[SUAVE: results](https://github.com/kas-lab/suave/blob/main/docs/source/results.md).

If you rather not use the `suave cli` you can run it directly with docker (no dependencies):

```bash
docker run -v /etc/localtime:/etc/localtime:ro -v "$HOME/suave/results:/home/ubuntu-user/suave/results" ghcr.io/kas-lab/suave-tactical-retreat:main suave batch start --config src/suave_tactical_retreat/config/runner/batch_campaigns.yml
```

## SUAVE runner

You can also run the SUAVE runner directly:

```bash
ros2 run suave_runner suave_runner \
  --ros-args \
  -p gui:=False \
  -p experiment_logging:=True \
  -p experiments:='[
    "{\"experiment_launch\": \"ros2 launch suave_tactical_retreat xtext_suave_tactical_retreat_bringup.launch.py\", \
      \"num_runs\": 2, \
      \"adaptation_manager\": \"tactical_retreat\", \
      \"mission_name\": \"suave\"}"
  ]'
```

## Development

To change this package, mount your checkout into the container and rebuild it:

```bash
git clone https://github.com/kas-lab/suave_tactical_retreat.git
suave docker run --image ghcr.io/kas-lab/suave-tactical-retreat:main --no-mount-src \
  --mount "$PWD/suave_tactical_retreat" --recreate --yes
suave build suave_tactical_retreat
suave test suave_tactical_retreat
```

`suave build` runs `colcon build --symlink-install`. Run it again after you
change launch files, configuration or models.

To build the image yourself, from the root of this repository:

```bash
docker build -t suave-tactical-retreat:dev .
suave docker run --image suave-tactical-retreat:dev --no-mount-src --recreate
```

To edit the models with syntax checking and validation, use the Eclipse
plugins from
[rebetmc_eclipse_projs](https://github.com/kas-lab/rebetmc_eclipse_projs).

## Citation

If you use this work, please cite:

*Tactical Retreat: Leveraging Runtime Models for Robotics Self-Adaptation.*

## License

[Apache License 2.0](LICENSE).
