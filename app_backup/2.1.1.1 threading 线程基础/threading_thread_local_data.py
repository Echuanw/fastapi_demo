import threading

# 创建线程局部数据对象
# 每个线程调用后都有自己独立的一份数据副本，这些数据在不同线程之间是隔离的。
thread_local_data = threading.local()

def process_user_session(user_id):
    # 为每个线程设置独立的用户 ID
    thread_local_data.user_id = user_id
    # 模拟处理用户会话
    print(f"线程 {threading.current_thread().name} 正在处理用户 {thread_local_data.user_id} 的会话")

# 创建多个线程模拟处理不同用户的会话
threads = []
user_ids = [101, 102, 103, 104, 105]  # 假设有5个用户
for user_id in user_ids:
    thread = threading.Thread(target=process_user_session, args=(user_id,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()