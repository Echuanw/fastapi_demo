# RLock 在 递归调用是使用
import threading

# 创建一个可重入锁
lock = threading.RLock()

def recursive_function(n):
    # 使用 with 语句自动管理锁的获取和释放
    with lock:
        print(f"Thread {threading.current_thread().name} is running with n = {n}")
        if n > 0:
            # 递归调用
            recursive_function(n - 1)

# 创建并启动线程
thread = threading.Thread(target=recursive_function, args=(3,))
thread.start()
thread.join()