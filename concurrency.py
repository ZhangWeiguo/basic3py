import time
import psutil,os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait,ALL_COMPLETED,FIRST_COMPLETED,FIRST_EXCEPTION
from concurrent.futures import ProcessPoolExecutor


class MultiThreads(ThreadPoolExecutor):
    def __init__(self, max_workers = psutil.cpu_count()):
        super(MultiThreads, self).__init__(max_workers)
        self.works = []

    def submit(self, fn, *args, **kwargs):
        fs = super(MultiThreads, self).submit(fn, *args, **kwargs)
        self.works.append(fs)
        return fs

    def wait_all_completed(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = ALL_COMPLETED)
    
    def wait_first_completed(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = FIRST_COMPLETED)

    def wait_first_exception(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = FIRST_EXCEPTION)

class MultiProcess(ProcessPoolExecutor):
    def __init__(self, max_workers = psutil.cpu_count()):
        super(MultiProcess, self).__init__(max_workers)
        self.works = []
    
    def submit(self, fn, *args, **kwargs):
        fs = super(MultiProcess, self).submit(fn, *args, **kwargs)
        self.works.append(fs)
        return fs

    def wait_all_completed(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = ALL_COMPLETED)
    
    def wait_first_completed(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = FIRST_COMPLETED)

    def wait_first_exception(self, timeout = None):
        wait(self.works, timeout = timeout, return_when = FIRST_EXCEPTION)

