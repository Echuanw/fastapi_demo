from concurrent.futures import ThreadPoolExecutor
import time

def task(n):
    if n == 2:
        raise ValueError("An error occurred in task 2")
    time.sleep(1)
    return f"Task {n} completed"

# 创建线程池
executor = ThreadPoolExecutor(max_workers=3)

# 提交任务
futures = [executor.submit(task, i) for i in range(5)]

# 处理任务结果和异常
for future in futures:
    try:
        result = future.result()  # 获取任务结果
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

# 关闭线程池
executor.shutdown()