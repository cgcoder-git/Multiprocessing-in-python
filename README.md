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

**Output**
```python
process2 Number: 0
process1 Number: 0
process1 Number: 1
process2 Number: 1
process1 Number: 2
process2 Number: 2
```

## Communication between processes
When a process is created, each process run independently & have their own memory space, so if we want inter process communication (data sharing & message passing) python provide us some tools.
Lets discuss how we can make it possible....
1. Shared memory
2. Server process
3. Queue

### Shared Memory:
Multiprocessing in python provides **Array** and **Value** Objects to share data between processes.
1. **Array** : a ctypes array allocated from shared memory. [Shared Iterable]
2. **Value** : a ctypes Object allocated from shared memory. [Single Shared Variable]

**Without Array**

```python
from multiprocessing import Process, Array

def squre_elements(array):
    for index, number in enumerate(array):
        array[index] = number * number
    print(f"Array inside process : {array[:]}")
    return  array

if __name__ == "__main__":
    list_v = [1,2,3,4]

    P1 = Process(target=squre_elements, args=(list_v, ))
    P1.start()
    P1.join()
    print(f"Array outside process : {list_v[:]}")

"""
Output :
Array inside process : [1, 4, 9, 16]
Array outside process : [1, 2, 3, 4]
"""
```

**With Array**

```python
from multiprocessing import Process, Array

def squre_elements(array):
    for index, number in enumerate(array):
        array[index] = number * number
    print(f"Array inside process : {array[:]}")
    return  array

if __name__ == "__main__":
    list_v = Array("i",[i for i in range(1, 5)])
    P1 = Process(target=squre_elements, args=(list_v, ))
    P1.start()
    P1.join()
    print(f"Array outside process : {list_v[:]}")

"""
Output:
Array inside process : [1, 4, 9, 16]
Array outside process : [1, 4, 9, 16]
"""
```
from the above example we can understand for first code section, list was not shared between main processes and p1 process, but while using the Array, memory location is being shared.

**Using Value**

```python
from multiprocessing import Process, Array, Value


def square_elements(array, sum_v):
    for index, num in enumerate(array):
        array[index] = num * num
        with sum_v.get_lock():  # Ensure safe updating of shared value
            sum_v.value += array[index]

    print(f"Array inside process: {array[:]}, Sum: {sum_v.value}")


if __name__ == "__main__":
    list_v = Array("i", [i for i in range(1, 5)])  # Shared array
    list_sum = Value("i", 0)  # Shared integer value

    P1 = Process(target=square_elements, args=(list_v, list_sum))
    P1.start()
    P1.join()

    print(f"Array outside process: {list_v[:]}, Sum: {list_sum.value}")

"""
Output:
Array inside process: [1, 4, 9, 16], Sum: 30
Array outside process: [1, 4, 9, 16], Sum: 30
"""
```

### Server process
When you start a Python program, a server process also starts in the background. If a new process is needed, the parent process asks the server to create one. This server process stores shared data and lets multiple processes access and modify it using proxies.
The multiprocessing module provides a **Manager** class to handle this server process, making it easy to share data between processes.

```python
from multiprocessing import Process, Manager
import os
import time

def square_list(records):
    for index, record in enumerate(records):
        time.sleep(1)  # Simulating a delay
        records[index] = record ** 2
        print(f"Process {os.getpid()} modified index {index}: {records}")

if __name__ == "__main__":
    with Manager() as manager:
        records = manager.list([i for i in range(2,6)])  # Shared list

        # Creating two processes
        p1 = Process(target=square_list, args=(records,))
        p2 = Process(target=square_list, args=(records,))

        # Start the processes
        start_time = time.time()
        p1.start()
        p2.start()

        # Join the processes
        p1.join()
        p2.join()

        end_time = time.time()
        print(f"Final List outside Process: {records}")
        print(f"Total Execution Time: {end_time - start_time:.2f} seconds")
```

**Output**
```python
Process 9412 modified index 0: [4, 3, 4, 5]
Process 9413 modified index 0: [4, 3, 4, 5]
Process 9413 modified index 1: [4, 9, 4, 5]
Process 9412 modified index 1: [4, 9, 4, 5]
Process 9413 modified index 2: [4, 9, 16, 5]
Process 9412 modified index 2: [4, 9, 16, 5]
Process 9412 modified index 3: [4, 9, 16, 25]
Process 9413 modified index 3: [4, 9, 16, 25]
Final List outside Process: [4, 9, 16, 25]
Total Execution Time: 4.07 seconds
```

## Queue & Pipe
Multiprocessing required some kind of communication chennel so that tasks can be devided and end result should be aggregation of all the process.
Multiprocessing supports two types of communication channel between processes:
1. Queue
2. Pipe

**Queue** : multiprocessing.Queue is used for safe inter-process communication. One process put the data on the queue and another process consume the data. 
Example: 
```python
from multiprocessing import Process, Queue
import time

def producer(q):
    for i in range(5):
        print(f"Producing: {i} Added")
        q.put(i)  # Put item in queue
        time.sleep(1)

def consumer(q):
    while not q.empty():
        item = q.get()  # Get item from queue
        print(f"Consuming: {item} Taken")
        time.sleep(1)

if __name__ == "__main__":
    q = Queue()  # Create a queue

    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    p1.start()
    time.sleep(2)  # Ensure producer starts first
    p2.start()

    p1.join()
    p2.join()

    print("Queue processing complete.")
```

**Output**
```python
Producing: 0 Added
Producing: 1 Added
Producing: 2 Added
Consuming: 0 Taken
Producing: 3 Added
Consuming: 1 Taken
Producing: 4 Added
Consuming: 2 Taken
Consuming: 3 Taken
Consuming: 4 Taken
Queue processing complete.
```

**Pipe** : multiprocessing.Pipe() is another way for inter-process communication. Unlike Queue, Pipe only has two endpoints: one for sending, one for receiving.
multiprocessing module provides Pipe() function which returns a pair of connection objects connected by a pipe. Each connection object has send() and recv() methods (among others).

**Example**
```python
import time
from multiprocessing import Process, Pipe
import time

def msg_sender(conn, data):
    for msg in data:
        time.sleep(0.1) # adding delay
        conn.send(msg) # send data
        print(f"Sender : {msg}")
    conn.close()

def msg_receiver(conn):
    while True:
        msg = conn.recv() # receive data
        print(f"Received : {msg}")
        if msg == 'Bye':
            break

if __name__ == "__main__":
    data = ['Hello', 'How are You', 'Good, Thanks', 'Bye']
    # make connection
    parent_conn, child_conn = Pipe()
    p1 = Process(target=msg_sender, args=(parent_conn, data))
    p2 = Process(target=msg_receiver, args=(child_conn, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
```

**Output**
```python
Sender : Hello
Received : Hello
Sender : How are You
Received : How are You
Sender : Good, Thanks
Received : Good, Thanks
Sender : Bye
Received : Bye
Process finished with exit code 0
```
