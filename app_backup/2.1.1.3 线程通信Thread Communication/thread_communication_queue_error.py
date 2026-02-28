import threading
import queue
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建一个队列用于线程间通信
exception_queue = queue.Queue()

def worker(thread_id):
    try:
        logging.info(f"线程 {thread_id} 开始工作")
        # 模拟工作过程
        time.sleep(2)
        # 模拟异常
        if thread_id == 1:
            raise ValueError("模拟异常：无效值")
        logging.info(f"线程 {thread_id} 完成工作")
    except Exception as e:
        # 将异常信息放入队列
        exception_queue.put((thread_id, e))

def main():
    # 创建并启动线程
    threads = []
    for i in range(2):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 处理队列中的异常
    while not exception_queue.empty():
        thread_id, exception = exception_queue.get()
        logging.error(f"线程 {thread_id} 遇到异常: {exception}")

if __name__ == "__main__":
    main()