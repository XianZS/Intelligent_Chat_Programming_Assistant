# 生成器测试
def get_numbers():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


print("--- 普通函数：")
nums = get_numbers()
print(nums)


def generate_numbers():
    for i in range(1, 10):
        print(f"输出>>>{i}")
        yield i


print("--- 生成器generator：")
gen = generate_numbers()
print(next(gen))
print(next(gen))
print(next(gen))
