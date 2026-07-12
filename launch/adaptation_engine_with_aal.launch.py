# Copyright 2026 KAS-lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Launch the SUAVE adaptation engine and generic execution layer."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import EmitEvent
from launch.actions import IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.events import matches_action
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from launch_ros.events.lifecycle import StateTransition
import lifecycle_msgs


def setup_node_is_finalized(event):
    """Return True once the adaptation engine setup node has shut down."""
    return (
        isinstance(event, StateTransition)
        and event.action.node_name.lstrip('/') == 'adaptation_engine_setup_node'
        and event.goal_state == 'finalized'
    )


def generate_launch_description():
    """Generate the composed adaptation launch description."""
    save_generated_tql = LaunchConfiguration('save_generated_tql')
    generated_tql_path = LaunchConfiguration('generated_tql_path')
    generated_tql_filename = LaunchConfiguration('generated_tql_filename')

    save_generated_tql_arg = DeclareLaunchArgument(
        'save_generated_tql',
        default_value='false',
        description='Save the generated TQL insert query to file',
    )
    generated_tql_path_arg = DeclareLaunchArgument(
        'generated_tql_path',
        default_value='',
        description='Directory path where the generated TQL file is saved '
                    '(empty = adapt_x share/generated/)',
    )
    generated_tql_filename_arg = DeclareLaunchArgument(
        'generated_tql_filename',
        default_value='setup_insert_query.tql',
        description='Filename for the generated TQL file',
    )

    adaptation_engine = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('suave_rebetmc'),
                'launch',
                'adaptation_engine.launch.py',
            )
        ),
        launch_arguments={
            'save_generated_tql': save_generated_tql,
            'generated_tql_path': generated_tql_path,
            'generated_tql_filename': generated_tql_filename,
        }.items(),
    )

    adaptation_layer = Node(
        package='aal',
        executable='adaptation_layer',
        name='adaptation_layer',
        output='screen'
    )

    suave_rebetmc_config = os.path.join(
        get_package_share_directory('suave_rebetmc'), 'config')
    adaptation_proxies_config = os.path.join(
        suave_rebetmc_config,
        'adaptation_proxies_config.yaml'
    )

    spiral_search_proxy_node = LifecycleNode(
        package='adapt_x',
        executable='adaptation_proxy',
        output='screen',
        name='spiral_search_adaptation_proxy',
        namespace='',
        parameters=[adaptation_proxies_config],
    )

    follow_pipeline_proxy_node = LifecycleNode(
        package='adapt_x',
        executable='adaptation_proxy',
        output='screen',
        name='follow_pipeline_adaptation_proxy',
        namespace='',
        parameters=[adaptation_proxies_config],
    )

    recover_thrusters_proxy_node = LifecycleNode(
        package='adapt_x',
        executable='adaptation_proxy',
        output='screen',
        name='recover_thrusters_adaptation_proxy',
        namespace='',
        parameters=[adaptation_proxies_config],
    )

    recharge_battery_proxy_node = LifecycleNode(
        package='adapt_x',
        executable='adaptation_proxy',
        output='screen',
        name='recharge_battery_adaptation_proxy',
        namespace='',
        parameters=[adaptation_proxies_config],
    )

    adaptation_proxy_names = [
        'spiral_search_adaptation_proxy',
        'follow_pipeline_adaptation_proxy',
        'recover_thrusters_adaptation_proxy',
        'recharge_battery_adaptation_proxy',
    ]

    lifecycle_manager = LifecycleNode(
        package='adapt_x',
        executable='lifecycle_manager',
        output='screen',
        name='adaptation_proxy_lifecycle_manager',
        namespace='',
        parameters=[{'nodes': adaptation_proxy_names}],
    )

    lifecycle_manager_config_event = RegisterEventHandler(
        OnStateTransition(
            matcher=setup_node_is_finalized,
            entities=[
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(lifecycle_manager),
                    transition_id=(
                        lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE
                    ),
                )),
            ],
            handle_once=True,
        )
    )

    lifecycle_manager_activate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=lifecycle_manager,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(lifecycle_manager),
                    transition_id=(
                        lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE
                    ),
                )),
            ],
            handle_once=True,
        )
    )

    lifecycle_manager_deactivate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=lifecycle_manager,
            start_state='activating',
            goal_state='active',
            entities=[
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(lifecycle_manager),
                    transition_id=(
                        lifecycle_msgs.msg.Transition.TRANSITION_DEACTIVATE
                    ),
                )),
            ],
            handle_once=True,
        )
    )

    inactive_shutdown_transition = (
        lifecycle_msgs.msg.Transition.TRANSITION_INACTIVE_SHUTDOWN
    )

    lifecycle_manager_shutdown_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=lifecycle_manager,
            start_state='deactivating',
            goal_state='inactive',
            entities=[
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(lifecycle_manager),
                    transition_id=inactive_shutdown_transition,
                )),
            ],
            handle_once=True,
        )
    )

    return LaunchDescription([
        save_generated_tql_arg,
        generated_tql_path_arg,
        generated_tql_filename_arg,
        adaptation_layer,
        spiral_search_proxy_node,
        follow_pipeline_proxy_node,
        recharge_battery_proxy_node,
        recover_thrusters_proxy_node,
        lifecycle_manager,
        lifecycle_manager_activate_event,
        lifecycle_manager_config_event,
        lifecycle_manager_deactivate_event,
        lifecycle_manager_shutdown_event,
        adaptation_engine,
    ])
