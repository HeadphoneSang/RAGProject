import json
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.messages import message_to_dict, _message_from_dict
from config import redis_histories_key
from storage import RedisStorage

histories = {}


def get_history_from_session(session_id: str):
    if session_id not in histories:
        histories[session_id] = RedisChatMessageHistory(session_id)
    return histories[session_id]


class RedisChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id: str, model_key: str = "default_memories"):
        self.session_id = session_id
        self.model_key = model_key
        self.redis_storage = RedisStorage()
        self.list_key = f"{redis_histories_key}:{self.session_id}"

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        new_messages = [message_to_dict(message) for message in messages]
        self.redis_storage.push_to_list_right(self.list_key, new_messages)

    @property
    def messages(self) -> list[BaseMessage]:
        serialized_messages: list[str] = self.redis_storage.get_all_list(self.list_key)
        return [_message_from_dict(json.loads(message)) for message in serialized_messages]

    def clear(self) -> None:
        self.redis_storage.delete_key(self.list_key)
