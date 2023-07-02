import threading
import time
import os

LOG_DIR_PATH = './Log/'
__all__ = ["Log"]



class Log:
    def __init__(self) -> None:
         nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
         self.__content = list(f"日志-{nowTime}\n")


    def __record_log(self, content, end='\n'):
        if '\n' in content:
            end =''
        self.__content.extend(list(str(content)))
        self.__content.extend(list(end))


    def i(self,msg,end = '\n'):
        print(f'[info]  {msg}',end= end)
        
    def d(self,msg,end = '\n'):
        print(f'[debug] {msg}',end= end)

    def e(self,msg,end = '\n'):
        print(f'[error] {msg}',end= end)

    def l(self,msg:str):
        string =  time.strftime("%Y-%m-%d %H:%M:%S") +'\n'+ msg
        self.__record_log(content = string)

    def close(self):
        nowTime = time.strftime("%Y%m%d%H%M%S")
        if not os.path.exists(LOG_DIR_PATH):
            os.mkdir(LOG_DIR_PATH)
        _lock = threading.Lock()
        _lock.acquire()
        with  open(f"{LOG_DIR_PATH}Log-{nowTime}.txt", "w", encoding='utf-8') as __file :
            __file.write("".join(self.__content))
        _lock.release()
        self.__content = []