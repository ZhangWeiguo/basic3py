# -*- encoding:utf-8 -*-
import logging,time,sys,os,platform
from logging.handlers import TimedRotatingFileHandler,RotatingFileHandler

'''
使用的时候只能使用单进程写，可以使用消息队列读取，避免写冲突
logger = Logger("Test","test", rotate = "Time", when = 'H', keep_num = 48)
logger = Logger("Test","test", rotate = "Size", max_bytes = 1028, keep_num = 48)
logger = Logger("Test","test", rotate = "None")
'''

def Logger(app_name, 
            file_name, 
            rotate       =   "None", 
            when         =   'H', 
            keep_num     =   24, 
            max_bytes    =   1024*1024*10):
    logger = logging.getLogger(app_name)
    formater = logging.Formatter(
        fmt         = "%(asctime)s %(filename)10s[line:%(lineno)5d] %(levelname)-8s %(message)s",
        datefmt     = "%Y-%m-%d %H:%M:%S")
    if rotate == 'Time':
        file_handler = TimedRotatingFileHandler(file_name, 
                                                when        =   when, 
                                                interval    =   1, 
                                                backupCount =   keep_num)
        if when == 'H':
            file_handler.suffix = "%Y%m%d%H.log"
        elif when  == 'M':
            file_handler.suffix = "%Y%m%d%H%M.log"
        elif when  == 'S':
            file_handler.suffix = "%Y%m%d%H%M%S.log"
        elif when  == 'D':
            file_handler.suffix = "%Y%m%d.log"
        else:
            raise Exception("when Must in (S,M,H,D)")
    elif rotate == 'Size':
        file_handler = RotatingFileHandler(filename = file_name, 
                                        maxBytes = max_bytes, 
                                        backupCount = keep_num)
    else:
        file_handler = logging.FileHandler(filename = file_name)

    file_handler.formatter = formater
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger   


class LoggerCustom:
    def __init__(self, app_name, keep_num = 24, buffer_num = 100):
        self.buffer_num = buffer_num
        self.buffer = []
        self.app_name = app_name
        self.file_name = "%s.%s.log"%(self.app_name, time.strftime("%Y%m%d%H"))
        self.file = open(self.file_name, 'a+')
    
    def log(self,data):
        if data.strip() != "":
            name = sys._getframe().f_back.f_code.co_filename
            line = str(sys._getframe().f_back.f_lineno)
            dt = time.strftime("%Y-%m-%d %H:%M:%S")
            s = "log_time=%s`locate=%s`data=%s\n"%(dt, name+":"+line, data)
            self.buffer.append(s)
        if len(self.buffer) >= self.buffer_num:
            self.flush()
    
    def flush(self):
        file_name = "%s.%s.log"%(self.app_name, time.strftime("%Y%m%d%H"))
        if file_name != self.file_name:
            self.file_name = file_name
            self.file.close()
            self.file = open(self.file_name, 'a+')
        self.file.writelines(self.buffer) 
        self.buffer.clear()
    
    def close(self):
        self.flush()
        self.file.close()

            
        
