# AGENTS.md

Guidance for coding agents working in this repository. This is the canonical
agent guide for the package; `CLAUDE.md` only imports this file.

## Project Overview

**suave_tactical_retreat** is the managing subsystem for the SUAVE AUV
pipeline-inspection mission, built on the **Tactical Retreat** framework. The
managed system is SUAVE; this package drives it through standard ROS 2
interfaces.

The active workflow is **Xtext-based and does not use TypeDB**:

- The Xtext DSL models in `models/tactical_retreat/` (plus the `ros2model`
  models) are loaded in memory through JPype/EMF by the `tactical_retreat_kb`
  lifecycle node (`typedb_tactics` package, `tactical_retreat` executable,
  backed by `tactical_retreat_kb_xtext.py` / `xtext_tactical_retreat_interface.py`).
  No TypeDB server is started or required.
- `adapt_x` adaptation proxies intercept the mission actions and query the KB
  for tactics/adaptation plans.
- AAL (`aal` `adaptation_layer`) executes the resulting reconfigurations.
- `ros_monitors` provide runtime measurements.

Runtime stack: ROS 2 Humble · Java 21 / JPype / Xtext / EMF · adapt_x · AAL ·
ros_monitors · ArduSub/ArduPilot SITL · Gazebo Harmonic · MAVROS · Docker.

## Xtext Launch Workflow

Entry point (also used by `config/runner/runner_config.yml`):

```bash
ros2 launch suave_tactical_retreat xtext_suave_tactical_retreat_bringup.launch.py
```

Launch chain:

```
xtext_suave_tactical_retreat_bringup.launch.py
├── suave_base (suave_base package)        managed system; use_action_server:=true
├── xtext_adaptation_engine_with_aal.launch.py
│   ├── aal/adaptation_layer
│   ├── adapt_x/adaptation_proxy  spiral_search_adaptation_proxy    (configured)
│   ├── adapt_x/adaptation_proxy  follow_pipeline_adaptation_proxy  (configured)
│   └── xtext_adaptation_engine.launch.py
│       └── typedb_tactics/tactical_retreat  node: tactical_retreat_kb
│           params: config/xtext_kb_config.yaml  (configure + activate)
└── suave_tactical_retreat_bt  node: mission_node
    started only after tactical_retreat_kb reaches the `active` state
```

- `mission_node` sends actions to `proxy_spiral_search` / `proxy_follow_pipeline`
  (the proxies), not directly to SUAVE.
- Proxy parameters live in `config/adaptation_proxies_config.yaml`
  (`adaptation_strategy: "tactic"`, `system_name: "suave_resolution"`). The
  `recover_thrusters` and `recharge_battery` proxies are currently commented out
  in the launch file.
- `config/xtext_kb_config.yaml` lists the model files for `/tactical_retreat_kb`
  (`context_path`, `var_path`, `resolution_path`, `tactics_path`, `reqs_path`,
  `ros_path`, `ros2_path`, `rossystem_path`). `ReplaceString` substitutes
  `<suave_tactical_retreat_models_dir>` with
  `share/suave_tactical_retreat/models` at launch time.
- Bringup arguments: `silent`, `result_path`, `result_filename`,
  `mission_config`, `record_bags`, `bag_output_path`.

## Legacy TypeDB Path (not used)

These files belong to the older TypeDB/`adapt_x` setup-node workflow. Keep them
unless asked to remove them, but do not extend them or base new work on them:

- `launch/suave_tactical_retreat_bringup.launch.py`
- `launch/adaptation_engine.launch.py`, `launch/adaptation_engine_with_aal.launch.py`,
  `launch/adaptation_engine_with_execution_layer_launch.py`
- `config/adaptation_engine_config.yaml`
- `models/typedb/suave_tactical_retreat.tql`
- `test/test_suave_tactics_kb.py` (CTest name `test_suave_tactics_kb`; needs a
  TypeDB server on `localhost:1729`)

When a task touches launch, config, or models, edit the `xtext_*` launch files
and `config/xtext_kb_config.yaml`.

## Repository Layout

```
models/tactical_retreat/   Xtext DSL source models (rebetmc_eclipse_projs DSLs)
  suave.context            ContextModel DSL
  suave.var                FeatureModel DSL
  suave.resolution         ResolutionModel DSL
  suave.tactics            Tactics DSL
  suave.reqs               Requirements DSL
models/interfaces/         ROS interface models (.ros, from ros2model)
models/ros/                ROS node models (.ros2, from ros2model)
models/system/             System model (suave.rossystem, from ros2model)
models/typedb/             LEGACY TypeDB schema, not used by the Xtext workflow
models/paper/, models/tmp/ Scratch/paper model variants, not loaded at runtime
launch/xtext_*.launch.py   Active Xtext launch chain (see above)
config/xtext_kb_config.yaml          KB model paths
config/adaptation_proxies_config.yaml  adapt_x proxy parameters
config/mission/, config/runner/      Experiment mission and runner configs
bts/                       BehaviorTree.CPP XML trees installed to share/suave_tactical_retreat/bts
src/                       C++ BehaviorTree runner sources (suave_tactical_retreat_bt)
suave_tactical_retreat/    Python package
scripts/run_suave_runner.sh  Experiment runner wrapper
CMakeLists.txt             Hybrid ament_cmake/ament_cmake_python build
suave_tactical_retreat.repos  VCS deps: suave, aal, adapt_x, ros_monitors, typedb_tactics, rebet*, rosa, ros_pytest
Dockerfile                 Extends ghcr.io/kas-lab/suave-headless
```

## Dependencies And Environment

- ROS 2 Humble and the full SUAVE stack (ArduPilot, Gazebo Harmonic, MAVROS),
  inherited from the `suave-headless` base image
- Java 21 JDK (`JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64`), Maven 3.9.16, `jpype1`
- adapt_x, aal, ros_monitors, typedb_tactics (Xtext KB node; the package name is historical)
- No TypeDB server or `typedb-driver` is needed for the Xtext workflow

## Build And Test Commands

Run inside the container (`suave_tactical_retreat`). Workspace: `/home/ubuntu-user/suave_ws`.

```bash
docker exec suave_tactical_retreat bash -lc 'cd /home/ubuntu-user/suave_ws && source /opt/ros/humble/setup.bash && source install/setup.bash && <command>'

colcon build --symlink-install
colcon build --symlink-install --packages-select suave_tactical_retreat
colcon test --packages-select suave_tactical_retreat --event-handlers console_direct+ --ctest-args -E '^test_suave_tactics_kb$'
colcon test-result --verbose
ros2 pkg executables suave_tactical_retreat
```

Always exclude the legacy `test_suave_tactics_kb` test (its `typedb` label is
commented out in CMake, so exclude it by name). From the host workspace,
`python3 scripts/focused_test.py --package suave_tactical_retreat` excludes it
for you and checks test exit codes; `--with-typedb` includes it again. The
wrapper does not build, so rebuild interfaces, C++ targets and installed assets
first.

Focused adapt_x tests that need ROS/JVM dependencies should be run in the
running `suave_tactical_retreat` container:

```bash
python3 scripts/focused_test.py --test src/adapt_x/adapt_x/test/test_aal_failures.py
```

**Mandatory lint gate:** before marking work complete, run `test_flake8`,
`test_pep257`, and `test_copyright` and make sure all pass. Run
`python3 -m py_compile` on any changed launch files.

For local verification in this workspace, prefer the system CMake and writable
ccache dirs if the sandboxed environment selects `/home/gus/.local/bin/cmake` or
ccache tries to write under read-only paths:

```bash
export PATH=/usr/bin:$PATH
export CCACHE_TEMPDIR=/tmp/ccache-tmp
export CCACHE_DIR=/tmp/ccache
```

## Docker

```bash
docker build -t suave-tactical-retreat:dev src/suave_rebetmc/
docker build --build-arg DEPS_CACHE_BUSTER=$(date +%s) -t suave-tactical-retreat:dev src/suave_rebetmc/
docker build --check src/suave_rebetmc/
```

## Model Rules

- `.context`, `.var`, `.resolution`, `.tactics`, and `.reqs` files are written
  in the [rebetmc_eclipse_projs](https://github.com/kas-lab/rebetmc_eclipse_projs)
  Xtext DSLs. Edit them by hand or in Eclipse with those plugins; the KB node
  parses them directly at runtime, so no generation step is needed.
- `models/interfaces/`, `models/ros/`, and `models/system/` are produced by
  `ros2model` (see `models/README.md`). Regenerate them rather than hand-editing
  large sections.
- Every model file the KB should load must be listed in
  `config/xtext_kb_config.yaml` under `<suave_tactical_retreat_models_dir>`:
  - `.ros` files: `models/interfaces/`
  - `.ros2` files: `models/ros/`
  - `.rossystem` files: `models/system/`
  - `.context`, `.var`, `.resolution`, `.tactics`, `.reqs`: `models/tactical_retreat/`
- CMake, not `setup.py`, owns package installation. Keep `config`, `launch`,
  `models`, and `bts` installed under `share/suave_tactical_retreat`.

## Behavior Tree Runner

- `suave_tactical_retreat_bt` loads `share/suave_tactical_retreat/bts/suave.xml`.
- Reuse mission action/condition nodes from `suave_bt`; do not duplicate those BT node implementations in this package.
- Do not add `ChangeMode` or `previous_modes` blackboard wiring unless a future tree actually uses them.
- `EnsureConfiguration` comes from `aal_bt`. Because `aal_bt` currently exports a CMake library path that may not resolve with `find_package(aal_bt)`, `suave_tactical_retreat_bt` loads the installed BT plugin at runtime from `share/aal_bt/bt_plugins/libaal_bt_nodes.so`. Keep `aal_bt` as a package dependency in `package.xml`.

## adapt_x / JPype Runtime Notes

- JPype Java package imports require `import jpype.imports` before statements like `from org.ros2.rcljava.rebet_java import RosToolingSupport`.
- Add `share/adapt_x/jars/rem/*` to the JPype classpath before starting/importing Java classes. The `rebet_java.jar` contains `org/ros2/rcljava/rebet_java/RosToolingSupport.class`.
- Loading FeatureIDE/Rhea-backed models needs EMF package initialization, not just JAR presence:
  - `AdvancedConstraintsFMmetamodelPackage.eINSTANCE.eClass()`
  - `BasicFMmetamodelPackage.eINSTANCE.eClass()`
- `Resource` from `org.eclipse.emf.ecore.resource` is a Java interface; do not instantiate it. When a Java overload requires a `Resource`, pass an existing EMF resource such as `self.tacticsModelResource`.
- A valid `.reqs` file can be minimal, e.g. `REQ1, Safety: "Placeholder requirement.", true`, but placeholder requirements should be replaced with real SUAVE requirements.
- Do not assume APIs from other branches exist. Check the active source before
  using helpers, and prefer isolated tests over constructing the full
  `AdaptationEngine`.

## ROS Managing Subsystem Interface

Must interact with:
- `/diagnostics` (`diagnostic_msgs/DiagnosticArray`)
- `/task/request`, `/task/cancel` (`suave_msgs/srv/Task`)
- `ChangeMode` services: `/f_maintain_motion/change_mode`, `/f_generate_search_path/change_mode`, `/f_follow_pipeline/change_mode`

## Coding Style

- Hybrid package: `ament_cmake` + `ament_cmake_python`; do not reintroduce `setup.py`.
- Python: `rclpy.node.Node`, `snake_case`, `PascalCase` classes.
- C++: C++17, ROS 2 style, `ament_target_dependencies`.
- Apache-2.0 header with `Copyright 2026 KAS-lab` on new C++ and Python files.
- Single-line docstrings where appropriate; keep flake8/pep257/copyright clean.
