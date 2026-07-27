# Enterprise Knowledge Assistant

Production-grade Retrieval Augmented Generation (RAG) application built using FastAPI, Azure OpenAI and enterprise AI patterns.

## Overview

Enterprise Knowledge Assistant enables users to query internal documents using natural language.

The system retrieves relevant knowledge chunks, applies access filtering, builds grounded prompts and generates responses with citations.

---

# Architecture


User
 |
 |
FastAPI API Layer
 |
 |
Chat Service
 |
 |-------------------
 |                  |
Retriever        Conversation
 |                  |
Vector DB       PostgreSQL
 |
 |
Prompt Builder
 |
 |
Azure OpenAI
 |
 |
Response + Citations


---

# Features

## RAG Pipeline

- Document ingestion
- Text chunking
- Embeddings generation
- Vector similarity search
- Hybrid retrieval support
- Metadata filtering
- Document permissions


## LLM Integration

- Azure OpenAI SDK
- GPT deployment support
- Prompt engineering
- Streaming responses
- Conversation-aware responses


## Enterprise Chat Features

- Conversation history
- Message persistence
- Source citations
- Multi-turn conversations


## AI Safety

- Prompt injection detection
- Input validation
- Output filtering
- PII protection


## Observability

- Latency tracking
- Token usage tracking
- Retrieval metrics
- LangSmith tracing support


## Production Features

- Async FastAPI
- PostgreSQL
- Redis caching
- Docker deployment
- CI/CD pipeline


---

# Tech Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy Async
- PostgreSQL


## AI

- Azure OpenAI
- LangChain
- LangGraph
- FAISS / Vector Database


## Infrastructure

- Docker
- Redis
- Azure DevOps


---

# API Endpoints


## Chat

POST

```
/chat
```


Example:

```json
{
 "question":
 "What is the leave policy?"
}
```


Response:

```json
{
 "answer":
 "Employees receive 20 leave days.",

 "sources":[
 {
  "filename":
  "HR_policy.pdf"
 }
 ]
}
```


---

## Streaming Chat

POST

```
/chat/stream
```


Uses Server Sent Events (SSE) for token streaming.

---

# Project Structure


app/

├── knowledge

│   ├── chat

│   ├── services

│   ├── repos

│

├── shared

│   ├── ai

│   ├── cache

│   ├── guardrails


---

# Running Locally


Create environment file:


```
.env
```


Add:

```
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=
```


Install:

```
pip install -r requirements.txt
```


Run:


```
uvicorn app.main:app --reload
```


---

# Testing


Run:


```
pytest
```


---

# Future Improvements

- Kubernetes deployment
- Advanced evaluation framework
- Agentic workflows
- Multi-agent security assistant
- Automated document ingestion pipeline


---

# Author

ManojKumar K

GenAI Engineer Portfolio Project