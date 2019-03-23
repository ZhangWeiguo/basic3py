import sys
sys.path.append("..")
from file_log import LoggerCustom,Logger
from concurrency import MultiThreads
def log(f, j):
    for i in range(10):
        f.info("Thread %d: %d th log is happend"%(j, i))

f = Logger("test", "test")
Mt = MultiThreads(16)
funs = []
for i in range(100):
    fun = Mt.submit(log, f, i)
    funs.append(fun)
Mt.wait_all_completed()


