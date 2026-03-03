from concurrent.futures import ThreadPoolExecutor

# 创建一个线程池，最大线程数为5
executor = ThreadPoolExecutor(max_workers=5)

def task(n):
    print(f"Processing {n}")
    return n * n

# submit() 方法用于提交单个任务。
future = executor.submit(task, 5)

# 获取任务结果
result = future.result()
print(f"Result: {result}")

print(f"################################")

# map() 提交多个任务
numbers = [1, 2, 3, 4, 5]
results = executor.map(task, numbers)

# 获取所有任务结果
for result in results:
    print(f"Result: {result}")

executor.shutdown(wait=True)