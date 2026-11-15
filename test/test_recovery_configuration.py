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

"""Verify the lifecycle-driven recover-motion adaptation configuration."""

from pathlib import Path

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load_proxy_config():
    """Load the adaptation proxies parameter file."""
    config_path = PACKAGE_ROOT / 'config' / 'adaptation_proxies_config.yaml'
    with config_path.open() as config_file:
        return yaml.safe_load(config_file)


def test_recover_thrusters_proxy_is_autonomous():
    """Verify the recovery proxy self-activates without an action goal."""
    config = load_proxy_config()
    parameters = config['recover_thrusters_adaptation_proxy'][
        'ros__parameters']
    assert parameters['operation_mode'] == 'autonomous'
    assert parameters['adaptation_strategy'] == 'tactic'
    assert 'interface_type' not in parameters


def test_task_proxies_remain_goal_bound():
    """Verify task proxies keep the default goal-bound action interface."""
    config = load_proxy_config()
    for proxy_name in ('spiral_search_adaptation_proxy',
                       'follow_pipeline_adaptation_proxy',
                       'recharge_battery_adaptation_proxy'):
        parameters = config[proxy_name]['ros__parameters']
        assert 'operation_mode' not in parameters
        assert 'interface_type' in parameters


def test_bringup_disables_recovery_action_server_only():
    """Verify only the recovery managed node runs lifecycle-driven."""
    bringup = (
        PACKAGE_ROOT / 'launch' / 'suave_tactical_retreat_bringup.launch.py'
    ).read_text()
    assert "'use_action_server': 'true'" in bringup
    assert "'recover_thrusters_use_action_server': 'false'" in bringup

    suave_base = (
        PACKAGE_ROOT / 'launch' / 'suave_base.launch.py'
    ).read_text()
    assert "'use_action_server': use_action_server" in suave_base
    assert "'recover_thrusters_use_action_server': (" in suave_base


def test_bt_has_no_recovery_dependency():
    """Verify the behavior tree does not orchestrate thruster recovery."""
    bringup = (
        PACKAGE_ROOT / 'launch' / 'suave_tactical_retreat_bringup.launch.py'
    ).read_text()
    assert 'recover_thrusters_action_name' not in bringup
    bt_xml = (PACKAGE_ROOT / 'bts' / 'suave.xml').read_text()
    assert 'recover_thrusters' not in bt_xml
