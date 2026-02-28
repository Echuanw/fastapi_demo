import threading
import time

def worker(event):
    print("Worker: 等待事件...")
    event.wait()                  # 等待 _flag = True
    print("Worker: 事件已设置，继续执行...")

def main():
    event = threading.Event()     # 创建 event 对象， _flag = Flase
    thread = threading.Thread(target=worker, args=(event,))
    thread.start()

    print("Main: 等待 3 秒后设置事件")
    time.sleep(3)
    event.set()                    # 这里，将 event _flag = True，之前阻塞的 worker 就可以继续执行。

    thread.join()
    print("Main: 线程已完成")

if __name__ == "__main__":
    main()