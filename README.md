# 📄 Enterprise-Grade RAG System (Zero-Cost & URL Support)

An enterprise-ready Retrieval-Augmented Generation (RAG) system that combines LLMs with external knowledge sources. This version features a **Zero-Cost Mode** for local simulation and **Web Scraping** capabilities.

## 🌟 Key Features

- **Zero-Cost Mode**: Test the full RAG cycle (Retrieval + Grounding) for free. When no API key is provided, the system uses a smart simulator to extract answers from local documents.
- **Web Content Ingestion**: Directly scrape and index web pages by pasting a URL.
- **Document Ingestion**: Supports PDF and TXT files for local knowledge base building.
- **Performance Tracking**: Built-in latency measurement to monitor system efficiency.
- **Vector Storage**: Uses **FAISS** for lightning-fast similarity search.
- **Streamlit UI**: A professional dashboard for interactive Question Answering.

## 🏗️ System Architecture

`User Query/URL` → `Web Scraper / Doc Loader` → `Recursive Chunking` → `HuggingFace Embeddings` → `FAISS Vector Store` → `Context Retrieval` → `Smart LLM / Simulation` → `Grounded Answer`

## 🛠️ Tech Stack

- **Framework**: LangChain
- **LLM**: OpenAI GPT-3.5 (Optional) / Grounded Simulation (Free)
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Scraping**: BeautifulSoup4 & WebBaseLoader
- **UI**: Streamlit

## ⚙️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 🚀 Usage Guide

### 1. Simple QA (Free Mode)
- Start the app and ask questions about the default `company_policy.txt` (e.g., *"What is the home office stipend?"*).
- No API key is required!

### 2. Adding Web Content
- Paste a URL (e.g., a Wikipedia page) into the sidebar under **"Add Web Content"**.
- Click **"Process URL"**. The system will scrape and index the site into your local database.
- Ask questions about the website content immediately.

### 3. Professional AI Mode
- Enter your **OpenAI API Key** in the sidebar to enable GPT-3.5 powered generation for more conversational and nuanced answers.

## 📝 Testing & Accuracy
The system reduces hallucinations by grounding every answer in the **Source Documents** section. You can verify the AI's "thought process" by expanding the sources at the bottom of the result.

## 🤝 Results
- **Latency**: Measured in seconds for every query.
- **Grounding**: 100% factual accuracy by citing retrieved snippets.
- **Cost**: $0.00 using local embeddings and simulation logic.


