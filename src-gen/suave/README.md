# suave

This package has be created automatically using the [RosTooling](https://github.com/ipa320/RosTooling).


It holds the launch file to run the following nodes:
- /suave_runner_node
- /gz_pipe_pose_bridge
- /gz_bluerov_pose_bridge
- /mavros/mavros_node
- /mavros/mavros_router
- /mavros/mavros
- /mavros/cmd
- /mavros/local_position
- /mavros/param
- /mavros/setpoint_position
- /mavros/sys
- /mavros/time
- /water_visibility_observer_node
- /battery_monitor
- /detect_pipeline
- /thruster_monitor
- /f_generate_search_path_node
- /f_follow_pipeline_node
- /generate_recharge_path_node
- /f_maintain_motion_node
- /mission_metrics
- /mission_node

The listed nodes offer the following connections:
- Publisher: model/min_pipes_pipeline/pose [geometry_msgs/PoseArray]
- Subscriber: sub_model/min_pipes_pipeline/pose [geometry_msgs/PoseArray]
- Publisher: model/bluerov2/pose [geometry_msgs/Pose]
- Subscriber: sub_model/bluerov2/pose [geometry_msgs/Pose]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- Publisher: uas1/mavlink_source [mavros_msgs/Mavlink]
- Subscriber: uas1/mavlink_sink [mavros_msgs/Mavlink]
- ServiceServer: mavros_router/add_endpoint [mavros_msgs/EndpointAdd]
- ServiceServer: mavros_router/del_endpoint [mavros_msgs/EndpointDel]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- Publisher: tf [tf2_msgs/TFMessage]
- Publisher: tf_static [tf2_msgs/TFMessage]
- Publisher: uas1/mavlink_sink [mavros_msgs/Mavlink]
- Subscriber: uas1/mavlink_source [mavros_msgs/Mavlink]
- ServiceServer: cmd/arming [mavros_msgs/CommandBool]
- ServiceServer: cmd/command [mavros_msgs/CommandLong]
- ServiceServer: cmd/command_int [mavros_msgs/CommandInt]
- ServiceServer: cmd/land [mavros_msgs/CommandTOL]
- ServiceServer: cmd/land_local [mavros_msgs/CommandTOLLocal]
- ServiceServer: cmd/set_home [mavros_msgs/CommandHome]
- ServiceServer: cmd/takeoff [mavros_msgs/CommandTOL]
- ServiceServer: cmd/takeoff_local [mavros_msgs/CommandTOLLocal]
- ServiceServer: cmd/trigger_control [mavros_msgs/CommandTriggerControl]
- ServiceServer: cmd/trigger_interval [mavros_msgs/CommandTriggerInterval]
- ServiceServer: cmd/vtol_transition [mavros_msgs/CommandVtolTransition]
- Publisher: local_position/accel [geometry_msgs/AccelWithCovarianceStamped]
- Publisher: local_position/odom [nav_msgs/Odometry]
- Publisher: local_position/pose [geometry_msgs/PoseStamped]
- Publisher: local_position/pose_cov [geometry_msgs/PoseWithCovarianceStamped]
- Publisher: local_position/velocity_body [geometry_msgs/TwistStamped]
- Publisher: local_position/velocity_body_cov [geometry_msgs/TwistWithCovarianceStamped]
- Publisher: local_position/velocity_local [geometry_msgs/TwistStamped]
- Publisher: param/event [mavros_msgs/ParamEvent]
- ServiceServer: param/pull [mavros_msgs/ParamPull]
- ServiceServer: param/set [mavros_msgs/ParamSetV2]
- Subscriber: global_position/global [sensor_msgs/NavSatFix]
- Subscriber: local_position/pose [geometry_msgs/PoseStamped]
- Subscriber: setpoint_position/global [geographic_msgs/GeoPoseStamped]
- Subscriber: setpoint_position/global_to_local [geographic_msgs/GeoPoseStamped]
- Subscriber: setpoint_position/local [geometry_msgs/PoseStamped]
- Publisher: battery [sensor_msgs/BatteryState]
- Publisher: estimator_status [mavros_msgs/EstimatorStatus]
- Publisher: extended_state [mavros_msgs/ExtendedState]
- Publisher: state [mavros_msgs/State]
- Publisher: status_event [mavros_msgs/StatusEvent]
- Publisher: statustext/recv [mavros_msgs/StatusText]
- Publisher: sys_status [mavros_msgs/SysStatus]
- Subscriber: statustext/send [mavros_msgs/StatusText]
- ServiceServer: set_message_interval [mavros_msgs/MessageInterval]
- ServiceServer: set_mode [mavros_msgs/SetMode]
- ServiceServer: set_stream_rate [mavros_msgs/StreamRate]
- ServiceServer: vehicle_info_get [mavros_msgs/VehicleInfoGet]
- Publisher: time_reference [sensor_msgs/TimeReference]
- Publisher: timesync_status [mavros_msgs/TimesyncStatus]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- Publisher: battery_monitor/recharge/complete [std_msgs/Bool]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- ServiceServer: battery_monitor/recharge [std_srvs/Trigger]
- Publisher: pipeline/detected [std_msgs/Bool]
- Subscriber: diagnostics [diagnostic_msgs/DiagnosticArray]
- Subscriber: model/bluerov2/pose [geometry_msgs/Pose]
- ServiceServer: pipeline/get_path [suave_msgs/GetPath]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- Publisher: f_generate_search_path_node/transition_event [lifecycle_msgs/TransitionEvent]
- ServiceServer: f_generate_search_path_node/change_state [lifecycle_msgs/ChangeState]
- ServiceServer: f_generate_search_path_node/get_available_states [lifecycle_msgs/GetAvailableStates]
- ServiceServer: f_generate_search_path_node/get_available_transitions [lifecycle_msgs/GetAvailableTransitions]
- ServiceServer: f_generate_search_path_node/get_state [lifecycle_msgs/GetState]
- ServiceServer: f_generate_search_path_node/get_transition_graph [lifecycle_msgs/GetAvailableTransitions]
- Publisher: pipeline/distance_inspected [std_msgs/Float32]
- Publisher: pipeline/inspected [std_msgs/Bool]
- Publisher: f_follow_pipeline_node/transition_event [lifecycle_msgs/TransitionEvent]
- ServiceServer: f_follow_pipeline_node/change_state [lifecycle_msgs/ChangeState]
- ServiceServer: f_follow_pipeline_node/get_available_states [lifecycle_msgs/GetAvailableStates]
- ServiceServer: f_follow_pipeline_node/get_available_transitions [lifecycle_msgs/GetAvailableTransitions]
- ServiceServer: f_follow_pipeline_node/get_state [lifecycle_msgs/GetState]
- ServiceServer: f_follow_pipeline_node/get_transition_graph [lifecycle_msgs/GetAvailableTransitions]
- Publisher: generate_recharge_path_node/transition_event [lifecycle_msgs/TransitionEvent]
- ServiceServer: generate_recharge_path_node/change_state [lifecycle_msgs/ChangeState]
- ServiceServer: generate_recharge_path_node/get_available_states [lifecycle_msgs/GetAvailableStates]
- ServiceServer: generate_recharge_path_node/get_available_transitions [lifecycle_msgs/GetAvailableTransitions]
- ServiceServer: generate_recharge_path_node/get_state [lifecycle_msgs/GetState]
- ServiceServer: generate_recharge_path_node/get_transition_graph [lifecycle_msgs/GetAvailableTransitions]
- Publisher: diagnostics [diagnostic_msgs/DiagnosticArray]
- Publisher: f_maintain_motion_node/transition_event [lifecycle_msgs/TransitionEvent]
- ServiceServer: f_maintain_motion_node/change_state [lifecycle_msgs/ChangeState]
- ServiceServer: f_maintain_motion_node/get_available_states [lifecycle_msgs/GetAvailableStates]
- ServiceServer: f_maintain_motion_node/get_available_transitions [lifecycle_msgs/GetAvailableTransitions]
- ServiceServer: f_maintain_motion_node/get_state [lifecycle_msgs/GetState]
- ServiceServer: f_maintain_motion_node/get_transition_graph [lifecycle_msgs/GetAvailableTransitions]
- Subscriber: diagnostics [diagnostic_msgs/DiagnosticArray]
- Subscriber: f_maintain_motion_node/transition_event [lifecycle_msgs/TransitionEvent]
- Subscriber: generate_recharge_path_node/transition_event [lifecycle_msgs/TransitionEvent]
- Subscriber: pipeline/detected [std_msgs/Bool]
- Subscriber: pipeline/distance_inspected [std_msgs/Float32]
- Subscriber: pipeline/inspected [std_msgs/Bool]
- ServiceServer: mission_metrics/save [std_srvs/Empty]
- Subscriber: diagnostics [diagnostic_msgs/DiagnosticArray]
- Subscriber: mavros/state [mavros_msgs/State]
- Subscriber: pipeline/detected [std_msgs/Bool]
- Subscriber: pipeline/inspected [std_msgs/Bool]

## Installation

### Using release

This package can be copied to a valid ROS 2 workspace. To be sure that all the related dependencies are installed and the command **rosdep install** can be used.
Then the workspace must be compiled using the common ROS 2 build command:

```
mkdir -p ros2_ws/src
cd ros2_ws/
cp -r PATHtoTHISPackage/suave src/.
rosdep install --from-path src/ -i -y
colcon build
source install/setup.bash
```



## Usage


To execute the launch file, the following command can be called:

```
ros2 launch suave suave.launch.py 
```

The generated launch files requires the xterm package, it can be installed by:

```
sudo apt install xterm
```



