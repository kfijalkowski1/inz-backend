import json
from datetime import datetime

import pytest

from code.database.declarations import Base
from tests.database_mock import mock_db


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    db_mock_config = []
    for table_name, table_content in mock_db.items():
        db_mock_config.append((table_name, table_content))
    return db_mock_config


def change_keys_to_time_obj(table_content, time_keys):
    for table_row in list(table_content):
        for key in time_keys:
            if key in dict(table_row).keys():
                table_row[key] = datetime.strptime(table_row[key], "%Y-%m-%d %H:%M:%S")