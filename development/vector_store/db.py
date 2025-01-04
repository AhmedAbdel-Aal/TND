from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from embedder import T5Embeddings


def get_db():
    db = Chroma(
        persist_directory="./data/chroma_gtr_t5_xl_db",
        embedding_function=T5Embeddings(),
    )
    print("DB Loaded - Entries:", db._collection.count())
    return db
