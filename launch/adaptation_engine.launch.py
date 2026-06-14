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
from launch.actions import EmitEvent
from launch.actions import IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.events import matches_action
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
import lifecycle_msgs
from nav2_common.launch import ReplaceString


def generate_launch_description():

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
        # os.path.join(
        #     schema_files, 'discover_tactics_model', 'discover_tactics_model.tql'),
        # os.path.join(schema_files, 'relaxed', 'relaxed_model.tql'),
        # os.path.join(
        #     schema_files,
        #     'discover_hypothetical_req_fulfillment',
        #     'discover_hypothetical_req_fulfillment.tql'),
    ]

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
        executable='adaptation_engine',
        output='screen',
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

    return LaunchDescription(
        [typedb, suave_adap_engine, config_event, activate]
    )
