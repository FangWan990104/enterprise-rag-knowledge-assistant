# Deployment Guide

## Requirements

- Python 3.10+
- Docker and Docker Compose
- DeepSeek API key
- SiliconFlow API key

## 1. Install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
```

Set the DeepSeek API key, SiliconFlow API key, model names, embedding dimension (1024), PostgreSQL connection URL and database password. Never commit .env.

## 3. Start PostgreSQL

```bash
docker compose up -d db
```

## 4. Start FastAPI

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 5. Start Streamlit

In another terminal:

```bash
streamlit run streamlit_app.py --server.port 8501
```

## 6. Verify

```bash
curl http://127.0.0.1:8000/health
```

## Notes

- Configure Redis separately on localhost:6379 if caching is enabled.
- Import documents before querying.
- Use a reverse proxy and authentication before exposing the application publicly.
- The public release configuration must be checked before deployment.
