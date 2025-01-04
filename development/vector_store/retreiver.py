from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from db import get_db


class GTR:
    def __init__(self):
        self.db = get_db()

    def retrieve(self, query: str, k: int = 5) -> list[tuple[Document, float]]:
        return self.db.similarity_search_with_score(query, k=k)

    @staticmethod
    def remove_par_text_prefix(text: str, case_name: str, paragraph_number: str | int):
        text = text.replace(f"{case_name}; § {paragraph_number}: ", "")
        return text
