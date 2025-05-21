import chromadb
from sentence_transformers import SentenceTransformer

def embed_and_store_from_entries(entries, persist_dir="cve_chroma_db"):
    if not entries:
        print("❌ No CVE entries provided.")
        return

    # ✅ NEW ChromaDB client API
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection("cve_embeddings")

    model = SentenceTransformer('all-MiniLM-L6-v2')

    texts = [entry.strip() for entry in entries if entry.strip()]
    ids = [f"cve_{i}" for i in range(len(texts))]

    print("🔄 Generating embeddings...")
    embeddings = model.encode(texts).tolist()

    print("💾 Storing in ChromaDB...")
    collection.add(documents=texts, embeddings=embeddings, ids=ids)
    print(f"✅ Stored {len(texts)} entries in ChromaDB.")
