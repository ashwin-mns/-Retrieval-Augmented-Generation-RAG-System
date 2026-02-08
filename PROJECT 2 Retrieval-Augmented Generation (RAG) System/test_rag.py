import time
from rag_engine import get_response

def evaluate_rag():
    test_queries = [
        "What are the core hours for remote work?",
        "What is the home office stipend?",
        "How do I access the VPN?",
        "Who should I contact for HR questions?"
    ]
    
    print("="*50)
    print("RAG SYSTEM EVALUATION: ACCURACY & LATENCY")
    print("="*50)
    
    total_latency = 0
    
    for i, query in enumerate(test_queries):
        print(f"\n[Test {i+1}] Query: '{query}'")
        
        # Measure latency
        res = get_response(query)
        latency = res["latency"]
        total_latency += latency
        
        print(f"Result: {res['result'][:200]}...") # Print first 200 chars
        print(f"Sources Found: {len(res['source_documents'])}")
        print(f"Latency: {latency}s")
        
        # Check if relevant content is found (basic accuracy check)
        if len(res['source_documents']) > 0:
            print("Status: ✅ Retrieval Success")
        else:
            print("Status: ❌ Retrieval Failed")
            
    avg_latency = total_latency / len(test_queries)
    print("\n" + "="*50)
    print(f"SUMMARY")
    print(f"Avg Latency: {round(avg_latency, 2)}s")
    print("="*50)

if __name__ == "__main__":
    evaluate_rag()
