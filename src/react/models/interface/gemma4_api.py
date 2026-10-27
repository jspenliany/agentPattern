import os
import threading
from openai import OpenAI


class LLMClientSingleton:
    _instance = None
    _initialized = False
    _lock = threading.Lock()  # 保证高并发场景下的线程安全

    def __new__(cls, *args, **kwargs):
        # 双重检查锁定（Double-Checked Locking），避免每次获取实例都加锁
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        base_url: str = "http://0.0.0.0:8000/v1",
        api_key: str = "no-key-required",
    ):
        if not LLMClientSingleton._initialized:
            with LLMClientSingleton._lock:
                if not LLMClientSingleton._initialized:
                    self.setup_client(base_url, api_key)
                    LLMClientSingleton._initialized = True

    def setup_client(self, base_url: str, api_key: str):
        """初始化 OpenAI 客户端

        支持优先读取环境变量（生产级最佳实践），若无则使用默认入参
        """
        target_base_url = os.getenv("LLM_BASE_URL", base_url)
        target_api_key = os.getenv("LLM_API_KEY", api_key)

        # 初始化底层 client 实例，可根据需要配置超时时间
        self._client = OpenAI(
            base_url=target_base_url,
            api_key=target_api_key,
            timeout=60.0,  # 大模型推理建议设置超时时间
            max_retries=2,  # 请求失败自动重试次数
        )

    @classmethod
    def get_client(cls) -> OpenAI:
        """获取内部封装的 OpenAI 客户端实例"""
        return cls()._client


# 导出全局单例客户端，业务代码可直接 import 使用
llm_client: OpenAI = LLMClientSingleton.get_client()