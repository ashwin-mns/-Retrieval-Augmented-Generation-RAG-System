import streamlit as st
from rag_engine import get_response
import os
import time

# Set page configuration
st.set_page_config(page_title="Enterprise RAG System", layout="centered")

st.title("📄 Enterprise Document QA System")
st.markdown("---")

# Instructions
st.sidebar.header("About")
st.sidebar.info("""
This RAG system allows you to ask questions about your documents.
It uses FAISS for vector storage and LangChain for retrieval.
""")

st.sidebar.header("Setup")
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    # Clear the environment variable if it exists to force Zero-Cost Mode
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    st.sidebar.warning("💡 **Zero-Cost Mode Active**: No API key detected. The system will simulate answers using local document snippets for free.")

# Check if vectorstore exists
if not os.path.exists("vectorstore/db_faiss"):
    st.warning("⚠️ Vector database not found. Please run indexing to start.")
    if st.button("Index Default Data"):
        with st.spinner("Indexing documents..."):
            import subprocess
            subprocess.run(["python", "ingest.py"])
            st.success("Indexing complete! Refreshing...")
            st.rerun()
else:
    if st.sidebar.button("🗑️ Clear Knowledge Base", help="This will delete all indexed documents and URLs."):
        import shutil
        if os.path.exists("vectorstore"):
            shutil.rmtree("vectorstore")
            st.sidebar.success("Knowledge base cleared! Refreshing...")
            time.sleep(1)
            st.rerun()

# URL Support
st.sidebar.header("Add Web Content")
url_to_add = st.sidebar.text_input("Paste URL here:", placeholder="https://example.com")
if st.sidebar.button("Process URL"):
    if url_to_add:
        # Set User-Agent to avoid scraping issues
        os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        with st.sidebar.status(f"Scraping {url_to_add}...", expanded=True) as status:
            try:
                from ingest import ingest_url
                ingest_url(url_to_add)
                status.update(label="✅ Content Indexed Successfully!", state="complete", expanded=False)
                st.sidebar.success(f"Added: {url_to_add}")
                # No rerun here so message stays visible
            except Exception as e:
                status.update(label="❌ Failed", state="error")
                st.sidebar.error(f"Error: {e}")
    else:
        st.sidebar.warning("Please enter a URL.")

# User input
query = st.text_input("Ask a question about your documents:", placeholder="e.g., What are the core hours for remote work?")

if query:
    with st.spinner("Searching for answers..."):
        try:
            response = get_response(query)
            
            st.subheader("Answer:")
            st.write(response["result"])
            
            # Display metrics
            st.info(f"⏱️ **Latency:** {response['latency']} seconds")
            
            with st.expander("Source Documents"):
                for i, doc in enumerate(response["source_documents"]):
                    st.markdown(f"**Source {i+1}:**")
                    st.write(doc.page_content)
                    st.markdown(f"*Metadata: {doc.metadata}*")
                    st.markdown("---")
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Built with LangChain, FAISS, and Streamlit.")
