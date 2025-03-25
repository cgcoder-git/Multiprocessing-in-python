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
