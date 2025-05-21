import chromadb
from sentence_transformers import SentenceTransformer

def semantic_search(
    query_text,
    top_k=1,
    persist_dir="cve_chroma_db",
    collection_name="cve_embeddings",
    model_name="all-MiniLM-L6-v2"
):
    # Load ChromaDB and embedding model
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(collection_name)
    model = SentenceTransformer(model_name)

    # Generate embedding for the query
    query_embedding = model.encode([query_text]).tolist()

    # Query ChromaDB using the vector
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents"]
    )

    print(f"\n Top {top_k} results for query: \"{query_text}\"\n")
    for i, doc in enumerate(results["documents"][0]):
        print(f"{i+1}. {doc}\n{'-' * 80}")

def get_by_ids(ids, persist_dir="cve_chroma_db", collection_name="cve_embeddings"):
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(collection_name)

    results = collection.get(ids=ids, include=["documents"])
    for doc_id, doc in zip(results["ids"], results["documents"]):
        print(f"🆔 {doc_id}\n{doc}\n{'-' * 80}")

# Example usage
if __name__ == "__main__":
    # Option 1: semantic search
    semantic_search("FortiVoice")

    # Option 2: get specific stored documents
    # get_by_ids(["cve_0", "cve_1"])
