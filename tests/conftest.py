"""Test bootstrap: provide a dummy API key so imports succeed offline."""
import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")


import pytest

@pytest.fixture(autouse=True)
def mock_daily_quota(monkeypatch):
    monkeypatch.setattr("app.main.check_daily_quota", lambda: True)

from unittest.mock import MagicMock

@pytest.fixture(autouse=True)
def mock_query_database():
    from app.main import app
    from app.database import get_db
    fake_db = MagicMock()
    fake_db.execute.return_value.one.return_value = (0, 0)
    previous = app.dependency_overrides.get(get_db)
    def override_get_db():
        yield fake_db
    app.dependency_overrides[get_db] = override_get_db
    yield
    if previous is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = previous
