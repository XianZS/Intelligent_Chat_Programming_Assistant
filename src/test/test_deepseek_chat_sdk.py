# DEEPSEEK API 第一次调用尝试
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.environ["PWD"])

from src.config import DEEPSEEK_BASE_URL  # type:ignore
from openai import OpenAI  # type:ignore


def _create_client(api_key: str) -> OpenAI:
    """
    创建 deepseek api 客户端
    """
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_once(api_key: str, prompt: str) -> None:
    """
    发送一次对话，返回回复文本（非流式返回结果）
    """
    client = _create_client(api_key)
    res = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4096,
    )
    print(res.choices[0].message.content)


if __name__ == "__main__":
    chat_once(os.environ["DEEPSEEK_API_KEY"], "简单介绍一下python")
