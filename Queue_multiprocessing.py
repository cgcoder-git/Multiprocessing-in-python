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
