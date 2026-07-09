# 实现流式对话生成器
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.environ["PWD"])

from collections.abc import Generator

from openai import OpenAI
from openai import (
    AuthenticationError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
)
from src.config import DEEPSEEK_BASE_URL, MODEL_FLASH, MODEL_PRO


def _create_client(api_key: str) -> OpenAI:
    # 创建 deepseek api 客户端
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_stream(
    api_key: str,
    message: list[dict[str, str]],
    model: str = MODEL_FLASH,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    enable_thinking: bool = False,
) -> Generator[dict, None, None]:
    # 实现流式对话生成器
    try:
        client = _create_client(api_key)
        # 设置 API 调用参数
        kwargs: dict = {
            "model": model,
            "messages": message,
            "stream": True,
            "max_tokens": max_tokens,
        }
        # 是否支持思维链路模式
        if enable_thinking and model == MODEL_PRO:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        else:
            kwargs["temperature"] = temperature
        # 发起 API 请求
        response = client.chat.completions.create(**kwargs)
        for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta is None:
                continue
            # 获取思维链路回复内容
            reasoning = getattr(delta, "reasoning_content", None) or ""
            if reasoning:
                yield {"type": "reasoning", "text": reasoning}
            # 获取普通回复内容
            if delta.content:
                yield {"type": "content", "text": delta.content}
        yield {"type": "done", "usage": None}
    except AuthenticationError:
        yield {
            "type": "error",
            "message": "API 密钥无效，请检查后重试，可以前往 platform.deepseek.com/api_keys 获取密钥",
        }
    except RateLimitError:
        yield {"type": "error", "message": "API 请求频率超限，请稍等片刻后重试"}
    except APITimeoutError:
        yield {"type": "error", "message": "API 请求超时，请检查网络连接后重试"}
    except APIConnectionError:
        yield {
            "type": "error",
            "message": "API 无法连接到 DeepSeek 服务器，请检查网络连接",
        }
    except Exception as e:
        error_msg = str(e)
        if "status_code" in error_msg and "400" in error_msg:
            yield {"type": "error", "message": "请求参数错误，请尝试清除对话历史后重试"}
        elif "status_code" in error_msg and "500" in error_msg:
            yield {"type": "error", "message": "DeepSeek 服务器内部错误，请稍后重试"}
        else:
            yield {"type": "error", "message": "发生未知错误:{error_msg}"}
