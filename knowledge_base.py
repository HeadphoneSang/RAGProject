import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services import RedisMD5Service
from datetime import datetime


class KnowledgeBaseService:
    def __init__(self):
        os.makedirs("./chroma_db", exist_ok=True)
        self.chroma = Chroma(
            collection_name="knowledge_base",
            persist_directory="./chroma_db",
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
        )
        self.max_text_len = 500
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_text_len, chunk_overlap=100, length_function=len, separators=["\n\n", "\n", " ", "",
                                                                                              "?", "!", ".", ":", ";"
                , "？", "。", "！", "；", "："
                , ",", "，", "、", "."]
        )
        self.md5_service = RedisMD5Service()

    def upload_by_str(self, file_str: str, file_name: str) -> {"status": bool, "msg": str}:
        if not self.md5_service.save_md5(file_str):
            return {"status": False, "msg": "文件已经存在于知识库中!"}
        if len(file_str) > self.max_text_len:
            knowledge_chunks: list[str] = self.splitter.split_text(file_str)
        else:
            knowledge_chunks = [file_str]
        metadata = {
            "source": file_name,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "system",
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for i in range(len(knowledge_chunks))]
        )
        return {"status": True, "msg": "上传知识文件成功!"}



