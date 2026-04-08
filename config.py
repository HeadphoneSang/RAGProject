import os
from pathlib import Path

top_k = 2
chat_model = "qwen3-vl-235b-a22b-thinking"
redis_host = "127.0.0.1"
redis_port = 6379
redis_histories_key = "default_memories"

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"
DATA_PATH = PROJECT_ROOT / "data"
