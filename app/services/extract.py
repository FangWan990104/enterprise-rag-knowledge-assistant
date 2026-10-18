"""Extract plain text from uploaded files (.txt, .md, .pdf)."""
from __future__ import annotations

import io

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from pypdf.errors import PdfReadError


async def extract_text(file: UploadFile) -> str:
    data = await file.read(50 * 1024 * 1024 + 1)
    if len(data) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File exceeds 50 MB")
    name = (file.filename or "").lower()
    if not name.endswith((".pdf", ".txt", ".md")):
        raise HTTPException(status_code=415, detail="Only PDF, TXT and MD files are allowed")

    if name.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(data))
        except (PdfReadError, ValueError, OSError) as exc:
            raise HTTPException(status_code=422, detail="Invalid PDF file") from exc
        if len(reader.pages) > 200:
            raise HTTPException(status_code=413, detail="PDF exceeds 200 pages")
        content = "\n".join(page.extract_text() or "" for page in reader.pages)
        if len(content) > 2_000_000:
            raise HTTPException(status_code=413, detail="Text exceeds 2 million characters")
        if not content.strip():
            raise HTTPException(status_code=422, detail="PDF contains no extractable text")
        return content

    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=422, detail="Text must be UTF-8") from exc
    if len(content) > 2_000_000:
        raise HTTPException(status_code=413, detail="Text exceeds 2 million characters")
    return content
