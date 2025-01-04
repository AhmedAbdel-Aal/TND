from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document


class T5Embeddings:

    def __init__(self, device: str = "cpu") -> None:
        self.model = SentenceTransformer(
            "sentence-transformers/gtr-t5-xl", cache_folder="cache/", device=device
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.tolist()
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.model.encode([text], convert_to_numpy=True)
        return embeddings.tolist()[0]
