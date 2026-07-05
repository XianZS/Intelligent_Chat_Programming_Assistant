import os
from dotenv import load_dotenv
from typing import Optional

old_length = len(os.environ)
load_dotenv()
new_length = len(os.environ)
if new_length - old_length == 2:
    print("加载成功")
else:
    print("加载失败")
    raise

# 配置API
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 标识模型参数
MODEL_FLASH = "deepseek-v4-flash"
MODEL_PRO = "deepseek-v4-pro"

# 指明元模型数据
MODELS: dict[str, dict] = {
    MODEL_FLASH: {
        "name": "DeepSeek V4 Flash",
        "description": "快速、经济实惠的通用模型，适合日常对话",
        "supports_thinking": False,
    },
    MODEL_PRO: {
        "name": "DeepSeek V4 Pro",
        "description": "高性能模型，支持思维链路推理，适合复杂任务",
        "supports_thinking": True,
    },
}

# 模型默认参数的设置
DEFAULT_MODEL = MODEL_FLASH
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
MIN_MAX_TOKENS = 256
NAX_MAX_TOKENS = 8192
TOKEN_STEP = 256

# 设置模型的token估算常量
TOKEN_WARNING_THRESHOLD = 50000
CHARS_PER_TOKEN = 2


# 密钥管理
def get_api_key() -> Optional[str]:
    # 获取API密钥，以字符串形式返回
    return os.environ.get("DEEPSEEK_API_KEY")


def set_api_key(api_key: str) -> None:
    # 设置api_key，从左侧栏设置
    os.environ["DEEPSEEK_API_KEY"] = api_key


def validate_config() -> tuple[bool, str]:  # type:ignore
    api_key = get_api_key()
    if not api_key:
        return False, "api_key 读取失败，请重新加载。"
    if api_key == "example_key":
        return False, "api_key 未设置为有效api_key"
    if not api_key.startswith("sk-"):
        return False, "api_key 格式不对，应以sk-开头"
    return True, "配置成功"


# 模型查询
def get_model_label(model_id: str) -> str:
    return MODELS.get(model_id, {}).get("name", model_id)


# 是否支持思维链路
def supports_thinking(model_id: str) -> bool:
    return MODELS.get(model_id, {}).get("supports_thinking", False)


if __name__ == "__main__":
    res = supports_thinking("deepseek-v4-flash")
    print(res)
    res = supports_thinking("deepseek-v4-pro")
    print(res)
