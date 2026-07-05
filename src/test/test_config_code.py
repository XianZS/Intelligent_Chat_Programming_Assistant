import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.environ["PWD"])

from src.config import validate_config, set_api_key


# 测试无密钥
def test_not_have_api_key():
    os.environ.pop("DEEPSEEK_API_KEY", None)
    valid, msg = validate_config()
    print(f"[valid]:\n{valid};\nmessage:\n{msg}")


# 测试密钥不正确
def test_api_key_not_true():
    set_api_key("example_key")
    valid, msg = validate_config()
    print(f"[valid]:\n{valid};\nmessage:\n{msg}")


# 测试密钥格式不正确
def test_api_key_not_format():
    set_api_key("ss-dhaiodhwiofjioqh")
    valid, msg = validate_config()
    print(f"[valid]:\n{valid};\nmessage:\n{msg}")


# 测试密钥格式正确情况
def test_true():
    valid, msg = validate_config()
    print(f"[valid]:\n{valid};\nmessage:\n{msg}")


if __name__ == "__main__":
    # test_not_have_api_key()
    # test_api_key_not_true()
    # test_api_key_not_format()
    test_true()
