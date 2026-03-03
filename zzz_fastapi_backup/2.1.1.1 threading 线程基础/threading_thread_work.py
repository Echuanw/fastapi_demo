# 使用 Thread 创建线程，调用函数并传参
# 线程设置名字，设置为守护线程
# 模拟线程池
# 启动线程
# 线程启动，同时阻塞主线程
# 使用 lock 避免资源竞争

import threading
import time

# 剩余票数
tickets = 10

# 创建锁对象
lock = threading.Lock()
# 日志列表
log = []

def buy_ticket(user_id):
    global tickets
    with lock:            # lock 确保在检查和更新票数时不会出现竞争条件
        if tickets > 0:
            tickets -= 1
            log_entry = f"用户 {user_id} 成功购买了一张票，剩余票数: {tickets}"
        else:
            log_entry = f"用户 {user_id} 购买失败，票已售罄"
        log.append(log_entry)
        print(log_entry)
        print(f"\tWorker thread is: {threading.current_thread().name}") 
        print(f"\tActive threads: {threading.active_count()}") 
        print(f"\tWorker thread id: {threading.get_ident()}")


def log_writer():
    while True:
        if log:
            with lock:
                # 模拟写入日志
                while log:
                    entry = log.pop(0)
                    print(f"[SUCCESS LOG]: {entry}")
        time.sleep(1)

# 创建日志线程并设置为守护线程
log_thread = threading.Thread(target=log_writer)
log_thread.name = "daemon_log_thread"
log_thread.daemon = True          
log_thread.start()

# 首先有个优先客户抢票（使用主线程）

buy_ticket(123)

# 创建多个线程模拟多个用户抢票
threads = []
for i in range(15):  # 假设有15个用户尝试购买票
    thread = threading.Thread(target=buy_ticket, args=(i,))      # 创建线程
    thread.name = "normal_user_thread_" + str(i)
    threads.append(thread)                                       # 线程就绪
    thread.start()                                               # 线程执行

# Main Thread 会等待所有线程完成
for thread in threads:
    thread.join()

# 给日志线程一些时间来处理剩余的日志
# 抢票的例子中，daemon 属性并不适用，因为我们希望所有用户线程都能完成其购票尝试，而不是在主线程结束时被强制终止。我们需要确保所有线程都执行完毕，以便正确地模拟所有用户的购票行为。因此，在这个例子中不建议使用守护线程，这里只是演示
time.sleep(5)