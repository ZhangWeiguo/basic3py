import sys,time
sys.path.append("..")
from file_log import LoggerCustom,Logger
from concurrency import MultiThreads

N = 1000
M = 16
def log(f, j):
    for i in range(N):
        f.info("Thread %d: %d th log is happend"%(j, i))
for thread_num in range(1, M + 1):
    f = Logger("test", "test")
    Mt = MultiThreads(thread_num)
    t0 = time.time()
    for i in range(M):
        fun = Mt.submit(log, f, i)
    Mt.wait_all_completed()
    del Mt
    print("%3d Threads: %d Log Cost %5.3f, Avg %d/S"%(
        thread_num,
        N * M, 
        time.time() - t0, 
        N * M / (time.time() - t0)))

