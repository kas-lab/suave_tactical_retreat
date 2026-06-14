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


def generate_launch_description():
    """Generate the composed adaptation launch description."""
    execution_layer_params = os.path.join(
        get_package_share_directory('suave_rebetmc'),
        'config',
        'execution_layer_params.yaml',
    )

    execution_layer = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('execution_layer'),
                'launch',
                'execution_layer_bringup.launch.py',
            )
        ),
        launch_arguments={
            'params_file': execution_layer_params,
        }.items(),
    )

    adaptation_engine = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('suave_rebetmc'),
                'launch',
                'adaptation_engine.launch.py',
            )
        )
    )

    return LaunchDescription([
        execution_layer,
        adaptation_engine,
    ])
