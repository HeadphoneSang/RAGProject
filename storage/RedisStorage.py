import redis
import json
from typing import Sequence
from config import redis_host, redis_port


class RedisStorage:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port,
            db=0,
            max_connections=50,
            decode_responses=False
        )
        self.redis_conn = redis.Redis(connection_pool=self.pool)

    def set_value(self, key, value):
        self.redis_conn.set(key, value)

    def get_value(self, key):
        return self.redis_conn.get(key)

    def get_all_list(self, key: str):
        return self.redis_conn.lrange(key, 0, -1)

    def push_to_list_right(self, key, items: Sequence[dict]) -> int:
        """
        向列表的右侧添加元素
        :param key: jian
        :param items: 添加的元素
        :return: 当前list的长度
        """
        json_list = [json.dumps(item) for item in items]
        return self.redis_conn.rpush(key, *json_list)

    def rm_key(self, key):
        self.redis_conn.delete(key)
