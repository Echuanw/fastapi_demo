import threading
import queue
import time

def worker(priority_queue):
    while not priority_queue.empty():
        priority, task = priority_queue.get()
        print(f"处理优先级 {priority} 的任务: {task}")
        time.sleep(1)  # 模拟任务处理时间
        priority_queue.task_done()

# 创建 PriorityQueue
priority_queue = queue.PriorityQueue()

# 添加任务到队列，优先级越小越优先
tasks = [(2, "任务A"), (1, "任务B"), (3, "任务C")]
for task in tasks:
    priority_queue.put(task)

# 创建并启动工作线程
thread = threading.Thread(target=worker, args=(priority_queue,))
thread.start()

# 等待所有任务完成
priority_queue.join()
print("所有任务已处理完毕")