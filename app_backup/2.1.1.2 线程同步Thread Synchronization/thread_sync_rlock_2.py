# RLock 被用于保护 ShoppingCart  类中的共享资源，确保在多线程环境下对购物车的操作是线程安全的。
import threading

class item:
    def __init__(self, name = "default_name", price = 0.0):
        self._name = name
        self._price = price
    
class ShoppingCart:
    # 初始化 创建 RLock 实例，用于保护购物车中的共享资源 self.items。
    def __init__(self):
        self.items = []
        self._lock = threading.RLock()

    # 添加商品
    def add_item(self, item):
        with self._lock:
            self.items.append(item)

    # 移除商品
    def remove_item(self, item):
        with self._lock:
            self.items.remove(item)

    # 计算总价
    def calculate_total(self):
        total = 0
        with self._lock:
            for item in self.items:
                total += item.price
        return total

    # 结账，里面调用了 calculate_total ，如果使用 Lock 会在这里出现死锁
    # （普通的 Lock 不允许同一个线程多次获取锁。）
    def checkout(self):
        with self._lock:
            total = self.calculate_total()
            if total > 0:
                self.process_payment(total)
                self.items.clear()