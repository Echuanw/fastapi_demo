import asyncio

async def fetch_data(task_id):
    print(f"Task {task_id}: Fetching data...")
    await asyncio.sleep(2)                        # 6 模拟耗时操作
    print(f"Task {task_id}: Data fetched")
    return f"data from task {task_id}"

async def process_data(task_id):                  # 4 并发执行3个process_data
    data = await fetch_data(task_id)              # 5 暂停当前的协程，执行调用fetch_data 协程对象
    print(f"Task {task_id}: Processing {data}")

async def main():
    tasks = [process_data(i) for i in range(3)]   # 2 创建三个协程对象
    await asyncio.gather(*tasks)                  # 3 并发执行所有任务

asyncio.run(main())                               # 1 协程执行入口，会启动事件循环并运行协程，会创建和管理事件循环的生命周期。