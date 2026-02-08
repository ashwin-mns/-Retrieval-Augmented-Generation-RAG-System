import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
DB_FAISS_PATH = "vectorstore/db_faiss"

# Custom Prompt Template
custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

def load_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        # In free mode, we return None and handle the "generation" manually
        return None
    
    try:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        return llm
    except Exception:
        return None

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import time

def get_response(query):
    start_time = time.time()
    
    # Load Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    
    # Diversified Retrieval: Use MMR (Maximal Marginal Relevance) to avoid redundant results
    # fetch_k=20 means it looks at top 20 candidates, then picks the top 3 most relevant and diverse ones
    docs = db.max_marginal_relevance_search(query, k=3, fetch_k=10)
    context = "\n".join([doc.page_content for doc in docs])
    
    # Load LLM
    llm = load_llm()
    
    if llm is None:
        # FREE MODE: Generate a helpful answer from the retrieved context
        if not docs:
            answer = "I couldn't find any relevant information in your documents to answer that question."
        else:
            # We filter for relevance using a basic keyword check
            relevant_docs = []
            query_keywords = set(query.lower().split())
            
            for doc in docs:
                content_lower = doc.page_content.lower()
                # Only count meaningful keyword matches (length > 3)
                matches = [word for word in query_keywords if len(word) > 3 and word in content_lower]
                
                # REFINEMENT: Requires at least 2 matches or 50% of the keywords to be considered "Reliable"
                if len(matches) >= 2 or (len(query_keywords) > 0 and len(matches) / len(query_keywords) >= 0.5):
                    relevant_docs.append(doc)
            
            # If no docs match our keyword filter, use the raw docs but add a warning
            target_docs = relevant_docs if relevant_docs else docs
            
            answer = f"**(FREE MODE: GROUNDED RAG SIMULATION)**\n\n"
            if not relevant_docs:
                answer += "⚠️ *Note: None of the retrieved snippets perfectly match your query keywords. Showing closest matches:* \n\n"
            else:
                answer += f"I found the following information in your documents that might answer your question:\n\n"
            
            # Show snippets clearly
            for i, doc in enumerate(target_docs):
                # Increased display limit to 1000 chars to avoid cutting off answers
                snippet = doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content
                answer += f"📍 *Snippet {i+1}:* {snippet}\n\n"
            
            answer += "-- --\n*Note: This response was generated using local retrieval (Expanded Knowledge Base).* "
    else:
        # PAID MODE: Actual LLM generation
        try:
            prompt = ChatPromptTemplate.from_template(custom_prompt_template)
            chain = prompt | llm | StrOutputParser()
            answer = chain.invoke({"context": context, "question": query})
        except Exception as e:
            # Fallback to Free Mode logic if the API call fails
            answer = f"**(FREE MODE FALLBACK - API ERROR)**\n\n"
            answer += f"I tried to use the API key, but it failed. Here is the information from your documents:\n\n"
            for i, doc in enumerate(docs):
                snippet = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                answer += f"📍 *Snippet {i+1}:* {snippet}\n\n"
            answer += f"\n*Original Error: {str(e)}*"
    
    end_time = time.time()
    latency = round(end_time - start_time, 2)
    
    return {
        "result": answer,
        "source_documents": docs,
        "latency": latency
    }

if __name__ == "__main__":
    # Quick CLI test
    query = "What are the core hours for remote work?"
    res = get_response(query)
    print(res["result"])
