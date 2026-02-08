import chromadb
from coach.memory.embedder import embed

client = chromadb.Client()
collection = client.get_or_create_collection(name="workout_memory")


def store_plan(plan_id: int, text: str):
    collection.add(
        ids=[str(plan_id)],
        embeddings=[embed(text)],
        documents=[text],
    )


def find_similar_plans(query: str, k: int = 3) -> list[str]:
    results = collection.query(
        query_embeddings=[embed(query)],
        n_results=k,
    )
    return results["documents"][0] if results["documents"] else []
