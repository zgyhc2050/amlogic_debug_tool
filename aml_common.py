import threading
import subprocess


RET_VAL_SUCCESS         = 0
RET_VAL_FAIL            = -1
RET_VAL_EXCEPTION       = -2

class AmlThread(threading.Thread):

    def __init__(self, func, thread_num=0, timeout=1.0):
        super(AmlThread, self).__init__()
        self.thread_num = thread_num
        self.__subFuc = func
        self.__stopped = False
        self.timeout = timeout

    def run(self):
        subthread = threading.Thread(target=self.__subFuc, args=())
        subthread.setDaemon(True)
        subthread.start()

        while not self.__stopped:
            subthread.join(self.timeout)

        print('Thread __stopped')

    def stop(self):
        self.__stopped = True

    def isStopped(self):
        return self.__stopped


def exe_adb_cmd_default_print(str):
    print(str)

def exe_adb_cmd(cmd, bprint=False, callback_print=exe_adb_cmd_default_print):
    try:
        ret = subprocess.Popen(cmd, shell=True)
        ret.wait()
        if bprint == True:
            if ret.returncode == 0:
                callback_print(cmd + ' --> Success')
            else:
                callback_print(cmd + ' --> Failed' + ', ret:'+ str(ret.returncode))
        return ret
    except:
        callback_print(cmd + ' --> Exception happend!!!')
        return RET_VAL_EXCEPTION
