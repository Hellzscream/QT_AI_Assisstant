import chromadb

def view_chroma_contents(persist_dir="cve_chroma_db", collection_name="cve_embeddings"):
    client = chromadb.PersistentClient(path=persist_dir)

    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        print(f"Error: Could not access collection '{collection_name}'.\n{e}")
        return

    count = 0
    batch_size = 20
    total_fetched = 0

    print(f"📦 Contents of collection '{collection_name}':\n")

    while True:
        ids = [f"cve_{i}" for i in range(count, count + batch_size)]
        results = collection.get(ids=ids, include=["documents"])  

        if not results["documents"]:
            break

        for i, doc in enumerate(results["documents"]):
            doc_id = ids[i]
            print(f" {doc_id}\n{doc}\n{'-' * 80}")

        total_fetched += len(results["documents"])
        count += batch_size

    if total_fetched == 0:
        print("⚠️ No entries found in the collection.")
    else:
        print(f"\n✅ Displayed {total_fetched} documents.")

if __name__ == "__main__":
    view_chroma_contents()
