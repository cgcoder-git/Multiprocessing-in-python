# Multiprocessing-in-python
Lets talk about multiprocessing in python and how memory can be shared between processes.

## What is Multiprocessing? 
Multiprocessing is a technique in computing where multiple processes are run simultaneously to execute tasks in parallel. It leverages multiple CPU cores to perform operations concurrently, thereby improving performance, especially for CPU-bound tasks.

### Key Concepts :
1. **Process**: An independent program in execution. Each process has its own memory space.
2. **Concurrency vs. Parallelism**: Concurrency involves multiple tasks making progress at the same time, while parallelism actually runs tasks simultaneously.
3. **CPU-Bound Tasks**: Tasks that require heavy computation, like data processing or mathematical calculations.
4. **GIL (Global Interpreter Lock)**: In Python, the GIL prevents multiple native threads from executing simultaneously. Multiprocessing avoids this by using separate processes.

## Multiprocessing Vs MultiThreading
Multithreading and multiprocessing may seem similar, but they are fundamentally different. In **multithreading**, multiple threads are created within the same process, sharing the same CPU core and memory space. These threads execute by rapidly switching between tasks (context switching), creating the illusion of parallel execution. However, in reality, they run concurrently rather than truly in parallel.
On the other hand, **multiprocessing** involves creating separate processes for each task, each with its own memory space. These processes run independently and can execute simultaneously on different CPU cores, achieving true parallelism.


![image](https://github.com/user-attachments/assets/a4a60dda-6a7b-4783-bfeb-24eb65ace30f)

## Multiprocessing in Python
Python’s **multiprocessing** module allows you to create and manage multiple processes easily.

```python
from multiprocessing import Process
import time

def print_numbers(process):
    for i in range(3):
        time.sleep(1)
        print(f"{process} Number: {i}")

if __name__ == "__main__":
    process1 = Process(target=print_numbers, args=("process1",))
    process2 = Process(target=print_numbers, args=("process2",))
    
    # start processes
    process1.start()
    process2.start()
    
    # Wait for completion
    process1.join()
    process2.join()
```
