import os
import tempfile

import pytest

from app import create_app
from app.db import get_db
from app.db import init_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "../instance/app.sqlite"), "rb") as f:
    _data_sql = f.read().decode("unicode_escape")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({"TESTING": True, "DATABASE": db_path})

    # create the database and load test data
    with app.app_context():
        get_db()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

