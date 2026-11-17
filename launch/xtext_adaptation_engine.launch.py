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
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import LifecycleTransition
from lifecycle_msgs.msg import Transition
from nav2_common.launch import ReplaceString


def generate_launch_description():
    config_files = os.path.join(
        get_package_share_directory('suave_tactical_retreat'), 'config')

    models_dir = os.path.join(
        get_package_share_directory('suave_tactical_retreat'), 'models')

    kb_config_file = os.path.join(
        config_files,
        'xtext_kb_config.yaml'
    )
    xtext_kb_config_file = ReplaceString(
        source_file=kb_config_file,
        replacements={
            '<suave_tactical_retreat_models_dir>': (
                models_dir
            )
        },
    )
    xtext_kb = LifecycleNode(
        name='tactical_retreat_kb',
        package='typedb_tactics',
        executable='tactical_retreat',
        output='screen',
        namespace='',
        parameters=[xtext_kb_config_file]
    )

    lc_transition = LifecycleTransition(
        lifecycle_node_names=['tactical_retreat_kb'],
        transition_ids=[
            Transition.TRANSITION_CONFIGURE,
            Transition.TRANSITION_ACTIVATE,
        ],
    )

    return LaunchDescription([
        xtext_kb,
        lc_transition
    ])
