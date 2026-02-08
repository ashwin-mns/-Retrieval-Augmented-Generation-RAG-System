import os
from ingest import ingest_url, create_vector_db

def seed_data():
    """
    Ingest a variety of high-quality sources to improve the knowledge base.
    """
    print("="*50)
    print("BATCH DATA INGESTION: BUILDING KNOWLEDGE BASE")
    print("="*50)
    
    # 1. First, index the local 'data/' directory (PDFs/TXTs)
    print("\n[Phase 1] Indexing local files...")
    create_vector_db()
    
    # 2. Ingest dozens of high-quality URLs for deep knowledge
    # Using a variety of technical domains to reach high volume
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Natural_language_processing",
        "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "https://en.wikipedia.org/wiki/Large_language_model",
        "https://en.wikipedia.org/wiki/Prompt_engineering",
        "https://en.wikipedia.org/wiki/Vector_database",
        "https://en.wikipedia.org/wiki/Cloud_computing",
        "https://en.wikipedia.org/wiki/Software_development",
        "https://en.wikipedia.org/wiki/Google_Developers",
        "https://en.wikipedia.org/wiki/Clothes_iron",
        "https://en.wikipedia.org/wiki/Home_appliance",
        "https://en.wikipedia.org/wiki/Consumer_electronics"
    ]
    
    # Adding more specific technical blog/doc URLs if needed
    # (Simplified for now to avoid long wait times, but extensible)
    
    print(f"\n[Phase 2] Ingesting {len(urls)} primary technical domains...")
    success_count = 0
    for i, url in enumerate(urls):
        try:
            print(f"({i+1}/{len(urls)}) Ingesting: {url}")
            ingest_url(url)
            success_count += 1
        except Exception as e:
            print(f"Failed to ingest {url}: {e}")
            
    print("\n" + "="*50)
    print(f"KNOWLEDGE BASE EXPANDED SUCCESSFULY ({success_count} sources)")
    print("="*50)

if __name__ == "__main__":
    seed_data()
