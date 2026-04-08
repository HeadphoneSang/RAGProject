import os.path

from services import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import chat_model
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from components import RedisChatMessageHistory, get_history_from_session
from config import PROJECT_ROOT


def get_emotion_prompts():
    prompts = []
    with open(os.path.join(PROJECT_ROOT, "data", "emotion_prompts.txt"), "r", encoding="utf-8") as f:
        for line in f:
            prompts.append(("system", line.strip()))
    return prompts


class RagService:
    def __init__(self):
        self.vector_service = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4"))
        self.model = ChatTongyi(model=chat_model)
        self.emotion_prompts = get_emotion_prompts()
        print(self.emotion_prompts)
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "请根据用户的历史消息回答问题："),
            MessagesPlaceholder(variable_name="chat_history"),
            ("assistant", "在考虑历史消息的情况下，我会根据系统提供的相关信息回答用户的问题："),
            MessagesPlaceholder(variable_name="knowledge"),
            ("system", "请回答用户问题,用暴躁的语气，比如:"),
            *self.emotion_prompts,
            ("system", "请回复用户的问题,如果不想回复可以不回复："),
            ("user", "{question}")
        ])
        self.base_chain = self.get_chain()

    def get_chain(self):
        def transform_knowledge(inputs: list):
            return [("assistant", document.page_content) for document in inputs]

        def print_data(data):
            print(data.to_string())
            return data

        chain = RunnableParallel(
            {
                "question": RunnableLambda(lambda data: data["question"]),
                "chat_history": RunnableLambda(lambda data: data["chat_history"]),
                "knowledge": RunnableLambda(
                    lambda data: data["question"]) | self.vector_service.get_retriever() | RunnableLambda(
                    transform_knowledge)
            }
        ) | self.chat_prompt | RunnableLambda(print_data) | self.model | StrOutputParser()
        wHistoriesChain = RunnableWithMessageHistory(
            chain,
            input_messages_key="question",
            history_messages_key="chat_history",
            get_session_history=get_history_from_session
        )
        return wHistoriesChain


if __name__ == "__main__":
    rag_service = RagService()
    session_config = {
        "configurable": {
            "session_id": "wang"
        }
    }
    response = rag_service.base_chain.stream({"question": "再具体一点，什么码，什么颜色，什么款式，简单的回答我"},
                                             config=session_config)
    for chunk in response:
        print(chunk, end="", flush=True)
