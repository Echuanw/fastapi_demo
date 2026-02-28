from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_data(source):
    print(f"Fetching data from {source}...")
    time.sleep(2)            # 模拟数据获取延迟
    return f"Data from {source}"

def process_data(future):
    data = future.result()
    print(f"Processing {data}")

# 创建线程池
executor = ThreadPoolExecutor(max_workers=3)

# 数据源列表
data_sources = ['Source A', 'Source B', 'Source C']

futures = [executor.submit(fetch_data, source) for source in data_sources]

# 使用 as_completed 处理任务结果
for future in as_completed(futures):
    try:
        result = future.result()
        print(result)
    except Exception as e:
        print(f"Exception: {e}")

# 关闭线程池
executor.shutdown()