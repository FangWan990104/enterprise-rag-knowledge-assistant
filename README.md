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

演示视频：待补充

## 项目部署

部署说明和环境变量配置将在发布前补充。

## 开源声明

基于 Dhairya Senjaliya 的 MIT Licensed RAG Starter 改造。保留原项目 LICENSE，具体改造内容将在发布前补充。
