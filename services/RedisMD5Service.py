import redis
import hashlib


class RedisMD5Service:
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(
            host='localhost', port=6379, db=0
        )
        self.rc = redis.Redis(connection_pool=self.redis_pool)

        self.md5_set_key = "knowledge_storage"

    def check_md5(self, file_str):
        """
        Check if the md5 of a file is in the set.
        """
        return self.rc.sismember(self.md5_set_key, self.get_md5_from_string(file_str))

    def save_md5(self, file_str):
        """
        Save the md5 of a file.
        """
        save_success = self.rc.sadd(self.md5_set_key, self.get_md5_from_string(file_str))
        return save_success

    def get_md5_from_string(self, file_str):
        hash_md5 = hashlib.md5()
        hash_md5.update(file_str.encode("utf-8"))
        return hash_md5.hexdigest()
