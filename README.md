# Autonomous-Research-Analyst

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-121212?style=flat-square)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4?style=flat-square&logo=google)](https://deepmind.google/technologies/gemini/)
[![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

An AI-powered research assistant designed to ingest complex reports, research papers, and web data to generate high-fidelity insights, structured reports, and presentation slides using a state-of-the-art **RAG (Retrieval-Augmented Generation)** pipeline.

---

## 🏗️ System Architecture

The application is built with a decoupled architecture, ensuring scalability and ease of deployment.

```mermaid
graph TD
    subgraph "Frontend (Streamlit)"
        UI[User Interface]
        UC[Upload Component]
        QC[Query Component]
        RC[Report Generator UI]
    end
    subgraph "Backend (FastAPI)"
        API[FastAPI Routes]
        DP[Document Processor]
        RM[RAG Manager]
        RG[Report Generator Core]
    end

    subgraph "Storage & Intelligence"
        VDB[(ChromaDB)]
        EMB[[HuggingFace Embeddings]]
        LLM[Google Gemini API]
    end

    UI --> API
    API --> DP
    DP --> EMB --> VDB
    API --> RM
    RM --> VDB
    RM --> LLM
    API --> RG
```

---

## 🔄 Core Workflows

### 1. Data Ingestion Flow
Transforming raw data into searchable knowledge.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant DP as Document Processor
    participant EMB as Embeddings (HuggingFace)
    participant VDB as ChromaDB

    User->>API: Upload PDF/DOCX or Submit URL
    API->>DP: Parse & Chunk Content
    DP->>EMB: Generate Vector Embeddings
    EMB->>VDB: Store Chunks with Metadata
    VDB-->>API: Success Response
    API-->>User: Ingestion Complete
```

### 2. Research & Analysis (RAG) Flow
Context-aware answering with citation tracking.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant VDB as ChromaDB
    participant LLM as Google Gemini
    
    User->>API: Ask Research Question
    API->>VDB: Semantic Search (Top K)
    VDB-->>API: Relevant Context + Sources
    API->>LLM: Prompt (Context + Question)
    LLM-->>API: Structured Answer
    API-->>User: Answer with Citations
```

---

## ✨ Key Features

- **🚀 Multi-Source Ingestion**: Support for PDF, DOCX, and direct URL crawling.
- **🧠 Advanced RAG**: Powered by LangChain and local HuggingFace embeddings (`all-MiniLM-L6-v2`) for cost-efficient vector search.
- **💎 Premium UI**: A modern, dark-themed dashboard built with Streamlit for a seamless user experience.
- **📄 Professional Exports**: Instantly convert research findings into PDF reports or PowerPoint presentations.
- **🔗 Citation Tracking**: Every answer includes references to the source material to ensure factual accuracy.
- **🐳 Dockerized**: Fully containerized setup for consistent performance across environments.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Plotly (for data visualization).
- **Backend**: FastAPI, Uvicorn.
- **Orchestration**: LangChain.
- **Vector Store**: ChromaDB.
- **LLM**: Google Gemini 1.5 Flash.
- **Embeddings**: SentenceTransformers (Local CPU optimized).
- **Document Parsing**: PyPDF, python-docx, Beautiful Soup.
- **Reporting**: FPDF2, Python-PPTX.

---

### Manual Installation (Development)

**1. Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**2. Frontend Setup**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 📖 Usage Guide

1. **Ingest Knowledge**: Use the **Ingestion** tab to upload your research materials or paste relevant URLs.
2. **Deep Analysis**: Switch to the **Analysis** tab to ask complex questions. The system will retrieve context and provide cited answers.
3. **Generate Reports**: In the **Reports** tab, review your insights and export them to PDF or Markdown for stakeholders.

---
