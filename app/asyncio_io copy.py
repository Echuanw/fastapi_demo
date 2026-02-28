import asyncio
import aiofiles

# 控制并发量的信号量
semaphore = asyncio.Semaphore(2)

async def read_file(file_path):
    async with semaphore:  # 使用信号量控制并发
        async with aiofiles.open(file_path, mode='r') as f:
            content = await f.read()
            print(f"Read from {file_path}: {content}")

async def write_file(file_path, content):
    async with semaphore:  # 使用信号量控制并发
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(content)
            print(f"Wrote to {file_path}: {content}")

async def main():
    # 文件路径和内容
    file_paths = ['app/aio/file1.txt', 'app/aio/file2.txt', 'app/aio/file3.txt']
    contents = ['Hello, World!', 'Async IO in Python', 'Controlled Concurrency']

    # 创建异步写入任务
    write_tasks = [write_file(file_path, content) for file_path, content in zip(file_paths, contents)]
    await asyncio.gather(*write_tasks)

    # 创建异步读取任务
    read_tasks = [read_file(file_path) for file_path in file_paths]
    await asyncio.gather(*read_tasks)

asyncio.run(main())