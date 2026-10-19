[简体中文](README.md) | [English](README_EN.md)

# Enterprise RAG Knowledge Assistant

基于 Python、FastAPI、DeepSeek 和 PostgreSQL/pgvector 的企业知识库智能问答系统。

## 项目简介

本项目支持 PDF 文档解析、文本切分、向量化、混合检索及基于文档的 AI 问答，并提供来源引用。

## 技术栈

- Python / FastAPI
- DeepSeek Chat
- SiliconFlow BAAI/bge-m3 Embedding
- PostgreSQL / pgvector
- Redis Cache-Aside
- Streamlit
- Docker Compose / Nginx / systemd

## 核心功能

1. PDF 文档解析与文本切分
2. 1024 维 Embedding 向量存储
3. 向量检索与关键词混合检索
4. RRF 排序融合及可选 Reranking
5. DeepSeek 问答及文档来源引用
6. Redis TTL 缓存
7. FastAPI 普通与流式问答
8. 请求限流、每日额度与输出 Token 限制

## 系统架构

[查看 RAG 架构图](docs/architecture.md)

## 实际演示

使用 Cisco My Devices PDF 进行文档问答测试，支持查看答案和引用来源。

### 演示视频 / Demo Video

[观看或下载演示视频 | Watch / Download Demo](https://rag-portfolio-demo-1501887039.cos.ap-shanghai.myqcloud.com/Enterprise-rag-demo-v1.mp4.MP4)

**中文：** 4分48秒真实运行演示，包括 Cisco 文档问答、GitLab Handbook 检索、来源引用及知识库外问题拒答。

**English:** A 4-minute-48-second demonstration covering Cisco documentation Q&A, GitLab Handbook retrieval, source citations, and out-of-scope question handling.

**观看提示 / Viewing Note:** 部分浏览器需要先下载 MP4 后观看。Some browsers may download the MP4 instead of playing it inline. HEVC playback support varies by device.

## 项目部署

本项目包含 FastAPI、PostgreSQL/pgvector、Redis、Streamlit 和 Docker 相关配置。环境变量请参考 `.env.example`，不要提交真实 API Keys。

**English:** The repository includes FastAPI, PostgreSQL/pgvector, Redis, Streamlit, and Docker-related configuration. Refer to `.env.example` for environment variables. Never commit real API keys.

## 开源声明

本项目基于 Dhairya Senjaliya 的 MIT Licensed RAG Starter 改造，保留原项目 LICENSE，并增加或完善了文档去重、缓存一致性、访问控制、测试及部署相关功能。

**English:** Adapted from the MIT-licensed RAG Starter with document deduplication, cache consistency improvements, access controls, tests, and deployment-related changes.


## Testing | 自动化测试

后端测试结果：**22 passed**。

Backend test suite: **22 tests passed** in the verified environment.

运行 / Run: `python -m pytest -q tests/`
