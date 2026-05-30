# suave_rebetmc — tech stack and pinned versions

## Runtime
- ROS 2 Humble (from `suave-headless:dev` base image)
- TypeDB 2.28.3 (apt: `typedb=2.28.3`)
- typedb-driver (pip): 2.28.0
- Java 21 (`openjdk-21-jre`)
- Maven 3.9.16 (installed from Apache tarball at `/opt/apache-maven-3.9.16/`)
- Python 3.10 (Ubuntu 22.04 default)

## Base Docker image
`suave-headless:dev` — contains ROS 2 Humble, Gazebo Harmonic, ArduSub SITL, MAVROS, and the full SUAVE workspace pre-built at `/home/ubuntu-user/suave_ws`.

## Python package pinning (inherited from typedb_tactics)
- setuptools==75.8.2, packaging==24.1, empy==3.3.4
- pandas==2.0.2, scipy==1.15.2, numpy==1.23.5

## Model toolchain
- rebetmc_eclipse_projs — Eclipse/Xtext DSL plugins (Java 21, Xtext 2.42.0) that compile `.context/.var/.resolution/.tactics` → `src-gen/`
- ros2model — generates ROS graph models from `.ros`/`.ros2`/`.rossystem` files into `src-gen/`

See `mem:core`, `mem:model_workflow`.
