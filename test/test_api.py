import json

import pytest
from app.db import get_db

def test_contents(client,app):
    response = client.get("/contents?page=1")
    with app.app_context():
        db = get_db()
        ex = db.execute("SELECT * FROM test_contents LIMIT 3;").fetchone()
        assert response.data.count(b'contents_title') == 10

