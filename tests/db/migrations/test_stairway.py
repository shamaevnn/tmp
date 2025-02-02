"""
The Stairway test is maintenance-free and allows you to quickly and cheaply find
a huge number of common typical mistakes in migrations:
- not implemented downgrade methods,
- non-removed data types in downgrade methods (e.g. enum),
- typos and other errors.
The idea of the test is to run migrations one at a time,
sequentially executing the upgrade, downgrade,
upgrade.
"""

from types import SimpleNamespace

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from tests.db.migrations.db_alembic_utils import _make_alembic_config


def get_revisions():
    # Create object with alembic configuration
    options = SimpleNamespace(
        config="alembic.ini", pg_url=None, name="alembic", raiseerr=False, x=None
    )
    config = _make_alembic_config(options)

    # Get folder with alembic migrations
    revisions_dir = ScriptDirectory.from_config(config)

    # Sort all migrations from first to last
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    downgrade(alembic_config, revision.down_revision or "-1")
    upgrade(alembic_config, revision.revision)
