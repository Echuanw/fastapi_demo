# 假设你正在开发一个应用程序，需要从多个数据源获取数据并进行处理。你可以使用线程池来并行处理这些数据源，并在每个任务完成后执行特定的操作。
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_data(source):
    print(f"Fetching data from {source}...")
    time.sleep(2)            # 模拟数据获取延迟
    return f"Data from {source}"

def process_data(future):
    data = future.result()
    print(f"Processing {data}")

def process_data_map(data):
    print(f"Map Processing {data}")

# 创建线程池
executor = ThreadPoolExecutor(max_workers=3)

# 数据源列表
data_sources = ['Source A', 'Source B', 'Source C']

# submit提交任务并添加回调，可以对每个任务进行单独的控制和处理。
futures = [executor.submit(fetch_data, source) for source in data_sources]
for future in futures:
    future.add_done_callback(process_data)

# 处理map提交任务的结果，更简洁，适合简单的批量任务处理。
futures = executor.map(fetch_data, data_sources)
for future in futures:
    process_data_map(future)

# 关闭线程池
executor.shutdown()