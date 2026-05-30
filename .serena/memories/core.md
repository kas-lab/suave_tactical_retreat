# suave_rebetmc — core overview

**suave_rebetmc** is a managing system for the SUAVE AUV pipeline-inspection mission (search → follow → inspect pipeline).

It is the *managing subsystem* that plugs into SUAVE's standard ROS 2 adaptation interfaces. The knowledge-base approach uses TypeDB to store variability, requirements, context, ROS graph, and tactics models, then queries them at runtime via `typedb_tactics` to decide when and how to adapt SUAVE.

## Key packages in the workspace (from suave_rebetmc.repos)
- `suave` — managed system (AUV mission)
- `aal` / `aal_msgs` — Autonomous Adaptation Layer (branch `mc`)
- `adapt_x` / `adapt_x_msgs` — adaptation execution framework
- `ros_monitors` — runtime monitors
- `typedb_tactics` (branch `dev`) — TypeDB KB interface and ROS node

## Workspace inside container
`/home/ubuntu-user/suave_ws` — built with `colcon build --symlink-install`, sourced in `.bashrc`.

See `mem:tech_stack`, `mem:model_workflow`, `mem:suggested_commands`.
