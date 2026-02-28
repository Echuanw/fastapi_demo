# 假设我们有一个资源（例如数据库连接池），最多允许三个线程同时访问。我们可以使用 Semaphore 来控制对该资源的访问。
import threading
import time

# 创建一个信号量，最多允许3个线程同时访问
semaphore = threading.Semaphore(value=3)

def access_resource(thread_id):
    print(f"Thread-{thread_id} is waiting to access the resource.")
    # 使用上下文管理器语法
    with semaphore:
        print(f"Thread-{thread_id} has accessed the resource.")
        time.sleep(2)  # 模拟资源访问
    print(f"Thread-{thread_id} has released the resource.")

# 创建多个线程
threads = []
for i in range(5):
    thread = threading.Thread(target=access_resource, args=(i,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("All threads have finished.")