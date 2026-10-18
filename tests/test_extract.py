import asyncio
import io
import pytest
from fastapi import HTTPException, UploadFile
from app.services.extract import extract_text

def test_invalid_pdf_returns_422():
    file = UploadFile(filename="broken.pdf", file=io.BytesIO(b"invalid PDF data"))
    with pytest.raises(HTTPException) as exc:
        asyncio.run(extract_text(file))
    assert exc.value.status_code == 422
