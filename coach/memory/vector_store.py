# coach/memory/vector_store.py

_embedder = None
_collection = None

def _init():
    global _embedder, _collection

    if _embedder is None:
        from coach.memory.embedder import embed
        from chromadb import Client

        _embedder = embed
        client = Client()
        _collection = client.get_or_create_collection("workout_plans")

def store_plan(plan_id: int, text: str):
    _init()
    embedding = _embedder(text)
    _collection.add(
        ids=[str(plan_id)],
        documents=[text],
        embeddings=[embedding],
    )

def find_similar_plans(query: str, k: int = 3):
    _init()
    embedding = _embedder(query)
    results = _collection.query(
        query_embeddings=[embedding],
        n_results=k,
    )
    return results.get("documents", [[]])[0]
