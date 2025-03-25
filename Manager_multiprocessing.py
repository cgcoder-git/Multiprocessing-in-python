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
