import os
from random import randint
from pathlib import Path
import queue
from queue import Queue
from threading import Thread
import sys

CURR_DIR = Path(__file__).parent
OUTPUT_DIR = CURR_DIR / "output"
RESULT_FILE = OUTPUT_DIR / "result.csv"
NUM_WORKERS = 11


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n - 1):
        f0, f1 = f1, f0 + f1
    return f1


def worker1(task_q: Queue, output_dir):
    while True:
        try:
            task = task_q.get(block=False)
        except queue.Empty:
            return

        result = fib(task)
        with open(output_dir / f"{task}.txt", "w") as f:
            f.write(str(result))

        task_q.task_done()


def func1(array: list):
    tasks = Queue()
    for num in array:
        tasks.put(num)

    threads = [
        Thread(target=worker1, args=(tasks, OUTPUT_DIR)) for _ in range(NUM_WORKERS)
    ]

    [t.start() for t in threads]

    tasks.join()


def worker2(task_q: Queue, result_file: str):
    while True:
        try:
            task = task_q.get()
        except task_q.empty:
            return
        str_to_write = task[0] + "," + task[1] + "\n"
        with open(result_file, "a") as f:
            f.write(str_to_write)


def func2(result_file: str):
    tasks2 = Queue()
    for file in Path(result_file).parent.iterdir():
        name = file.name
        ord_num = name.split(".")[0]
        with open(file) as f:
            fib_num = f.read()
        tasks2.put((ord_num, fib_num))

    threads = [
        Thread(target=worker2, args=(tasks2, result_file)) for _ in range(NUM_WORKERS)
    ]

    [t.start() for t in threads]

    tasks2.join()


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    sys.set_int_max_str_digits(30000)

    func1(array=[randint(1000, 100000) for _ in range(1000)])  # 1000
    func2(result_file=RESULT_FILE)
