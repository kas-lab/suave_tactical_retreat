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
"""Launch the complete SUAVE/RebetMC system."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import StateTransition


def generate_launch_description():
    """Generate the complete SUAVE/RebetMC launch description."""
    silent = LaunchConfiguration('silent')
    result_path = LaunchConfiguration('result_path')
    result_filename = LaunchConfiguration('result_filename')
    mission_config = LaunchConfiguration('mission_config')

    mission_config_default = os.path.join(
        get_package_share_directory('suave_missions'),
        'config',
        'mission_config.yaml',
    )

    silent_arg = DeclareLaunchArgument(
        'silent',
        default_value='false',
        description='Suppress all output (launch logs + node logs)',
    )
    result_path_arg = DeclareLaunchArgument(
        'result_path',
        default_value='~/suave/results',
        description='Path where to save the results',
    )
    result_filename_arg = DeclareLaunchArgument(
        'result_filename',
        default_value='suave_rebetmc_results',
        description='Name of the results file',
    )
    mission_config_arg = DeclareLaunchArgument(
        'mission_config',
        default_value=mission_config_default,
        description='Mission configuration file',
    )

    suave_rebetmc_share = get_package_share_directory('suave_rebetmc')
    suave_base_share = get_package_share_directory('suave_base')
    suave_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                suave_base_share,
                'launch',
                'suave_base.launch.py',
            )
        ),
        launch_arguments={
            'silent': silent,
            'result_path': result_path,
            'result_filename': result_filename,
            'mission_config': mission_config,
            'use_action_server': 'true',
            'recover_thrusters_use_action_server': 'false',
        }.items(),
    )

    adaptation_engine_with_execution_layer = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                suave_rebetmc_share,
                'launch',
                'xtext_adaptation_engine_with_aal.launch.py',
            )
        ),
    )

    suave_rebetmc_bt = Node(
        package='suave_rebetmc',
        executable='suave_rebetmc_bt',
        name='mission_node',
        output='screen',
        parameters=[mission_config, {
            'spiral_search_action_name': 'proxy_spiral_search',
            'use_action_server': True,
            'follow_pipeline_action_name': 'proxy_follow_pipeline',
        }],
    )

    def tactical_retreat_is_active(event):
        if not isinstance(event, StateTransition):
            return False
        node_name = event.action.node_name
        return (
            event.goal_state == 'active' and
            (
                node_name == 'tactical_retreat_kb' or
                node_name.endswith('/tactical_retreat_kb')
            )
        )

    launch_bt_when_kb_is_active = RegisterEventHandler(
        OnStateTransition(
            matcher=tactical_retreat_is_active,
            entities=[suave_rebetmc_bt],
            handle_once=True,
        )
    )

    return LaunchDescription([
        silent_arg,
        result_path_arg,
        result_filename_arg,
        mission_config_arg,
        suave_base,
        launch_bt_when_kb_is_active,
        adaptation_engine_with_execution_layer,
    ])
