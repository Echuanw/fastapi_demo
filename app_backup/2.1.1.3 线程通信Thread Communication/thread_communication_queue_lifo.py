# LifoQueue 实现了后进先出（LIFO）的队列行为，类似于堆栈。以下是一个简单的示例，模拟一个需要回溯的任务处理场景LifoQueue
import threading
import queue
import time

def worker(lifo_queue):
    while not lifo_queue.empty():
        task = lifo_queue.get()
        print(f"处理任务: {task}")
        time.sleep(1)  # 模拟任务处理时间
        lifo_queue.task_done()

# 创建 LifoQueue
lifo_queue = queue.LifoQueue()

# 添加任务到队列
for i in range(5):
    lifo_queue.put(f"任务{i}")

# 创建并启动工作线程
thread = threading.Thread(target=worker, args=(lifo_queue,))
thread.start()

# 等待所有任务完成
lifo_queue.join()
print("所有任务已处理完毕")