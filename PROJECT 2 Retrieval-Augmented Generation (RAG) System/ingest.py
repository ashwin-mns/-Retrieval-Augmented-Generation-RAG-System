import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader, WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

# Configuration
DATA_PATH = "data/"
DB_FAISS_PATH = "vectorstore/db_faiss"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                 model_kwargs={'device': 'cpu'})

def create_vector_db():
    # Load documents from the data directory
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    
    # Also load txt files if any
    txt_loader = DirectoryLoader(DATA_PATH,
                                 glob='*.txt',
                                 loader_cls=TextLoader)
    documents.extend(txt_loader.load())

    if not documents:
        print("No documents found in the data directory.")
        return

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Create and save the vector store
    db = FAISS.from_documents(texts, get_embeddings())
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database saved to {DB_FAISS_PATH}")

def ingest_url(url):
    print(f"Ingesting URL: {url}")
    # Use WebBaseLoader but with a custom soup extractor to clean noise
    # Adding User-Agent to mimic a browser and bypass simple blocks
    loader = WebBaseLoader(
        url,
        header_template={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    )
    
    # Aggressive cleaning logic to remove common boilerplate
    def clean_soup(soup):
        # Remove common technical tags
        for element in soup(["nav", "footer", "script", "style", "aside", "header", "form", "svg"]):
            element.decompose()
        
        # Remove elements with common noise-related class names or IDs
        for noise_class in ["sidebar", "menu", "nav", "footer", "advertisement", "social-share", "cookie-banner", "breadcrumb"]:
            for element in soup.find_all(class_=lambda x: x and noise_class in x.lower()):
                element.decompose()
            for element in soup.find_all(id=lambda x: x and noise_class in x.lower()):
                element.decompose()
                
        return soup.get_text()

    loader.bs_get_text_kwargs = {"separator": "\n"}
    
    documents = loader.load()
    
    # Process documents to ensure clean text and meaningful content
    cleaned_docs = []
    for doc in documents:
        # Strip and remove empty lines
        lines = [line.strip() for line in doc.page_content.split("\n") if len(line.strip()) > 20]
        text = "\n".join(lines)
        
        # Only keep the document if it has significant content
        if len(text) > 100:
            doc.page_content = text
            cleaned_docs.append(doc)
    
    if not cleaned_docs:
        print("No meaningful content found at the provided URL after aggressive cleaning.")
        return
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700,
                                                   chunk_overlap=150)
    texts = text_splitter.split_documents(cleaned_docs)
    
    embeddings = get_embeddings()
    
    if os.path.exists(DB_FAISS_PATH):
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(texts)
    else:
        db = FAISS.from_documents(texts, embeddings)
        
    db.save_local(DB_FAISS_PATH)
    print(f"Vector database updated with content from {url}")

if __name__ == "__main__":
    create_vector_db()
