# 库存最大10个，但是一开始是满库存的，里面就有10个商品。生产者每4秒生产一个商品，消费者每2秒消费一个商品，当库存商品小于3个时，通知生产者停止生产。当库存商品为0时，通知消费者停止消费。然后再主程序里进行总结，除了一开始的10个商品以外，生产者又生产多少商品，消费者一共消费了多少商品。
import threading
import time

# 库存
class Inventory:
    def __init__(self, max_items):
        self.max_items = max_items
        self.items = max_items          # 初始库存为满
        self.condition = threading.Condition()
        self.producer_active = True     # 是否继续生产 | 消费
        self.consumer_active = True
        self.produced_count = 0
        self.consumed_count = 0
        self.empty_times = 0
        self.max_empty_times = 3

    def produce(self):
        with self.condition:
            while self.items >= self.max_items:
                print("库存已满，生产者等待中...")
                self.condition.wait()
            self.items += 1
            self.produced_count += 1
            print(f"生产者生产了一个商品，当前库存: {self.items}")
            if self.items <= 3:
                print(f"当前库存: {self.items},库存商品小于3个时，生产者停止生产。")
                self.producer_active = False
            self.condition.notify_all()

    def consume(self):
        with self.condition:
            while self.items == 0 or not self.consumer_active:
                print("库存为空或消费者被停止，消费者等待中...")
                self.condition.wait()
            self.items -= 1
            self.consumed_count += 1
            print(f"消费者消费了一个商品，当前库存: {self.items}")
            if self.items == 0:
                self.consumer_active = False
            self.condition.notify_all()

# 生产者生产商品
def producer(inventory: Inventory):
    while True:
        if not inventory.producer_active:
            break
        time.sleep(2)                   # 生产者每2秒生产一个商品
        inventory.produce()

# 消费生产商品
def consumer(inventory: Inventory):
    while True:
        if not inventory.consumer_active:
            break
        time.sleep(1)                   # 消费者每1秒消费一个商品
        inventory.consume()

if __name__ == "__main__":
    inventory = Inventory(max_items=5)
    producer_thread = threading.Thread(target=producer, args=(inventory,))
    consumer_thread = threading.Thread(target=consumer, args=(inventory,))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print(f"生产者共生产了 {inventory.produced_count} 个商品。")
    print(f"消费者共消费了 {inventory.consumed_count} 个商品。")