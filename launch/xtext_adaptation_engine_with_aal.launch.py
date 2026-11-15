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
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource

from launch_ros.actions import LifecycleNode
from launch_ros.actions import LifecycleTransition
from launch_ros.actions import Node

from lifecycle_msgs.msg import Transition


def generate_launch_description():
    """Generate the composed adaptation launch description."""
    adaptation_engine = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('suave_tactical_retreat'),
                'launch',
                'xtext_adaptation_engine.launch.py',
            )
        ),
    )

    adaptation_layer = Node(
        package='aal',
        executable='adaptation_layer',
        name='adaptation_layer',
        output='full',
    )

    suave_tactical_retreat_config = os.path.join(
        get_package_share_directory('suave_tactical_retreat'), 'config')
    adaptation_proxies_config = os.path.join(
        suave_tactical_retreat_config,
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

    # recover_thrusters_proxy_node = LifecycleNode(
    #     package='adapt_x',
    #     executable='adaptation_proxy',
    #     output='screen',
    #     name='recover_thrusters_adaptation_proxy',
    #     namespace='',
    #     parameters=[adaptation_proxies_config],
    # )

    # recharge_battery_proxy_node = LifecycleNode(
    #     package='adapt_x',
    #     executable='adaptation_proxy',
    #     output='screen',
    #     name='recharge_battery_adaptation_proxy',
    #     namespace='',
    #     parameters=[adaptation_proxies_config],
    # )

    adaptation_proxy_transition = LifecycleTransition(
        lifecycle_node_names=[
            'spiral_search_adaptation_proxy',
            # 'recover_thrusters_adaptation_proxy',
            'follow_pipeline_adaptation_proxy',
            # 'recharge_battery_adaptation_proxy',
        ],
        transition_ids=[
            Transition.TRANSITION_CONFIGURE,
            # Transition.TRANSITION_ACTIVATE,
        ],
    )

    return LaunchDescription([
        adaptation_layer,
        spiral_search_proxy_node,
        follow_pipeline_proxy_node,
        # recharge_battery_proxy_node,
        # recover_thrusters_proxy_node,
        adaptation_engine,
        adaptation_proxy_transition,
    ])
