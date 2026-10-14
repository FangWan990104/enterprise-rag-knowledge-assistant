[简体中文](README.md) | [English](README_EN.md)

# Enterprise RAG Knowledge Assistant

A Python-based enterprise document question-answering system powered by FastAPI, DeepSeek, PostgreSQL/pgvector, and Redis.

## Overview

This project implements Retrieval-Augmented Generation (RAG) for enterprise documents. It supports PDF ingestion, text chunking, embedding generation, hybrid retrieval, and grounded answers with source citations.

## Technology Stack

- Backend: Python, FastAPI
- LLM: DeepSeek Chat
- Embeddings: SiliconFlow BAAI/bge-m3 (1024 dimensions)
- Database: PostgreSQL + pgvector
- Retrieval: Vector Search, Full-Text Search, RRF
- Reranking: Optional reranking
- Cache: Redis with TTL
- Frontend: Streamlit
- Deployment: Docker Compose, Nginx, systemd

## Key Features

1. PDF extraction and text chunking
2. Embedding generation and vector storage
3. Hybrid semantic and keyword retrieval
4. Reciprocal Rank Fusion and optional reranking
5. DeepSeek-powered answers with source citations
6. Redis caching and fallback handling
7. REST API and streaming responses
8. Rate limiting, daily request quotas, and output token limits

## Architecture

[View System Architecture](docs/architecture.md)

## Demonstration

The system has been tested with a Cisco My Devices PDF manual. Users can ask questions and inspect cited document excerpts.

Demo video: Coming soon.

## Deployment

Reproducible setup instructions will be added before release.

## Attribution

Based on the MIT-licensed RAG Starter by Dhairya Senjaliya. The original copyright notice and license are preserved in LICENSE.
