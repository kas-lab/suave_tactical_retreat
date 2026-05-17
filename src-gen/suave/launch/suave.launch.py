import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression, PathJoinSubstitution, TextSubstitution

def generate_launch_description():
  ld = LaunchDescription()

  # *** PARAMETERS ***
  /mavros/mavros_node_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/mavros/mavros_node.yaml'
  )
  /mavros/mavros_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/mavros/mavros.yaml'
  )
  /mavros/param_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/mavros/param.yaml'
  )
  /mavros/sys_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/mavros/sys.yaml'
  )
  /mavros/time_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/mavros/time.yaml'
  )
  /water_visibility_observer_node_config = os.path.join(
    get_package_share_directory('suave'),
    'config',
    '/water_visibility_observer_node.yaml'
  )
  discharge_time_arg = DeclareLaunchArgument(
    "discharge_time", default_value=TextSubstitution(text="200.0")
  )
  ld.add_action(discharge_time_arg)
  qa_publishing_period_arg = DeclareLaunchArgument(
    "qa_publishing_period", default_value=TextSubstitution(text="1.0")
  )
  ld.add_action(qa_publishing_period_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  thruster_events_arg = DeclareLaunchArgument(
    "thruster_events", default_value=TextSubstitution(text="[(1,failure,35)]")
  )
  ld.add_action(thruster_events_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  spiral_altitude_arg = DeclareLaunchArgument(
    "spiral_altitude", default_value=TextSubstitution(text="1.0")
  )
  ld.add_action(spiral_altitude_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  recharge_station_gz_pos_arg = DeclareLaunchArgument(
    "recharge_station_gz_pos", default_value=TextSubstitution(text="[-3.0, -2.0, -19.5]")
  )
  ld.add_action(recharge_station_gz_pos_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)
  time_limit_arg = DeclareLaunchArgument(
    "time_limit", default_value=TextSubstitution(text="300")
  )
  ld.add_action(time_limit_arg)
  use_sim_time_arg = DeclareLaunchArgument(
    "use_sim_time", default_value=TextSubstitution(text="false")
  )
  ld.add_action(use_sim_time_arg)

  # *** ROS 2 nodes ***
  /suave_runner_node = Node(
    package="suave_runner",
    executable="suave_runner",
    output='screen',
    name="/suave_runner_node"
  )
  /gz_pipe_pose_bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    output='screen',
    name="/gz_pipe_pose_bridge",
    remappings=[
      ("model/min_pipes_pipeline/pose", "model/min_pipes_pipeline/pose")]
  )
  /gz_bluerov_pose_bridge = Node(
    package="ros_gz_bridge",
    executable="parameter_bridge",
    output='screen',
    name="/gz_bluerov_pose_bridge",
    remappings=[
      ("model/bluerov2/pose", "model/bluerov2/pose")]
  )
  /mavros/mavros_node = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/mavros_node",
    parameters = [/mavros/mavros_node_config]
  )
  /mavros/mavros_router = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/mavros_router",
    remappings=[
      ("diagnostics", "diagnostics"),
      ("uas1/mavlink_source", "uas1/mavlink_source"),
      ("uas1/mavlink_sink", "uas1/mavlink_sink"),
      ("mavros_router/add_endpoint", "mavros_router/add_endpoint"),
      ("mavros_router/del_endpoint", "mavros_router/del_endpoint")]
  )
  /mavros/mavros = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/mavros",
    remappings=[
      ("diagnostics", "diagnostics"),
      ("tf", "tf"),
      ("tf_static", "tf_static"),
      ("uas1/mavlink_sink", "uas1/mavlink_sink"),
      ("uas1/mavlink_source", "uas1/mavlink_source")]
    ,
    parameters = [/mavros/mavros_config]
  )
  /mavros/cmd = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/cmd",
    remappings=[
      ("cmd/arming", "cmd/arming"),
      ("cmd/command", "cmd/command"),
      ("cmd/command_int", "cmd/command_int"),
      ("cmd/land", "cmd/land"),
      ("cmd/land_local", "cmd/land_local"),
      ("cmd/set_home", "cmd/set_home"),
      ("cmd/takeoff", "cmd/takeoff"),
      ("cmd/takeoff_local", "cmd/takeoff_local"),
      ("cmd/trigger_control", "cmd/trigger_control"),
      ("cmd/trigger_interval", "cmd/trigger_interval"),
      ("cmd/vtol_transition", "cmd/vtol_transition")]
  )
  /mavros/local_position = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/local_position",
    remappings=[
      ("local_position/accel", "local_position/accel"),
      ("local_position/odom", "local_position/odom"),
      ("local_position/pose", "local_position/pose"),
      ("local_position/pose_cov", "local_position/pose_cov"),
      ("local_position/velocity_body", "local_position/velocity_body"),
      ("local_position/velocity_body_cov", "local_position/velocity_body_cov"),
      ("local_position/velocity_local", "local_position/velocity_local")]
  )
  /mavros/param = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/param",
    remappings=[
      ("param/event", "param/event"),
      ("param/pull", "param/pull"),
      ("param/set", "param/set")]
    ,
    parameters = [/mavros/param_config]
  )
  /mavros/setpoint_position = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/setpoint_position",
    remappings=[
      ("global_position/global", "global_position/global"),
      ("local_position/pose", "local_position/pose"),
      ("setpoint_position/global", "setpoint_position/global"),
      ("setpoint_position/global_to_local", "setpoint_position/global_to_local"),
      ("setpoint_position/local", "setpoint_position/local")]
  )
  /mavros/sys = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/sys",
    remappings=[
      ("battery", "battery"),
      ("estimator_status", "estimator_status"),
      ("extended_state", "extended_state"),
      ("state", "state"),
      ("status_event", "status_event"),
      ("statustext/recv", "statustext/recv"),
      ("sys_status", "sys_status"),
      ("statustext/send", "statustext/send"),
      ("set_message_interval", "set_message_interval"),
      ("set_mode", "set_mode"),
      ("set_stream_rate", "set_stream_rate"),
      ("vehicle_info_get", "vehicle_info_get")]
    ,
    parameters = [/mavros/sys_config]
  )
  /mavros/time = Node(
    package="mavros",
    executable="mavros_node",
    output='screen',
    name="/mavros/time",
    remappings=[
      ("time_reference", "time_reference"),
      ("timesync_status", "timesync_status")]
    ,
    parameters = [/mavros/time_config]
  )
  /water_visibility_observer_node = Node(
    package="suave_monitor",
    executable="water_visibility_observer",
    output='screen',
    name="/water_visibility_observer_node",
    remappings=[
      ("diagnostics", "diagnostics")]
    ,
    parameters = [/water_visibility_observer_node_config]
  )
  /battery_monitor = Node(
    package="suave_monitor",
    executable="battery_monitor",
    output='screen',
    name="/battery_monitor",
    remappings=[
      ("battery_monitor/recharge/complete", "battery_monitor/recharge/complete"),
      ("diagnostics", "diagnostics"),
      ("battery_monitor/recharge", "battery_monitor/recharge")]
    ,
    parameters=[{
    "discharge_time": LaunchConfiguration("discharge_time"),
    "qa_publishing_period": LaunchConfiguration("qa_publishing_period"),
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /detect_pipeline = Node(
    package="suave",
    executable="pipeline_detection_wv",
    output='screen',
    name="/detect_pipeline",
    remappings=[
      ("pipeline/detected", "pipeline/detected"),
      ("diagnostics", "diagnostics"),
      ("model/bluerov2/pose", "model/bluerov2/pose"),
      ("pipeline/get_path", "pipeline/get_path")]
  )
  /thruster_monitor = Node(
    package="suave_monitor",
    executable="thruster_monitor",
    output='screen',
    name="/thruster_monitor",
    remappings=[
      ("diagnostics", "diagnostics")]
    ,
    parameters=[{
    "thruster_events": LaunchConfiguration("thruster_events"),
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /f_generate_search_path_node = Node(
    package="suave",
    executable="spiral_search",
    output='screen',
    name="/f_generate_search_path_node",
    remappings=[
      ("f_generate_search_path_node/transition_event", "f_generate_search_path_node/transition_event"),
      ("f_generate_search_path_node/change_state", "f_generate_search_path_node/change_state"),
      ("f_generate_search_path_node/get_available_states", "f_generate_search_path_node/get_available_states"),
      ("f_generate_search_path_node/get_available_transitions", "f_generate_search_path_node/get_available_transitions"),
      ("f_generate_search_path_node/get_state", "f_generate_search_path_node/get_state"),
      ("f_generate_search_path_node/get_transition_graph", "f_generate_search_path_node/get_transition_graph")]
    ,
    parameters=[{
    "spiral_altitude": LaunchConfiguration("spiral_altitude"),
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /f_follow_pipeline_node = Node(
    package="suave",
    executable="follow_pipeline",
    output='screen',
    name="/f_follow_pipeline_node",
    remappings=[
      ("pipeline/distance_inspected", "pipeline/distance_inspected"),
      ("pipeline/inspected", "pipeline/inspected"),
      ("f_follow_pipeline_node/transition_event", "f_follow_pipeline_node/transition_event"),
      ("f_follow_pipeline_node/change_state", "f_follow_pipeline_node/change_state"),
      ("f_follow_pipeline_node/get_available_states", "f_follow_pipeline_node/get_available_states"),
      ("f_follow_pipeline_node/get_available_transitions", "f_follow_pipeline_node/get_available_transitions"),
      ("f_follow_pipeline_node/get_state", "f_follow_pipeline_node/get_state"),
      ("f_follow_pipeline_node/get_transition_graph", "f_follow_pipeline_node/get_transition_graph")]
    ,
    parameters=[{
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /generate_recharge_path_node = Node(
    package="suave",
    executable="recharge_battery",
    output='screen',
    name="/generate_recharge_path_node",
    remappings=[
      ("generate_recharge_path_node/transition_event", "generate_recharge_path_node/transition_event"),
      ("generate_recharge_path_node/change_state", "generate_recharge_path_node/change_state"),
      ("generate_recharge_path_node/get_available_states", "generate_recharge_path_node/get_available_states"),
      ("generate_recharge_path_node/get_available_transitions", "generate_recharge_path_node/get_available_transitions"),
      ("generate_recharge_path_node/get_state", "generate_recharge_path_node/get_state"),
      ("generate_recharge_path_node/get_transition_graph", "generate_recharge_path_node/get_transition_graph")]
    ,
    parameters=[{
    "recharge_station_gz_pos": LaunchConfiguration("recharge_station_gz_pos"),
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /f_maintain_motion_node = Node(
    package="suave",
    executable="recover_thrusters",
    output='screen',
    name="/f_maintain_motion_node",
    remappings=[
      ("diagnostics", "diagnostics"),
      ("f_maintain_motion_node/transition_event", "f_maintain_motion_node/transition_event"),
      ("f_maintain_motion_node/change_state", "f_maintain_motion_node/change_state"),
      ("f_maintain_motion_node/get_available_states", "f_maintain_motion_node/get_available_states"),
      ("f_maintain_motion_node/get_available_transitions", "f_maintain_motion_node/get_available_transitions"),
      ("f_maintain_motion_node/get_state", "f_maintain_motion_node/get_state"),
      ("f_maintain_motion_node/get_transition_graph", "f_maintain_motion_node/get_transition_graph")]
    ,
    parameters=[{
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )
  /mission_metrics = Node(
    package="suave_metrics",
    executable="mission_metrics",
    output='screen',
    name="/mission_metrics",
    remappings=[
      ("diagnostics", "diagnostics"),
      ("f_maintain_motion_node/transition_event", "f_maintain_motion_node/transition_event"),
      ("generate_recharge_path_node/transition_event", "generate_recharge_path_node/transition_event"),
      ("pipeline/detected", "pipeline/detected"),
      ("pipeline/distance_inspected", "pipeline/distance_inspected"),
      ("pipeline/inspected", "pipeline/inspected"),
      ("mission_metrics/save", "mission_metrics/save")]
  )
  /mission_node = Node(
    package="suave_missions",
    executable="mission_node",
    output='screen',
    name="/mission_node",
    remappings=[
      ("diagnostics", "diagnostics"),
      ("mavros/state", "mavros/state"),
      ("pipeline/detected", "pipeline/detected"),
      ("pipeline/inspected", "pipeline/inspected")]
    ,
    parameters=[{
    "time_limit": LaunchConfiguration("time_limit"),
    "use_sim_time": LaunchConfiguration("use_sim_time"),}]
  )

  # *** ROS 2 subsystems (include launch files)***

  # *** Add actions ***
  ld.add_action(/suave_runner_node)
  ld.add_action(/gz_pipe_pose_bridge)
  ld.add_action(/gz_bluerov_pose_bridge)
  ld.add_action(/mavros/mavros_node)
  ld.add_action(/mavros/mavros_router)
  ld.add_action(/mavros/mavros)
  ld.add_action(/mavros/cmd)
  ld.add_action(/mavros/local_position)
  ld.add_action(/mavros/param)
  ld.add_action(/mavros/setpoint_position)
  ld.add_action(/mavros/sys)
  ld.add_action(/mavros/time)
  ld.add_action(/water_visibility_observer_node)
  ld.add_action(/battery_monitor)
  ld.add_action(/detect_pipeline)
  ld.add_action(/thruster_monitor)
  ld.add_action(/f_generate_search_path_node)
  ld.add_action(/f_follow_pipeline_node)
  ld.add_action(/generate_recharge_path_node)
  ld.add_action(/f_maintain_motion_node)
  ld.add_action(/mission_metrics)
  ld.add_action(/mission_node)

  return ld
