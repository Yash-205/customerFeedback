# 🧠 Customer Intelligence Engine (RLM-Powered)

Experience the power of **Recursive Language Modeling (RLM)** and **Agentic Graph RAG**. This system turns fragmented customer feedback into high-level strategic intelligence using a 5-layer autonomous stack.

## 🚀 Overview

The Customer Intelligence Engine is designed to solve "Context Fragmentation" in traditional RAG systems. By using **DSPy RLM**, the system creates a hierarchy of understanding, allowing users to ask both granular and strategic questions about their feedback data.

### Key Features:
- **Hierarchical RLM**: LLM-driven recursive reasoning to synthesize insights.
- **Agentic Analysis**: LangGraph-powered agent that navigates Vector and Graph memories.
- **Real-time Feedback**: Multi-step progress tracking for ingestion and queries.
- **Persistent Memory**: Historical chat storage with ChatGPT-style interface.

---

## 🛠️ Project Structure

```
.
├── ai-engine/          # FastAPI Backend (Python)
│   ├── app/            # Core logic (RLM Agents, Storage, API)
│   ├── start.sh        # Quickstart script
│   └── ARCHITECTURE.md # Detailed technical deep-dive
└── web-app/            # Next.js Frontend (TypeScript)
    └── src/            # UI Components and Services
```

---

## 🏁 Quickstart

### 1. Backend (AI Engine)
Detailed instructions in `ai-engine/DEPLOYMENT.md`.

```bash
cd ai-engine
# Configure .env with GROQ_API_KEY, QDRANT_URL, and NEO4J_URL
./start.sh
```

### 2. Frontend (Web App)
```bash
cd web-app
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to start analyzing feedback.

---

## 🧠 Hierarchical RLM vs Traditional RAG

| Traditional RAG | Our Hierarchical RLM |
| :--- | :--- |
| **Fragmented**: Chunks are isolated. | **Contextual**: Chunks are summarized into themes. |
| **Rigid**: Fixed retrieval rules. | **Adaptive**: Agent decides the best strategy. |
| **Shallow**: Hard to answer "What are the trends?" | **Deep**: Built-in global theme aggregation. |

---

## 📊 Tech Stack

- **Intelligence**: DSPy, LangGraph, Groq (Llama-3.1-8B)
- **Memory**: Qdrant (Vector), Neo4j (Graph)
- **UI**: Next.js, Tailwind CSS, TanStack Query

---

## 📜 Documentation
For a deep dive into the system design, check out [ai-engine/app_architecture.md](ai-engine/app_architecture.md).
