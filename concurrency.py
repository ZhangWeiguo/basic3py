import time
import psutil,os
from concurrent.futures import ThreadPoolExecutor,wait,ALL_COMPLETED
from concurrent.futures import ProcessPoolExecutor


class MultiThreads(ThreadPoolExecutor):
    def __init__(self, max_workers = psutil.cpu_count()):
        super(MultiThreads, self).__init__(max_workers)


class MultiProcess(ProcessPoolExecutor):
    def __init__(self, max_workers = psutil.cpu_count()):
        super(MultiProcess, self).__init__(max_workers)



if __name__ == "__main__":
    def work():
        pr = psutil.Process(os.getpid())
        print("name(%10s) path(%20s) pid(%5d:%5d) Is Running"%(pr.name(), pr.cwd(), os.getpid(), os.getppid()))
    MT = MultiThreads()
    print("Max Workers: %d"%MT._max_workers)
    fs = []
    for i in range(10):
        fs.append(MT.submit(work))
    wait(fs, None, ALL_COMPLETED)