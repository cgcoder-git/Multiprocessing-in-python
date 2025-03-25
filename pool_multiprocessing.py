import time
from multiprocessing import Pool, Process, Array
import os


def square(num):
    time.sleep(1)
    print(f"Task Perfromed by : {os.getpid()}")
    return num * num

if __name__ == "__main__":
    nums = [1,2,3,4]
    with Pool(3) as pool:
        result = pool.map(square, nums)
    print(f"Squred Numbers : {result}")
