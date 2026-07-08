import sys
import os
from dotenv import load_dotenv

load_dotenv()
# 确保项目根目录在 sys.path 中
sys.path.append(os.environ["PWD"])

print(len(os.environ))

api_key=os.environ.get("DEEPSEEK_API_KEY")
print(f"[api_key]:{api_key}")

test_key=os.environ.get("TEST_KEY")
print(f"[test_api]:{test_key}")

# D:\code\py_item\Intelligent_Chat_Programming_Assistant\src>python test.py
# [api_key]:example-key
# [test_api]:测试内容
