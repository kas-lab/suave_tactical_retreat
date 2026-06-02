from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
# from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from nav2_common.launch import ReplaceString
from launch.actions import EmitEvent
from launch.actions import RegisterEventHandler
from launch.events import matches_action

from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
# from launch.actions import TimerAction
import lifecycle_msgs


def generate_launch_description():

    config_files = os.path.join(
        get_package_share_directory("suave_rebetmc"), "config")
    schema_files = os.path.join(
        get_package_share_directory("typedb_tactics"), "schemas")

    engine_config_file = os.path.join(
        config_files,
        'adaptation_engine_config.yaml'
    )

    models_dir = os.path.join(
        get_package_share_directory("suave_rebetmc"), "models")

    engine_config_file = ReplaceString(
        source_file=engine_config_file,
        replacements={
            "<suave_rebetmc_models_dir>": (
                models_dir
            )
        },
    )

    typedb = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(get_package_share_directory("typedb_tactics"), "launch",
                         "tactical_retreat_kb.launch.py")
        ),
        launch_arguments={
            "schema_path": f"[{os.path.join(schema_files, 'data_structure', 'data_structure.tql')}, \
                              {os.path.join(schema_files, 'context_model', 'context_model.tql')}, \
                              {os.path.join(schema_files, 'ros_model', 'ros_model.tql')}, \
                              {os.path.join(schema_files, 'logical_expressions', 'logical_expression.tql')}, \
                              {os.path.join(schema_files, 'logical_expressions', 'fuzzy_expression.tql')}, \
                              {os.path.join(schema_files, 'feature_model', 'feature_model.tql')}, \
                              {os.path.join(schema_files, 'feature_model', 'feature_model_logical_expression.tql')}, \
                              {os.path.join(schema_files, 'tactics_model', 'tactics_model.tql')}, \
                              {os.path.join(schema_files, 'discover_tactics_model', 'discover_tactics_model.tql')}, \
                              {os.path.join(schema_files, 'relaxed', 'relaxed_model.tql')}, \
                              {os.path.join(schema_files, 'discover_hypothetical_req_fulfillment', 'discover_hypothetical_req_fulfillment.tql')}, \
                              {os.path.join(schema_files, 'discover_tactics_model', 'discover_tactics_model.tql')}]",
            "force_database": "True",
            "force_data": "True",
        }.items(),
    )

    suave_adap_engine = LifecycleNode(
        package="adapt_x",
        executable="adaptation_engine",
        output="screen",
        name='adaptation_engine',
        namespace='',
        parameters=[engine_config_file]
    )

    config_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(suave_adap_engine),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )

    activate = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=suave_adap_engine,
            goal_state='inactive',
            entities=[
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(suave_adap_engine),
                    transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE,
                )),
            ],
        )
    )

    # start = Node(
    #     package="suave_rebetmc",
    #     executable="tree_action_client.py",
    #     arguments=["suave_AAL_TACTICAL"],
    #     prefix='xterm -hold -e ',
    # )

    # start_trigger = RegisterEventHandler(
    #     OnStateTransition(
    #         target_lifecycle_node=suave_adap_engine,
    #         goal_state='active',
    #         entities=[
    #             TimerAction(
    #                 period=10.0,  # Delay for 5 seconds
    #                 actions=[start],
    #             )
    #         ],
    #     )
    # )

    return LaunchDescription(
        # [typedb]
        [typedb, suave_adap_engine, config_event, activate]
        # [typedb, suave_adap_engine, config_event, activate, start_trigger]
        # [typedb, delay_adap_engine, aal, context_model]
        # [typedb, delay_adap_engine, aal, context_model] #, arborist, ]
    )
