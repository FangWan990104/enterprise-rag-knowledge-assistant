from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from app.services import ingestion


def test_commit_failure_rolls_back(monkeypatch):
    monkeypatch.setattr(ingestion, "get_settings", lambda: SimpleNamespace(chunk_size=800, chunk_overlap=120))
    monkeypatch.setattr(ingestion, "chunk_text", lambda content, size, overlap: ["sample chunk"])
    monkeypatch.setattr(ingestion, "embed_texts", lambda pieces: [[0.0] * 1024])
    db = MagicMock()
    db.execute.return_value.rowcount = 1
    db.scalar.return_value = None
    db.commit.side_effect = RuntimeError("simulated commit failure")
    with pytest.raises(RuntimeError, match="simulated commit failure"):
        ingestion.ingest_document(db, "sample.txt", "sample content", "sample.txt")
    db.add.assert_called_once()
    db.rollback.assert_called_once()
    db.refresh.assert_not_called()


def test_duplicate_skips_embedding(monkeypatch):
    from unittest.mock import MagicMock
    existing = MagicMock()
    existing.id = 42
    db = MagicMock()
    db.execute.return_value.rowcount = 1
    db.scalar.return_value = existing
    def forbidden(pieces):
        raise AssertionError("Embedding should not be called")
    monkeypatch.setattr(ingestion, "embed_texts", forbidden)
    result = ingestion.ingest_document(db, "duplicate.txt", "same content", "duplicate.txt")
    assert result is existing
    db.commit.assert_not_called()
    db.execute.assert_not_called()
    db.flush.assert_not_called()


def test_concurrent_duplicate_conflict(monkeypatch):
    from unittest.mock import MagicMock
    from sqlalchemy.exc import IntegrityError
    from types import SimpleNamespace
    monkeypatch.setattr(ingestion, "get_settings", lambda: SimpleNamespace(chunk_size=800, chunk_overlap=120))
    monkeypatch.setattr(ingestion, "chunk_text", lambda content, size, overlap: ["sample chunk"])
    monkeypatch.setattr(ingestion, "embed_texts", lambda pieces: [[0.0] * 1024])
    existing = MagicMock()
    existing.id = 42
    db = MagicMock()
    db.execute.return_value.rowcount = 1
    db.scalar.side_effect = [None, existing]
    db.commit.side_effect = IntegrityError("INSERT", {}, Exception("duplicate key"))
    result = ingestion.ingest_document(db, "duplicate.txt", "same content", "duplicate.txt")
    assert result is existing
    db.rollback.assert_called_once()
    db.commit.assert_called_once()


def test_new_document_updates_revision(monkeypatch):
    from unittest.mock import MagicMock
    from types import SimpleNamespace
    monkeypatch.setattr(ingestion, "get_settings", lambda: SimpleNamespace(chunk_size=800, chunk_overlap=120))
    monkeypatch.setattr(ingestion, "chunk_text", lambda content, size, overlap: ["sample chunk"])
    monkeypatch.setattr(ingestion, "embed_texts", lambda pieces: [[0.0] * 1024])
    db = MagicMock()
    db.scalar.return_value = None
    db.execute.return_value.rowcount = 1
    ingestion.ingest_document(db, "new.txt", "new content", "new.txt")
    sql = str(db.execute.call_args.args[0])
    assert "UPDATE knowledge_base_revision" in sql
    assert "revision + 1" in sql
    db.flush.assert_called_once()
    db.commit.assert_called_once()


def test_revision_update_failure_rolls_back(monkeypatch):
    from unittest.mock import MagicMock
    from types import SimpleNamespace
    import pytest
    monkeypatch.setattr(ingestion, "get_settings", lambda: SimpleNamespace(chunk_size=800, chunk_overlap=120))
    monkeypatch.setattr(ingestion, "chunk_text", lambda content, size, overlap: ["sample chunk"])
    monkeypatch.setattr(ingestion, "embed_texts", lambda pieces: [[0.0] * 1024])
    db = MagicMock()
    db.scalar.return_value = None
    db.execute.return_value.rowcount = 0
    with pytest.raises(RuntimeError, match="revision row missing"):
        ingestion.ingest_document(db, "test.txt", "test content", "test.txt")
    db.flush.assert_called_once()
    db.rollback.assert_called_once()
    db.commit.assert_not_called()
