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
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


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
        ),
        launch_arguments={
            'save_generated_tql': save_generated_tql,
            'generated_tql_path': generated_tql_path,
            'generated_tql_filename': generated_tql_filename,
        }.items(),
    )

    return LaunchDescription([
        save_generated_tql_arg,
        generated_tql_path_arg,
        generated_tql_filename_arg,
        execution_layer,
        adaptation_engine,
    ])
