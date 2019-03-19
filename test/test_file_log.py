import sys
sys.path.append("..")
from file_log import LoggerCustom

f = LoggerCustom("test")
for i in range(1000):
    f.log("%d th log is happend"%i)
f.close()