import concurrent.futures
from functools import wraps
from progress.bar import Bar
import time
import random


random.seed(42)

def concurrent_processing(executor_type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with executor_type() as executor:
                futures = [executor.submit(func, arg) for arg in args[0]]
                with Bar('Processing', max=len(args[0])) as bar:
                    for future in concurrent.futures.as_completed(futures):
                        bar.next()
                        yield future.result()
        return wrapper
    return decorator

@concurrent_processing(concurrent.futures.ThreadPoolExecutor)
def process_data(data):
    time.sleep(random.randint(1, 3))
    return data * 2

data_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
start = time.time()
results = list(process_data(data_list))
end = time.time()
print(f"Time taken: {end - start}")
print(results)

def process_data(data):
    time.sleep(random.randint(1, 3))
    return data * 2
start = time.time()
results = [process_data(data) for data in data_list]
end = time.time()
print(f"Time taken: {end - start}")
print(results)

# Processing |################################| 10/10
# Time taken: 3.0061538219451904
# [6, 4, 20, 16, 14, 12, 10, 18, 8, 2]
# Time taken: 19.092655181884766
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
