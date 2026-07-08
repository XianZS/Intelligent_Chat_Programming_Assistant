# 流式对话生成器
import sys
import os
from dotenv import load_dotenv
from openai.lib.azure import API_KEY_SENTINEL

load_dotenv()

sys.path.append(os.environ["PWD"])
from src.config import DEEPSEEK_BASE_URL, MODEL_FLASH, MODEL_PRO

from collections.abc import Generator
from openai import OpenAI, responses

# API 密钥无效或者过期
from openai import AuthenticationError

# 请求频率超出限制
from openai import RateLimitError

# 请求超时错误
from openai import APITimeoutError

# 网络链接失败
from openai import APIConnectionError


def _create_client(api_key: str) -> OpenAI:
    # 创建deepseek api client 对象
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
    # dict-type:
    # {"type":"reasoning","text":"..."} 思维链路推理片段
    # {"type":"content","text":"..."} 回复内容片段
    # {"type":"done","text":"..."} 流式信息输出结束
    # {"type":"error","text":"..."} 错误信息
    try:
        client = _create_client(api_key)
        # args kwargs
        # 顺序传参 键值对传参
        kwargs: dict = {
            "model": model,
            "messages": message,
            "stream": True,
            "max_tokens": max_tokens,
        }
        # flash model 和 pro model 最主要的区别是什么？
        # 后者支持思维链路模式
        if enable_thinking and model == MODEL_PRO:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        else:
            kwargs["temperature"] = temperature
        # 发起流式 API 请求
        response = client.chat.completions.create(**kwargs)
        for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta is None:
                continue
            reasoning = getattr(delta, "reasoning_content", None) or ""
            if reasoning:
                yield {"type": "reasoning", "text": reasoning}
            if delta.content:
                yield {"type": "content", "text": delta.content}
        yield {"type": "done", "usage": None}
    except AuthenticationError:
        yield {"type": "error", "message": "API 密钥无效，请检查密钥是否正确，或前往 platform.deepseek.com 重新生成"}
    except RateLimitError:
        yield {"type": "error", "message": "请求频率超限，请稍后重试"}
    except APITimeoutError:
        yield {"type": "error", "message": "api请求超时"}
    except APIConnectionError:
        yield {"type": "error", "message": "api网络不通"}
    except Exception as e:
        print(e)
        error_msg = str(e)
        if "status_code" in error_msg and "400" in error_msg:
            # 请求参数错误
            yield {"type": "error", "message": "api请求参数错误"}
        elif "status_code" in error_msg and "500" in error_msg:
            yield {"type": "error", "message": "api服务器内部错误"}
        else:
            yield {"type": "error", "message": "api发生了未知错误"}
