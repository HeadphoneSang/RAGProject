from config import top_k
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from config import CHROMA_DB_PATH


class VectorStoreService:
    def __init__(self, embedding):
        self.top_k = top_k
        self.chroma = Chroma(
            collection_name="knowledge_base",
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding,
        )

    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={"k": self.top_k})


if __name__ == "__main__":
    vector_service = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4"))
    list_doc = vector_service.get_retriever().invoke("你好身高190cm，体重160斤，穿什么尺码比较合适？")
    print(list_doc)
