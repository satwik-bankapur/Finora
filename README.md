# Finora — AI-Powered Personal Financial Advisor

Finora is a full-stack financial advisory application built around a **multi-agent GenAI architecture**.
It gives Indian users personalized tax optimization, investment planning, spending analysis,
and AI-generated financial advice — all grounded in real financial documents via a **RAG pipeline**.

---

## Table of Contents

- [Overview](#overview)
- [How the AI Works](#how-the-ai-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Agent Details](#agent-details)

---

## Overview

Finora takes a user's financial profile (income, investments, risk appetite, goals) and runs it through a
pipeline of specialized AI agents, each handling a specific domain. A **Coordinator Agent** orchestrates
the full pipeline, combining outputs from the Tax Agent, Investment Agent, and a RAG query to produce a
holistic, personalized financial plan via an LLM.

---

## How the AI Works

```
User Profile Input
        │
        ▼
┌───────────────────────────────────────────────┐
│              Coordinator Agent                │
│         (LangGraph orchestration)             │
│                                               │
│   ┌─────────────┐     ┌────────────────────┐  │
│   │  Tax Agent  │     │  Investment Agent  │  │
│   │             │     │                    │  │
│   │ • Slabs     │     │ • Portfolio alloc  │  │
│   │ • 80C/80D   │     │ • SIP returns      │  │
│   │ • Tax saved │     │ • Risk profiling   │  │
│   └─────────────┘     └────────────────────┘  │
│              │                │               │
│              └──────┬─────────┘               │
│                     │                         │
│          RAG Query (FAISS Vector Store)        │
│          HuggingFace all-MiniLM-L6-v2          │
│                     │                         │
│          Groq API — Llama 3.1 8B Instant       │
│                     │                         │
│        Personalized Financial Summary          │
└───────────────────────────────────────────────┘
```

---

## Features

### 🧾 Tax Optimization
- Calculates tax liability under Indian income tax slabs
- Applies Section **80C** deductions (ELSS, PPF, etc.) and **80D** (health insurance)
- Shows gross tax, tax after deductions, and **tax saved**

### 📈 Investment Planning
- Allocates monthly savings across instruments based on **risk profile** (low / medium / high)
- Instruments: ELSS, PPF, Index Funds, FD, Debt Mutual Funds, Direct Stocks
- Uses SIP future-value formula to **estimate retirement corpus**

### 💸 Spending Analysis
- Categorizes transactions and computes spending breakdown with percentages
- Detects **anomalies** (transactions 2 standard deviations above average)
- Identifies **recurring subscriptions** from transaction history
- Computes a **Financial Health Score (0–100, grade A–D)** based on savings rate,
  investment percentage, and anomaly count
- LLM generates 3 actionable insights specific to the user's spending pattern

### 📚 RAG Pipeline
- Ingests financial/tax PDFs using `PyPDFLoader`
- Chunks documents with `RecursiveCharacterTextSplitter` (500 tokens, 50 overlap)
- Embeds chunks using **HuggingFace `all-MiniLM-L6-v2`**
- Stores and queries embeddings via **FAISS** vector store
- Retrieved context grounds all LLM responses — no hallucinations on financial facts

### 📊 What-If Simulator
- Models different savings/investment scenarios
- Compare outcomes across risk profiles and time horizons

### 📄 PDF Report Generator
- Exports the complete financial plan as a formatted PDF using `reportlab`

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Orchestration | LangChain, LangGraph |
| LLM | Groq API — Llama 3.1 8B Instant |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS (CPU) |
| PDF Ingestion | LangChain `PyPDFLoader`, `pdfplumber` |
| Backend API | FastAPI + Uvicorn |
| Frontend | React, JavaScript |
| Data Validation | Pydantic v2 |
| PDF Export | ReportLab |

---

## Project Structure

```
Finora/
├── ai_core/
│   ├── rag_pipeline.py        # PDF → chunks → FAISS vector store
│   ├── rag_with_llm.py        # RAG query + LLM response generation
│   ├── coordinator_agent.py   # Orchestrates all agents into one plan
│   ├── tax_agent.py           # Indian tax slab + 80C/80D deductions
│   ├── investment_agent.py    # Portfolio allocation + SIP return estimates
│   ├── spending_analysis.py   # Transaction analysis, score, LLM insights
│   ├── whatif_simulator.py    # Scenario modeling
│   ├── report_generator.py    # PDF report export
│   └── chat.py                # Conversational AI interface
├── backend/
│   └── main.py                # FastAPI routes (/tax, /invest, /health)
├── data/
│   ├── faiss_index/           # Persisted vector store
│   ├── transactions.json      # User transaction data
│   └── users.json             # User profiles
└── requirements.txt
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com) (free tier available)

### Installation

```bash
git clone https://github.com/satwik-bankapur/Finora.git
cd Finora

pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Build the RAG Vector Store

Place your financial/tax PDF documents in `data/`, then:

```bash
python ai_core/rag_pipeline.py
```

This ingests the PDFs and saves the FAISS index to `data/faiss_index/`.

### Run the Backend API

```bash
cd backend
uvicorn main:app --reload
```

API runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run Agents Directly

```bash
# Full financial plan (tax + investment + AI advice)
python ai_core/coordinator_agent.py

# Spending analysis + financial score
python ai_core/spending_analysis.py

# Investment planning only
python ai_core/investment_agent.py
```

---

## API Reference

### `GET /health`
Returns server status.

```json
{ "status": "running" }
```

---

### `POST /tax`
Calculate tax liability and optimization.

**Request:**
```json
{
  "name": "Rahul Sharma",
  "annual_income": 800000,
  "investments": {
    "ELSS": 50000,
    "PPF": 30000,
    "health_insurance": 15000
  }
}
```

**Response:**
```json
{
  "name": "Rahul Sharma",
  "annual_income": 800000,
  "total_deductions": 95000,
  "tax_before_deductions": 75000,
  "tax_after_deductions": 58750,
  "tax_saved": 16250
}
```

---

### `POST /invest`
Get portfolio allocation and estimated retirement corpus.

**Request:**
```json
{
  "name": "Priya Patel",
  "monthly_savings": 15000,
  "risk_profile": "medium",
  "age": 28,
  "goal": "retirement"
}
```

**Response:**
```json
{
  "portfolio": {
    "ELSS": { "percentage": "30%", "monthly_amount": 4500 },
    "Index Funds": { "percentage": "20%", "monthly_amount": 3000 }
  },
  "estimated_returns": {
    "total_future_value": 4250000
  }
}
```

---

## Agent Details

### Tax Agent
Implements Indian income tax slabs (FY 2024-25 regime) and calculates:
- Gross tax on total income
- Deductions: 80C (max ₹1.5L) — ELSS, PPF, LIC; 80D (max ₹25K) — health insurance
- Net tax after deductions and tax saved

### Investment Agent
- Maps risk profiles (low/medium/high) to instrument allocations
- Uses compound SIP formula: `FV = P × [((1+r)ⁿ - 1) / r]`
- Return rates: ELSS 12%, Index Funds 11%, PPF 7.1%, FD 6.5%
- Queries RAG for document-grounded investment tips before generating LLM advice

### Spending Analysis Agent
- Aggregates transactions by category, computes % breakdown
- Anomaly detection via 2-sigma threshold
- Recurring subscription detection by transaction description frequency
- Financial Health Score: savings rate (40pts) + investment % (30pts) − anomaly penalty (up to 30pts)

### Coordinator Agent
Runs all three agents sequentially, merges results, queries RAG for relevant tax planning context,
then generates a unified 4–5 line financial summary + 3 actionable recommendations via Groq LLM.
