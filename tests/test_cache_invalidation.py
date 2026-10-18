"""HTTP-level cache invalidation test with isolated DB and cache fakes."""
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.routers import query as query_module
from app.services.search import SearchResult


def test_http_cache_invalidation(monkeypatch):
    state = {"revision": 1, "generation_calls": 0, "search_calls": 0}
    cache = {}

    class FakeDB:
        def execute(self, statement):
            return SimpleNamespace(one=lambda: (state["revision"],))

    def fake_db():
        yield FakeDB()

    def fake_search(db, question, top_k):
        state["search_calls"] += 1
        return SearchResult(chunks=[], confidence=0.9)

    def fake_generate(question, chunks):
        state["generation_calls"] += 1
        return f"Answer version {state['revision']}"

    monkeypatch.setattr("app.main.check_rate_limit", lambda ip: True)
    monkeypatch.setattr("app.main.check_daily_quota", lambda: True)
    monkeypatch.setattr(query_module, "search", fake_search)
    monkeypatch.setattr(query_module, "generate_answer", fake_generate)
    monkeypatch.setattr(query_module, "get_cache", lambda key: cache.get(key))
    monkeypatch.setattr(query_module, "set_cache", lambda key, value: cache.__setitem__(key, value))

    old_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = fake_db
    try:
        with TestClient(app) as client:
            payload = {"question": "Cache invalidation test", "top_k": 3}
            first = client.post("/query", json=payload)
            second = client.post("/query", json=payload)
            assert first.status_code == 200
            assert second.status_code == 200
            assert first.json()["answer"] == "Answer version 1"
            assert second.json() == first.json()
            assert state["generation_calls"] == 1
            assert state["search_calls"] == 1
            assert len(cache) == 1

            state["revision"] = 2
            third = client.post("/query", json=payload)
            assert third.status_code == 200
            assert third.json()["answer"] == "Answer version 2"
            assert state["generation_calls"] == 2
            assert state["search_calls"] == 2
            assert len(cache) == 2

            fourth = client.post("/query", json=payload)
            assert fourth.status_code == 200
            assert fourth.json() == third.json()
            assert state["generation_calls"] == 2
            assert state["search_calls"] == 2
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old_overrides)
