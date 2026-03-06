# 超时自动取消，抛出 asyncio.TimeoutError
import asyncio
import random

async def fetch_data(url):
    print(f"开始从 {url} 获取数据")
    await asyncio.sleep(random.uniform(2.0, 3.0))
    print(f"从 {url} 获取数据完成")
    return f"数据来自 {url}"

async def main():
    urls = ["http://example.com/a", "http://example.com/b", "http://example.com/c"]
    tasks = [asyncio.create_task(fetch_data(url)) for url in urls]

    try:
        results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=1.0)
        print("所有任务完成:", results)
    except asyncio.TimeoutError:
        print("任务超时，取消未完成的任务（注意：wait_for 已经替你取消了 gather 和子任务）")
        for t in tasks:
            print(f"{t.get_name()} -> done={t.done()}, cancelled={t.cancelled()}")
            # 如果仍想统一收尾（吞掉 CancelledError），可再次收集
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())