# Copyright 2026 KAS Lab
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

import pathlib

from ament_index_python.packages import get_package_share_directory
import pytest

from typedb_tactics.typedb_tactical_retreat_interface import TacticalRetreatInterface


PACKAGE_DIR = pathlib.Path(__file__).parent.parent
TYPEDB_TACTICS_SHARE = pathlib.Path(get_package_share_directory('typedb_tactics'))
SCHEMAS = [
    str(TYPEDB_TACTICS_SHARE / 'schemas/data_structure/data_structure.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/context_model/context_model.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/logical_expressions/logical_expression.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/ros_model/ros_model.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/feature_model/feature_model.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/feature_model/feature_model_logical_expression.tql'),
    str(TYPEDB_TACTICS_SHARE / 'schemas/tactics_model/tactics_model.tql'),
]


@pytest.fixture(scope='module')
def kb_interface():
    """Load suave_tactics.tql into a fresh TypeDB database."""
    interface = TacticalRetreatInterface(
        'localhost:1729',
        'test_suave_rebetmc',
        SCHEMAS,
        [str(PACKAGE_DIR / 'models/typedb/suave_tactics.tql')],
        force_database=True,
        force_data=True,
        infer=True,
    )
    yield interface
    interface.delete_database()


def test_suave_tactics_kb_initializes(kb_interface):
    """Check that suave_tactics.tql loads into TypeDB without errors."""
    assert kb_interface is not None


def test_suave_tactics_tactic_rules_loaded(kb_interface):
    """Verify all tactic rules from suave_tactics.tql are present in the DB."""
    result = kb_interface.fetch_database(
        'match $r isa tactic_rule, has rule_name $n; fetch $n;'
    )
    rule_names = {r['n']['value'] for r in result}
    assert rule_names == {
        'LOW_ALTITUDE', 'MEDIUM_ALTITUDE', 'HIGH_ALTITUDE',
        'RECOVER_MOTION', 'END_RECOVER_MOTION',
    }
