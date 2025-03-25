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


"""
process2 Number: 0
process1 Number: 0
process1 Number: 1
process2 Number: 1
process1 Number: 2
process2 Number: 2
"""