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
from launch.actions import DeclareLaunchArgument
from launch.actions import EmitEvent
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.actions import Shutdown
from launch.event_handlers import OnProcessExit
from launch.event_handlers import OnProcessStart
from launch.events import matches_action
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
import lifecycle_msgs
from nav2_common.launch import ReplaceString


def generate_launch_description():

    save_generated_tql = LaunchConfiguration('save_generated_tql')
    generated_tql_path = LaunchConfiguration('generated_tql_path')
    generated_tql_filename = LaunchConfiguration('generated_tql_filename')

    save_generated_tql_arg = DeclareLaunchArgument(
        'save_generated_tql',
        # default_value='false',
        default_value='true',
        description='Save the generated TQL insert query to file',
    )
    generated_tql_path_arg = DeclareLaunchArgument(
        'generated_tql_path',
        # default_value='',
        default_value='/home/ubuntu-user/suave_ws/src/suave_rebetmc/models/tmp',
        description='Directory path where the generated TQL file is saved '
                    '(empty = adapt_x share/generated/)',
    )
    generated_tql_filename_arg = DeclareLaunchArgument(
        'generated_tql_filename',
        # default_value='setup_insert_query.tql',
        default_value='suave_generated.tql',
        description='Filename for the generated TQL file',
    )

    config_files = os.path.join(
        get_package_share_directory('suave_rebetmc'), 'config')
    schema_files = os.path.join(
        get_package_share_directory('typedb_tactics'), 'schemas')

    engine_config_file = os.path.join(
        config_files,
        'adaptation_engine_config.yaml'
    )

    models_dir = os.path.join(
        get_package_share_directory('suave_rebetmc'), 'models')

    engine_config_file = ReplaceString(
        source_file=engine_config_file,
        replacements={
            '<suave_rebetmc_models_dir>': (
                models_dir
            )
        },
    )

    schema_paths = [
        os.path.join(schema_files, 'data_structure', 'data_structure.tql'),
        os.path.join(schema_files, 'context_model', 'context_model.tql'),
        os.path.join(schema_files, 'ros_model', 'ros_model.tql'),
        os.path.join(
            schema_files, 'logical_expressions', 'logical_expression.tql'),
        os.path.join(
            schema_files, 'logical_expressions', 'fuzzy_expression.tql'),
        os.path.join(schema_files, 'feature_model', 'feature_model.tql'),
        os.path.join(
            schema_files,
            'feature_model',
            'feature_model_logical_expression.tql'),
        os.path.join(schema_files, 'tactics_model', 'tactics_model.tql'),
        os.path.join(
            schema_files, 'discover_tactics_model', 'discover_tactics_model.tql'),
        os.path.join(schema_files, 'relaxed', 'relaxed_model.tql'),
        os.path.join(schema_files, 'feature_adaptation_plan', 'feature_adaptation_plan.tql'),
    ]

    typedb_server = ExecuteProcess(
        cmd=['typedb', 'server'],
        name='typedb_server',
        output='screen'
    )

    typedb_ready_probe = ExecuteProcess(
        cmd=[
            'python3',
            '-c',
            (
                'import sys\n'
                'import time\n'
                'from typedb.driver import TypeDB\n'
                '\n'
                'deadline = time.monotonic() + 10.0\n'
                'while True:\n'
                '    try:\n'
                '        driver = TypeDB.core_driver("localhost:1729")\n'
                '        driver.close()\n'
                '        sys.exit(0)\n'
                '    except Exception:\n'
                '        if time.monotonic() >= deadline:\n'
                '            sys.exit(1)\n'
                '        time.sleep(0.1)\n'
            ),
        ],
        name='wait_for_typedb',
        output='screen',
    )

    typedb = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('typedb_tactics'),
                'launch',
                'tactical_retreat_kb.launch.py')
        ),
        launch_arguments={
            'schema_path': '[' + ', '.join(schema_paths) + ']',
            'force_database': 'True',
            'force_data': 'True',
        }.items(),
    )

    suave_adap_engine = LifecycleNode(
        package='adapt_x',
        executable='setup_node',
        output='screen',
        name='adaptation_engine_setup_node',
        namespace='',
        parameters=[engine_config_file]
    )

    config_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(suave_adap_engine),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )

    def on_typedb_probe_exit(event, context):
        del context

        if event.returncode == 0:
            return [typedb, suave_adap_engine, config_event]

        return [
            Shutdown(
                reason='TypeDB did not become ready within 10 seconds',
            ),
        ]

    start_typedb_probe = RegisterEventHandler(
        OnProcessStart(
            target_action=typedb_server,
            on_start=[typedb_ready_probe],
        )
    )

    launch_after_typedb_ready = RegisterEventHandler(
        OnProcessExit(
            target_action=typedb_ready_probe,
            on_exit=on_typedb_probe_exit,
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

    return LaunchDescription([
        save_generated_tql_arg,
        generated_tql_path_arg,
        generated_tql_filename_arg,
        activate,
        launch_after_typedb_ready,
        start_typedb_probe,
        typedb_server,
    ])
