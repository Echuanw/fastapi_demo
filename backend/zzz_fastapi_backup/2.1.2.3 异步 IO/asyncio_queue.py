import asyncio
import random

async def producer(queue, n):
    for i in range(n):
        # 模拟生产数据
        await asyncio.sleep(random.uniform(0.1, 0.5))
        item = f'item-{i}'
        await queue.put(item)
        print(f'Produced {item}')

async def consumer(queue, consumer_id):
    while True:
        item = await queue.get()
        if item is None:
            # 生产者发出结束信号
            break
        # 模拟消费数据
        await asyncio.sleep(random.uniform(0.1, 0.5))
        print(f'Consumer {consumer_id} consumed {item}')
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    # 创建生产者任务
    producer_task = asyncio.create_task(producer(queue, 10))

    # 创建多个消费者任务
    consumer_tasks = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    # 等待生产者完成
    await producer_task

    # 向队列中放入结束信号
    for _ in consumer_tasks:
        await queue.put(None)

    # 等待所有消费者完成
    await asyncio.gather(*consumer_tasks)

asyncio.run(main())