# Realtime RAG Pipeline

A **real-time PDF RAG (Retrieval-Augmented Generation) pipeline** built with **FastAPI, Celery, Redis, LangChain, ChromaDB, and OpenAI embeddings**.  

This project demonstrates how to handle **long-running ML or indexing jobs** with:

- **Asynchronous task processing** via Celery + Redis
- **Real-time progress updates** through Redis Pub/Sub and WebSockets
- **PDF text extraction** with PyMuPDF
- **Text chunking** using LangChain’s RecursiveCharacterTextSplitter
- **Vector embeddings & indexing** using OpenAI embeddings + ChromaDB
- **Live dashboard** to visualize extraction, chunking, and indexing progress

---

## Features

- Upload PDFs → extract text page-by-page  
- Chunk text intelligently with overlapping chunks  
- Generate embeddings and index chunks into a persistent ChromaDB collection  
- All new PDFs **append to the same global collection** for cumulative RAG knowledge  
- Real-time progress updates via **WebSocket and dashboard**  
- Long-running tasks handled asynchronously via **Celery**, making it scalable for large PDFs or multiple concurrent jobs  

---

## Tech Stack

- **Python 3.10+**  
- **FastAPI** – API server + WebSocket endpoint  
- **Celery** – asynchronous task queue for long-running jobs  
- **Redis** – message broker & pub/sub for progress updates  
- **PyMuPDF** – PDF text extraction  
- **LangChain** – recursive character chunking  
- **OpenAI** – embeddings for vectorization  
- **ChromaDB** – local vector database for RAG indexing  
- **Websocket** – for having long live connection  

---

## Usage

### Run locally with Docker Compose

```bash
git clone <repo_url>
cd realtime-rag-pipeline
docker-compose up --build
