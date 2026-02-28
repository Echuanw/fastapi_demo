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

    done, pending = await asyncio.wait(tasks, timeout=1.0)
    print(f"done={len(done)}, pending={len(pending)}")

    # 取消未完成的任务并清理
    for t in pending:
        t.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

    for t in tasks:
        print(f"{t.get_name()} -> done={t.done()}, cancelled={t.cancelled()}")

asyncio.run(main())