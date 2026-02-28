import threading
import queue
import time
import random

# 定义生产者线程
def producer(q, data_source):
    for item in data_source:
        print(f"生产者: 生产数据 {item}")
        q.put(item)                           # 将任务添加到队列
        time.sleep(random.uniform(0.1, 0.5))  # 模拟处理时间

# 定义消费者线程
def consumer(q):
    while True:
        item = q.get()                        # 从队列获取任务
        if item is None:                      # 检查是否收到退出信号
            break
        print(f"消费者: 消费数据 {item}")
        q.task_done()                         # 通知队列任务已经完成
        time.sleep(random.uniform(0.1, 0.5))

# 数据源，假设有10个数据
data_source = [f"数据{i}" for i in range(10)]

# 创建队列
q = queue.Queue()           # 先进先出
# q = queue.LifoQueue()     # 先进后出

# 创建并启动生产者线程和消费者线程
producer_thread = threading.Thread(target=producer, args=(q, data_source))
consumer_thread = threading.Thread(target=consumer, args=(q,))
producer_thread.start()
consumer_thread.start()
# 启动后，就会执行方法，此时有三个线程执行 Main, produce, consumer

# 等待生产者线程完成，此时会阻塞 Main，直到 produce 完成
producer_thread.join()

# produce 完成后，Main 向 queue 添加 None，给 Consumer 发送完成信号
q.put(None)

# 阻塞 Main，直到 consumer 完成
consumer_thread.join()

print("所有数据已处理完毕")