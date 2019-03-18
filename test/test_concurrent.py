import time
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,wait,ALL_COMPLETED
import threading
# 多线程并发测试

class MultiThreads(ThreadPoolExecutor):
    def __init__(self):
        pass

L = []
thread_num = 8
test_num = 1000



def cal_mult(x, sleep = True):
    for i in x:
        for j in range(10000):
            i += 1
        if sleep:
            time.sleep(0.0005)
        L.append(i)


def cal_serial(sleep = True):
    t0 = time.time()
    cal_mult(list(range(test_num)), sleep)
    t1 = time.time()
    print("No  Thread: Len(%d) Cost(%5.5f)"%(len(L), t1 - t0))



def cal_thread(sleep = True):
    Mt = ThreadPoolExecutor(max_workers = thread_num)
    works = []
    t0 = time.time()
    for i in range(thread_num):
        start = int(i * test_num / thread_num)
        end = int(min((i + 1) * test_num / thread_num, test_num))
        work = Mt.submit(cal_mult, list(range(start, end)), sleep)
        works.append(work)
    wait(works, None, ALL_COMPLETED)
    t1 = time.time()
    print("New Thread: Len(%d) Cost(%5.5f)"%(len(L), t1 - t0))


def cal_thread_old(sleep = True):
    t0 = time.time()
    p = []
    for i in range(thread_num):
        start = int(i * test_num / thread_num)
        end = int(min((i + 1) * test_num / thread_num, test_num))
        p.append(threading.Thread(
            target=cal_mult, 
            args=(list(range(start, end)), sleep, )))
    for i in p:
        i.start()
    for i in p:
        i.join()
    t1 = time.time()
    print("Old Thread: Len(%d) Cost(%5.5f)"%(len(L), t1 - t0))

def cal_process(sleep = True):
    Mt = ProcessPoolExecutor(max_workers = thread_num)
    works = []
    t0 = time.time()
    for i in range(thread_num):
        start = int(i * test_num / thread_num)
        end = int(min((i + 1) * test_num / thread_num, test_num))
        work = Mt.submit(cal_mult, list(range(start, end)), sleep)
        works.append(work)
    wait(works, None, ALL_COMPLETED)
    t1 = time.time()
    print("Processes : Len(%d) Cost(%5.5f)"%(len(L), t1 - t0))


if __name__ == "__main__":
    print("With    Sleep In Every Thread")
    cal_serial(True)
    cal_thread_old(True)
    cal_thread(True)
    cal_process()
    print("Without Sleep In Every Thread")
    cal_serial(False)
    cal_thread_old(False)
    cal_thread(False)
    cal_process(False)
    