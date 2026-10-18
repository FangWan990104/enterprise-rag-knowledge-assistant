"""Document ingestion: chunk -> embed -> persist."""
from __future__ import annotations

import hashlib

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
import hashlib

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Chunk, Document
from app.services.chunking import chunk_text
from app.services.embeddings import embed_texts


def ingest_document(
    db: Session, title: str, content: str, source: str | None
) -> Document:
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    existing = db.scalar(select(Document).where(Document.content_hash == content_hash))
    if existing is not None:
        return existing

    settings = get_settings()
    pieces = chunk_text(content, settings.chunk_size, settings.chunk_overlap)
    if not pieces:
        raise ValueError("Document produced no chunks (empty content?)")

    embeddings = embed_texts(pieces)

    document = Document(title=title, source=source, content_hash=content_hash)
    document.chunks = [
        Chunk(chunk_index=i, content=piece, embedding=embedding)
        for i, (piece, embedding) in enumerate(zip(pieces, embeddings, strict=True))
    ]
    try:
        db.add(document)
        db.flush()
        result = db.execute(text("UPDATE knowledge_base_revision SET revision = revision + 1 WHERE id = 1"))
        if result.rowcount != 1:
            raise RuntimeError("Knowledge base revision row missing")
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.scalar(select(Document).where(Document.content_hash == content_hash))
        if existing is not None:
            return existing
        raise
    except Exception:
        db.rollback()
        raise
    db.refresh(document)
    return document
