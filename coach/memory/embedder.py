# coach/memory/embedder.py

_model = None

def embed(text: str):
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model.encode(text).tolist()
