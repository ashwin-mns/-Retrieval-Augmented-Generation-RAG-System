# Retrieval-Augmented Generation (RAG) System

An enterprise-grade RAG system that combines LLMs with external knowledge sources to generate accurate and context-aware responses. This system mitigates hallucinations by grounding responses in local documents (PDFs and Text files).

## 🚀 Features

- **Document Ingestion**: Efficient loading and chunking of PDF and TXT files.
- **Vector Storage**: Uses **FAISS** for fast local vector storage and similarity search.
- **Robust Retrieval**: Implements a manual retrieval logic that is compatible with various LangChain versions.
- **Interactive UI**: A sleek **Streamlit** dashboard for easy document QA.
- **Accuracy**: Reduced hallucinations by using grounded context-aware prompts.

## 🛠️ Tech Stack

- **Framework**: LangChain
- **LLM**: OpenAI GPT-3.5 (or similar)
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **UI**: Streamlit
- **Language**: Python

## 🏗️ System Architecture

`User Query` → `Embedding Model` → `Vector Database (FAISS)` → `Relevant Docs` → `LLM` → `Answer`

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key

## ⚙️ Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## 🚀 Usage

### 1. Index Documents
Place your PDFs or TXT files in the `data/` directory and run the ingestion script:
```bash
python ingest.py
```

### 2. Run the Application
Launch the Streamlit interface:
```bash
streamlit run app.py
```

## 📂 Project Structure

- `data/`: Input document storage.
- `vectorstore/`: Local FAISS index.
- `ingest.py`: Document processing and indexing script.
- `rag_engine.py`: Core RAG logic and LLM chain.
- `app.py`: Streamlit frontend.
- `requirements.txt`: Project dependencies.
- `.env`: Environment variables (API keys).

## 📝 Testing

Sample data is provided in `data/company_policy.txt`. You can test the system by asking questions like:
- "What are the core hours for remote work?"
- "What is the home office stipend?"

## 🤝 Results and Discussion
The RAG system effectively reduces LLM hallucinations by providing specific document context. It ensures that answers are grounded in real enterprise data, significantly improving domain-specific accuracy.

