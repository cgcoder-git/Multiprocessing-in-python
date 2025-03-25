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