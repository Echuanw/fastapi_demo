import threading

# Create a bounded semaphore with an initial value of 2
sem = threading.BoundedSemaphore(2)
# sem = threading.Semaphore(2)

# Acquire the semaphore twice
sem.acquire()
sem.acquire()

# This will raise a ValueError, because the semaphore value cannot exceed its initial value
sem.release()
sem.release()
sem.release()