# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**suave_rebetmc** implements a managing system for the SUAVE AUV pipeline-inspection mission using the **RebetMC** framework. It combines:

- **TypeDB** as a knowledge base storing variability, requirements, context, ROS graph, and tactics models
- **typedb_tactics** to query and reason over the knowledge base at runtime and decide adaptations
- **adapt_x** as the adaptation execution layer
- **AAL** (Autonomous Adaptation Layer) for monitoring and actuation interfaces
- **ros_monitors** for runtime monitoring

The managed system is SUAVE (see `suave.repos` / the SUAVE CLAUDE.md). suave_rebetmc is the *managing subsystem* that plugs into SUAVE's `/task/request`, `/task/cancel`, and `system_modes` interfaces.

Runtime stack: ROS 2 Humble · TypeDB 2.29.1 · adapt_x · AAL · ros_monitors · ArduSub/ArduPilot SITL · Gazebo Harmonic · MAVROS · Docker.

## Repository Layout

| Path | Purpose |
|---|---|
| `suave_rebetmc/` | Python package (managing system node logic — currently early stage) |
| `models/tactical_retreat/` | **DSL source models** — edited by hand using rebetmc_eclipse_projs Eclipse plugins |
| `models/typedb/suave_tactics.tql` | Symlink → `src-gen/suave_tactics.tql`; TypeDB schema loaded at runtime |
| `models/interfaces/` | ROS interface descriptions (`.ros` files) — input to `ros2model` tool |
| `models/ros/` | ROS node descriptions (`.ros2` files) — input to `ros2model` tool |
| `models/system/suave.rossystem` | System model — input to `ros2model` tool |
| `src-gen/` | **Generated code** — do not edit by hand; regenerated from DSL files via Eclipse plugins |
| `test/` | ament lint tests (flake8, pep257, copyright) |
| `suave_rebetmc.repos` | VCS deps: suave, aal, adapt_x, ros_monitors, typedb_tactics |
| `Dockerfile` | Extends `suave-headless:dev`; adds TypeDB, Java 21, Maven, and the extra deps |

## Model Workflow

The files in `models/tactical_retreat/` are written in the Xtext DSLs defined by [rebetmc_eclipse_projs](https://github.com/kas-lab/rebetmc_eclipse_projs):

| File | DSL | Extension |
|---|---|---|
| `suave.context` | ContextModel | `.context` |
| `suave.var` | FeatureModel | `.var` |
| `suave.resolution` | ResolutionModel | `.resolution` |
| `suave.tactics` | Tactics | `.tactics` |

**To regenerate `src-gen/`**: open the models in the Eclipse IDE with the rebetmc plugins installed and run "Generate Artifacts" (or the matching MWE2 workflow). The key output is `src-gen/suave_tactics.tql`, the TypeDB schema that `typedb_tactics` loads at runtime.

`src-gen/` is committed and should not be hand-edited. `models/typedb/suave_tactics.tql` is a symlink to `src-gen/suave_tactics.tql`; Docker dereferences the symlink and copies the file content into the container.

The `models/interfaces/`, `models/ros/`, and `models/system/` files are inputs to `ros2model` (see `models/README.md`); their output also goes to `src-gen/`.

## Build & Test

Run build and test commands inside the `suave_rebetmc` container (built from `Dockerfile`). The workspace is at `/home/ubuntu-user/suave_ws`.

```bash
# Default exec pattern
docker exec suave_rebetmc bash -lc 'cd /home/ubuntu-user/suave_ws && source /opt/ros/humble/setup.bash && source install/setup.bash && <command>'

# Build all
colcon build --symlink-install

# Build this package only
colcon build --symlink-install --packages-select suave_rebetmc

# Lint tests
colcon test --packages-select suave_rebetmc --event-handlers console_direct+
colcon test-result --verbose

# Direct pytest
python3 -m pytest -q suave_rebetmc/test
```

**Mandatory before finishing:** always run `test_flake8` and `test_pep257` and ensure both pass.

## Docker

```bash
# Build
docker build --secret id=gh_token,src=<(gh auth token) -t suave-rebetmc:dev src/suave_rebetmc/

# Force fresh dep clone
docker build --secret id=gh_token,src=<(gh auth token) --build-arg DEPS_CACHE_BUSTER=$(date +%s) -t suave-rebetmc:dev src/suave_rebetmc/

# Syntax check only
docker build --check src/suave_rebetmc/
```

The Dockerfile extends `suave-headless:dev` and adds: TypeDB 2.29.1, Java 21 (`openjdk-21-jre`), Maven 3.9.16, `typedb-driver==2.29.7`, and the extra workspace deps via `suave_rebetmc.repos` + `vcs import --skip-existing`.

## Dependencies

| Dependency | Source | Role |
|---|---|---|
| `suave` + sub-packages | suave_rebetmc.repos | Managed system |
| `aal` / `aal_msgs` | AAL-ROS2 (branch `mc`) | Adaptation layer msgs |
| `adapt_x` / `adapt_x_msgs` | kas-lab/adapt_x | Adaptation execution |
| `ros_monitors` | kas-lab/ros_monitors | Runtime monitoring |
| `typedb_tactics` | kas-lab/typedb_tactics (branch `dev`) | TypeDB KB interface |

## ROS Interfaces

suave_rebetmc is a **managing subsystem** for SUAVE. It must interact with:
- **`/diagnostics`** — `diagnostic_msgs/DiagnosticArray`
- **`/task/request`** and **`/task/cancel`** — `suave_msgs/srv/Task`
- **system_modes** `ChangeMode` services: `/f_maintain_motion/change_mode`, `/f_generate_search_path/change_mode`, `/f_follow_pipeline/change_mode`

See the SUAVE CLAUDE.md for the full managing subsystem interface contract.

## Code Conventions

Follows the same conventions as the SUAVE Python packages:
- `ament_python`, `rclpy.node.Node` subclasses, `snake_case`, `PascalCase` classes
- Apache-2.0 header on all new Python files (Copyright 2026 KAS Lab)
- Single-line docstrings, flake8/pep257 clean
- `extras_require={'test': ['pytest']}` in `setup.py`

## Before Finishing Changes

- `colcon test --packages-select suave_rebetmc --event-handlers console_direct+` — lint must pass
- `python3 -m py_compile` for any new launch files
- `docker build --check src/suave_rebetmc/` after Dockerfile edits
- `bash -n <script>` for shell script changes
- Do not hand-edit `src-gen/`; regenerate via Eclipse instead
