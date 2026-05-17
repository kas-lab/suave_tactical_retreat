# Ros2Model

```bash
ros2 model node -o models/ros --include-description
```

```bash
ros2 model system -o models/ros/system/suave --include-description
```

ros2 model system -o test5/system/system --include-description

```bash
ros2 model msg -p std_msgs -p std_srvs -p geographic_msgs -p sensor_msgs -p tf2_msgs -p geometry_msgs -p suave_msgs -p mavros_msgs -p system_modes_msgs -p diagnostic_msgs -p builtin_interfaces -p lifecycle_msgs -p unique_identifier_msgs -p rcl_interfaces -p nav_msgs -o models/interfaces
```

```bash
ros2 model msg -p nav_msgs -o models/interfaces
```

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/gus/ros_workspaces/suave_rebetmc_ws/venv/bin/python -m colcon test \
    --event-handlers console_cohesion+ \
    --packages-select ros2model
```