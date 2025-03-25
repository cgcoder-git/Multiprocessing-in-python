from multiprocessing import Process, Value, Lock

def withdrawl_amt(balance, lock):
    for _ in range(500):
        with lock:
            balance.value -= 5

def deposite_amt(balance, lock):
    for _ in range(500):
        with lock:
            balance.value += 10

if __name__ == "__main__":
    Balance = Value("i", 10000)  # Shared memory variable
    lock = Lock()
    p1 = Process(target=deposite_amt, args=(Balance,lock))
    p2 = Process(target=withdrawl_amt, args=(Balance,lock))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Final Balance: {Balance.value}")
